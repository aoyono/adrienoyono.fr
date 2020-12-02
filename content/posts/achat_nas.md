---
title: "FreeNAS: achat et configuration"
date: 2019-12-28T23:04:03Z
status: published
tags:
    - nas
    - stockage
    - freenas
    - openzfs
    - freebsd
    - lifehacker
---

Après  avoir   longtemps  hésité  et  m'être   posé  moultes
questions, j'ai  finalement décidé de me  lancé dans l'achat
d'un
[NAS](https://en.wikipedia.org/wiki/Network-attached_storage). La
motivation m'est venue suite à  la naissance imminente de ma
fille,  au   caractère  international  de  ma   famille,  et
également du fait que je ne voulais pas me résigner à rendre
ma petite princesse ultra  populaire dans la vie alternative
d'internet dès son plus bas age, sans qu'elle aie eu son mot
à  dire.  J'espère  qu'elle  sera d'accord  avec  mon  choix
d'alors quand  elle sera grande  (si tu lis ceci  ma chérie,
n'oublie pas que  je t'aime plus que  tout, quoiqu'il arrive
:kiss:).

J'avais         déjà         entendu        parlé         de
[FreeNAS](https://www.freenas.org/) par  des collègues, mais
j'ai quand même parcouru un peu  le net pour voir ce qu'il y
avait d'autre  sur le  marché.  Les  solutions propriétaires
"classiques" ne m'ont pas suffisamment convaincu, et FreeNAS
en  plus  d'être  un  logiciel  libre,  semblait  avoir  une
entreprise   suffisamment  expérimentée   vendant  des   NAS
préinstallés                    avec                    l'OS
([ixsystems](https://www.ixsystems.com/)).      J'ai    donc
finalement       opté       pour      l'offre       [FreeNAS
mini](https://web.archive.org/web/20191124030610/https://www.ixsystems.com/freenas-mini/)
sans disque  attaché (en effet,  acheter les disques  à part
revenait moins cher  dans l'ensemble). Et j'ai  opté pour la
recommandation de  ixsystems d'utiliser des  disques Western
Digital
[RED](https://www.westerndigital.com/products/internal-drives/wd-red-hdd)
de 3TB chacun.

Ca a donc été une  nouvelle occasion d'en apprendre un peu
plus sur  le monde merveilleux des  ordinateurs. En effet,
La  lecture  de  la  documentation  de  FreeNAS  m'a  fait
decouvrir   plein  de   choses  concernant   les  systemes
d'exploitation de  type UNIX. Unix  reste la mère  de tous
ces  systèmes, et  BSD, qui  est basé  sur une version de
recherche d'UNIX, est un de ses forks les plus importants.
Je  parle  de  BSD  parce  qu'à partir  de  BSD,  qui  est
propriétaire,            a             été            créé
[FreeBSD](https://www.freebsd.org)  entre autres,  qui est
la base  de FreeNAS,  les 2  étant des  logiciels libres.
L'article
[suivant](https://en.wikipedia.org/wiki/Berkeley_Software_Distribution)
fournit un  bel apercu de  cet historique.  On peu  y voir
une figure  qui résume  bien l'évolution  des OS  à partir
d'UNIX.    J'ai    aussi   découvert   au    passage   que
[Darwin](https://en.wikipedia.org/wiki/Darwin_\(operating_system\)),
le noyau de macOS est fortement basé sur BSD.
Le   système   de   fichiers   utilisé   par   FreeNAS   est
[ZFS](https://en.wikipedia.org/wiki/ZFS#Terminology_and_storage_structure)
(plus       précisément        la       version       libre:
[OpenZFS](https://en.wikipedia.org/wiki/OpenZFS), qui  a été
développée  par Sun  Microsystems  comme  faisant partie  de
[Solaris](https://en.wikipedia.org/wiki/Solaris_\(operating_system\)).

Après ce  passage par l'histoire  d'Unix, j'ai décidé  de me
lancer dans la configuration du  NAS. Il faut dire que c'est
quelque chose  d'assez technique.  J'aurais pu  commander le
NAS préconfiguré et prêt à  utiliser, mais hé, il paraît que
j'aime  me  compliquer  la  vie (si  aimer  apprendre  c'est
effectivement synonime de ça, alors oui :laughing:). L'étape
la plus sensible  de cette aventure a  été la [configuration
du
stockage](https://www.ixsystems.com/documentation/freenas/11.2-U7/storage.html),
car la moindre petite erreur  à ce niveau pourrait impliquer
une perte  de données plus  tard. C'est aussi une  étape qui
contient beaucoup de jargon propre  à ZFS et FreeNAS (zpool,
vdev,  RAID, etc.).  Je ne  vais pas  expliquer ce  que sont
chacun de  ces concepts ici, peut-être  y reviendrai-je dans
le futur.

Mon choix a été d'opter pour 1 seul zpool contenant 1 unique
vdev                                                      en
[RAIDZ2](http://www.zfsbuild.com/2010/05/26/zfs-raid-levels/):
2 disques sont  authorisés à échouer en meme  temps. Du coup
avec mes 4  disques, ça fait que les 2  autres sont utilisés
comme disques de  réplication.  Ca me laisse  6TB de données
disponibles  (Il y  a de  quoi dire  que j'ai  l'espace pour
stocker toute  ma vie dedans).   J'ai crypté les  données du
disque  et sauvegardé  la  clé  sur mon  laptop  et sur  mon
téléphone. De  plus, j'ai réservé  10Gb de chaque  disque en
tant  que   swap  space   (mémoire  disque   utilisée  quand
l'utilisation  de   la  mémoire  RAM  dépasse   la  capacité
disponible), juste  au cas  où (la  valeur par  defaut c'est
2Gb).

Pour ce qui  est du nom du zpool ainsi  créé, j'ai opté pour
**deadpool**    (compatible   avec    la   [convention    de
nommage](https://docs.oracle.com/cd/E23824_01/html/821-1448/gbcpt.html)),
parce que zpool ça rime avec  deadpool et que ce dernier est
trop cool (hahahaha qu'est ce que je suis marrant).

Cette  configuration de  base terminée,  me voilà  l'heureux
propriétaire  d'un  système  complexe  à  la  pointe  de  la
technologie. La première application  faire de ce NAS, c'est
me  créer un  cloud privé.  Comme j'aime  le logiciel  libre
(vous l'aurez sans  doutes compris arrivé à  ce point), j'ai
choisi  [Nextcloud](https://nextcloud.com/),  un  équivalent
libre de Dropbox ou encore Google Drive. J'y reviendrai dans
un autre article. Nextcloud  me permettra de sauvegarder des
photos de ma fille et de les rendre accessibles à la famille
éparpillée à travers le monde.

Voilà, c'est  à peu près tout  ce que j'avais à  dire sur ce
sujet.  J'ai appris  beaucoup de  choses, et  me suis  rendu
responsable de la maintenance  de ce système plutôt complexe
vis-à-vis de moi même et de ma famille.
