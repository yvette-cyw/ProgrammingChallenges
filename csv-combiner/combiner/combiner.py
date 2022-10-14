import argparse
import csv
import os
import sys


def path_verify(file, _type):
    """
    File path verification method
    :param file: the file path
    :param _type: "input" file for combination or "output" file for combined result
    :return:
    """
    if _type == 'input':
        if not os.path.isfile(file):
            print("error: {} does not exist".format(file))
            sys.exit(1)
    elif _type == 'output':
        if os.path.isfile(file):
            print("{} exists.".format(file))
            sys.exit(1)


def arg(argv=None):
    """
    Check and retrieve command-line arguments
    :return: A list contains file paths and an output file path.
    """
    parser = argparse.ArgumentParser(description='Input the csv file paths to be combined and the combined csv path.',
                                     usage='csv-combiner')
    parser.add_argument('-i', '--input', nargs='+', help='Type in the csv files paths to be combined', required=True)
    parser.add_argument('-o', '--output', nargs=1, help='Type in a combined csv file path', required=True)
    args = parser.parse_args(argv)
    file_list = args.input
    output_file = args.output[0]

    # Verify source file paths
    for f_in in file_list:
        path_verify(f_in, 'input')

    # Verify destination file path
    path_verify(output_file, 'output')

    return file_list, output_file


def header(file_list):
    """
    Get all column names/headers by checking all files' headers/column names and adding one header named "filename".
    :param file_list: List of file paths.
    :return: List of all headers (no duplicate).
    """
    col_names = []
    for file_name in file_list:
        with open(file_name, "r", newline="") as f_in:
            reader = csv.reader(f_in)
            headers = next(reader)
            for h in headers:
                if h not in col_names:
                    col_names.append(h)
    col_names.append('filename')
    return col_names


def combine(file_list, output_file):
    """
    A method could combine multiple csv files into one csv file and print its contents to stdout.
    :param file_list: List of file paths waiting for combination.
    :param output_file: The output csv file path.
    :return: The number of rows of combined file.
    """
    col_names = header(file_list)
    cnt = 0
    with open(output_file, "w", newline="") as f_out:
        writer = csv.DictWriter(f_out, fieldnames=col_names)
        writer.writeheader()
        for filename in file_list:
            with open(filename, "r", newline="") as f_in:
                reader = csv.DictReader(f_in)
                for line in reader:
                    line.update({'filename': filename.split('/')[-1]})
                    writer.writerow(line)
                    cnt += 1
    return cnt


def main(argv=None):
    """
    Combiner of csv files.
    :return: a combination csv file and its contents in stdout.
    """
    file_list, output_file = arg(argv)
    row_num = combine(file_list, output_file)
    with open(output_file, "r") as csv_file:
        datareader = csv.reader(csv_file)
        for i in range(row_num):
            print(datareader.__next__())


if __name__ == '__main__':
    main()
