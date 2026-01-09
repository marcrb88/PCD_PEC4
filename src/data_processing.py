"""
Mòdul de neteja de les dades i filtrat.

Aquest mòdul conté les funcions per netejar, homogeneïtzar columnes i
agregar dades de rendiment i abandonament universitari. Inclou la
lògica per fusionar ambdós datasets mitjançant una operació de fusió.
"""

import pandas as pd


def clean_and_homogenize(df_perf, df_aband):
    """
    Reanomenem les columnes del dataset taxa_abandonament.xlsx perquè coincideixi
    amb el dataset rendiment_estudiants.xlsx.
    També eliminem les columnes mencionades a l'enunciat.

    Args:
        df_perf (pd.DataFrame): Dataset de rendiment acadèmic.
        df_aband (pd.DataFrame): Dataset d'abandonament acadèmic.
    Returns:
        pd.DataFrame: Dataset de rendiment acadèmic netejat i transformat.
        pd.DataFrame: Dataset d'abandonament acadèmic amb les columnes renombrades.
    """
    # Renombrament de columnes del dataframe taxa_abandonament.
    rename_map = {
        'Naturalesa universitat responsable': 'Tipus universitat',
        'Universitat Responsable': 'Universitat',
        'Sexe Alumne': 'Sexe',
        'Tipus de centre': 'Integrat S/N'
    }
    df_aband = df_aband.rename(columns=rename_map)

    # Eliminar les columnes al dataframe de rendiment acadèmic.
    df_perf = df_perf.drop(columns=[
        'Universitat', 'Unitat',
        'Crèdits ordinaris superats', 'Crèdits ordinaris matriculats'
    ], errors='ignore')

    # Eliminar les columnes al dataframe d'abandonament acadèmic.
    df_aband = df_aband.drop(columns=[
        'Universitat', 'Unitat'
    ], errors='ignore')

    return df_perf, df_aband


def aggregate_by_branch(df, metric_col):
    """
    Agrupem totes les files per les característiques demanades i
    calculem la mitjana de la mètrica en ambdós datasets.

    Args:
        df (pd.DataFrame): Dataset de rendiment acadèmic o d'abandonament.
        metric_col (string): Columna amb el rendiment o abandonament mitjà.
    Returns:
        pd.DataFrame: Dataset de rendiment mitjà en cas del dataset de rendiment i amb taxa mitjana
        d'abandonament en cas del dataset d'abandonament.
    """

    group_cols = [
        'Curs Acadèmic', 'Tipus universitat', 'Sigles',
        'Tipus Estudi', 'Branca', 'Sexe', 'Integrat S/N'
    ]

    # Generem la nova columna amb el rendiment o abandonament mitjà i
    # resetejem l'índex per obtenir el dataframe.
    df_grouped = df.groupby(group_cols)[metric_col].mean().reset_index()

    return df_grouped


def merge_datasets(df_perf, df_aband):
    """
    Fusionem ambdós datasets en un. El dataset resultant només contindrà les files
    coincidents en ambdós datasets.

    Args:
        df_perf (pd.DataFrame): Dataset de rendiment acadèmic.
        df_aband (pd.DataFrame): Dataset d'abandonament.
    Returns:
        pd.DataFrame: Dataset final resultat de la fusió d'ambdós datasets.
    """
    join_cols = [
        'Curs Acadèmic', 'Tipus universitat', 'Sigles',
        'Tipus Estudi', 'Branca', 'Sexe', 'Integrat S/N'
    ]

    df_final = pd.merge(df_perf, df_aband, on=join_cols, how='inner')

    return df_final
