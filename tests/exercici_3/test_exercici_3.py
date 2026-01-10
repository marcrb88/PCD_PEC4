"""
Tests unitaris per a l'exercici 3: Anàlisi visual de tendències temporals.

Aquest mòdul verifica la generació del gràfic de tendències temporals
i assegura que el fitxer .png es crea correctament al directori de proves.
"""

# 1. Standard Library Imports
import unittest
import os

# 2. Third Party Imports
import matplotlib
import matplotlib.pyplot as plt
import pandas as pd

# 3. Local Application Imports
from src.visualization import plot_temporal_trends

# Configurem Matplotlib per a mode no interactiu (no obre finestres).
matplotlib.use('Agg')


class TestExercici3(unittest.TestCase):
    """Suite de tests per a la generació de visualitzacions."""

    def setUp(self):
        """Configura dades simulades i rutes de prova."""
        test_name = self.id().split('.')[-1]
        print(f"\n> EXECUTANT PROVA: {test_name}")
        print("-" * 30)

        # Creem dades mínimes necessàries per al gràfic.
        self.test_df = pd.DataFrame({
            'Curs Acadèmic': ['2020-21', '2021-22', '2020-21', '2021-22'],
            'Branca': ['Salut', 'Salut', 'Arts', 'Arts'],
            'Taxa rendiment': [0.8, 0.85, 0.7, 0.72],
            '% Abandonament a primer curs': [0.1, 0.08, 0.15, 0.12]
        })

        self.student_name = "Test_User"
        # Ruta on el codi original voldrà desar la imatge.
        self.expected_path = "src/img/evolucio_test_user.png"

    def test_plot_generation_file_exists(self):
        """Verifica que la funció crea el fitxer PNG físicament."""
        # Netegem si ja existia d'una prova anterior.
        if os.path.exists(self.expected_path):
            os.remove(self.expected_path)

        # Executem la visualització.
        plot_temporal_trends(self.test_df, self.student_name)

        # Comprovem que el fitxer s'ha creat.
        self.assertTrue(os.path.exists(self.expected_path), "El gràfic no s'ha generat.")

        # Opcional: Verificar que el fitxer no està buit.
        if os.path.exists(self.expected_path):
            self.assertGreater(os.path.getsize(self.expected_path), 0)

    def test_plot_content_logic(self):
        """Verifica que la funció no falla amb un DataFrame d'una sola branca."""
        single_branch_df = self.test_df[self.test_df['Branca'] == 'Salut']

        # Si falla, unittest ho marca com Error automàticament.
        plot_temporal_trends(single_branch_df, "Single_Branch")

    def tearDown(self):
        """Neteja de les imatges de test generades."""
        # Neteja imatge del primer test.
        if os.path.exists(self.expected_path):
            os.remove(self.expected_path)

        # Neteja imatge del segon test.
        single_path = "src/img/evolucio_single_branch.png"
        if os.path.exists(single_path):
            os.remove(single_path)

        # Tanquem totes les figures per alliberar memòria.
        plt.close('all')


if __name__ == '__main__':
    unittest.main()
