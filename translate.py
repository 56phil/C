#!/usr/bin/env python3

fn_i = '/home/p/Chris/2019-03-18 All but VP sequences.txt'
fn_o = '/home/p/Chris/2019-03-18 All but VP sequences.OUT.txt'
delimiters = "[", "]"
template = []


def get_name_and_sequence(str_i):
    try:
        start, end = [i for i, c in enumerate(str_i) if c in delimiters]
        return ['>' + str_i[start+1:end], str_i[end+1:]]
    except:
        pass
    return []


def format_sequence(n, str_i):
    lst_u = []
    for i, b in enumerate(template):
        if b:
            lst_u.append(str_i[i])
        else:
            lst_u.append('+')
    return ''.join(lst_u)


def scan_first_ds(str_i):
    global template
    template = [False for _ in range(len(str_i))]
    for i in range(len(str_i)):
        if str_i[i].isalpha():
            template[i] = True
    return


def read_file():
    with open(fn_i) as f:
        ds = f.readlines()
    return ''.join(ds).split('>')


def parse_raw_data(raw_data):
    data = []
    for datum in raw_data:
        lst = get_name_and_sequence(datum)
        try:
            t0, t1 = lst
            if t0 and t1:
                data.append(lst)
        except:
            pass
    return data


def format_parsed_data(data):
    scan_first_ds(data[0][1])
    for i in range(len(data)):
        data[i][1] = format_sequence(i, data[i][1])
    data[0][1] = data[0][1].replace('+', '-')
    return data


def write_file(data):
    f = open(fn_o, "w")
    for datum in data:
        str_n, str_d = datum
        f.write(str_n + '\n')
        f.write(str_d + '\n\n')
    f.close()


if __name__ == '__main__':
    write_file(format_parsed_data(parse_raw_data(read_file())))
