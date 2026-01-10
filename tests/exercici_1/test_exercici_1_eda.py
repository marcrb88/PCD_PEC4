"""
Tests unitaris per a l'Exploració de Dades (EDA) de l'Exercici 1.
"""

import unittest
from unittest.mock import patch
import io
import pandas as pd
from src.dataset_exploration import perform_dataset_exploration


class TestEDA(unittest.TestCase):
    """Suite de tests per a la funció d'exploració de dades."""

    def setUp(self):
        """S'executa abans de cada test."""
        # Creem un DataFrame de prova.
        self.sample_df = pd.DataFrame({
            'ColumnaA': [1, 2, 3],
            'ColumnaB': ['A', 'B', 'C']
        })

    def test_perform_exploration_output(self):
        """Verifica que la funció imprimeix les seccions d'exploració requerides."""
        # Utilitzem io.StringIO per capturar el que es printa a la consola.
        with patch('sys.stdout', new=io.StringIO()) as fake_out:
            perform_dataset_exploration(self.sample_df)
            output = fake_out.getvalue()

        # Comprovem que apareixen els títols definits a la funció.
        self.assertIn("--- 1.1. Cinc primeres files ---", output)
        self.assertIn("--- 1.2. Columnes del dataset ---", output)
        self.assertIn("--- 1.3. Informació general (info) ---", output)

        # Verifiquem que apareixen els noms de les columnes.
        self.assertIn("ColumnaA", output)
        self.assertIn("ColumnaB", output)

    def test_perform_exploration_empty_df(self):
        """Verifica que la funció no peta amb un DataFrame buit."""
        empty_df = pd.DataFrame()

        with patch('sys.stdout', new=io.StringIO()):
            perform_dataset_exploration(empty_df)


if __name__ == '__main__':
    unittest.main()
