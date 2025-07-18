from lxml import etree
import os
import math

# Paramètres
input_file = "/Users/philipm/Documents/Pipeline_TEI/PYTHON/output/megv_corpus.xml"
output_dir = "/Users/philipm/Documents/Pipeline_TEI/PYTHON/output/parts"
divs_per_file = 178

# Créer dossier de sortie s'il n'existe pas
os.makedirs(output_dir, exist_ok=True)

# Parse XML
tree = etree.parse(input_file)
ns = {"tei": "http://www.tei-c.org/ns/1.0"}

# Récupère le teiHeader
tei_header = tree.find(".//tei:teiHeader", namespaces=ns)

# Récupère tous les <div type="file"> dans le body
divs = tree.xpath("//tei:body/tei:div[@type='file']", namespaces=ns)
print(f"🔍 Total de <div type='file'> trouvés : {len(divs)}")

# Nombre total de fichiers à générer
total_parts = math.ceil(len(divs) / divs_per_file)

for i in range(total_parts):
    start = i * divs_per_file
    end = start + divs_per_file
    div_chunk = divs[start:end]

    # Nouveau root TEI
    tei = etree.Element("{http://www.tei-c.org/ns/1.0}TEI", nsmap={None: "http://www.tei-c.org/ns/1.0"})

    # Ajout du teiHeader
    tei.append(tei_header)

    # Construction de text > body > divs
    text_el = etree.SubElement(tei, "{http://www.tei-c.org/ns/1.0}text")
    body_el = etree.SubElement(text_el, "{http://www.tei-c.org/ns/1.0}body")

    for div in div_chunk:
        body_el.append(div)

    # Sauvegarde
    output_path = os.path.join(output_dir, f"megv_corpus_part{i+1}.xml")
    etree.ElementTree(tei).write(output_path, encoding="utf-8", xml_declaration=True, pretty_print=True)
    print(f"✅ Écrit : {output_path}")
