---
title: "Implémenter un protocole réseau pour serveur TCP avec Twisted"
date: 2019-02-19
status: published
tags:
    - python
    - network programming
---

Du  temps où  je  travaillais dans  l'équipe CI  (Continuous
Integration)  d'Intel  à  Toulouse (autour  de  2016),  nous
développions l'infrastructure  d'intégration continue  en se
basant  sur   [Buildbot](https://buildbot.net/).   C'est  un
outil  très puissant  et très  configurable, avec  une belle
architecture asynchrone et en  micro-services. Si on rajoute
à ces caractéristiques des  développeurs ultra compétents et
super sympas, ça donne un environnement d'apprentissage très
prolifique! C'est là où  j'ai appris la programmation réseau
et asynchrone, de même que l'architecture en micro-services.

Au   coeur    de   Buildbot,   se   trouve    le   framework
[Twisted](https://twistedmatrix.com/trac/),   un  noyau   de
programmation réseau  asynchrone en  Python. Ce  framework a
pleinement     tiré     avantage      du     concept     des
[générateurs](https://wiki.python.org/moin/Generators)  pour
rendre  un  code  a  base  de  fonctions  de  rappel  (a.k.a
callbacks) lisible, pythonique  et facilement apprenable. Il
inclut aussi tout un ensemble de batteries qui permettent de
facilement développer des protocoles de communication réseau
plus ou  moins bas niveau  en Python.  Ce billet  se propose
d'explorer  cela,  et est  largement  basé  sur le  tutoriel
trouvé  dans  la  documentation  principale  de  Twisted  en
anglais.

## Techniquement, comment crée-t-on un protocole reseau avec Twisted?

D'une manière  générale, la  prise en charge  des protocoles
réseaux se fait via la création de sous-classes de la classe
`twisted.internet.protocol.Protocol`. Ces  sous-classes sont
instanciées lors de l'établissement  de la connexion et sont
détruites à la fin. Elles sont donc instantiées à la volée.

Comme  les  protocoles  sont des  entités  *temporaires*  du
processus  *serveur*, il  vaut  mieux ne  pas  y mettre  les
paramètres  de  configuration  de  la prise  en  charge  des
protocoles persistants. Pour  permettre cette possibilité de
configurer  de  manière  persistante,  l'écosystème  Twisted
interpose  une *fabrique*  de protocoles,  chargée de  créer
l'instance   du  protocole.   Cette   fabrique  n'a   aucune
connaissance du réseau dans lequel elle est insérée.

## Les protocoles

Les protocoles  dans une application TWisted  contiennent la
plupart  du code  et  permettent de  prendre  en charge  les
différentes étapes de la connexion utilisant ce protocole de
manière  asynchrone,  en  répondant  à  des  évènements  qui
déclenchent  des   appels  à  des  méthodes   de  la  classe
implémentant le  protocole. Ces événements sont  connectés à
des fonctions  de rappels (callbacks) de  4 types documentés
dans                     l'[interface                    des
protocoles](https://twistedmatrix.com/documents/current/api/twisted.internet.interfaces.IProtocol.html). Ces
fonctions de rappel sont dans l'ordre d'occurrence:

- makeConnection: pour établir une connection à un transport
  (exemple TCP) passé en paramètre, et à un serveur

- connectionMade: appelée une fois la connexion établie

- dataReceived: appelée une fois qu'un bloc de données a été
  reçu (le bloc de données est reçu en paramètre)

- connectionLost: appelée  une fois que la  connection a été
  interrompue (la raison de l'interruption de connection est
  passé en paramètre)

Voici  un exemple  de protocole  écho simple  qui, une  fois
qu'une connexion a été établie, s'enregistre comme connexion
supplémentaire et signale le  nombre de connexions utilisant
ce protocole. Quand la connexion est perdue, le protocole se
désenregistre.


```python
from twisted.internet.protocol import Protocol

class Echo(Protocol):
    
    def __init__(self, factory):
        self.factory = factory
        
    def connectionMade(self):
        self.factory.numProtocols += 1
        self.transport.write(
            "Hello. We are {} connexions using this protocol".format(
                self.factory.numProtocols
            ).encode('utf-8')
        )
        
    def connectionLost(self, reason):
        self.factory.numProtocols -= 1
        
    def dataReceived(self, data):
        self.transport.write(data)
```

## Les fabriques

Les fabriques instantient les protocoles auxquels elles sont
liées   à   travers   la  méthode   `buildProtocol`.   Elles
implémentent      [l'interface     des      fabriques     de
protocole](https://twistedmatrix.com/documents/18.7.0/api/twisted.internet.interfaces.IProtocolFactory.html)
avec 3 fonctions:

- buildProtocol:  appelée une fois  que la connection  a été
  établie avec l'adresse réseau reçue en paramètre. Si cette
  ne  retroune rien,  la  connection est  réputée avoir  été
  refusée et la connection est close immédiatement.

- doStart: appelée chaque fois que la fabrique est connectée
  à un port ou à un connecteur

-  doStop:   appelée  chaque   fois  que  la   fabrique  est
  déconnectée d'un port ou d'un connecteur

Souvent,  les  fabriques  vont initialiser  un  ensemble  de
paramètres  persistants de  configuration  et instantier  le
protocole qu'elles doivent créer, sans nécessairement passer
des paramètres d'initialisation à ce protocole. Dans ce cas,
il faut le créer de la façon suivante:


```python
from twisted.internet.protocol import Factory, Protocol


class UnProtocole(Protocol):
    pass

class UneFabrique(Factory):
    protocol = UnProtocole
```

Ceci va  automatiquement appeler la  méthode `buildProtocol`
de la fabrique et renvoyer une instance de `UnProtocole`.

Une fabrique du protocole `Echo` est la suivante:


```python
class EchoFactory(Factory):
    
    def __init__(self):
        self.numProtocols = 0
    
    def buildProtocol(self, addr):
        return Echo(self)
```

## Implémentation d'un serveur TCP complet

Une fois qu'on dispose d'un  protocole et de sa fabrique, on
peut  désormais créer  un  serveur qui  écoute  sur un  port
donné,     à    l'aide     du     concept    Twisted     des
[endpoints](https://twistedmatrix.com/documents/current/core/howto/endpoints.html). Nous
n'entrons pas dans le détail de ce concept. Pour simplifier,
il  faut toujours  se  dire que  dans  une application,  une
connection est comme un long tube dont l'application ne voit
que les bouts (les end points),  que ce soit côté serveur ou
côté  client.   Ces  bouts  sont  abstraits   au  niveau  de
l'application par les  `transports` (l'attribut du protocole
`transport`   utilisé   dans   sa   méthode   `dataReceived`
ci-dessus)  et les  `protocoles`. Les  endpoints repésentent
les transports.

Nous  allons utiliser  ici  un transport  TCP  basé sur  une
couche IP v4. Un endpoint reçoit généralement en entrée:

- un
  [réacteur](https://twistedmatrix.com/documents/current/core/howto/reactor-basics.html)
  qui, pour  simplifier, est  une boucle  événementielle qui
  écoute des événements et les  dispatche à des fonctions de
  rappel.

- les informations de  connections (port d'écoute, interface
  réseau)

Le code complet de l'application serveur est le suivant:


```python
from twisted.internet.endpoints import TCP4ServerEndpoint
from twisted.internet import reactor

endpoint = TCP4ServerEndpoint(reactor, 8098, interface='localhost')

# appel non bloquant retournant un Deferred auquel on peut rajouter
# des callbacks et/ou des errbacks
endpoint.listen(EchoFactory())

# Pour débuter la boucle événementielle
reactor.run()
```

Nous nous  arreterons ici,  esperant vous avoir  donne envie
d'en savoir un  peu plus. Si c'est le  cas, la documentation
du  projet est  tres bien  faite, je  vous invite  a [vous  y
rendre](https://twistedmatrix.com/trac/).
