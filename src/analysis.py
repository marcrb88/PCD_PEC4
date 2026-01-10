"""
Mòdul d'anàlisi estadística automatitzada pel rendiments dels estudiants universitaris de Catalunya.

Aquest mòdul conté funcions per calcular estadístiques tant globals com específiques
per branca d'estudi, tendències de rendiment i abandonament
i generar un informe final en format JSON.
"""
import json
import os
from datetime import datetime
from scipy.stats import linregress, pearsonr


def get_tendencia(years, values):
    """
    Interpreta el pendent de la regressió lineal per categoritzar la tendència.

    Args:
        years (list): Llista amb els noms dels períodes temporals (ex: ['19-20', '20-21']).
        values (list): Llista de valors numèrics (mitjanes) corresponents a cada període.
    Returns:
        str: Categorització de la tendència: 'creciente', 'decreciente' o 'estable'.
    """
    slope, _, _, _, _ = linregress(range(len(years)), values)
    if slope > 0.01:
        return "creciente"
    if slope < -0.01:
        return "decreciente"
    return "estable"


def get_branch_analysis(df, branches):
    """
    Realitza l'anàlisi estadístic detallat per a cada branca d'estudi.

    Agrupa les dades per any acadèmic, calcula les mitjanes, desviacions
    i les tendències temporals per a cada branca de coneixement.

    Args:
        df (pd.DataFrame): Dataset fusionat.
        branches (numpy.ndarray): Llista de branques a analitzar.

    Returns:
        dict: Diccionari on cada clau és una branca amb les seves estadístiques i tendències.
    """
    analysis_branch = {}
    for branch in branches:
        branch_data = df[df['Branca'] == branch]

        # Agrupem les dades per any acadèmic per a cada branca.
        branch_by_year = branch_data.groupby('Curs Acadèmic').agg({
            '% Abandonament a primer curs': 'mean',
            'Taxa rendiment': 'mean'
        }).reset_index()

        # Extreiem les llistes d'anys i valors.
        years = branch_by_year['Curs Acadèmic'].tolist()
        abandonment_values = branch_by_year['% Abandonament a primer curs'].tolist()
        performance_values = branch_by_year['Taxa rendiment'].tolist()

        # Seleccionem les columnes per facilitar el càlcul d'estadístics
        col_aband = branch_data['% Abandonament a primer curs']
        col_perf = branch_data['Taxa rendiment']

        analysis_branch[branch] = {
            "abandono_medio": round(float(col_aband.mean()), 2),
            "abandono_std": round(float(col_aband.std()), 2),
            "abandono_min": round(float(col_aband.min()), 2),
            "abandono_max": round(float(col_aband.max()), 2),
            "rendimiento_medio": round(float(col_perf.mean()), 2),
            "rendimiento_std": round(float(col_perf.std()), 2),
            "rendimiento_min": round(float(col_perf.min()), 2),
            "rendimiento_max": round(float(col_perf.max()), 2),
            "tendencia_abandono": get_tendencia(years, abandonment_values),
            "tendencia_rendimiento": get_tendencia(years, performance_values),
            "años_anomalos": []
        }
    return analysis_branch


def analyze_dataset(df):
    """
    Informació bàsica sobre l'anàlisis estadística que estem realitzant.

    Args:
        df (pd.DataFrame): Dataset fusionat a analitzar estadísticament.
    Returns:
        dict: Un diccionari amb el resum estadístic complet (metadades,
              correlacions, anàlisi per branca i rànquings).
    """
    # Calculem la informació bàsica de l'anàlisi.
    metadata = {
        "fecha_analisis": datetime.now().strftime("%Y-%m-%d"),
        "num_registros": int(len(df)),
        "periodo_temporal": sorted(df['Curs Acadèmic'].unique().tolist())
    }

    # Calculem la correlació entre l'abandonament i rendiment.
    corr, _ = pearsonr(df['% Abandonament a primer curs'].dropna(),
                       df['Taxa rendiment'].dropna())

    # Anàlisi detallat per branca.
    analysis_branch = get_branch_analysis(df, df['Branca'].unique())

    # Ordenem de forma descendent per taxa de rendiment.
    performance_sorted_df = df.sort_values(
        by=["Taxa rendiment"],
        ascending=False
    )

    best_performance_tax = performance_sorted_df["Branca"].iloc[0]
    worst_performance_tax = performance_sorted_df["Branca"].iloc[-1]

    abandonment_sorted_df = df.sort_values(
        by=["% Abandonament a primer curs"],
        ascending=False
    )

    best_abandonment = abandonment_sorted_df["Branca"].iloc[0]
    worst_abandonment = abandonment_sorted_df["Branca"].iloc[-1]

    full_report = {
        "metadata": metadata,
        "estadisticas_globales": {
            "abandono_medio": round(float(df['% Abandonament a primer curs'].mean()), 2),
            "rendimiento_medio": round(float(df['Taxa rendiment'].mean()), 2),
            "correlacion_abandono_rendimiento": round(float(corr), 2)
        },
        "analisis_por_rama": analysis_branch,
        "ranking_ramas": {
            "mejor_rendimiento": [best_performance_tax],
            "peor_rendimiento": [worst_performance_tax],
            "mayor_abandono": [best_abandonment],
            "menor_abandono": [worst_abandonment]
        }
    }

    # Exportació a JSON
    output_path = "src/report/analisi_estadistic.json"
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(full_report, f, indent=2, ensure_ascii=False)

    print(f"Informe generat correctament a: {output_path}")

    return full_report
