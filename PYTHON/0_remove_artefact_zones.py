import os
import re

# Dossier racine des fichiers TEI originaux
root_dir = "data"
log_path = "log_zone_removal.txt"

def remove_artefact_zones(file_path):
    """
    Supprime les <div type='DigitizationArtefactZone'> et <div type='StampZone'>
    dans des fichiers TEI non-XML (format texte avec balises).
    """
    try:
        # Lire le contenu brut du fichier
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        zones_removed = 0
        
        # Pattern pour matcher une div complète (ouverture + contenu + fermeture)
        # Capture les types recherchés avec leurs variantes (guillemets simples ou doubles)
        patterns = [
            # Avec guillemets simples
            r"<div type='DigitizationArtefactZone'>.*?</div>",
            r"<div type='StampZone'>.*?</div>",
            # Avec guillemets doubles
            r'<div type="DigitizationArtefactZone">.*?</div>',
            r'<div type="StampZone">.*?</div>',
        ]
        
        # Supprimer chaque type de zone
        for pattern in patterns:
            matches = re.findall(pattern, content, re.DOTALL)
            zones_removed += len(matches)
            content = re.sub(pattern, '', content, flags=re.DOTALL)
        
        # Nettoyer les lignes vides multiples qui pourraient rester
        content = re.sub(r'\n\s*\n\s*\n+', '\n\n', content)
        
        # Sauvegarder seulement si des zones ont été supprimées
        if zones_removed > 0:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            return f"[OK] {file_path} → {zones_removed} zone(s) supprimée(s)"
        else:
            return f"[SKIP] {file_path} → Aucune zone à supprimer"
        
    except Exception as e:
        return f"[ERREUR] {file_path} → {str(e)}"

def inspect_file_structure(file_path):
    """Inspecte la structure d'un fichier pour debug"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        print(f"\n{'='*70}")
        print(f"📄 Inspection : {os.path.basename(file_path)}")
        print(f"{'='*70}")
        
        # Compter tous les types de <div>
        div_types = re.findall(r"<div type=['\"]([^'\"]+)['\"]>", content)
        
        if div_types:
            from collections import Counter
            type_counts = Counter(div_types)
            print(f"🔍 Types de <div> trouvés ({len(div_types)} total) :")
            for div_type, count in sorted(type_counts.items()):
                marker = "🎯" if div_type in ['DigitizationArtefactZone', 'StampZone'] else "  "
                print(f"  {marker} {div_type}: {count}")
        else:
            print("⚠️  Aucun <div type='...'> trouvé")
        
        # Montrer un extrait
        print("\n📝 Extrait du fichier (300 premiers caractères):")
        print("-" * 70)
        print(content[:300])
        print("...")
        print("-" * 70)
        
    except Exception as e:
        print(f"❌ Erreur d'inspection : {e}")

def remove_zones_from_all_files():
    """Parcours récursif des fichiers .tei pour supprimer les zones d'artefacts"""
    log_entries = []
    total_files = 0
    processed_files = 0
    total_zones = 0
    
    # Collecter tous les fichiers
    all_files = []
    for dirpath, _, filenames in os.walk(root_dir):
        for filename in filenames:
            if filename.endswith(".tei"):
                all_files.append(os.path.join(dirpath, filename))
    
    print("🔍 INSPECTION DE LA STRUCTURE DES FICHIERS")
    print("="*70)
    
    # Inspecter 5 fichiers échantillon
    sample_files = all_files[:5] if len(all_files) >= 5 else all_files
    for sample_file in sample_files:
        inspect_file_structure(sample_file)
    
    input("\n⏸️  Appuyez sur Entrée pour continuer le traitement...")
    
    print("\n\n🔄 TRAITEMENT DE TOUS LES FICHIERS")
    print("="*70)
    
    # Traiter tous les fichiers
    for file_path in all_files:
        total_files += 1
        result = remove_artefact_zones(file_path)
        log_entries.append(result)
        
        # Afficher seulement les fichiers modifiés ou en erreur
        if "[OK]" in result:
            print(result)
            processed_files += 1
            # Extraire le nombre de zones
            match = re.search(r'(\d+) zone\(s\)', result)
            if match:
                total_zones += int(match.group(1))
        elif "[ERREUR" in result:
            print(result)
    
    # Sauvegarder le log complet
    with open(log_path, "w", encoding="utf-8") as log_file:
        log_file.write("\n".join(log_entries))
    
    # Résumé final
    print("\n" + "="*70)
    print("📊 RÉSUMÉ FINAL")
    print("="*70)
    print(f"📁 Fichiers analysés      : {total_files}")
    print(f"✅ Fichiers modifiés      : {processed_files}")
    print(f"⏭️  Fichiers ignorés       : {total_files - processed_files}")
    print(f"🧹 Total zones supprimées : {total_zones}")
    print(f"📝 Log sauvegardé dans    : {log_path}")
    print("="*70)
    
    if total_zones == 0:
        print("\n⚠️  ATTENTION : Aucune zone supprimée !")
        print("\nCauses possibles :")
        print("  1. Aucun fichier ne contient de <div type='DigitizationArtefactZone'>")
        print("  2. Aucun fichier ne contient de <div type='StampZone'>")
        print("  3. Ces zones ont déjà été supprimées précédemment")
        print("\n💡 Vérifiez l'inspection ci-dessus pour voir les types réels.")
    else:
        print(f"\n✅ Succès ! {total_zones} zones d'artefacts ont été supprimées.")
        print("📌 Vous pouvez maintenant lancer le script 1_clean_tei.py")

if __name__ == "__main__":
    remove_zones_from_all_files()