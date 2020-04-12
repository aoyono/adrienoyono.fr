---
title: "Exploring Facebook Graph API with Python"
date: 2018-05-18T20:22:38+02:00
status: published
tags:
    - python
    - facebook
    - social analysis
    - data mining
lastmod: 2020-04-12
---

In this post,  I propose to explore Facebook  Graph API with
Python. The use case will  be gathering some information and
do some  analysis on some of  your (mine in my  case :wink:)
friends' posts, with the aim  of discovering what words they
use the most.

###### UPDATE: 2020-04-12

As of today, the method I used below doesn't work anymore as
Facebook has decided to further restrict access to its users
data  (not a  bad thing  actually).  Now  your app  needs to
explicitly requests access your  friends' data. You can find
out                                                     more
[here](https://developers.facebook.com/docs/facebook-login/permissions#user-data).


## Setting up the working environment


To         do        this,         I        will         use
[facebook-sdk](https://facebook-sdk.readthedocs.io/en/latest/). If
you wish to follow along with the post, go ahead and install
the sdk (after creating a virtual env of course):

```bash
python -m pip install facebook-sdk
```

Now that  the sdk  is installed, we  can start  working with
it. I skip  the details of creating a facebook  app. To know
how         to        do         that,        go         see
[here](https://developers.facebook.com/docs/apps).

After the app  is created, you can get an  access token from
[facebook's                  graph                  explorer
tool](https://developers.facebook.com/tools/explorer/). This
will get you started quickly without bothering yourself with
generating client access  key and secret. Make  sure you get
the  token  for the  right  set  of permissions.   For  this
experiment, you only  need `public_profile`, `user_friends`,
`user_status` and `user_posts`.

After you get  your access token, use the  following code to
get started with a configured facebook graph object:


```python
import facebook
from getpass import getpass
token = getpass('access token from graph explorer:')
graph = facebook.GraphAPI(access_token=token, version="2.12")c
```

The code will ask for your graph explorer access token as if
it was a password (it won't  be printed in the console), and
then   will    configure   the   `GraphAPI`    object   from
`facebook-sdk` package. Note that  we specify the version of
the official  Facebook graph  API, with  `version="2.12"` so
that the package knows which requests to make to facebook to
get what you need.


## Warming up

Now we can start looking around.   First, let see how to get
the list of your friends:

```python
friends = graph.get_connections(id='me', connection_name='friends')
```

You can  see we  use the  `get_connections` method  from the
`GraphAPI`  object. You  have  to specify  the  `id` of  the
person whose friends you want to  get. In this case, you use
`me` to specify  that it's for your own  friends. The second
parameter   is  a   `connection_name`   which   is  set   to
`"friends"`. We  will explain  why this parameter  is called
like that later.


To understand how  Facebook Graph API is  organised, we have
to                           go                          and
[rtfd](https://developers.facebook.com/docs/graph-api/overview). If
you are a  good guy (I have  no doubt you are),  you read it
and saw that  facebook says its api is made  of nodes, edges
(like any graph structure)  and fields. Nodes are individual
objects  linked to  many  other objects  through edges,  and
having fields, like that:

<img src="/images/exploring_facebook_graph_api/output_16_0.svg" alt="output_16_0" style="background-color: white;" />


So for example, we could have this representation for Me and
some of my friends:


<img src="/images/exploring_facebook_graph_api/output_18_0.svg" alt="output_18_0" style="background-color: white;" />


If we  make a request  to an edge,  say `friends`, we  get a
collection of nodes. And this  request should be done from a
node. Nothing really difficult to understand then.

Since in this  session, what we need is to  get the posts of
our friends, we need the top node (that's the `id` parameter
of  `get_connections` with  value  `"me"`). And  we need  to
request  the `friends`  edge or  connection (that's  why the
second parameter is called `connection_name`).


## Start building real stuff

To have  access to  our friends' posts,  we need  to request
their name and id, so that later on, we can request for each
one  of them  the `posts`  edge. That  is the  logic of  the
following  piece of  code. We  also add  the possibility  to
store the collected posts in  a database, waiting to be used
for the analysis.

Fine, here goes the code:


```python
class Person(object):
    def __init__(self, name, facebook_id):
        self.name = name
        self.facebook_id = facebook_id
        
    def __repr__(self):
        return '<Person({name}, {facebook_id})>'.format(**self.__dict__)

import sqlite3

connection = sqlite3.connect('fb_people_db.sqlite3')
PEOPLE_TABLE = 'people'


def initialise_db(table, fields):
    cursor = connection.cursor()
    cursor.execute('create table if not exists {} ({})'.format(table, ','.join(fields)))
    connection.commit()
    cursor.close()


def save_people(people):
    save_in_db(PEOPLE_TABLE, [(person.name, person.facebook_id) for person in people])

    
def initialise_people_table():
    initialise_db(PEOPLE_TABLE, ['name, facebook_id'])
    

def save_in_db(table, objects):
    cursor = connection.cursor()
    cursor.executemany(
        'insert into {} values ({})'.format(table, ','.join('?' * len(objects[0]))),
        objects)
    connection.commit()
    cursor.close()


initialise_people_table()
people = [
    Person(friend['name'], friend['id'])
    for friend in friends['data']
]
save_people(people)
```

That's a  good start. You  can copy/paste the  following url
that I tested for you into the Graph Explorer tool mentioned
above to see the result. I use it below to get the fields to
request for our  purpose:


```python
explorer_url = 'me/posts?fields=description,shares,type,caption,created_time,is_hidden,message,message_tags,name,properties,application,feed_targeting,from,is_popular,source,story,status_type,via,target,attachments{description,description_tags,type,url},comments{comment_count,id,like_count,user_likes},likes{name,id,username},reactions&include_hidden=true'
fields = explorer_url.split('=')[-2].rstrip('&include_hidden')
```

Now we can  build up a Python dict with  our friends' id and
name as key and the list of their posts as value:


```python
friends_posts = {
    (person.facebook_id, person.name): graph.get_connections(
        id=person.facebook_id, connection_name='posts', fields=fields, include_hidden=True)['data']
    for person in people
}
```

You can  see we  use the  same method as  above, with  2 new
parameters  to specify  the `fields`  to return  and ask  to
`include_hidden` fields.


## Building further

Now Let's do some OO modeling for some of the nodes returned
by the  latest call to the  graph API. We use  the excellent
[attrs](https://www.attrs.org/en/stable/)  package  to  make
the code cleaner:


```python
import attr


@attr.s
class Attachment(object):
    description = attr.ib()
    description_tags = attr.ib()
    type = attr.ib()
    url = attr.ib()
    

@attr.s
class Comment(object):
    id = attr.ib()
    like_count = attr.ib()
    user_likes = attr.ib()
    

@attr.s
class Like(object):
    id = attr.ib()
    liker_name = attr.ib()
    #liker_username = attr.ib()


@attr.s
class Post(object):
    id = attr.ib()
    description = attr.ib()
    type = attr.ib()
    caption = attr.ib()
    publication_date = attr.ib()
    is_hidden = attr.ib()
    message = attr.ib()
    message_tags = attr.ib()
    name = attr.ib()
    properties = attr.ib()
    author = attr.ib()
    source = attr.ib()
    story = attr.ib()
    status_type = attr.ib()
    attachements = attr.ib(default=attr.Factory(list))
    comments = attr.ib(default=attr.Factory(list))
    likes = attr.ib(default=attr.Factory(list))
    reactions = attr.ib(default=attr.Factory(list))
    
    @classmethod
    def from_record(cls, record):
        attachments = [
            Attachment(
                att.get('description', ''), 
                att.get('description_tags', []), 
                att.get('type', ''), 
                att.get('url', ''))
            for att in record.get('attachments', {}).get('data', {})
        ]
        
        comments = [
            Comment(
                c.get('like_count', 0),
                c['id'],
                c.get('user_likes', False))
            for c in record.get('comments', {}).get('data', {})
        ]
        
        likes = [
            Like(
                l['id'],
                l.get('name', l.get('username', '')))
            for l in record.get('likes', {}).get('data', {})
        ]
        
        return cls(
            record.get('id'),
            record.get('description'),
            record.get('type'),
            record.get('caption'),
            record.get('created_time'),
            record.get('is_hidden'),
            record.get('message', ''),
            record.get('message_tags', ''),
            record.get('name'),
            record.get('properties'),
            record.get('from'),
            record.get('source', ''),
            record.get('story', ''),
            record.get('status_type'),
            attachments,
            comments,
            likes,
            record.get('reactions', {})
        )
        
        
```

Now we  have some  Records containers. We  use it  like that
(build a post object from the first post of a given friend):


```python
post = Post.from_record(friends_posts[(friend_id, friend_name)][0])
```

## And now comes the time for fun

Well, now comes the time  for some analysis!  There are very
well developed packages out there  for that, the most famous
being maybe [nltk](http://www.nltk.org/) library for natural
language analysis.  But  we won't do any of  that.  For now,
let's  do some  basic  word counting  with Python's  builtin
batteries:


```python
from collections import Counter
nbr_likes = len(post.likes)
word_occurrences = Counter(post.message.split())
```

The              above             snippet              uses
[Counter](https://docs.python.org/3.8/library/collections.html#collections.Counter)
to count the  number of word occurences in  a single message
from the post we built previously.

Now  let's scale  that snippet  to all  messages of  all our
friends' posts to have their total word occurences:

```python
total_word_occurences = Counter(
    word
    for posts in friends_posts.values()
    for record in posts
    for word in Post.from_record(record).message.split()
)
```

To classify that from the most  used words to the least, you
simply call `most_common` from the `Counter` object:

```python
total_word_occurences.most_common()
```



## Assembling Everything

Now we have a very basic app that can get our friends' posts
and show us  what are the most common words  used in them. I
have  recapitulated  the entire  program  below  for you  to
copy/paste as you wish (I know, I  am a good guy) - Be aware
that  all credits  go to  the  original authors  of all  the
libraries I used here.


```python
from collections import Counter
from getpass import getpass
import sqlite3

import attr
import facebook


connection = sqlite3.connect('fb_people_db.sqlite3')
PEOPLE_TABLE = 'people'


class Person(object):
    def __init__(self, name, facebook_id):
        self.name = name
        self.facebook_id = facebook_id
        
    def __repr__(self):
        return '<Person({name}, {facebook_id})>'.format(**self.__dict__)


@attr.s
class Attachment(object):
    description = attr.ib()
    description_tags = attr.ib()
    type = attr.ib()
    url = attr.ib()
    


@attr.s
class Comment(object):
    id = attr.ib()
    like_count = attr.ib()
    user_likes = attr.ib()
    


@attr.s
class Like(object):
    id = attr.ib()
    liker_name = attr.ib()
    #liker_username = attr.ib()


@attr.s
class Post(object):
    id = attr.ib()
    description = attr.ib()
    type = attr.ib()
    caption = attr.ib()
    publication_date = attr.ib()
    is_hidden = attr.ib()
    message = attr.ib()
    message_tags = attr.ib()
    name = attr.ib()
    properties = attr.ib()
    author = attr.ib()
    source = attr.ib()
    story = attr.ib()
    status_type = attr.ib()
    attachements = attr.ib(default=attr.Factory(list))
    comments = attr.ib(default=attr.Factory(list))
    likes = attr.ib(default=attr.Factory(list))
    reactions = attr.ib(default=attr.Factory(list))
    
    @classmethod
    def from_record(cls, record):
        attachments = [
            Attachment(
                att.get('description', ''), 
                att.get('description_tags', []), 
                att.get('type', ''), 
                att.get('url', ''))
            for att in record.get('attachments', {}).get('data', {})
        ]
        
        comments = [
            Comment(
                c.get('like_count', 0),
                c['id'],
                c.get('user_likes', False))
            for c in record.get('comments', {}).get('data', {})
        ]
        
        likes = [
            Like(
                l['id'],
                l.get('name', l.get('username', '')))
            for l in record.get('likes', {}).get('data', {})
        ]
        
        return cls(
            record.get('id'),
            record.get('description'),
            record.get('type'),
            record.get('caption'),
            record.get('created_time'),
            record.get('is_hidden'),
            record.get('message', ''),
            record.get('message_tags', ''),
            record.get('name'),
            record.get('properties'),
            record.get('from'),
            record.get('source', ''),
            record.get('story', ''),
            record.get('status_type'),
            attachments,
            comments,
            likes,
            record.get('reactions', {})
        )
    


def initialise_db(table, fields):
    cursor = connection.cursor()
    cursor.execute('create table if not exists {} ({})'.format(table, ','.join(fields)))
    connection.commit()
    cursor.close()


def save_people(people):
    save_in_db(PEOPLE_TABLE, [(person.name, person.facebook_id) for person in people])

    
def initialise_people_table():
    initialise_db(PEOPLE_TABLE, ['name, facebook_id'])
    

def save_in_db(table, objects):
    cursor = connection.cursor()
    cursor.executemany(
        'insert into {} values ({})'.format(table, ','.join('?' * len(objects[0]))),
        objects)
    connection.commit()
    cursor.close()


if __name__ == '__main__':
    import logging
    
    logging.basicConfig()
    logger = logging.getLogger('minage')
    logger.setLevel(logging.DEBUG)
    
    logger.info('Getting authentication')
    
    token = getpass('access token from graph explorer:')
    graph = facebook.GraphAPI(access_token=token, version="2.12")
    
    me = graph.get_object(id='me')
    
    logger.info('Getting some friends of: %s ...', me['name'])
    friends = graph.get_connections(id='me', connection_name='friends')

    logger.info('Initializing people database ...')
    initialise_people_table()
    people = [
        Person(friend['name'], friend['id'])
        for friend in friends['data']
    ]
    logger.info('Saving people ...')
    save_people(people)
    explorer_url = 'me/posts?fields=description,shares,type,caption,created_time,is_hidden,message,message_tags,name,properties,application,feed_targeting,from,is_popular,source,story,status_type,via,target,attachments{description,description_tags,type,url},comments{comment_count,id,like_count,user_likes},likes{name,id,username},reactions&include_hidden=true'
    fields = explorer_url.split('=')[-2].rstrip('&include_hidden')
    
    logger.info('Retrieving all posts from friends ...')
    friends_posts = {
        (person.facebook_id, person.name): graph.get_connections(
            id=person.facebook_id, connection_name='posts', fields=fields, include_hidden=True)['data']
        for person in people
    }
    excluded = 'la le les un des de the at une à et du a que pour dans I ! est sur'
    total_word_occurences = Counter(
        word
        for posts in friends_posts.values()
        for record in posts
        for word in Post.from_record(record).message.split()
        if word not in excluded.split()
    )
    print("These are the top words used by %s's friends:" % me['name'])
    print(total_word_occurences.most_common())
```

That's all folks!
