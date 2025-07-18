import os
import re
from lxml import etree

data_dir = "data"
output_dir = "data"
os.makedirs(output_dir, exist_ok=True)

def extract_num(filename):
    match = re.search(r'_(\d{4,5})\.tei$', filename)
    return int(match.group(1)) if match else 0

for dossier in sorted(os.listdir(data_dir)):
    dossier_path = os.path.join(data_dir, dossier)
    if not os.path.isdir(dossier_path):
        continue

    tei_files = [f for f in os.listdir(dossier_path) if f.endswith(".tei")]
    tei_files = [f for f in tei_files if re.search(r'_\d{4,5}\.tei$', f)]
    tei_files.sort(key=extract_num)

    # Racine TEI vide
    root = etree.Element("TEI")
    body = etree.SubElement(root, "body")

    for tei_file in tei_files:
        tei_path = os.path.join(dossier_path, tei_file)
        
        # Ajouter la balise <pb corresp="..."/>
        pb = etree.Element("pb")
        pb.set("corresp", f"{dossier}/{tei_file[:-4]}")
        body.append(pb)

        # Lire contenu brut du fichier
        with open(tei_path, "r", encoding="utf-8") as f:
            content = f.read()

        # Enrober le contenu brut dans un élément temporaire
        try:
            # On encapsule dans un élément temporaire
            temp = etree.fromstring(f"<wrapper>{content}</wrapper>")
            for child in temp:
                body.append(child)
        except etree.XMLSyntaxError as e:
            print(f"[Erreur XML ignorée] Fichier: {tei_file} — {e}")
            continue

    # Sauvegarder le fichier compilé
    output_path = os.path.join(output_dir, f"{dossier}.tei")
    with open(output_path, "wb") as f:
        f.write(etree.tostring(root, pretty_print=True, xml_declaration=True, encoding="UTF-8"))

    print(f"[OK] {output_path}")
