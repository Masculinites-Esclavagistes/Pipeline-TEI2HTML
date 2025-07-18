import os
from lxml import etree

# Dossier contenant les fichiers TEI
base_folder = "/Users/philipm/Documents/Pipeline_TEI/PYTHON/data"

# Fonction de validation XML
def validate_tei_file(file_path):
    try:
        with open(file_path, 'rb') as f:
            etree.parse(f)  # parse le fichier comme XML complet
        return True, None
    except Exception as e:
        return False, str(e)

# Parcours récursif du dossier
invalid_files = []

for root, dirs, files in os.walk(base_folder):
    for file in files:
        if file.endswith(".tei"):
            full_path = os.path.join(root, file)
            is_valid, error_msg = validate_tei_file(full_path)
            if not is_valid:
                print(f"❌ Invalide : {full_path}\n   ↪︎ Erreur : {error_msg}")
                invalid_files.append(full_path)

# Résumé
print("\n--- Résumé ---")
if not invalid_files:
    print("✅ Tous les fichiers .tei sont bien formés.")
else:
    print(f"⚠️ {len(invalid_files)} fichier(s) mal formé(s).")
