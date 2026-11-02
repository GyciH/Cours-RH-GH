# Construit Cours RH·GH à partir de l'appli complète (dépôt GyciH/cours, déjà construit).
# Usage : python3 outils/filtrer.py <dossier GyciH/cours> <dossier de sortie (racine de ce dépôt)>
# Ne garde que les cours sur Rhino, Grasshopper et la géométrie ; les QCM (déjà triés :
# notions seulement, pas de paramétrage) sont repris tels quels.
import json, os, shutil, sys, hashlib
from PIL import Image, ImageDraw

SRC, OUT = sys.argv[1], sys.argv[2]

# Chapitres gardés : None = le chapitre entier, sinon la liste des cours gardés.
GARDE = {
    "2B": [49],                 # nombres flottants : tolérances et précision géométrique
    "3A": None, "3B": None,     # Rhino et Grasshopper
    "4A": None, "4B": None,     # maths de la géométrie, géométrie algorithmique
    "5A": None, "5B": None,     # génératif et optimisation de forme
    "6A": None,                 # dessiner sur le canvas Grasshopper
    "7A": [53, 85, 86, 90],     # caméra, maillages, normales, profondeur (sans GPU, transparence, gamma)
}

cat = json.load(open(f"{SRC}/catalogue.json", encoding="utf-8"))
parties = []
for p in cat["parties"]:
    chs = []
    for ch in p["chs"]:
        if ch["id"] not in GARDE: continue
        g = GARDE[ch["id"]]
        l = [n for n in ch["cours"] if g is None or n in g]
        assert g is None or len(l) == len(g), ch["id"]
        chs.append({**ch, "cours": l})
    if chs: parties.append({**p, "chs": chs})
# le cours 49 (partie 2, niveau 3) ferme le parcours au lieu de l'ouvrir
parties.sort(key=lambda p: p["p"] == 2)
gardes = {n for p in parties for ch in p["chs"] for n in ch["cours"]}
cours = [c for c in cat["cours"] if c["n"] in gardes]
assert len(cours) == len(gardes)
comps = [k for k in cat["comps"] if any(c["comp"] == k["id"] for c in cours)]
cat2 = {**cat, "parties": parties, "comps": comps, "cours": cours}

for x in ("c", "f"):
    shutil.rmtree(f"{OUT}/{x}", ignore_errors=True)
os.makedirs(f"{OUT}/c"); shutil.copytree(f"{SRC}/f", f"{OUT}/f")
# polices.css est dans f/ : ses url() se lisent depuis f/, pas depuis la racine
pc = open(f"{OUT}/f/polices.css").read().replace("url(f/", "url(")
open(f"{OUT}/f/polices.css", "w").write(pc)
for c in cours: shutil.copy(f"{SRC}/c/{c['s']}.html", f"{OUT}/c/")
for x in ("trame.css", "trame-app.css"): shutil.copy(f"{SRC}/c/{x}", f"{OUT}/c/")
j = json.dumps(cat2, ensure_ascii=False, separators=(",", ":")).replace("�", "\\ufffd")
open(f"{OUT}/catalogue.json", "w", encoding="utf-8").write(j)

h = open(f"{SRC}/index.html", encoding="utf-8").read()
def rep(a, b):
    global h
    assert a in h, a
    h = h.replace(a, b)
rep("<title>Bibliothèque de cours</title>", "<title>Cours Rhino · Grasshopper</title>")
# clé distincte : les deux applis partagent l'origine gycih.github.io
rep("var CLE='bibliotheque-cours-progres';", "var CLE='cours-rh-gh-progres';")
rep("Les 12 parties", "Les '+CAT.parties.length+' parties")
rep("a.download='progression-cours-'", "a.download='progression-cours-rh-gh-'")
rep('<meta name="theme-color" content="#F6F4F0" media="(prefers-color-scheme: light)">',
    '<meta name="theme-color" content="#F6F4F0" media="(prefers-color-scheme: light)">\n<meta name="application-name" content="Cours RH·GH">')
open(f"{OUT}/index.html", "w", encoding="utf-8").write(h)

