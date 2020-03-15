# A project to help a friend get a step closer to graduation.
## Overview:
This is a python program that reads a text file and writes a text file with a name derived from the name of the input file (e.g. d.txt -> d.OUT.txt). It reads the first data set, determines where the protein sequence is in the count. Then, in every subsequent data set,  the program will only return data that is related to that count. This will replace data that does that does not precisely align with sequence positions from the first data set (whether they are a dash or a letter). The output file will have the same number of data sets  as the input file. The protiens sequence of the first data set is unchanged. In the remaining data sets, each character of the sequence is unchanged if the corresponding character of the first sequence is a letter. Otherwise, it is replaced with the specified replacement character. If none is specified, the default '+' will be used.

## Input file format:
    '>' + other species information + '[' + full species name + ']' + protiens sequence

## Output file format:
    '>' + full species name + '\n' + protiens sequence + '\n'

## Usage:
    $./translate.py <FILE NAME> [LENGTH OF SEQUENCE LINES] [REPLACEMENT CHARACTER]

## Examples:
<ol>
<li>$./translate.py some_file.txt 42 .</li>
<ul>
<li>The protiens sequence will be will be 42 characters long</li>
<li>The replacement character will be a period.</li>
</ul>
<li>$./translate.py some_file.txt 123 \?</li>
<ul>
<li>The protiens sequence will be will be 123 characters long</li>
<li>The replacement character will be a question mark. (The backslash is needed to 'escape' some characters that have special meanings in regular expresions.)</li>
</ul>
<li>$./translate.py some_file.txt</li>
<ul>
<li>The protiens sequence will be will be the default of 60 characters long</li>
<li>The replacement character will be the default, a plus sign.</li>
</ul>
</ol>


---
### Notes:
*   An input data set may contain any number of '\n' characters. They are ignored.
*   The line length parameter is optional and defaults to 60.
*   The replacement character parameter is optional and defaults to '+'.
