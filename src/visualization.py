import matplotlib.pyplot as plt
import os


def plot_temporal_trends(df, student_name):
    """
    Genera i desa gràfics de línies sobre l'evolució de l'abandonament i el rendiment.

    Aquesta funció crea una figura amb dos subplots:
    1. L'evolució del percentatge d'abandonament per branca i curs.
    2. L'evolució de la taxa de rendiment per branca i curs.
    La imatge resultant es desa automàticament a la carpeta src/img/.

    Args:
        df (pd.DataFrame): Dataset fusionat que conté la informació a representar gràficament.
        student_name (str): Nom de l'estudiant que s'utilitzarà per generar el
            nom del fitxer de sortida (format: evolucio_nom_cognom.png).

    Returns:
        None: La funció no retorna cap valor, però genera i desa un fitxer PNG.
    """
    # Ordenem el dataframe per Curs Acadèmic (per default ascendent -> de més antic a més actual).
    df = df.sort_values('Curs Acadèmic')
    branques = df['Branca'].unique()

    # Creem el gràfic amb 2 subplots: taxa de rendiment acadèmic i % abandonament acadèmic.
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(14, 10))

    # Definim els colors.
    colors = plt.cm.tab10.colors

    # SUBPLOT 1: Abandonament acadèmic.
    for i, branca in enumerate(branques):
        subset = df[df['Branca'] == branca]
        # Agrupem per curs perquè hi ha diverses files per branca i calculem la mitjana.
        plot_data = subset.groupby('Curs Acadèmic')['% Abandonament a primer curs'].mean()

        ax1.plot(plot_data.index, plot_data.values, marker='o', label=branca, color=colors[i % 10])

    # Afegim informació general del gràfic: títol, etiqueta, llegenda.
    ax1.set_title("Evolució del % d'Abandonament per curs acadèmic", fontsize=14, fontweight='bold')
    ax1.set_ylabel("% Abandonament")
    ax1.grid(True, linestyle='--', alpha=0.7)
    ax1.legend(title="Branques", bbox_to_anchor=(1.05, 1), loc='upper left')

    # SUBPLOT 2: Rendiment acadèmic.
    for i, branca in enumerate(branques):
        subset = df[df['Branca'] == branca]
        # Fem el mateix que amb l'abandonament, agrupem per curs i calculem la mitjana.
        plot_data = subset.groupby('Curs Acadèmic')['Taxa rendiment'].mean()

        ax2.plot(plot_data.index, plot_data.values, marker='s', label=branca, color=colors[i % 10])

    # Afegim informació general del gràfic: títol, etiquetes, llegenda.
    ax2.set_title("Evolució de la Taxa de Rendiment per curs acadèmic", fontsize=14, fontweight='bold')
    ax2.set_xlabel("Curs Acadèmic")
    ax2.set_ylabel("Taxa de Rendiment (0-1)")
    ax2.grid(True, linestyle='--', alpha=0.7)
    ax2.legend(title="Branques", bbox_to_anchor=(1.05, 1), loc='upper left')

    # Ajustaments finals de format
    plt.xticks(rotation=45)
    plt.tight_layout()

    # Desem la visualització a la carpeta src/img.
    output_dir = "src/img"
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        print(f"Directori creat: {output_dir}")

    filename = f"evolucio_{student_name.lower().replace(' ', '_')}.png"
    save_path = os.path.join(output_dir, filename)

    plt.savefig(save_path, dpi=300, bbox_inches='tight')
    print(f"Gràfic desat correctament a: {save_path}")