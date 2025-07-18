import os
import re

# Dossier racine des fichiers TEI
root_dir = "data"
log_path = "log_cleaning.txt"

# Caractères interdits ou problématiques en XML
def escape_xml(text):
    text = text.replace("&", "&amp;")  # important: doit être fait en premier
    text = text.replace("<", "&lt;")
    text = text.replace(">", "&gt;")
    text = text.replace('"', "&quot;")
    text = text.replace("'", "&apos;")
    # attention aux entités mal fermées :
    text = re.sub(r"&(?!(amp|lt|gt|quot|apos);)", "&amp;", text)
    return text

# Supprime toutes les balises XML
def strip_xml_tags(text):
    return re.sub(r"</?[^>]+>", "", text)

# Nettoyage et restructuration du fichier
def clean_tei_file(file_path):
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            lines = f.readlines()

        # Supprimer balises et nettoyer caractères interdits
        cleaned_lines = []
        for line in lines:
            text = strip_xml_tags(line.strip())
            if text:  # Ignore lignes vides
                text = escape_xml(text)
                cleaned_lines.append(f"{text}<lb/>")

        final_text = "<p>\n" + "\n".join(cleaned_lines) + "\n</p>"

        with open(file_path, "w", encoding="utf-8") as f:
            f.write(final_text)

        return f"[OK] Nettoyé : {file_path}"
    
    except Exception as e:
        return f"[ERREUR] {file_path} — {str(e)}"

# Parcours récursif des fichiers .tei
def clean_all_tei_files():
    log_entries = []
    for dirpath, _, filenames in os.walk(root_dir):
        for filename in filenames:
            if filename.endswith(".tei"):
                file_path = os.path.join(dirpath, filename)
                log_entries.append(clean_tei_file(file_path))

    with open(log_path, "w", encoding="utf-8") as log_file:
        log_file.write("\n".join(log_entries))

    print(f"✅ Traitement terminé. Log disponible dans : {log_path}")

if __name__ == "__main__":
    clean_all_tei_files()
