import csv
import os
import unittest
from unittest import mock
from io import StringIO
import sys
import combiner

path = './test_data/'
test_files = {
    'test1.csv': [['Blouses', 'Satchels'], [1, 1]],
    'test2.csv': [['Watches', 'Wallets', 'Purses', 'Satchels'], [2] * 4, [3] * 4],
    'test3.csv': [['Purses'], [4], [5], [6]]
}
file_list = [path + file for file in test_files.keys()]
output_file = path + 'test.csv'
expected_header = ['Blouses', 'Satchels', 'Watches', 'Wallets', 'Purses', 'filename']
output_rows = [expected_header,
               ['1', '1', '', '', '', 'test1.csv'],
               ['', '2', '2', '2', '2', 'test2.csv'],
               ['', '3', '3', '3', '3', 'test2.csv'],
               ['', '', '', '', '4', 'test3.csv'],
               ['', '', '', '', '5', 'test3.csv'],
               ['', '', '', '', '6', 'test3.csv']]


class MyTestCase(unittest.TestCase):

    def setUp(self):
        for file, rows in test_files.items():
            with open(path + file, 'w', newline='') as csv_file:
                writer = csv.writer(csv_file, dialect='excel')
                writer.writerows(rows)


    def tearDown(self):
        for file in test_files.keys():
            os.remove(path + file)



    @mock.patch('os.path.isfile')
    @mock.patch('sys.exit')
    def test_path_verify(self, mock_isfile, mock_exit):
        mock_isfile.return_value = False
        combiner.path_verify(mock_isfile, _type='input')
        assert mock_exit.called

        mock_isfile.return_value = True
        combiner.path_verify(mock_isfile, _type='input')
        assert mock_exit.not_called

        mock_isfile.return_value = False
        combiner.path_verify(mock_isfile, _type='output')
        assert mock_exit.not_called

        mock_isfile.return_value = True
        combiner.path_verify(mock_isfile, _type='output')
        assert mock_exit.called

    def test_arg(self):
        file_in, file_out = combiner.arg(['--input', path + 'test1.csv', path + 'test2.csv', path + 'test3.csv', '--output', output_file])
        self.assertListEqual(file_in, file_list)
        self.assertEqual(file_out, output_file)

    def test_header(self):
        self.assertListEqual(combiner.header(file_list), expected_header)

    def test_combine(self):
        self.assertEqual(combiner.combine(file_list, output_file), 6)
        os.remove(output_file)


    def test_main(self):
        expected_output = '\n'.join([str(row) for row in output_rows])
        with mock.patch('sys.stdout', new=StringIO()) as fake_out:
            combiner.main(['--input', path + 'test1.csv', path + 'test2.csv', path + 'test3.csv', '--output', output_file])
            for i in range(6):
                self.assertEqual(fake_out.getvalue().split('\n')[i], str(output_rows[i]))
        os.remove(output_file)


if __name__ == '__main__':
    unittest.main()
