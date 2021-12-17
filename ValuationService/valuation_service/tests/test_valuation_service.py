import logging
import unittest
from ValuationService.valuation_service.valuation_service import *
import pandas as pd


class ArgumentsTestCase(unittest.TestCase):
    def test_check_if_existing_path(self):
        existing_paths = ['tests_files/currencies_empty_cells.csv', 'tests_files/data_empty_cells.csv',
                          'tests_files/empty_output.csv', 'tests_files/nonempty_output.csv',
                          'tests_files/valid_currencies.csv',
                          'tests_files/valid_data.csv', 'tests_files/valid_matchings.csv']
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
        invalid_data_paths = ['tests_files/empty_output.csv', 'tests_files/valid_matchings.csv',
                              'tests_files/valid_currencies.csv']
        for path in invalid_data_paths:
            with self.assertRaises(argparse.ArgumentTypeError) as context:
                check_if_valid_data_file(path)
            self.assertTrue('File "{}" is not of valid data format'.format(path) in  str(context.exception))

    def test_check_if_valid_currencies_file(self):
        valid_currencies_paths = ['tests_files/currencies_empty_cells.csv', 'tests_files/valid_currencies.csv']
        for path in valid_currencies_paths:
            assert check_if_valid_currencies_file(path) == path
        invalid_currencies_paths = ['tests_files/empty_output.csv', 'tests_files/valid_matchings.csv',
                                    'tests_files/valid_data.csv']
        for path in invalid_currencies_paths:
            with self.assertRaises(argparse.ArgumentTypeError) as context:
                check_if_valid_currencies_file(path)
            self.assertTrue('File "{}" is not of valid currency format'.format(path) in str(context.exception))

    def test_check_if_valid_matching_file(self):
        valid_matching_paths = ['tests_files/valid_matchings.csv']
        for path in valid_matching_paths:
            assert check_if_valid_matching_file(path) == path
        invalid_matching_paths = ['tests_files/empty_output.csv', 'tests_files/currencies_empty_cells.csv',
                                  'tests_files/valid_currencies.csv']
        for path in invalid_matching_paths:
            with self.assertRaises(argparse.ArgumentTypeError) as context:
                check_if_valid_matching_file(path)
            self.assertTrue('File "{}" is not of valid matching format'.format(path) in  str(context.exception))


class SavingFileTestCase(unittest.TestCase):
    @staticmethod
    def test_saving_file():
        output_data = pd.DataFrame([(1, 2000, 201, 'GBP', 2), (3, 200, 21, 'EUR', 0), (5, 30, 21, 'GBP', 1)],
                                   columns=['matching_id', 'total_price', 'avg_price', 'currency',
                                            'ignored_products_count'])

        paths = ['tests_files/empty_output.csv', 'tests_files/nonexistent_output.csv']
        for path in paths:
            save_results(output_data, path)
            saved_data = pd.read_csv(path)
            assert output_data.equals(saved_data)


class ChangingCSVTestCase(unittest.TestCase):
    @staticmethod
    def test_add_total_price():
        data = pd.read_csv('tests_files/valid_data.csv')
        add_total_price(data)
        assert 'total_price' in data
        data_with_total_price = pd.read_csv('tests_files/data_with_total_price.csv')
        assert data.equals(data_with_total_price)

    def test_add_total_price_empty_cells(self):
        data = pd.read_csv('tests_files/data_empty_cells.csv')
        add_total_price(data)
        assert 'total_price' in data
        data_with_total_price = pd.read_csv('tests_files/data_with_total_price_empty_cells.csv')
        assert data.equals(data_with_total_price)
        with self.assertLogs('val') as cm:
            logging.getLogger('val').error('Empty cells found in data file. The record will be omitted.')
        self.assertEqual(cm.output, ['ERROR:val:Empty cells found in data file. The record will be omitted.'])

    @staticmethod
    def test_convert_currency_to_PLN():
        data = pd.read_csv('tests_files/valid_data.csv')
        currency = pd.read_csv('tests_files/valid_currencies.csv')
        convert_currency_to_PLN(data, currency)
        converted_data = pd.read_csv('tests_files/valid_data_converted.csv')
        assert data.equals(converted_data)

    def test_convert_currency_to_PLN_no_currency(self):
        data = pd.read_csv('tests_files/valid_data.csv')
        currency = pd.read_csv('tests_files/currencies_empty_cells.csv')
        convert_currency_to_PLN(data, currency)
        with self.assertLogs('root') as cm:
            logging.getLogger('root').error('Ratio for currency was not found. This matching will be omitted.')
        self.assertEqual(cm.output, ['ERROR:root:Ratio for currency was not found. This matching will be omitted.'])

    def test_convert_currency_to_PLN_empty_cells(self):
        data = pd.read_csv('tests_files/data_empty_cells.csv')
        currency = pd.read_csv('tests_files/valid_currencies.csv')
        convert_currency_to_PLN(data, currency)
        converted_data = pd.read_csv('tests_files/invalid_data_converted.csv')
        assert data.equals(converted_data)
        with self.assertLogs('root') as cm:
            logging.getLogger('root').error('Not all data has required info. Incomplete rows will be omitted.')
        self.assertEqual(cm.output, ['ERROR:root:Not all data has required info. Incomplete rows will be omitted.'])

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
            [(1, 2000, 'GBP', 2, 1, 4000), (3, 200, 'PLN', 1, 2, 200), (5, 30, 'GBP', 2, 2, 60),
             (3, 300, 'PLN', 1, 5, 1500), (5, 500, 'GBP', 2, 2, 1000)],
            columns=['id', 'price', 'currency', 'quantity', 'matching_id', 'total_price'])
        matching = pd.DataFrame([(1, 2), (2, 1)], columns=['matching_id', 'top_priced_count'])
        data = get_required_data(valid_data, matching)
        expected_data = pd.DataFrame([(1, 1700, 850, 'PLN', 0), (2, 4000, 1686.67, 'GBP', 2)],
                                     columns=['matching_id', 'total_price', 'avg_price', 'currency',
                                              'ignored_products_count'])
        assert data.equals(expected_data)

        matching = pd.DataFrame([(1, 30), (2, 2)], columns=['matching_id', 'top_priced_count'])
        data = get_required_data(valid_data, matching)
        expected_data = pd.DataFrame([(1, 1500, 850, 'PLN', 1), (2, 5000, 1686.67, 'GBP', 1)],
                                     columns=['matching_id', 'total_price', 'avg_price', 'currency',
                                              'ignored_products_count'])
        assert data.equals(expected_data)

        with self.assertLogs('val') as cm:
            logging.getLogger('val').error('Too many elements required. Counting all elements with matching_id.')
        self.assertEqual(cm.output, ['ERROR:val:Too many elements required. Counting all elements with matching_id.'])

        matching = pd.DataFrame([('', 30), (2, '')], columns=['matching_id', 'top_priced_count'])
        data = get_required_data(valid_data, matching)
        expected_data = pd.DataFrame([], columns=['matching_id', 'total_price', 'avg_price', 'currency',
                                                  'ignored_products_count'])
        assert data.equals(expected_data)

        with self.assertLogs('val') as cm:
            logging.getLogger('val').error('Matching misses data. Omitting this matching.')
        self.assertEqual(cm.output, ['ERROR:val:Matching misses data. Omitting this matching.'])


if __name__ == '__main__':
    unittest.main()
