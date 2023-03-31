---
title: "Creating a plugin for Freenas"
date: 2020-11-28T23:02:02Z
draft: true
---

It's been  almost a  year I've been  enjoying my  FreeNAS. I
installed a few plugins  (nextcloud, plex, syncthing, etc.).
They all  work really well  and I  am very glad  I convinced
myself to buy  it. So now I wanted to  understand better how
to  create a  plugin and  make  it available  for people  to
download on their  own appliances. As a  tech enthousiast, I
constantly look for technologies that  can help me manage my
life better (what technology is  supposed to be ultimately -
at  least IMHO).   It's during  one of  these quests  on the
internet            that             I            discovered
[monica](https://www.monicahq.com/),   a   web   application
developed in PHP that help you manage your relationships. It
has a really  nice set of feature for that  purpose, so it's
needless  to say  I was  immediately seduced  and wanted  it
hosted on my  NAS. Combined with the objective  I set myself
earlier,  and I  had  a good  use case  for  a new  learning
experience. Here is how I  managed to create and install the
monica plugin for FreeNAS from scratch.

First,           I          headed           to          the
[reference](https://www.ixsystems.com/documentation/freenas/11.3-U5/plugins.html#create-a-plugin)
for creating a plugin for FreeNAS. There I found there are 2 git repositories involved in the plugin creation process:

-  The  community  plugins  catalog  repository,  where  all
  available   plugins  developed   by   the  community   are
  referenced
- A repository  for storing the _artifacts_  of your plugin,
  containing:
  - a script  that will be run after the  BSD jail that will
    host  your  application  is  created  and  the  required
    packages are installed, called `post_install.sh`
  - an `overlay` directory where  you put files that need to
    be deployed in specific folders  of the jail created for
    the plugin.  For  example, if you want to  deploy a file
    named  `foo.conf` in  the jail's  `/etc/`, you  create a
    directory  named `etc`  under `overlay`,  and you  place
    `foo.conf` there and the Jail  manager will put it there
    during the plugin installation.
  -  a  `settings.json`  file  where  you  specify  specific
    commands like plugin restart, or getting plugin's info.
  - a `ui.json`

First step  is to  create an  artifact repository  on github
(first locally,  then push to  github). Use the ref  doc for
that.

Then we  need to  fork the community  iocage-plugin-index in
github, clone our fork locally and then add a git remote (we
name    it   upstream)    to   point    to   the    official
iocage-plugin-index to follow all the updates from there:

    git remote add upstream git@github.com:ix-plugin-hub/iocage-plugin-index.git
    
Then now  we can create our  entry to our local  copy of the
plugin index: monica.json

In that file, there is a  need to specify which packages are
needed by the plugin. Therefore, for monica, that's where we
start looking into  how to install it on  FreeBSD.  We refer
to                                                     [this
documentation](https://github.com/monicahq/monica/blob/master/docs/installation/providers/generic.md). From
my understanding of  how to create a freenas  plugin and the
requirement for  monica (it's a  web app, thus relying  on a
webserver, a  database, a programming  language - PHP  and a
web  framework), I  will  only need  to  have the  following
packages available in the jail created for the plugin:
- git
- PHP 7.2+
- Composer
- MySQL
- Redis
- Apache

First thing  to do is to  check if these packages  exists in
FreeBSD                                               [ports
database](https://www.freebsd.org/cgi/ports.cgi).

Mysql pkg is named **mysql57-server**  PHP 7.2+ pkg found is
**php74-7.4.12**       Composer      pkg       found      is
**php74-composer-1.10.15** PHP extensions needed are:
    - bcmath: **php74-bcmath-7.4.12**
    - curl: **php74-curl-7.4.12**
    - dom: **php74-dom-7.4.12**
    - gd: **php74-gd-7.4.12**
    - gmp: **php74-gmp-7.4.12**
    - iconv: **php74-iconv-7.4.12**
    - intl: **php74-intl-7.4.12_1**
    - json: **php74-json-7.4.12**
    - mbstring: **php74-mbstring-7.4.12**
    - mysqli: **php74-mysqli-7.4.12**
    - opcache: **php74-opcache-7.4.12**
    - pdo_mysql: **php74-pdo_mysql-7.4.12**
    - redis: **php74-pecl-redis-5.3.2**
    - sodium: **php74-sodium-7.4.12**
    - xml: **php74-xml-7.4.12**
    - zip: **php74-zip-7.4.12**
    - imagick: **php74-pecl-imagick-im7-3.4.4_2**


Then  after  creating  the  minimal  files  for  the  plugin
artifacts and  the plugin definition, its  necessary to test
the plugin in freenas with the following command:

    iocage -D fetch -P iocage-plugin-index/monica.json -n monica dhcp="true"
    
the  `-D`   option  to   `iocage`  is  for   printing  debug
information. Since I didn't  push the plugin definition file
to the community iocage plugin repository, I created a clone
locally in freenas, that's why I can specify the path to the
plugin            definition            with:            `-P
iocage-plugin-index/monica.json`. `-n` sets  the name of the
plugin. Then  at the end,  I define  how I want  the network
properties of the  plugin to be applied (how  the IP address
will  be assigned).  The options  are: `dhcp="true"`  to use
DHCP to  automatically assign an  IP address to  the plugin;
`nat="true"`  to do  NAT,  or an  explicit  IP address  with
`ip4_addr="igb0|XXX.YYY.ZZZ.AAA"`.    It   will  surely   be
necessary to run that command  multiple times, so it will be
necessary  to destroy  previously  created  plugins and  all
their snapshots (zfs does a snapshot for every newly created
jail). The following 2 commands will then be necessary:

    iocage stop monica
    iocage destroy monica
    # To get the snapshots to remove, run: zfs list -t snapshot | grep monica
    zfs destroy <the path to the snapshot>
