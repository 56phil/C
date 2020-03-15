A project to help a friend get a step closer to graduation.

This python program reads a text file and writes a text file. It reads the very first data set, determines where the protein sequence is in the count. Then in every subsequent data set the program will only return data that is related to that count. This will remove data that does that does not precisely align with Drosophila sequence positions  (wether they are dash or letter). The output file will have the same number of data sets. The sequence of the first data set is unchanged. In the remaining data sets, each character of the sequence is unchanged if the corresponding character of the first sequence is a letter. Otherwise it is replaced with a '+'.

Input file format:
    '>' + other species information + '\[' + full species name + ']' +
    protiens sequence

Output file format:
    '>' + full species name + '\n' + protiens sequence + '\n'

Usage:

    $./translate.py <FILE NAME> [LENGTH OF SEQUENCE LINES]

Examples:

    $./translate.py some_file.txt 80
    
    $./translate.py some_file.txt

    $./translate.py some_file.txt 0

The line length parameter is optional and defaults to 60. If no line ends within a sequence is needed, enter 0.
