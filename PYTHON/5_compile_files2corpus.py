import os
from lxml import etree

# === 📁 Chemins ===
input_dir = "data"
header_file = "tei_header.xml"
output_file = "output/votre_corpus.xml"

# === 📄 Lire le fichier tei_header.xml (même s’il ne contient QUE <teiHeader>) ===
with open(header_file, 'r', encoding='utf-8') as f:
    header_content = f.read()
try:
    header_tree = etree.fromstring(header_content.encode("utf-8"))
except Exception as e:
    raise ValueError(f"❌ Erreur de parsing dans tei_header.xml : {e}")

# Vérifie que l'élément racine est bien <teiHeader>
if header_tree.tag != "{http://www.tei-c.org/ns/1.0}teiHeader":
    raise ValueError("❌ Le fichier tei_header.xml ne contient pas de <teiHeader> en racine")

# === 📚 Collecter tous les fichiers .tei ===
file_paths = []
for root_dir, _, files in os.walk(input_dir):
    for file in files:
        if file.endswith(".tei"):
            file_paths.append(os.path.join(root_dir, file))

# Tri alphabétique par nom de fichier
file_paths.sort(key=lambda x: os.path.basename(x).lower())

# === 🧱 Créer l’élément racine <TEI> ===
NS_TEI = "http://www.tei-c.org/ns/1.0"
NSMAP = {None: NS_TEI}
tei_root = etree.Element("TEI", nsmap=NSMAP)

# Ajouter le teiHeader
tei_root.append(header_tree)

# === 🏗️ Créer <text><body> pour accueillir les divs ===
text_el = etree.SubElement(tei_root, "text")
body_el = etree.SubElement(text_el, "body")

# === 📦 Parcourir et ajouter chaque fichier TEI
for file_path in file_paths:
    filename = os.path.basename(file_path)
    if filename.startswith("FRCAOM06_COLE"):
        print(f"⏭️ Ignoré (image OCR inutilisée) : {filename}")
        continue

    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            tei_tree = etree.parse(f)
            tei_root_in = tei_tree.getroot()

        # Extraire <body>
        body_in = tei_root_in.find(".//{http://www.tei-c.org/ns/1.0}body")
        if body_in is None or not list(body_in):
            print(f"⚠️ Aucun contenu valide dans : {filename}")
            continue

        # Créer une <div type="file" corresp="Nom_fichier_sans_tei">
        div_el = etree.SubElement(body_el, "div", type="file",
                                  corresp=os.path.splitext(filename)[0])

        # Copier le contenu du <body>
        for child in body_in:
            div_el.append(child)

        print(f"✅ Ajouté : {filename}")

    except Exception as e:
        print(f"❌ Erreur avec {filename} : {e}")

# === 💾 Sauvegarde dans le fichier de sortie
tree_out = etree.ElementTree(tei_root)
os.makedirs(os.path.dirname(output_file), exist_ok=True)
tree_out.write(output_file, encoding="utf-8", xml_declaration=True, pretty_print=True)

print(f"\n✅ Compilation TEI terminée avec succès :\n{output_file}")
