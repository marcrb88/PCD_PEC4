"""
Mòdul de càrrega dels datasets acadèmics.

Aquest mòdul proporciona les eines per importar fitxers Excel de rendiment
i abandonament universitari, incloent-hi un menú interactiu per a la
selecció de fitxers.
"""

import os
import warnings
import pandas as pd


def load_dataset(path=None):
    """
    Carrega el dataset passat per paràmetre.
    Si no es proporciona cap ruta, es demana a l'usuari quin dataset carregar.
    En cas de que l'usuari seleccioni una opció de dataset invàlida,
    carreguem el primer per defecte.

    Args:
        path (str, opcional): Ruta al dataset. Per defecte és None.
    Returns:
        pd.DataFrame: El dataset carregat en un DataFrame de pandas.
    """
    # Ignorem els avisos de format de openpyxl
    warnings.filterwarnings("ignore", category=UserWarning, module="openpyxl")

    if path is None:
        print("Quin dataset desitges carregar?")
        print("1. Taxa de rendiment (rendiment_estudiants.xlsx)")
        print("2. Taxa d'abandonament (taxa_abandonament.xlsx)")

        option = input("Introdueix 1 o 2: ")

        if option == '1':
            path = "data/rendiment_estudiants.xlsx"
        elif option == '2':
            path = "data/taxa_abandonament.xlsx"
        else:
            print("Opció no vàlida. Carreguem el primer per defecte.")
            # Presa de decisió: si l'usuari no introdueix una opció vàlida,
            # seleccionem per defecte el primer dataset.
            path = "data/rendiment_estudiants.xlsx"

    if not os.path.exists(path):
        raise FileNotFoundError(f"No s'ha trobat l'arxiu a la ruta: {path}")

    df = pd.read_excel(path)

    return df
