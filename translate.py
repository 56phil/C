#!/usr/bin/env python3

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

# globals

# input file name
fn_i = '/home/p/Chris/2019-03-18 All but VP sequences.txt'

delimiters = "[", "]"   # surrounds Full species name (fsn)
template = [] #from first ds


def get_fsn_and_sequence(str_i):
    """ Extracts elements from a data set
        input: string
        returns: list
    """
    start, end = [i for i, c in enumerate(str_i) if c in delimiters]
    return ['>' + str_i[start+1:end], str_i[end+1:]]


def format_sequence(sequence):
    """ Places a '+' everywhere there is a False in the template list
        input: string
        returns: string
    """
    lst_u = []
    for i, b in enumerate(template):
        if b:
            lst_u.append(sequence[i])
        else:
            lst_u.append('+')
    return ''.join(lst_u)


def scan_first_dataset(sequence):
    """ Builds the template list where each letter in the input is represented
        with a True. All other values result in a False.
        input: string
        returns: None
    """
    global template
    template = [False for _ in range(len(sequence))]
    for i in range(len(sequence)):
        if sequence[i].isalpha():
            template[i] = True
    return


def read_file():
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
    scan_first_dataset(data[0][1])
    for i in range(len(data)):
        data[i][1] = format_sequence(data[i][1])
    data[0][1] = data[0][1].replace('+', '-')
    return data


def write_file(data):
    """ Writes the results to a text file named by fn_o
        input: list
        returns: None
    """
    fn_o = fn_i.replace('.', '.OUT.')
    f = open(fn_o, "w")
    for datum in data:
        str_n, str_d = datum
        f.write(str_n + '\n')
        f.write(str_d + '\n\n')
    f.close()


if __name__ == '__main__':
    write_file(format_parsed_data(parse_raw_data(read_file())))
