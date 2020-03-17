#!/usr/bin/env python3
import argparse
import os.path

'''
translate.py

This is a python program that reads a text file and writes a
text file with a name derived from the name of the input file (e.g. d.txt ->
d.OUT.txt). It reads the first data set, determines where the protein sequence
is in the count. Then, in every subsequent data set, the program will only
return data that is related to that count. This will replace data that does
that does not precisely align with sequence positions from the first data set
(whether they are a dash or a letter). The output file will have the same
number of data sets  as the input file. The protiens sequence of the first
data set is unchanged. In the remaining data sets, each character of the
sequence is unchanged if the corresponding character of the first sequence is
a letter. Otherwise, it is replaced with the specified replacement character.
If none is specified, the default '+' will be used.

Input file format:
    '>' + other species information + '[' + full species name + ']' +
    protiens sequence

Output file format:
    '>' + full species name + '\n' + protiens sequence + '\n'

Usage:
    $./translate.py <FILE NAME> [MAXIMUM LENGTH OF SEQUENCE LINES]
    [REPLACEMENT CHARACTER]

Examples:
    $./translate.py some_file.txt 42 .
    $./translate.py some_file.txt 123 \?
    $./translate.py some_file.txt

    The line length parameter is optional and defaults to 60.
    The default replacement character is '+'.
'''


def get_fsn_and_sequence(str_i):
    """ Extracts elements from a data set
        input: string
        returns: list
    """
    delimiters = '[', ']'
    start, end = [i for i, c in enumerate(str_i) if c in delimiters]
    return ['>' + str_i[start+1:end], str_i[end+1:].replace('\n', '')]


def format_sequence(template, sequence, repl_char):
    """ Places the replacement character everywhere there is a False in the
        template list
        input: list list string
        returns: string
    """
    return ''.join([c if b else repl_char for b, c in zip(template, sequence)])


def read_file(file_name):
    """ Builds the raw data list by reading the text file named by file_name
        input: string
        returns: list
    """
    with open(file_name) as f:
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


def format_parsed_data(data, repl_char):
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
        data[i][1] = format_sequence(template, datum[1], repl_char)
    data[0][1] = sequence
    return data


def write_file(file_name, data, line_length):
    """ Writes the results to a text file using a name based on file_name
        input: string, list
        returns: None
    """
    pos = file_name.rfind('.')
    fn_o = file_name[:pos] + '.OUT' + file_name[pos:]
    f = open(fn_o, "w")
    for fsn, sequence in data:
        f.write(fsn + '\n')
        for p in range(0, len(sequence), line_length):
            f.write(sequence[p:p+line_length] + '\n')
    f.close()


def check_fname(fname):
    cnt = 0
    while not os.path.isfile(fname):
        if cnt > 0 or not fname == '':
            print('Can\'t locate "{}"'.format(fname))
        fname = input("Please enter the input file name: ")
    cnt += 1
    return fname


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='translate.py')
    parser.add_argument('file_name', type=str, nargs='?', default='',
                        help='Name of input file.')
    parser.add_argument('line_length', type=int, nargs='?', default=60,
                        help='Number of characters in a sequence line.')
    parser.add_argument('replacement_character', type=str,
                        nargs='?', default='+',
                        help='Character used to mark openings.')
    args = parser.parse_args()

    repl_char = args.replacement_character[0]

    fname = check_fname(args.file_name )

    write_file(args.file_name,
        format_parsed_data(parse_raw_data(read_file(fname)),
        repl_char), args.line_length)
