"""
Tests unitaris per a l'exercici 1: Càrrega de Datasets.
"""

import unittest
from unittest.mock import patch
import pandas as pd
from src.data_loader import load_dataset


class TestExercici1(unittest.TestCase):
    """Suite de tests per al mòdul de càrrega de dades."""

    def setUp(self):
        """S'executa abans de cada test."""
        test_name = self.id().split('.')[-1]
        print(f"\n> EXECUTANT PROVA: {test_name}")
        print("-" * 30)

    @patch('os.path.exists')
    @patch('pandas.read_excel')
    def test_load_dataset_direct_path(self, mock_read_excel, mock_exists):
        """Verifica la càrrega quan es passa una ruta directament."""
        # Configurem el comportament dels mocks.
        mock_exists.return_value = True
        mock_read_excel.return_value = pd.DataFrame({'col1': [1, 2]})

        # Executem.
        load_dataset("ruta/inventada.xlsx")

        # Verifiquem.
        mock_exists.assert_called_with("ruta/inventada.xlsx")
        mock_read_excel.assert_called_once()

    def test_load_dataset_file_not_found(self):
        """Verifica que s'aixeca FileNotFoundError si el fitxer no existeix."""
        with patch('os.path.exists', return_value=False):
            with self.assertRaises(FileNotFoundError):
                load_dataset("data/no_existeixo.xlsx")

    @patch('builtins.input', return_value='2')
    @patch('os.path.exists', return_value=True)
    @patch('pandas.read_excel')
    def test_load_dataset_menu_option_2(self, mock_read_excel, mock_exists, mock_input):
        """Verifica que l'opció 2 del menú selecciona el fitxer d'abandonament."""
        mock_read_excel.return_value = pd.DataFrame()

        load_dataset(None)

        # 1. Verifiquem que s'ha demanat input a l'usuari.
        mock_input.assert_called_once()
        # 2. Verifiquem que s'ha comprovat si existeix el fitxer correcte.
        mock_exists.assert_called_with("data/taxa_abandonament.xlsx")
        # 3. Verifiquem que s'ha intentat llegir el fitxer correcte.
        mock_read_excel.assert_called_with("data/taxa_abandonament.xlsx")

    @patch('builtins.input', return_value='99')
    @patch('os.path.exists', return_value=True)
    @patch('pandas.read_excel')
    def test_load_dataset_default_fallback(self, mock_read_excel, mock_exists, mock_input):
        """Verifica que una opció invàlida carrega el fitxer de rendiment per defecte."""
        mock_read_excel.return_value = pd.DataFrame()

        load_dataset(None)

        mock_input.assert_called_once()
        # Si l'opció no és vàlida, hauria d'anar al de rendiment per defecte.
        mock_exists.assert_called_with("data/rendiment_estudiants.xlsx")
        mock_read_excel.assert_called_with("data/rendiment_estudiants.xlsx")


if __name__ == '__main__':
    unittest.main()