m = json.load(open(f"{SRC}/manifest.webmanifest", encoding="utf-8"))
m.update(name="Cours Rhino · Grasshopper", short_name="Cours RH·GH", id="./?app=cours-rh-gh")
json.dump(m, open(f"{OUT}/manifest.webmanifest", "w", encoding="utf-8"), ensure_ascii=False, indent=1)

# icône différente de l'appli complète : fond bleu Rhino, trois dos de livres et une courbe
def icone(t, masque=False):
    im = Image.new("RGB", (t, t), "#1F5F7A"); d = ImageDraw.Draw(im)
    m = t * (0.26 if masque else 0.2); L = t - 2 * m
    w = L / 4.2
    for i, c in enumerate(["#F6F4F0", "#B9DCE6", "#F6F4F0"]):
        x = m + i * w * 1.25; hh = L * (0.62 if i == 1 else 0.72)
        d.rounded_rectangle([x, m + L - hh, x + w, m + L], radius=t * .015, fill=c)
    pts = []
    for k in range(41):  # courbe de Bézier quadratique au-dessus des livres
        s = k / 40; a, b, c2 = (m, m + L * .22), (m + L * .5, m - L * .12), (m + L, m + L * .22)
        pts.append(((1-s)**2*a[0] + 2*(1-s)*s*b[0] + s*s*c2[0], (1-s)**2*a[1] + 2*(1-s)*s*b[1] + s*s*c2[1]))
    d.line(pts, fill="#F2B544", width=max(2, int(t * .035)), joint="curve")
    for p in (pts[0], pts[-1]):
        r = t * .03; d.ellipse([p[0]-r, p[1]-r, p[0]+r, p[1]+r], fill="#F2B544")
    return im
for t in (180, 192, 512): icone(t).save(f"{OUT}/icone-{t}.png")
icone(512, True).save(f"{OUT}/icone-masque-512.png")

fichiers = ["./", "index.html", "manifest.webmanifest", "catalogue.json", "icone-192.png", "icone-512.png",
            "icone-180.png", "icone-masque-512.png", "f/polices.css"] + \
    ["f/" + x for x in sorted(os.listdir(f"{OUT}/f")) if x.endswith(".woff2")] + ["c/" + x for x in sorted(os.listdir(f"{OUT}/c"))]
hsh = hashlib.sha1()
for x in fichiers[1:]: hsh.update(open(f"{OUT}/{x}", "rb").read())
v = hsh.hexdigest()[:10]
# Le cache porte un préfixe propre et n'efface que ses anciennes versions : l'appli complète
# vit sur la même origine. Si un cache a disparu, l'ouverture de l'appli le remplit de nouveau.
open(f"{OUT}/sw.js", "w").write(f"""// Met les cours en cache : l'app marche ensuite sans réseau.
const PREFIXE = 'rhgh-';
const CACHE = PREFIXE + '{v}';
const FICHIERS = {json.dumps(fichiers, ensure_ascii=False)};
const remplir = () => caches.open(CACHE).then(c => Promise.all(FICHIERS.map(f => c.match(f).then(r => r || c.add(f).catch(() => {{}})))));
self.addEventListener('install', e => e.waitUntil(caches.open(CACHE).then(c => c.addAll(FICHIERS)).then(() => self.skipWaiting())));
self.addEventListener('activate', e => e.waitUntil(caches.keys().then(ks => Promise.all(ks.filter(k => k.startsWith(PREFIXE) && k !== CACHE).map(k => caches.delete(k)))).then(() => self.clients.claim())));
self.addEventListener('fetch', e => {{
  if (e.request.method !== 'GET') return;
  if (e.request.mode === 'navigate') e.waitUntil(remplir());
  e.respondWith(caches.open(CACHE).then(c => c.match(e.request, {{ignoreSearch: true}})).then(r => r || fetch(e.request)));
}});
""")
print(len(cours), "cours,", sum(len(c["q"]) for c in cours), "questions,", len(parties), "parties,",
      len(fichiers), "fichiers en cache, version", v)
