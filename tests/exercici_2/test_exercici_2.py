"""
Tests unitaris per a l'exercici 2: Neteja de dades i filtrat.

Aquest mòdul verifica la neteja de columnes, l'homogeneïtzació,
l'agregació per branques i la fusió final (merge) dels datasets.
"""

import unittest
import pandas as pd
from src.data_processing import clean_and_homogenize, aggregate_by_branch, merge_datasets


class TestExercici2(unittest.TestCase):
    """Suite de tests per al processament i transformació de dataframes."""

    def setUp(self):
        """Configura l'entorn de proves i dades simulades."""

        # Dades de rendiment simulades.
        self.perf_data = pd.DataFrame({
            'Curs Acadèmic': ['2021-22', '2021-22'],
            'Universitat': ['UB', 'UB'],
            'Sigles': ['UB', 'UB'],
            'Unitat': ['Facultat A', 'Facultat A'],
            'Tipus Estudi': ['Grau', 'Grau'],
            'Branca': ['Salut', 'Salut'],
            'Sexe': ['Dona', 'Home'],
            'Integrat S/N': ['S', 'S'],
            'Tipus universitat': ['Pública', 'Pública'],
            'Taxa rendiment': [0.8, 0.9],
            'Crèdits ordinaris superats': [100, 100],
            'Crèdits ordinaris matriculats': [120, 120]
        })

        # Dades d'abandonament simulades (amb noms de columnes originals).
        self.aband_data = pd.DataFrame({
            'Curs Acadèmic': ['2021-22', '2021-22'],
            'Naturalesa universitat responsable': ['Pública', 'Pública'],
            'Universitat Responsable': ['UB', 'UB'],
            'Sigles': ['UB', 'UB'],
            'Unitat': ['Facultat A', 'Facultat A'],
            'Tipus Estudi': ['Grau', 'Grau'],
            'Branca': ['Salut', 'Salut'],
            'Sexe Alumne': ['Dona', 'Home'],
            'Tipus de centre': ['S', 'S'],
            '% Abandonament a primer curs': [0.1, 0.2]
        })

    def test_clean_and_homogenize(self):
        """Verifica que les columnes es reanomenen i s'eliminen correctament."""
        df_p, df_a = clean_and_homogenize(self.perf_data.copy(), self.aband_data.copy())

        # Comprovem reanomenament a l'abandonament.
        self.assertIn('Tipus universitat', df_a.columns)
        self.assertIn('Sexe', df_a.columns)
        self.assertIn('Integrat S/N', df_a.columns)

        # Comprovem eliminació de columnes a rendiment.
        self.assertNotIn('Unitat', df_p.columns)
        self.assertNotIn('Crèdits ordinaris superats', df_p.columns)
        self.assertNotIn('Universitat', df_p.columns)

    def test_aggregate_by_branch(self):
        """Verifica que l'agrupació calcula correctament la mitjana."""
        # Creem un cas amb dues files que s'han d'agrupar en una (mateixes claus).
        df_to_group = pd.DataFrame({
            'Curs Acadèmic': ['21-22', '21-22'],
            'Tipus universitat': ['P', 'P'],
            'Sigles': ['U', 'U'],
            'Tipus Estudi': ['G', 'G'],
            'Branca': ['B', 'B'],
            'Sexe': ['D', 'D'],
            'Integrat S/N': ['S', 'S'],
            'Valor': [10, 20]
        })

        df_res = aggregate_by_branch(df_to_group, 'Valor')

        # Ha de quedar 1 sola fila i la mitjana ha de ser 15.0.
        self.assertEqual(len(df_res), 1)
        self.assertEqual(df_res['Valor'].iloc[0], 15.0)

    def test_merge_datasets_inner(self):
        """Verifica que la fusió inner només manté les files coincidents."""
        # Preparem dades ja netejades i agregades.
        df_p, df_a = clean_and_homogenize(self.perf_data, self.aband_data)

        # Agreguem (en aquest cas de test sortirà 1 fila per cada sexe).
        df_p_agg = aggregate_by_branch(df_p, 'Taxa rendiment')
        df_a_agg = aggregate_by_branch(df_a, '% Abandonament a primer curs')

        merged = merge_datasets(df_p_agg, df_a_agg)

        # Comprovem que tenim columnes d'ambdós datasets.
        self.assertIn('Taxa rendiment', merged.columns)
        self.assertIn('% Abandonament a primer curs', merged.columns)
        # En el nostre setUp, hi ha 2 coincidències (Dona i Home).
        self.assertEqual(len(merged), 2)

    def test_merge_datasets_no_match(self):
        """Verifica que si no hi ha coincidències, el merge és buit."""
        df_p = pd.DataFrame({
            'Curs Acadèmic': ['A'], 'Tipus universitat': ['A'], 'Sigles': ['A'],
            'Tipus Estudi': ['A'], 'Branca': ['A'], 'Sexe': ['A'], 'Integrat S/N': ['A'],
            'Taxa rendiment': [0.5]
        })
        df_a = pd.DataFrame({
            'Curs Acadèmic': ['B'], 'Tipus universitat': ['B'], 'Sigles': ['B'],
            'Tipus Estudi': ['B'], 'Branca': ['B'], 'Sexe': ['B'], 'Integrat S/N': ['B'],
            '% Abandonament a primer curs': [0.1]
        })

        merged = merge_datasets(df_p, df_a)
        self.assertEqual(len(merged), 0)


if __name__ == '__main__':
    unittest.main()
