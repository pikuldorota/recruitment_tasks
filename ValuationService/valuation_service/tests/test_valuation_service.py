import logging
import os
import unittest
from ValuationService.valuation_service.valuation_service import *
import pandas as pd
import numpy as np


class ArgumentsTestCase(unittest.TestCase):
    def test_check_if_existing_path(self):
        existing_paths = ['tests_files/currencies_empty_cells.csv', 'tests_files/data_empty_cells.csv',
                          'tests_files/empty_output.csv', 'tests_files/nonempty_output.csv',
                          'tests_files/valid_currencies.csv',
                          'tests_files/valid_data.csv', 'tests_files/valid_matching.csv']
        for path in existing_paths:
            assert check_if_existing_path(path) == path

        nonexistent_paths = ['./sample.csv', './subdirectory/different.csv']
        for path in nonexistent_paths:
            with self.assertRaises(argparse.ArgumentTypeError) as context:
                check_if_existing_path(path)
            self.assertTrue('File "{}" does not exist'.format(path) in str(context.exception))
        pass

    def test_check_if_valid_data_file(self):
        valid_data_paths = ['tests_files/data_empty_cells.csv', 'tests_files/valid_data.csv']
        for path in valid_data_paths:
            assert check_if_valid_data_file(path) == path
        invalid_data_paths = ['tests_files/empty_output.csv', 'tests_files/valid_matching.csv',
                              'tests_files/valid_currencies.csv']
        for path in invalid_data_paths:
            with self.assertRaises(argparse.ArgumentTypeError) as context:
                check_if_valid_data_file(path)
            self.assertTrue('File "{}" is not of valid data format'.format(path) in str(context.exception))

    def test_check_if_valid_currencies_file(self):
        valid_currencies_paths = ['tests_files/currencies_empty_cells.csv', 'tests_files/valid_currencies.csv']
        for path in valid_currencies_paths:
            assert check_if_valid_currencies_file(path) == path
        invalid_currencies_paths = ['tests_files/empty_output.csv', 'tests_files/valid_matching.csv',
                                    'tests_files/valid_data.csv']
        for path in invalid_currencies_paths:
            with self.assertRaises(argparse.ArgumentTypeError) as context:
                check_if_valid_currencies_file(path)
            self.assertTrue('File "{}" is not of valid currency format'.format(path) in str(context.exception))

    def test_check_if_valid_matching_file(self):
        valid_matching_paths = ['tests_files/valid_matching.csv']
        for path in valid_matching_paths:
            assert check_if_valid_matching_file(path) == path
        invalid_matching_paths = ['tests_files/empty_output.csv', 'tests_files/currencies_empty_cells.csv',
                                  'tests_files/valid_currencies.csv']
        for path in invalid_matching_paths:
            with self.assertRaises(argparse.ArgumentTypeError) as context:
                check_if_valid_matching_file(path)
            self.assertTrue('File "{}" is not of valid matching format'.format(path) in str(context.exception))


class SavingFileTestCase(unittest.TestCase):

    _paths = ['tests_files/empty_output.csv', 'tests_files/nonexistent_output.csv']

    def tearDown(self):
        for path in self._paths:
            os.remove(path)
        open(self._paths[0], 'w').close()

    def test_saving_file(self):
        output_data = pd.DataFrame([(1, 2000, 201, 'GBP', 2), (3, 200, 21, 'EUR', 0), (5, 30, 21, 'GBP', 1)],
                                   columns=['matching_id', 'total_price', 'avg_price', 'currency',
                                            'ignored_products_count'])

        for path in self._paths:
            save_results(output_data, path)
            saved_data = pd.read_csv(path)
            assert output_data.equals(saved_data)

        path = "tests_files/nonempty_output.csv"
        with self.assertRaises(FileExistsError) as context:
            save_results(output_data, path)
        self.assertTrue('File "{}" already contains data. Choose different output file.'.format(path)
                        in str(context.exception))


