---
title: Découverte d'openstreetmap
tags: [tuiles, openstreetmap, libre]
status: published
slug: decouverte-d-openstreetmap
author: Morning Dew
date: 2018-07-28
images: 
---


[Openstreetmap](https://www.openstreetmap.org/)          est
l'alternative
[LIBRE](https://www.gnu.org/philosophy/free-sw.fr.html)   du
très  populaire  Google  maps  pour fournir  un  service  de
cartographie sur le web ou sur d'autres plateformes (mobile,
etc).   C'est  un  projet  maintenu par  une  communauté  de
bénévoles, des gens  comme vous et moi qui  font profiter au
reste du monde de  leurs connaissances géographiques de leur
environnement. Comme  tout projet libre qui  se respecte, il
met à disposition de tout le monde ses entrailles techniques
(logiciels, données,  tutoriels, etc.). Nous  nous proposons
d'explorer dans  ce billet  ce qu'il  faut pour  inclure une
carte dans  une page web, de  même que le minimum  pour être
soi-même  un fournisseur  de  tuiles  pour l'élaboration  de
cartes basées sur les données d'openstreetmap.

La  pile  technologique   utilisée  par  openstreetmap  pour
effectuer du rendu de cartes est la suivante:

-  Postgresql  avec  l'extension Postgis  pour  stocker  les
  données
- Mapnik pour effectuer le rendu des tuiles
- Leaflet pour les afficher dans le navigateur

------------------------------------

## Inclusion d'une carte openstreetmap dans une page web


Le scénario classique  pour afficher une carte  sur une page
web  consiste à  disposer  d'un fournisseur  de cartes,  qui
offre:

- Un jeu de tuiles  "rendues" (dessinées) depuis une base de
  données, qui sont ensuite combinées pour faire une carte
- Une  API (Javascript  pour le web  et Android  par exemple
  pour  les  mobiles)  pour   afficher  les  cartes  sur  la
  plateforme

C'est donc  cela qu'offre  OpenStreetMap.  Il  ne fonctionne
pas en  fournisseur de tuiles,  mais met à  dispositions ses
données  pour  permettre  de générer  soi-même  ses  propres
tuiles.     Les     données     sont     disponibles     sur
[planet.openstreetmap.org](https://planet.openstreetmap.org).

Pour      l'API,      on      a     le      choix      entre
[Leaflet](https://openlayers.org/)     plus     léger     et
[OpenLayers](https://openlayers.org/)  plus  lourd. Dans  ce
billet, nous nous limiterons à Leaflet.

Pour  la mise  en pratique,  nous allons  inclure une  carte
leaflet  à  la page  d'accueil  par  défaut du  serveur  web
[nginx](https://nginx.org/). Référez-vous à la documentation
de nginx pour l'installer sur votre système.


**NOTE**:  J'utilise exclusivement  linux, pricipalement  la
distribution Kubuntu

Nous allons récupérer le code source de Leaflet:



```bash
git clone https://github.com/Leaflet/Leaflet.git
```

Une fois le  code cloné en local, il faut  se mettre sur une
branche de version.  Nous allons nous mettre  sur la branche
v1.3.1 par exemple:


```bash
cd Leaflet
git checkout -b v1.3.1 v1.3.1
```

Selon           les           instructions           données
[ici](https://switch2osm.org/fr/utilisation-des-tuiles/debuter-avec-leaflet/),
nous créons  un fichier  `leafletembed.js` que  nous plaçons
dans le répertoire `dist`. Et voici son contenu:


```bash
cat dist/leafletembed.js
#    var map;
#    var ajaxRequest;
#    var plotlist;
#    var plotlayers = [];
#    
#    // set up AJAX request
#    ajaxRequest = GetXmlHttpObject();
#    if (ajaxRequest == null) {
#        alert("This browser does not support HTTP Request");
#    }
#    
#    function GetXmlHttpObject() {
#        if (window.XMLHttpRequest) {
#            return new XMLHttpRequest();
#        }
#    
#        if (window.ActiveXObject) {
#            return new ActiveXObject("Microsoft.XMLHTTP");
#        }
#        return null;
#    }
#    
#    function askForPlots() {
#        // request the marker info with AJAX for the current bounds
#        var bounds = map.getBounds();
#        var min_lat_lon = bounds.getSouthWest();
#        var max_lat_lon = bounds.getNorthEast();
#        var msg = 'leaflet/findbybbox.cgi?format=leaflet&bbox=' + min_lat_lon.lng + ',' + min_lat_lon.lat + ',' + max_lat_lon.lng + ',' + max_lat_lon.lat;
#    
#        ajaxRequest.onreadystatechange = stateChanged;
#        ajaxRequest.open('GET', msg, true);
#        ajaxRequest.send(null);
#    }
#    
#    function stateChanged() {
#        // if AJAX returned a list of markers, add them to the map
#        if (ajaxRequest.readyState == 4) {
#            // use the info here that was returned
#            if (ajaxRequest.status == 200) {
#                plotlist = eval("(" + ajaxRequest.responseText + ")");
#                removeMarkers();
#                for (i = 0; i < plotlist.length; i++) {
#                    var plotll = new L.LatLng(plotlist[i].lat, plotlist[i].lon, true);
#                    var plotmark = new L.Marker(plotll);
#                    plotmark.data = plotlist[i];
#                    map.addLayer(plotmark);
#                    plotmark.bindPopup("<h3>" + plotlist[i].name + "</h3>" + plotlist[i].details);
#                    plotlayers.push(plotmark);
#                }
#            }
#        }
#    }
#    
#    function removeMarkers() {
#        for (i = 0; i < plotlayers.length; i++) {
#            map.removeLayer(plotlayers[i]);
#        }
#        plotlayers = [];
#    }
#    
#    function initmap() {
#        // set up the map
#        map = new L.Map('map');
#    
#        // Create the title layer with correct arrtribution
#        var osm_url = 'https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png';
#        var osm_attrib = 'Map data &copy; <a href="http://openstreetmap.org">OpenStreetMap</a> contributors';
#        var osm = new L.TileLayer(osm_url, {minZoom: 0, maxZoom: 12, attribution: osm_attrib});
#    
#        // start the map
#        zoetele = new L.LatLng(3.2687, 11.8275);
#        map.setView(zoetele, 12);
#        map.addLayer(osm);
#    
#        // add the functionality of showing the markers as we move on the map
#        askForPlots();
#        map.on('moveend', onMapMove);
#    }
#    
#    // moveend map callback
#    function onMapMove(e) {
#        askForPlots();
#    }
```

Voici le contenu de la page d'accueil du serveur nginx, avec
les rajouts effectués en suivant les instructions:


```bash
cat /var/www/html/index.html
#    <!DOCTYPE html>
#    <html>
#    <head>
#    <title>Welcome to nginx!</title>
#    <style>
#        body {
#            width: 35em;
#            margin: 0 auto;
#            font-family: Tahoma, Verdana, Arial, sans-serif;
#        }
#    
#        #map { height: 500px; }
#    </style>
#    <link rel="stylesheet" type="text/css" href="leaflet/leaflet.css" />
#    <script type="text/javascript" src="leaflet/leaflet.js"></script>
#    <script type="text/javascript" src="leaflet/leafletembed.js"></script>
#    </head>
#    <body>
#    <h1>Welcome to nginx!</h1>
#    <p>If you see this page, the nginx web server is successfully installed and
#    working. Further configuration is required.</p>
#    
#    <p>For online documentation and support please refer to
#    <a href="http://nginx.org/">nginx.org</a>.<br/>
#    Commercial support is available at
#    <a href="http://nginx.com/">nginx.com</a>.</p>
#    
#    <p><em>Thank you for using nginx.</em></p>
#    
#    <div id="map"></div>
#    
#    <script>
#      initmap();
#    </script>
#    
#    </body>
#    </html>
```


Si  la carte  ne  s'affiche  pas, ce  qui  manque, c'est  de
préciser  une taille  pour l'élément  html dans  lequel sera
affiché la  carte. Il  faut donc  rajouter dans  l'entête un
style en plus pour l'élément `<div id="map"></div>`: ```html
<style> <!-- ... --> #map { height: 180px; } </style>```

Avec cette modification, le  résultat attendu apparaît enfin
!

![welcome_page_nginx](/images/decouverte-osm/welcome_nginx.png)



## Créer un serveur de tuiles

----------------

Afficher une  carte sur un  site web est  finalement (ultra)
facile.

Si on veut  servir des tuiles soi-même à  partir des données
libres d'openstreetmap,  voici la  source du savoir  faire à
suivre: https://switch2osm.org/fr/servir-des-tuiles/.

L'option de  construire soi-même  à la  main son  serveur de
tuiles  est  celle  qui  est  utilisée  pour  construire  ce
[conteneur
docker](https://hub.docker.com/r/homme/openstreetmap-tiles/).
Nous allons donc le tirer localement:


```bash
docker pull homme/openstreetmap-tiles
```

Servir ses propres tuiles est quelque chose de très gourmant
en capacités système, surtout si  on vise une grande étendue
de la planète. Donc, pour  le faire sur un laptop classique,
nous   pouvons  nous   limiter  à   une  ville   **(Zoétélé:
latitude=3.2687, longitude=11.8275)**.
   
   
### La chaîne d'outils openstreetmap

Nous   rappelons  ici   la   pile   d'outils  utilisée   par
openstreetmap et leur enchaînement.

- Apache traite les requêtes  clients et défère le rendu des
  tuiles à son module
- [mod_tile](https://github.com/openstreetmap/mod_tile/tree/master/src)
  qui gère  un cache et  une queue  de requêtes de  rendu de
  carte. Le rendu proprement dit est effectué par
- [Mapnik](https://github.com/mapnik/mapnik) qui utilise les
  données openstreetmap stockées dans une base de données
- [Postgresql](https://www.postgresql.org/) qui  est créée à
  partir des données osm (fichier d'extension `.osm`) par un
  outil openstreetmap:
-    [osm2pgsql](https://github.com/openstreetmap/osm2pgsql)
  comme  suit (exemple  le plus  basique, avec  une base  de
  données créée en  amont): **`osm2pgsql --create --database
  gis data.osm.pbf`**


### La récupération des données osm

-  Pour  récupérer les données  sur les pays et  les régions
  ==> https://download.geofabrik.de/
-  Pour récupérer les  données sur les aires métropolitaines
  ==> https://mapzen.com/metro-extracts/  (mais le  lien est
  cassé)

Il n'est pas possible de télécharger les données d'une seule
ville  (en  ce  qui  est  du Cameroun  du  moins),  il  faut
nécessairement les  récupérer pour l'ensemble  du territoire
d'un      pays.        Nous      allons       donc      [les
récupérer](https://download.geofabrik.de/africa/cameroon.html).


```bash
mkdir openstreetmap
cd openstreetmap/
```

Ci-dessous,  une   commande  Bash  avec   l'utilitaire  très
pratique  [http](https://httpie.org/)   pour  récupérer  les
données les plus récentes sur le Cameroun et les enregistrer
dans un  fichier local  contenant l'emprunte  de la  date de
téléchargement  de ces  données.  Par la  suite, on  vérifie
l'intégrité des données téléchargées.


```bash
http get https://download.geofabrik.de/africa/cameroon-latest.osm.pbf > cameroon-latest-$(date --iso-8601 | sed 's/\-//g').osm.pbf
[ "$(md5sum < cameroon-latest-20180428.osm.pbf)" = "7dcd0a2e27b50c073f8cb6359b9760f9  -" ] && echo ":)" || echo ":("
```


Maintenant   que   nous   avons  le   fichier   de   données
openstreetmap  pour le  Cameroun, nous  allons les  importer
dans notre base de données  spatiale et lancer notre serveur
de tuiles local (tout cela  en utilisant le conteneur Docker
tiré précédemment).


```bash
mkdir osm-postgresql
mkdir $(pwd)/data
# Création du conteneur avec les bons paramètres
docker run --name osm-tile-server-cameroon -P -v $(pwd)/osm-postgresql:/var/lib/postgresql -v $(pwd)/data:/data homme/openstreetmap-tiles
# Démarrage du conteneur
docker start osm-tile-server-cameroon
# Initialisation de la base de données
docker exec -t osm-tile-server-cameroon bash -c 'run initdb startdb createuser createdb'
```

**N.B:**  Avant  de  faire  l'import des  données,  il  faut
insérer  les  données  de  références  spatiales  (voir  [ce
bug](https://github.com/geo-data/openstreetmap-tiles-docker/issues/5)).


```bash
docker exec -t osm-tile-server-cameroon bash -c 'setuser www-data psql -d gis -c "TRUNCATE spatial_ref_sys" && setuser www-data psql -d gis -f /usr/share/postgresql/9.3/contrib/postgis-2.1/spatial_ref_sys.sql && echo OK'
cp cameroon-latest-20180428.osm.pbf $(pwd)/data/import.pbf
# Import des données dans la base de données spatiale
docker exec -t osm-tile-server-cameroon bash -c 'run import'
# Démarrage du serveur de tuiles
docker exec -t osm-tile-server-cameroon bash -c 'run startdb startservices'
```

