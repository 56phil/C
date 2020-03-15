#!/usr/bin/env python3
import sys
import argparse

'''
translate.py

This is a python program that can read a text file (fn_i) and write a text file
with named fs_o. It reads the very first data set, determines where the protein
sequence is in the count. Then in every subsequent data set the program will
only return data that is related to that count. This will remove data that does
that does not precisely align with Drosophila sequence positions  (wether they
are dash or letter). The output file will have the same number of data sets. The
sequence of the first data set is unchanged. In the remaining data sets, each
character of the sequence is unchanged if the corresponding character of the
first sequence is a letter. Otherwise it is replaced with a '+'.

Input file format:
    '>' + other species information + '[' + full species name + ']' +
    protiens sequence

Output file format:
    '>' + full species name + '\n' + protiens sequence + '\n\n'

Usage:
    $./translate.py <FILE NAME> [LENGTH OF SEQUENCE LINES]

Examples:
    $./translate.py some_file.txt 80
    $./translate.py some_file.txt

    The line length parameter is optional and defaults to 60.
'''


def get_fsn_and_sequence(str_i):
    """ Extracts elements from a data set
        input: string
        returns: list
    """
    delimiters = '[', ']'
    start, end = [i for i, c in enumerate(str_i) if c in delimiters]
    return ['>' + str_i[start+1:end], str_i[end+1:].replace('\n', '')]


def format_sequence(template, sequence):
    """ Places a '+' everywhere there is a False in the template list
        input: string
        returns: string
    """
    return ''.join([c if b else '+' for b, c in zip(template, sequence)])


def read_file(fn_i):
    """ Builds the raw data list by reading the text file named by fn_i
        input: None
        returns: list
    """
    with open(fn_i) as f:
        ds = f.readlines()
    raw_list = ''.join(ds).split('>')[1:]
    lc = len(raw_list)
    if lc < 2:
        print('Input data exception: Not enough data sets')
    return raw_list


def parse_raw_data(raw_list):
    """ Builds a list where each data set is a two element list.
        The first element contains the full species name.
        The second element is the protien sequence.
        input: list
        returns: list
    """
    return [get_fsn_and_sequence(raw_dataset) for raw_dataset in raw_list]


def format_parsed_data(data):
    """ Builds the template list
        Replaces each character in the sequence with '+' where the corresponding
        value in the template is False.
        Returns the controlling sequence to its original state.
        input: list
        returns: list
    """
    sequence = data[0][1]
    template = [True if c.isalpha() else False for c in sequence]
    for i, datum in enumerate(data):
        data[i][1] = format_sequence(template, datum[1])
    data[0][1] = sequence
    return data


def write_file(fn_i, data, step_size):
    """ Writes the results to a text file using a name based on fn_i
        input: string, list
        returns: None
    """
    pos = fn_i.rfind('.')
    fn_o = fn_i[:pos] + '.OUT' + fn_i[pos:]
    f = open(fn_o, "w")
    for fsn, sequence in data:
        f.write(fsn + '\n')
        for p in range(0, len(sequence), step_size):
            f.write(sequence[p:p+step_size] + '\n')
    f.close()


def print_usage():
    print('')


if __name__ == '__main__':
    # Instantiate the parser
    parser = argparse.ArgumentParser(description='translate.py')
    parser.add_argument('file_name', type=str,
                        help='Fully qulified name of input file.')
    parser.add_argument('step_size', default=60, type=int, nargs='?',
                        help='Number of characters in a sequence line.')
    args = parser.parse_args()

    write_file(args.file_name,
        format_parsed_data(parse_raw_data(read_file(args.file_name))),
        args.step_size)
