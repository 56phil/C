#!/usr/bin/env python3

'''
translate.py

This is a python program that can read a text file and write a text file with a different name. It reads the very first data set (drosophila melanogster) determine where the protein sequence is in the count. Then in every subsequent data set the program will only return data that is related to that count. This will remove data that does that does not precisely align with Drosophila sequence positions  (wether they are dash or letter). When rewriting each data set it should start with > then Species name an enter and then the protein sequence string.

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

# output file name
fn_o = '/home/p/Chris/2019-03-18 All but VP sequences.OUT.txt'

delimiters = "[", "]"   # surrounds Full species name (fsn)
template = [] #from first ds


def get_name_and_sequence(str_i):
    """ Extracts elements from a data set
        input: string
        returns: list (empty on any error)
    """
    try:
        start, end = [i for i, c in enumerate(str_i) if c in delimiters]
        return ['>' + str_i[start+1:end], str_i[end+1:]]
    except:
        pass
    return []


def format_sequence(str_i):
    """ Places a '+' everywhere there is a False in the template list
        input: string
        returns: string
    """
    lst_u = []
    for i, b in enumerate(template):
        if b:
            lst_u.append(str_i[i])
        else:
            lst_u.append('+')
    return ''.join(lst_u)


def scan_first_ds(str_i):
    """ Builds the template list where each letter in the input is represented
        with a True. All other values result in a False.
        input: string
        returns: list
    """
    global template
    template = [False for _ in range(len(str_i))]
    for i in range(len(str_i)):
        if str_i[i].isalpha():
            template[i] = True
    return


def read_file():
    """ Builds the raw data list by reading the text file named by fn_i
        input: None
        returns: list
    """
    with open(fn_i) as f:
        ds = f.readlines()
    return ''.join(ds).split('>')


def parse_raw_data(raw_data):
    """ Builds a list where each data set is a two element list.
        The first element contains the full species name.
        The second element is the protien sequence.
        input: list
        returns: list
    """
    data = []
    for raw_dataset in raw_data:
        result = get_name_and_sequence(raw_dataset)
        try:
            t0, t1 = result
            if t0 and t1:
                data.append(result)
        except:
            pass
    return data


def format_parsed_data(data):
    """ Builds the template list
        Replaces each character in the sequence with '+' where the corresponding
        value in the template is False.
        Returns the controlling sequence to its original state.
        input: list
        returns: list
    """
    # print(data)
    scan_first_ds(data[0][1])
    for i in range(len(data)):
        data[i][1] = format_sequence(data[i][1])
    data[0][1] = data[0][1].replace('+', '-')
    return data


def write_file(data):
    """ Writes the results to a text file named by fn_o
        input: list
        returns: None
    """
    f = open(fn_o, "w")
    for datum in data:
        str_n, str_d = datum
        f.write(str_n + '\n')
        f.write(str_d + '\n\n')
    f.close()


if __name__ == '__main__':
    write_file(format_parsed_data(parse_raw_data(read_file())))
