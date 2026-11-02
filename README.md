# Cours Rhino · Grasshopper

Version de l'application de cours limitée à Rhino, Grasshopper, RhinoCommon et la géométrie : 50 cours et 500 questions, installable sur téléphone et utilisable hors ligne.

Cours gardés, avec les numéros et chapitres de la bibliothèque complète :

- **3 · Rhino et Grasshopper** : tout (plugin Grasshopper, géométrie RhinoCommon, document Rhino).
- **4 · Mathématiques et géométrie** : tout (vecteurs, matrices, Bézier et B-splines, intersections, géométrie algorithmique).
- **5 · Le génératif** : tout (hasard, bruit, répartition de points, pavages, optimisation de forme).
- **6A · Dessiner sur le canvas** (GDI+, attributs Grasshopper, interaction, mise en page).
- **7A · De la scène à l'image** : caméra et projection, maillages, normales, profondeur et précision.
- **2B** : les nombres à virgule flottante (tolérances), placé en fin de parcours.

Les QCM sont ceux de l'application complète, déjà triés : uniquement des questions de notion, aucune question de paramétrage des projets, et pas de QCM dans les PDF.

## Installer

Ouvrir https://gycih.github.io/Cours-RH-GH/ dans Chrome, puis menu ⋮ → « Installer l'application ». Au premier lancement tout est mis en cache ; ensuite l'app marche sans réseau. La progression reste sur le téléphone, séparée de celle de l'application complète. Pour reprendre la progression déjà faite, l'exporter depuis l'onglet Progrès de l'application complète et l'importer ici : seuls les cours présents sont gardés.

## Mettre à jour

Les fichiers sont générés à partir du dépôt GyciH/cours (déjà construit) : ne pas les modifier à la main.

```
git clone --depth 1 https://github.com/GyciH/cours ../cours
python3 outils/filtrer.py ../cours .
```

La liste des chapitres gardés est en tête de `outils/filtrer.py` (`GARDE`).
