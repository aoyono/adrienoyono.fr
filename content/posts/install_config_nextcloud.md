---
title: "Installation et configuration de Nextcloud sur FreeNAS"
date: 2020-01-15T00:52:23Z
status: published
tags:
    - nextcloud
    - freenas
    - lifehacker
    - LetsEncrypt
    - sharing
---

Cet  article  fait  suite  à   celui  sur  l'[achat  de  mon
NAS]({{< ref
"achat_nas.md" >}}). Nextcloud
était le moyen le plus facile pour moi de préserver ma fille
des  sites des  réseaux sociaux,  tout en  permettant à  mes
proches d'être témoins de son  évolution à travers photos et
vidéos  en temps  réel. Bonne  nouvelle côté  technique, cela
s'est  révélé plutôt  facile  à faire  avec l'offre  FreeNAS
d'ixsystems. En  effet, ils ont  mis en place le  concept de
[plugins](https://www.ixsystems.com/documentation/freenas/11.3-U1/plugins.html)
qui permettent d'installer facilement une application qui va
fonctionner directement  avec le  NAS. Cet  article présente
mon aventure dans l'installation du plugin Nextcloud.

Avant tout, un  petit intermède technique sur  le concept de
plugins d'ixsystems.  Ils s'appuient  sur le concept FreeBSD
de
[Jail](https://www.freebsd.org/doc/en_US.ISO8859-1/books/handbook/jails.html). Les
Jails  de   FreeBSD  sont  équivalents  aux   containers  de
GNU/Linux   (voir  [docker](https://www.docker.com/)).    Il
s'agit d'une  virtualisation "légère" (au niveau  du système
d'exploitation), qui  permettent à un ensemble  de processus
de s'exécuter  de manière isolée dans  l'environnement hôte.
Les  plugins  sont des  Jails  déjà  pré-configurés avec  un
ensemble  de  logiciels  prêts  à  utiliser  (notamment  des
applications web, comme Nextcloud).

Pour installer  le plugin  nextcloud, il  suffit donc  de se
rendre dans l'interface web d'administration du FreeNAS (une
application  web  développée  en Python  avec  le  framework
Django), dans la section "Plugins" et choisir nextcloud puis
cliquer sur "installer". Ca peut-être long, car le processus
installe et configure plusieurs paquets (pour nextcloud, par
exemple, php, nginx,  mysql, etc.).  Une fois  que le plugin
est installé, il faut  terminer l'installation (spécifique à
nextcloud),  lors de  la  première  connexion à  l'interface
utilisateur. Cette  dernière phase  était assez  pénible car
l'interface  de  nextcloud  exigeait de  connaître  certains
paramètres comme  le nom de  la base de données  créée, mais
ces informations n'étaient pas fournies après l'installation
du  plugin.   Il   m'a  donc  fallu  aller   dans  le  [code
source](https://github.com/freenas/iocage-ix-plugins)    des
plugins officiels de ixsystems, pour  savoir ce qui se passe
quand on installe un plugin. De là, j'ai trouvé le lien vers
le
[code](https://github.com/freenas/iocage-plugin-nextcloud/blob/master/post_install.sh)
qui s'execute une  fois que ce plugin  est installé. Dedans,
on peut voir  tous ces paramètres.  Le  plugin utilise nginx
comme serveur web, configuré uniquement en HTTP.  La conf se
trouve,     dans     la     jail     du     plugin,     sous
/usr/local/etc/nginx/conf.d/nextcloud.conf.  Etant donné que
je  comptais ouvrir  l'accès à  Nextcloud à  internet depuis
chez  moi,  il  était  hors de  question  de  laisser  cette
configuration en HTTP. J'ai donc créé une autre conf pour le
HTTPS                                                   sous
/usr/local/etc/nginx/conf.d/nextcloud.https.conf. Il fallait
également trouver comment générer  les certificats SSL. J'ai
d'abord           pensé            au           traditionnel
[certbot](https://certbot.eff.org/),  mais  après  plusieurs
lectures    sur    le     web,    notamment    sur    [cette
discussion](https://www.truenas.com/community/threads/how-to-install-lets-encrypt-ssl-certificate-on-nextcloud-plugin.72218/),
j'ai                                               découvert
[acme.sh](https://github.com/Neilpang/acme.sh),   un  client
Let's  Encrypt  écrit  en  script  shell,  et  j'ai  préféré
l'utiliser. En effet, il m'a semblé beaucoup plus agréable à
utiliser, ~~mais surtout c'était  un nouveau jouet tout neuf
avec lequel il fallait absolument que je fasse joujou~~. Mon
nom de domaine personnel étant  enregistré chez OVH, j'ai dû
suivre                      le                     [tutoriel
suivant](https://github.com/Neilpang/acme.sh/wiki/How-to-use-OVH-domain-api)
pour  permettre à  acme.sh de  générer les  certificats. Ces
derniers         ont         été        générés         sous
`/root/.acme.sh/<nom-de-domaine>` dans la jail du plugin. Il
ne restait plus qu'à configurer la crontab dans la jail pour
pouvoir   mettre  à   jour   les   certificats  de   manière
automatique:

    echo '5 0 * * * "/root/.acme.sh"/acme.sh --cron --home "/root/.acme.sh" > /dev/null' | crontab -

Ces étapes m'ont permis de  partager les photos et vidéos de
ma petite princesse  de façon sereine, et le  résultat a été
très encourageant  et gratifiant.  Certains de  mes proches,
peu enclins aux choses  informatiques, étaient sceptiques au
début quand je leur disais que je voulais mettre en place ce
système pour  mettre à  jour les photos  de la  princesse et
leur permettre  de suivre  son évolution.  Je peux  dire que
cela  a  été une  réussite  puisqu'ils  se sont  ravisés  et
apprécient le  côté temps réel  et l'effet de  surprise créé
tous les jours :satisfied:.
