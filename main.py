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

    # Exercici 1
    if level == 1:
        # CAS A: L'usuari selecciona l'exercici 1 i NO passa cap path com a argument.
        if path_rendiment is None and path_abandonament is None:
            try:
                df_exploracio = load_dataset(None)
                print("\n--- Vista prèvia del dataset Seleccionat ---")
                print(df_exploracio.head())
                print("Finalitzat exercici 1")
                return
            except Exception as e:
                print(f"Error: {e}")
                sys.exit(1)

        # CAS B: L'usuari selecciona l'exercici 1 i passa el path de rendiment com a argument.
        elif path_rendiment is not None and path_abandonament is None:
            print(f"   -> Carregant NOMÉS rendiment: {path_rendiment}")
            df = load_dataset(path_rendiment)
            print("\n--- Vista prèvia rendiment acadèmic ---")
            print(df.head())
            print("Finalitzat exercici 1.")
            return

        # CAS C: L'usuari selecciona l'exercici 1 i passa el path d'abandonament com a argument.
        elif path_abandonament is not None and path_rendiment is None:
            print(f"   -> Carregant NOMÉS abandonament: {path_abandonament}")
            df = load_dataset(path_abandonament)
            print("\n--- Vista prèvia abandonament acadèmic ---")
            print(df.head())
            print("Finalitzat exercici 1.")
            return

    # PREPARACIÓ PER NIVELLS SUPERIORS
    # A partir d'aquí ens hem d'assegurar que tenim 2 datasets carregats per poder
    # efectuar les operacions que vindran en els propers exercicis,
    # per tant, en cas de tenir algun dataset a None, el sistema el carregarà.

    if path_rendiment is None:
        path_rendiment = DEFAULT_RENDIMENT
    if path_abandonament is None:
        path_abandonament = DEFAULT_ABANDONAMENT

    # Carreguem els dos datasets necessaris.
    try:
        print(f"   -> Rendiment: {path_rendiment}")
        raw_perf = load_dataset(path_rendiment)

        print(f"   -> Abandonament: {path_abandonament}")
        raw_drop = load_dataset(path_abandonament)
    except Exception as e:
        print(f"Error crític carregant dades: {e}")
        sys.exit(1)

    # Exercici 2.
    print("\n2. [Ex 2] Netejant i fusionant dades...")
    perf_clean, drop_clean = clean_and_homogenize(raw_perf, raw_drop)
    perf_agg = aggregate_by_branch(perf_clean, 'Taxa rendiment')
    drop_agg = aggregate_by_branch(drop_clean, '% Abandonament a primer curs')
    merged_df = merge_datasets(perf_agg, drop_agg)

    if level == 2:
        print(f"Datasets fusionats. Total files: {len(merged_df)}")
        print("Finalitzat exercici 2.")
        return

    # Exercici 3.
    print("\n3. [Ex 3] Generant gràfics...")
    plot_temporal_trends(merged_df, "Marc_Roige")

    if level == 3:
        print("Gràfics generats a 'src/img/'. Finalitzat exercici 3.")
        return

    # Exercici 4.
    print("\n4. [Ex 4] Generant informe estadístic...")
    analyze_dataset(merged_df)
    print("Informe generat a 'src/report/'. Finalitzat exercici 4 (Flux complet).")


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
        choices=[1, 2, 3, 4],
        help="Nivell d'execució (1-4). Si no s'indica, s'executa tot."
    )

    parser.add_argument(
        '-d', '--dataset',
        type=str,
        help="Ruta a un dels fitxers de dades."
    )

    args = parser.parse_args()
    target_level = args.exercise

    # 2. Determinació de paths
    final_rendiment = None
    final_abandonament = None

    if args.dataset:
        user_path = args.dataset
        filename = os.path.basename(user_path).lower()

        # Si l'usuari passa com argument un fitxer, assignem aquell i deixem l'altre com a None.
        if "abandonament" in filename:
            final_abandonament = user_path
        else:
            final_rendiment = user_path

    # Executem la lògica
    run_batch_mode(target_level, final_rendiment, final_abandonament)


if __name__ == "__main__":
    main()
