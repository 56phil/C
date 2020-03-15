#!/usr/bin/env python3
import sys

'''
translate.py

This is a python program that can read a text file (fn_i) and write a text file with named fs_o. It reads the very first data set, determines where the protein sequence is in the count. Then in every subsequent data set the program will only return data that is related to that count. This will remove data that does that does not precisely align with Drosophila sequence positions  (wether they are dash or letter). When rewriting each data set it should start with > then Species name an enter and then the protein sequence string.

File discription:

    1.  Each data set starts with '>'

    2.  The first line describes the species name and designation

    3.  The full species name can be found between '[ ]'

    4.  '-' represent an opening for alignment

    5.  The letters represent the proteins sequence
'''


def get_fsn_and_sequence(str_i):
    """ Extracts elements from a data set
        input: string
        returns: list
    """
    delimiters = '[', ']'
    start, end = [i for i, c in enumerate(str_i) if c in delimiters]
    return ['>' + str_i[start+1:end], str_i[end+1:]]


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
    raw_list = ''.join(ds).split('>')
    return raw_list[1:]


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
    template = [True if c.isalpha() else False for c in data[0][1]]
    for i in range(len(data)):
        data[i][1] = format_sequence(template, data[i][1])
    data[0][1] = data[0][1].replace('+', '-')
    return data


def write_file(fn_i, data):
    """ Writes the results to a text file using a name based on fn_i
        input: string, list
        returns: None
    """
    pos = fn_i.rfind('.')
    fn_o = fn_i[:pos] + '.OUT' + fn_i[pos:]
    f = open(fn_o, "w")
    for datum in data:
        str_n, str_d = datum
        f.write(str_n + '\n')
        f.write(str_d + '\n\n')
    f.close()


if __name__ == '__main__':
    fn_i = sys.argv[1]
    write_file(fn_i, format_parsed_data(parse_raw_data(read_file(fn_i))))
