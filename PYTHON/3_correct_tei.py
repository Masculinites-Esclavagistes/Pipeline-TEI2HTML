import os
from lxml import etree

# Dossier où se trouvent les fichiers
base_folder = "/Users/philipm/Documents/Pipeline_TEI/PYTHON/data"

def correct_tei_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Si le fichier ne contient pas le namespace TEI, on le corrige
    if '<TEI>' in content:
        content = content.replace('<TEI>', '<TEI xmlns="http://www.tei-c.org/ns/1.0">')

    # Si le fichier contient directement <body> au lieu de <text><body>, on l'encapsule
    if '<body>' in content and '<text>' not in content:
        content = content.replace('<body>', '<text>\n<body>', 1)
        content = content.replace('</body>', '</body>\n</text>', 1)

    # On vérifie que c’est bien du XML valide maintenant
    try:
        etree.fromstring(content.encode('utf-8'))
    except Exception as e:
        print(f"❌ ERREUR dans {file_path} : {e}")
        return

    # On remplace le fichier corrigé
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
        print(f"✅ Corrigé : {file_path}")

# Parcours récursif
for root, dirs, files in os.walk(base_folder):
    for file in files:
        if file.endswith(".tei"):
            correct_tei_file(os.path.join(root, file))