class ChangingCSVTestCase(unittest.TestCase):
    @staticmethod
    def test_add_total_price():
        input_data = pd.read_csv('tests_files/valid_data.csv')
        add_total_price(input_data)
        assert 'total_price' in input_data
        data_with_total_price = pd.read_csv('tests_files/data_with_total_price.csv')
        assert input_data.equals(data_with_total_price)

    def test_add_total_price_empty_cells(self):
        input_data = pd.read_csv('tests_files/data_empty_cells.csv')
        add_total_price(input_data)
        assert 'total_price' in input_data
        data_with_total_price = pd.read_csv('tests_files/data_with_total_price_empty_cells.csv')
        assert input_data.equals(data_with_total_price)
        with self.assertLogs() as cm:
            logging.getLogger().error('Empty cells found in data file. The record will be omitted.')
        self.assertIn('Empty cells found in data file. The record will be omitted.', '\n'.join(cm.output))

    @staticmethod
    def test_convert_currency_to_PLN():
        input_data = pd.read_csv('tests_files/valid_data.csv')
        currency = pd.read_csv('tests_files/valid_currencies.csv')
        convert_currency_to_pln(input_data, currency)
        converted_data = pd.read_csv('tests_files/valid_data_converted.csv')
        assert input_data.equals(converted_data)

    def test_convert_currency_to_PLN_no_currency(self):
        input_data = pd.read_csv('tests_files/valid_data.csv')
        currency = pd.read_csv('tests_files/currencies_empty_cells.csv')
        convert_currency_to_pln(input_data, currency)
        with self.assertLogs() as cm:
            logging.getLogger().error('Ratio for currency was not found. This matching will be omitted.')
        self.assertIn('Ratio for currency was not found. This matching will be omitted.', '\n'.join(cm.output))

    def test_convert_currency_to_PLN_empty_cells(self):
        input_data = pd.read_csv('tests_files/data_empty_cells.csv')
        currency = pd.read_csv('tests_files/valid_currencies.csv')
        convert_currency_to_pln(input_data, currency)
        converted_data = pd.read_csv('tests_files/invalid_data_converted.csv')
        assert input_data.equals(converted_data)
        with self.assertLogs() as cm:
            logging.getLogger().error('Not all data has required info. Incomplete rows will be omitted.')
        self.assertIn('Not all data has required info. Incomplete rows will be omitted.', '\n'.join(cm.output))

    @staticmethod
    def test_check_if_all_same_currency():
        different_currency = pd.DataFrame([(1, 2000, 'GBP', 2, 1), (3, 200, 'EUR', 0, 3), (5, 30, 'GBP', 1, 2)],
                                          columns=['id', 'price', 'currency', 'quantity', 'matching_id'])
        assert check_if_all_same_currency(different_currency) is False

        same_currency = pd.DataFrame([(1, 2000, 'GBP', 2, 1), (3, 200, 'GBP', 0, 3), (5, 30, 'GBP', 1, 2)],
                                     columns=['id', 'price', 'currency', 'quantity', 'matching_id'])
        assert check_if_all_same_currency(same_currency) is True

        blank_currency = pd.DataFrame([(1, 2000, 'GBP', 2, 1), (3, 200, '', 0, 3), (5, 30, 'GBP', 1, 2)],
                                      columns=['id', 'price', 'currency', 'quantity', 'matching_id'])
        assert check_if_all_same_currency(blank_currency) is False

    def test_get_required_data(self):
        valid_data = pd.DataFrame(
            [(1, 2000, 'GBP', 2, 1), (3, 200, 'PLN', 1, 2), (5, 30, 'GBP', 2, 1),
             (3, 300, 'PLN', 5, 2), (5, 500, 'GBP', 2, 1)],
            columns=['id', 'price', 'currency', 'quantity', 'matching_id'])
        matching_frame = pd.DataFrame([(1, 1), (2, 2)], columns=['matching_id', 'top_priced_count'])
        currency = pd.read_csv("tests_files/valid_currencies.csv")
        input_data = get_required_data(valid_data, matching_frame, currency)
        expected_data = pd.DataFrame([(1, 4000, 843.33, 'GBP', 2), (2, 1700, 250.00, 'PLN', 0)],
                                     columns=['matching_id', 'total_price', 'avg_price', 'currency',
                                              'ignored_products_count'])
        assert input_data.equals(expected_data)

        matching_frame = pd.DataFrame([(1, 30), (2, 2)], columns=['matching_id', 'top_priced_count'])
        input_data = get_required_data(valid_data, matching_frame, currency)
        expected_data = pd.DataFrame([(1, 5060, 843.33, 'GBP', 0), (2, 1700, 250, 'PLN', 0)],
                                     columns=['matching_id', 'total_price', 'avg_price', 'currency',
                                              'ignored_products_count'])
        assert input_data.equals(expected_data)

        with self.assertLogs() as cm:
            logging.getLogger().error('Too many elements required. Counting all elements with matching_id.')
        self.assertIn('Too many elements required. Counting all elements with matching_id.', '\n'.join(cm.output))

        matching_frame = pd.DataFrame([(np.nan, 30), (2, np.nan)], columns=['matching_id', 'top_priced_count'])
        print(matching_frame)
        input_data = get_required_data(valid_data, matching_frame, currency)
        expected_data = pd.DataFrame([], columns=['matching_id', 'total_price', 'avg_price', 'currency',
                                                  'ignored_products_count'])
        assert input_data.equals(expected_data)

        with self.assertLogs() as cm:
            logging.getLogger().error('Matching misses data. Omitting this matching.')
        self.assertIn('Matching misses data. Omitting this matching.', '\n'.join(cm.output))


if __name__ == '__main__':
    unittest.main()
