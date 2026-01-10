"""
Tests unitaris per a l'exercici 4: Anàlisi estadística automatitzada.

Aquest mòdul verifica les metadades, estadístiques globals, els càlculs de tendències,
estadístiques per branca i la correcta generació de l'informe JSON.
"""

import unittest
import os
import json
import pandas as pd
from src.analysis import get_tendencia, analyze_dataset


class TestExercici4(unittest.TestCase):
    """Suite de tests per a les funcions d'anàlisi estadística automatitzada."""

    def setUp(self):
        """Prepara un DataFrame de prova amb tendències controlades."""
        self.test_df = pd.DataFrame({
            'Curs Acadèmic': ['2020-21', '2021-22', '2022-23', '2020-21', '2021-22', '2022-23'],
            'Branca': ['Branca A', 'Branca A', 'Branca A', 'Branca B', 'Branca B', 'Branca B'],
            'Taxa rendiment': [0.1, 0.5, 0.9, 0.9, 0.5, 0.1],  # Creixent vs Decreixent
            '% Abandonament a primer curs': [0.2, 0.21, 0.2, 0.5, 0.5, 0.5]  # Estable
        })
        self.output_json = "src/report/analisi_estadistic.json"

    def test_get_tendencia_logic(self):
        """Verifica la categorització de la regressió lineal."""
        years = ['1', '2', '3']
        creixent = [10, 20, 30]
        decreixent = [30, 20, 10]
        estable = [10, 10.001, 10]

        self.assertEqual(get_tendencia(years, creixent), "creciente")
        self.assertEqual(get_tendencia(years, decreixent), "decreciente")
        self.assertEqual(get_tendencia(years, estable), "estable")

    def test_analyze_dataset_full_flow(self):
        """Comprova que l'informe es genera i conté les claus correctes."""
        report = analyze_dataset(self.test_df)

        # Verificació de l'estructura del diccionari retornat.
        self.assertIn('metadata', report)
        self.assertIn('analisis_por_rama', report)
        self.assertIn('ranking_ramas', report)

        # Verificació dels rànquings.
        self.assertEqual(len(report['ranking_ramas']['mejor_rendimiento']), 1)

        # Verificació de la creació física del fitxer.
        self.assertTrue(os.path.exists(self.output_json))

    def test_json_content(self):
        """Verifica que el JSON desat sigui vàlid i llegible."""
        analyze_dataset(self.test_df)
        with open(self.output_json, 'r', encoding='utf-8') as f:
            data = json.load(f)

        self.assertEqual(data['metadata']['num_registros'], 6)
        self.assertEqual(len(data['analisis_por_rama']), 2)


if __name__ == '__main__':
    unittest.main()
