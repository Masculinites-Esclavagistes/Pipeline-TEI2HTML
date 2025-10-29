import os
from lxml import etree

# === 📁 Chemins ===
input_dir = "data"
header_file = "tei_header.xml"
output_file = "output/corpus_final.xml"

# === 📄 Lire le fichier tei_header.xml ===
print("📖 Lecture du fichier tei_header.xml...")
with open(header_file, 'r', encoding='utf-8') as f:
    header_content = f.read()

try:
    header_tree = etree.fromstring(header_content.encode("utf-8"))
except Exception as e:
    raise ValueError(f"❌ Erreur de parsing dans tei_header.xml : {e}")

# Vérifie que l'élément racine est bien <teiHeader>
if header_tree.tag != "{http://www.tei-c.org/ns/1.0}teiHeader":
    raise ValueError("❌ Le fichier tei_header.xml ne contient pas de <teiHeader> en racine")

print("✅ tei_header.xml chargé avec succès\n")

# === 📚 Collecter SEULEMENT les fichiers compilés (à la racine de data/) ===
print(f"🔍 Recherche des fichiers compilés dans '{input_dir}/'...")
file_paths = []

# Lister uniquement les fichiers .tei à la racine de input_dir
# (pas dans les sous-dossiers)
for item in os.listdir(input_dir):
    full_path = os.path.join(input_dir, item)
    # Vérifier que c'est un fichier (pas un dossier) et qu'il se termine par .tei
    if os.path.isfile(full_path) and item.endswith(".tei"):
        file_paths.append(full_path)
        print(f"  📄 Trouvé : {item}")

# Vérification : y a-t-il des fichiers ?
if not file_paths:
    print("\n⚠️ ATTENTION : Aucun fichier .tei trouvé à la racine de 'data/'")
    print("💡 Vérifiez que :")
    print("   1. Le script 2 a bien été exécuté")
    print("   2. Les fichiers compilés (ex: Dossier1.tei) sont bien dans 'data/'")
    print("   3. Le chemin 'data/' est correct")
    exit(1)

print(f"\n✅ {len(file_paths)} fichier(s) compilé(s) détecté(s)\n")

# Tri alphabétique par nom de fichier
file_paths.sort(key=lambda x: os.path.basename(x).lower())

# === 🧱 Créer l'élément racine <TEI> avec namespace ===
print("🏗️ Construction de la structure TEI...")
NS_TEI = "http://www.tei-c.org/ns/1.0"
NSMAP = {None: NS_TEI}
tei_root = etree.Element("TEI", nsmap=NSMAP)

# Ajouter le teiHeader en premier
tei_root.append(header_tree)
print("  ✅ <teiHeader> ajouté")

# === 🗂️ Créer <text><body> pour accueillir le contenu ===
text_el = etree.SubElement(tei_root, "text")
body_el = etree.SubElement(text_el, "body")
print("  ✅ Structure <text><body> créée\n")

# === 📦 Parcourir et ajouter chaque fichier TEI compilé ===
print("📥 Intégration des fichiers compilés dans le corpus...\n")
files_added = 0
files_skipped = 0
files_error = 0

for file_path in file_paths:
    filename = os.path.basename(file_path)

    try:
        # Parser le fichier TEI compilé
        with open(file_path, 'r', encoding='utf-8') as f:
            tei_tree = etree.parse(f)
            tei_root_in = tei_tree.getroot()

        # Extraire le <body> du fichier compilé
        body_in = tei_root_in.find(".//{http://www.tei-c.org/ns/1.0}body")
        
        # Si pas de namespace, essayer sans
        if body_in is None:
            body_in = tei_root_in.find(".//body")
        
        # Vérifier qu'il y a du contenu
        if body_in is None or not list(body_in):
            print(f"⚠️ Ignoré (pas de contenu) : {filename}")
            files_skipped += 1
            continue

        # Créer une <div> pour encapsuler le contenu de ce fichier
        # corresp contient le nom du fichier sans extension
        div_el = etree.SubElement(body_el, "div", 
                                  type="file",
                                  corresp=os.path.splitext(filename)[0])

        # Copier tout le contenu du <body> du fichier compilé
        for child in body_in:
            div_el.append(child)

        print(f"✅ Ajouté : {filename} ({len(list(body_in))} élément(s))")
        files_added += 1

    except etree.XMLSyntaxError as e:
        print(f"❌ Erreur XML dans {filename} : {e}")
        files_error += 1
    except Exception as e:
        print(f"❌ Erreur avec {filename} : {e}")
        files_error += 1

# === 💾 Sauvegarde dans le fichier de sortie ===
print(f"\n💾 Sauvegarde du corpus final...")
tree_out = etree.ElementTree(tei_root)

# Créer le dossier output s'il n'existe pas
os.makedirs(os.path.dirname(output_file), exist_ok=True)

# Écrire le fichier XML avec déclaration et indentation
tree_out.write(output_file, 
               encoding="utf-8", 
               xml_declaration=True, 
               pretty_print=True)

# === 📊 Résumé final ===
print("\n" + "="*70)
print("📊 RÉSUMÉ DE LA COMPILATION")
print("="*70)
print(f"✅ Fichiers ajoutés      : {files_added}")
print(f"⚠️ Fichiers ignorés      : {files_skipped}")
print(f"❌ Fichiers en erreur    : {files_error}")
print(f"📁 Fichiers traités      : {len(file_paths)}")
print("="*70)
print(f"\n✅ Compilation TEI terminée avec succès !")
print(f"📄 Fichier créé : {output_file}")
print("="*70)