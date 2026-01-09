"""
Mòdul d'exploració dels datasets.

Aquest mòdul conté les funcions necessàries per realitzar una inspecció
inicial dels datasets, incloent la visualització de mostres, l'estructura
de columnes i la informació tècnica dels tipus de dades.
"""
def perform_dataset_exploration(df):
    """
    Realitza una exploració bàsica del DataFrame proporcionat.

    Args:
        df (pd.DataFrame): El DataFrame a explorar.
    """
    print("\n--- 1.1. Cinc primeres files ---")
    print(df.head())

    print("\n--- 1.2. Columnes del dataset ---")
    print(df.columns.tolist())

    print("\n--- 1.3. Informació general (info) ---")
    df.info()
