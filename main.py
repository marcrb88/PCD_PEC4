from src.data_loader import load_dataset
from src.data_processing import clean_and_homogenize, aggregate_by_branch, merge_datasets
from src.visualization import plot_temporal_trends
from src.analysis import analyze_dataset


def mostrar_menu():
    """
    Mostra el menú interactiu principal i recull l'opció seleccionada per l'usuari.

    Imprimeix per pantalla les diferents opcions corresponents als exercicis
    de la PAC i retorna l'entrada de l'usuari per a la seva gestió.

    Returns:
        str: El caràcter o número introduït per l'usuari a través de la consola.
    """
    print("\n" + "=" * 50)
    print("      PEC4: ANÀLISI DEL RENDIMENT DELS ESTUDIANTS UNIVERSITARIS A CATALUNYA")
    print("=" * 50)
    print("1. Exercici 1: Carregar i explorar un dataset")
    print("2. Exercici 2: Neteja i fusió de dades (Merge)")
    print("3. Exercici 3: Anàlisi Visual (Sèries Temporals)")
    print("4. Exercici 4: Anàlisi Estadística (Informe JSON)")
    print("5. Executar tot: Flux complet de la PEC")
    print("0. Sortir")
    return input("\nSelecciona una opció: ")


def main():
    # Variables d'estat per emmagatzemar els DataFrames entre passos
    perf_df = None  # Per a les dades de rendiment
    drop_df = None  # Per a les dades d'abandonament
    merged_df = None  # Per al dataset final fusionat

    while True:
        choice = mostrar_menu()

        if choice == '1':
            # Exercici 1: Carrega del dataset i EDA.
            print("\nQuin dataset desitges explorar?")
            print("1. Taxa de rendiment (rendiment_estudiants.xlsx)")
            print("2. Taxa d'abandonament (taxa_abandonament.xlsx)")
            selection = input("Introdueix 1 o 2: ")

            if selection == '1':
                perf_df = load_dataset("data/rendiment_estudiants.xlsx")
                print("\n--- Vista prèvia del Dataset de Rendiment ---")
                print(perf_df.head())
            elif selection == '2':
                drop_df = load_dataset("data/taxa_abandonament.xlsx")
                print("\n--- Vista prèvia del Dataset d'Abandonament ---")
                print(drop_df.head())
            else:
                print("Selecció no vàlida.")

        elif choice == '2':
            # Exercici 2: Neteja i filtrat de dades.
            print("\nProcessant les dades per a la fusió...")
            if perf_df is None:
                print("Carregant dades de Rendiment (pendents)...")
                perf_df = load_dataset("data/rendiment_estudiants.xlsx")
            if drop_df is None:
                print("Carregant dades d'Abandonament (pendents)...")
                drop_df = load_dataset("data/taxa_abandonament.xlsx")

            # Pas 2.1 i 2.2: Neteja i homogeneïtzació.
            perf_clean, drop_clean = clean_and_homogenize(perf_df, drop_df)

            # Pas 2.3: Agrupació per branca.
            perf_agg = aggregate_by_branch(perf_clean, 'Taxa rendiment')
            drop_agg = aggregate_by_branch(drop_clean, '% Abandonament a primer curs')

            # Pas 2.4: Merge de datasets.
            merged_df = merge_datasets(perf_agg, drop_agg)
            print(f"Fusió completada amb èxit! Registres resultants: {len(merged_df)}")

        elif choice == '3':
            # Exercici 3: Anàlisi visual de tendències temporals.
            if merged_df is None:
                print("Error: Primer has d'executar l'Exercici 2 (Neteja i Fusió).")
            else:
                print("\nGenerant gràfics de sèries temporals...")
                plot_temporal_trends(merged_df, "Marc_Roige")

        elif choice == '4':
            # Exercici 4: Anàlisi estadística automatitzada.
            if merged_df is None:
                print("Error: Primer has d'executar l'Exercici 2 (Neteja i Fusió).")
            else:
                print("\nRealitzant anàlisi estadística i generant JSON...")
                report = analyze_dataset(merged_df)

        elif choice == '5':
            # Execució completa de la PEC4.
            print("\nIniciant flux complet de la PEC...")

            # Exercici 1 i 2: Càrrega dels datasets, neteja, homogeneïtzació i fusió dels datasets.
            raw_p = load_dataset("data/rendiment_estudiants.xlsx")
            raw_d = load_dataset("data/taxa_abandonament.xlsx")
            p_clean, d_clean = clean_and_homogenize(raw_p, raw_d)
            p_agg = aggregate_by_branch(p_clean, 'Taxa rendiment')
            d_agg = aggregate_by_branch(d_clean, '% Abandonament a primer curs')
            merged_df = merge_datasets(p_agg, d_agg)

            # Exercici 3: Visualització i desat del gràfic.
            plot_temporal_trends(merged_df, "Marc_Roige")

            # Pas 4: Generació d'informe estadístic.
            analyze_dataset(merged_df)

            print("\nPEC finalitzada correctament. Revisa les carpetes 'src/img' i 'src/report'.")

        elif choice == '0':
            print("Sortint del programa.")
            break
        else:
            print("Opció no vàlida. Torna-ho a intentar.")


if __name__ == "__main__":
    main()