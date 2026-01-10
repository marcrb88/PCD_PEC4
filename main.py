import argparse
import sys
import os
from src.data_loader import load_dataset
from src.data_processing import clean_and_homogenize, aggregate_by_branch, merge_datasets
from src.visualization import plot_temporal_trends
from src.analysis import analyze_dataset

# Rutes per defecte
DEFAULT_RENDIMENT = "data/rendiment_estudiants.xlsx"
DEFAULT_ABANDONAMENT = "data/taxa_abandonament.xlsx"


def run_batch_mode(level, path_rendiment, path_abandonament):
    """
    Executa la lògica del programa.
    """
    print(f"\n--- Iniciant execució automàtica fins a l'exercici {level} ---")

    print("1. [Ex 1] Carregant datasets...")

    # --- LÒGICA EXERCICI 1 (Exploració) ---
    if level == 1:
        # CAS A: Interactivitat pura (Cap argument passat)
        if path_rendiment is None and path_abandonament is None:
            try:
                df_exploracio = load_dataset(None)
                print("\n--- Vista prèvia del Dataset Seleccionat ---")
                print(df_exploracio.head())
                print("Finalitzat Exercici 1 (Exploració interactiva).")
                return
            except Exception as e:
                print(f"Error: {e}")
                sys.exit(1)

        # CAS B: Només Rendiment passat per argument
        elif path_rendiment is not None and path_abandonament is None:
            print(f"   -> Carregant NOMÉS Rendiment: {path_rendiment}")
            df = load_dataset(path_rendiment)
            print("\n--- Vista prèvia Rendiment ---")
            print(df.head())
            print("Finalitzat Exercici 1 (Exploració Rendiment).")
            return

        # CAS C: Només Abandonament passat per argument
        elif path_abandonament is not None and path_rendiment is None:
            print(f"   -> Carregant NOMÉS Abandonament: {path_abandonament}")
            df = load_dataset(path_abandonament)
            print("\n--- Vista prèvia Abandonament ---")
            print(df.head())
            print("Finalitzat Exercici 1 (Exploració Abandonament).")
            return

    # --- PREPARACIÓ PER NIVELLS SUPERIORS (O EX 1 amb dos fitxers) ---
    # Si arribem aquí i volem continuar (o si level=1 però tenim els dos fitxers),
    # hem d'assegurar-nos que tenim els dos paths. Si algun és None, posem el Default.

    if path_rendiment is None:
        path_rendiment = DEFAULT_RENDIMENT
    if path_abandonament is None:
        path_abandonament = DEFAULT_ABANDONAMENT

    # Carreguem els dos datasets (necessari per Ex 2, 3, 4)
    try:
        print(f"   -> Rendiment: {path_rendiment}")
        raw_perf = load_dataset(path_rendiment)

        print(f"   -> Abandonament: {path_abandonament}")
        raw_drop = load_dataset(path_abandonament)
    except Exception as e:
        print(f"Error crític carregant dades: {e}")
        sys.exit(1)

    # Si estàvem al nivell 1 però (per algun motiu) teníem els dos fitxers, mostrem els dos
    if level == 1:
        print("\nDataset Rendiment Head:\n", raw_perf.head())
        print("\nDataset Abandonament Head:\n", raw_drop.head())
        print("Finalitzat Exercici 1.")
        return

    # --- EXERCICI 2: Processament ---
    print("\n2. [Ex 2] Netejant i fusionant dades...")
    perf_clean, drop_clean = clean_and_homogenize(raw_perf, raw_drop)
    perf_agg = aggregate_by_branch(perf_clean, 'Taxa rendiment')
    drop_agg = aggregate_by_branch(drop_clean, '% Abandonament a primer curs')
    merged_df = merge_datasets(perf_agg, drop_agg)

    if level == 2:
        print(f"Datasets fusionats. Total files: {len(merged_df)}")
        print("Finalitzat Exercici 2.")
        return

    # --- EXERCICI 3: Visualització ---
    print("\n3. [Ex 3] Generant gràfics...")
    plot_temporal_trends(merged_df, "Marc_Roige")

    if level == 3:
        print("Gràfics generats a 'src/img/'. Finalitzat Exercici 3.")
        return

    # --- EXERCICI 4: Anàlisi ---
    print("\n4. [Ex 4] Generant informe estadístic...")
    analyze_dataset(merged_df)
    print("Informe generat a 'src/report/'. Finalitzat Exercici 4 (Flux complet).")


def main():
    """
    Punt d'entrada principal.
    """
    parser = argparse.ArgumentParser(
        description="PEC4: Anàlisi de Rendiment i Abandonament Universitari"
    )

    parser.add_argument(
        '-ex', '--exercise',
        type=int,
        choices=[1, 2, 3, 4, 5],
        help="Nivell d'execució (1-4). Si no s'indica, s'executa tot."
    )

    parser.add_argument(
        '-d', '--dataset',
        type=str,
        help="Ruta a un dels fitxers de dades."
    )

    args = parser.parse_args()

    # 1. Determinació del nivell
    if args.exercise:
        target_level = 4 if args.exercise == 5 else args.exercise
    else:
        target_level = 4

    # 2. Determinació de paths
    final_rendiment = None
    final_abandonament = None

    if args.dataset:
        user_path = args.dataset
        filename = os.path.basename(user_path).lower()

        # MODIFICACIÓ CLAU:
        # Si l'usuari passa un fitxer, assignem aquell i DEIXEM L'ALTRE COM A NONE.
        # No forcem el default aquí encara, per permetre que l'Ex 1 detecti que només n'hi ha un.
        if "abandonament" in filename:
            final_abandonament = user_path
            # final_rendiment es queda None
        else:
            final_rendiment = user_path
            # final_abandonament es queda None

    # Executem la lògica
    run_batch_mode(target_level, final_rendiment, final_abandonament)


if __name__ == "__main__":
    main()
