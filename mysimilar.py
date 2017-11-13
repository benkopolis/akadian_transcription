'''
@author: Zbigniew Manasterski
@contact  benkopolis@gmail.com
@date Jul 18, 2017
'''
import sys

SRC_FILES = ['res_10saa.txt.trans', 'res_16saa.txt.trans', 'res_esarhaddon.txt.trans']

SIM_WORDS = {}

def levenshtein_distance(s1, s2):
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
    return float(distances[-1])

def levenshtein_distance_novovels(s1, s2):
    vowels = ('a', 'e', 'i', 'o', 'u')
    s1_stripped = ''.join([l for l in s1 if l not in vowels]);
    s2_stripped = ''.join([l for l in s1 if l not in vowels]);
    if len(s1_stripped) > len(s2_stripped):
        s1_stripped, s2_stripped = s2_stripped, s1_stripped

    distances = range(len(s1_stripped) + 1)
    for i2, c2 in enumerate(s2_stripped):
        distances_ = [i2+1]
        for i1, c1 in enumerate(s1_stripped):
            if c1 == c2:
                distances_.append(distances[i1])
            else:
                distances_.append(1 + min((distances[i1], distances[i1 + 1], distances_[-1])))
        distances = distances_
    return float(distances[-1])

def store_similar(distance, s1, s2):
    storable = False
    if distance == 0:
        return
    if len(s1) > len(s2):
        storable = float(distance) / float(len(s1)) < 0.3
    else:
        storable = float(distance) / float(len(s2)) < 0.3
    if not storable:
        return
    if s1 not in SIM_WORDS and s2 not in SIM_WORDS:
        SIM_WORDS[s1] = set()
    if s2 in SIM_WORDS:
        if s1 not in SIM_WORDS[s2]:
            SIM_WORDS[s2].add(s1)
    elif s1 in SIM_WORDS:
        if s2 not in SIM_WORDS[s1]:
            SIM_WORDS[s1].add(s2)
    else:
        raise NotImplementedError()



def main(argv):
    """
    Main function
    """
    if len(argv) < 4:
        print('Too few arguments')
        return
    output_index = argv.index('-o') + 1
    output = argv[output_index]
    switch_index = argv.index('-s') + 1
    switch = argv[switch_index]
    print('Storing to {}, based on switch: {}'.format(output, switch))
    all_words = set()
    skip = False
    for file in SRC_FILES:
        with open(file, 'r') as input:
            for line in input:
                if skip == False and line.startswith('='):
                    skip = True
                    continue
                if skip == True and line.startswith('='):
                    skip = False
                    continue
                if skip == True:
                    continue
                for word in line.split(' '):
                    word = word.strip()
                    if word not in all_words:
                        all_words.add(word)
    for w1 in all_words:
        for w2 in all_words:
            if w1 == w2:
                continue
            dist = 0
            if switch == 'normal':
                dist = levenshtein_distance(w1, w2)
            elif switch == 'nonvovel':
                dist = levenshtein_distance_novovels(w1, w2)
            store_similar(dist, w1, w2)
    print('stored {} words'.format(len(SIM_WORDS.keys())))
    with open(output, 'w') as result:
        for key in SIM_WORDS:
            try:
                result.write(key)
                result.write(': ')
                for w in SIM_WORDS[key]:
                    result.write(w)
                    result.write(', ')
                result.write('\n')
            except UnsupportedOperation as ex:
                pass
    print('Done')


if __name__ == "__main__":
    main(sys.argv[1:])
