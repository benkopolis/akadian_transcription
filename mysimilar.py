'''
@author: Zbigniew Manasterski
@contact  benkopolis@gmail.com
@date Jul 18, 2017
'''
import sys

SRC_FILES = ['res_10saa.txt', 'res_16saa.txt', 'res_esarhaddon.txt']

SIM_WORDS = {}

def levenshteinDistance(s1, s2):
    if len(s1) > len(s2):
        s1, s2 = s2, s1

    distances = range(len(s1) + 1)
    for i2, c2 in enumerate(s2):
        distances_ = [i2+1]
        for i1, c1 in enumerate(s1):
            if c1 == c2:
                distances_.append(distances[i1])
            else:
                distances_.append(1 + min((distances[i1], distances[i1 + 1], distances_[-1])))
        distances = distances_
    return distances[-1]

def main(argv):
    """
    Main function
    """
    if len(argv) == 3:
        return
    for file in SRC_FILES:

if __name__ == "__main__":
    main(sys.argv[1:])
