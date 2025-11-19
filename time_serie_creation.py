import numpy as np
import pandas as pd
import os

def create_continuous_sequences(df: pd.DataFrame, k: int, interval_minutes: int = 15) -> tuple[list[pd.DataFrame], list[pd.DataFrame]]:
    """
    Crée des séquences continues de taille k+1 (k étapes d'entrée et 1 étape de sortie) à partir du DataFrame.
    S'assure que la différence de temps entre chaque étape est exactement de interval_minutes.
    
    Args:
        df (pd.DataFrame): DataFrame contenant une colonne 'Datetime'.
        k (int): Taille de la fenêtre glissante (séquence d'entrée).
        interval_minutes (int): Intervalle de temps attendu en minutes (défaut: 15).
        
    Returns:
        list[pd.DataFrame]: Liste de DataFrames contenant les séquences d'entrée et de sortie.
    """
    sequences = []
    targets = []
    
    # Vérification de la colonne Datetime
    if 'Datetime' not in df.columns:
        raise ValueError("Le DataFrame doit avoir une colonne 'Datetime'")
        
    df = df.copy()
    
    # Conversion en datetime si nécessaire
    if not pd.api.types.is_datetime64_any_dtype(df['Datetime']):
        df['Datetime'] = pd.to_datetime(df['Datetime'], utc=True)
        
    df = df.sort_values('Datetime')

    # Suppression de la colonne 'Unnamed: 0' si elle existe
    if 'Unnamed: 0' in df.columns:
        df = df.drop(columns=['Unnamed: 0'])
    
    # Calcul de la différence de temps entre chaque ligne
    df['time_diff'] = df['Datetime'].diff()
    
    # Identifier les ruptures de continuité (différence != intervalle attendu)
    # La première ligne aura NaT, donc on considère ça comme une rupture (True)
    df['gap'] = df['time_diff'] != pd.Timedelta(minutes=interval_minutes)
    
    # Créer des groupes continus : à chaque 'gap', on incrémente l'ID du groupe
    df['group_id'] = df['gap'].cumsum()
    
    # Colonnes à conserver (toutes sauf les colonnes techniques ajoutées)
    cols_to_keep = [c for c in df.columns if c not in ['time_diff', 'gap', 'group_id']]
    
    # Pour chaque groupe continu, on extrait les séquences
    for g_id, group in df.groupby('group_id'):
        # On travaille uniquement sur les colonnes originales
        group_data = group[cols_to_keep]
        
        if len(group_data) > k:
            # Création des fenêtres glissantes
            # Pour avoir une séquence d'entrée de taille k et une cible à k+1,
            # il faut au moins k+1 éléments.
            for i in range(len(group_data) - k):
                # Séquence d'entrée : lignes i à i+k (exclus) -> k lignes
                seq = group_data.iloc[i : i+k].copy()
                # Cible : ligne i+k -> 1 ligne (sous forme de DataFrame pour garder la structure)
                target = group_data.iloc[[i+k]].copy()
                
                sequences.append(seq)
                targets.append(target)
                
    return sequences, targets

if __name__ == "__main__":
    # Exemple d'utilisation
    # Chemin relatif vers un fichier de données (à adapter selon votre structure)
    file_path = "data/AC.PA.csv"
    
    if os.path.exists(file_path):
        print(f"Chargement de {file_path}...")
        df = pd.read_csv(file_path)
        
        k = 20  # Taille de la fenêtre
        print(f"Génération de séquences avec k={k} et intervalle de 15 min...")
        
        X, y = create_continuous_sequences(df, k)
        
        print(f"Nombre de séquences générées: {len(X)}")
        if len(X) > 0:
            print(f"Type de X[0]: {type(X[0])}")
            print(f"Shape de X[0]: {X[0].shape}")
            print(f"Type de y[0]: {type(y[0])}")
            print(f"Shape de y[0]: {y[0].shape}")
        
            print("\nExemple de première séquence (Input):")
            print(X[0].head())
            print("\nExemple de cible correspondante (Target):")
            print(y[0])
    else:
        print(f"Fichier {file_path} non trouvé. Veuillez vérifier le chemin.")
