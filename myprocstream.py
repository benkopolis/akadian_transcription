'''
@author: Zbigniew Manasterski
@contact  benkopolis@gmail.com
@date Jul 18, 2017
'''
import sys
import re

SRC_FILES = ['res_10saa.txt', 'res_16saa.txt', 'res_esarhaddon.txt']
HYPHENS = [r'\u002d', r'\u007e', r'\u00ad', r'\u058a', r'\u05be', r'\u1400', r'\u1806',
           r'\u2010', r'\u2011', r'\u2012', r'\u2013', r'\u2014', r'\u2015', r'\u2053',
           r'\u207b', r'\u208b', r'\u2212', r'\u2e17', r'\u2e3a', r'\u2e3b', r'\u301c',
           r'\u3030', r'\u30a0', r'\ufe31', r'\ufe32', r'\ufe58', r'\ufe63', r'\uff0d']
RE_REMOVE3 = r'\{[0-9a-zA-Z]{1,1}\}'
RE_REMOVE = '[{}]'.format(HYPHENS)
SEPARATORS = ['========================',
              '=======TITLE=======',
              '=======TRANSLITERATION=======',
              'DONE']
CONN_RE = re.compile(r'([A-Z]|\u0160|\u1e6c)-([a-z]|\u0161|\u1e6d)')
BIG_RE = re.compile(r'((?:[A-Z]|\u0160|\u1e6c){1,})-((?:[A-Z]|\u0160|\u1e6c){1,})')

RE_VOWELS = re.compile(r'(:[eui]){2,2}')

def replace_all_matching(to_replace, pattern, substitution):
    tmp_word = re.sub(pattern, substitution, to_replace, 0)
    while tmp_word != to_replace:
        to_replace = tmp_word
        tmp_word = re.sub(pattern, substitution, to_replace, 0)
    return tmp_word

def proc_file(input):
    ofile = open('{}.trans'.format(input), "w")
    with open(input, 'r') as ifile:
        was_title = False
        for line in ifile:
            if len(line) == 0:
                ofile.write('\n')
                continue
            if line in SEPARATORS:
                if 'TITLE' in line:
                    was_title = True
                ofile.write(line)
                continue
            if was_title:
                was_title = False
                ofile.write(line)
                continue
            new_line = ''
            for word in line.split(' '):
                word = re.sub(RE_REMOVE3, "", word, 0)
                word = word.replace('{', '')
                word = word.replace('}', '-')
                word = word.replace('ʾ', '')
                word = word.replace('@', '')
                word = word.replace('v', '')
                word = word.replace('₃', '')
                word = word.replace('₂', '')
                word = replace_all_matching(word, BIG_RE, r'\1.\2')
                word = replace_all_matching(word, CONN_RE, r'\1 \2')
                word = re.sub(RE_REMOVE, "", word, 0)
                word = word.replace('-', '')
                word = re.sub('a{2,3}', 'aya', word, 0)
                word = word.replace('ee', 'e')
                word = word.replace('uu', 'u')
                word = word.replace('iia', 'iya')
                found = RE_VOWELS.findall(word)
                for f in found:
                    word = re.sub(f, f[0], word, 0)
                new_line = '{} {}'.format(new_line, word)
            ofile.write(word)
    ofile.close()

def main(argv):
    """
    Main function
    """
    if len(argv) == 3:
        return
    for file in SRC_FILES:
        proc_file(file)

if __name__ == "__main__":
    main(sys.argv[1:])
