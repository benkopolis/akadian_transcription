'''
@author: Zbigniew Manasterski
@contact  benkopolis@gmail.com
@date Jul 18, 2017
'''
import sys

SRC_FILES = ['res_10saa.txt.trans', 'res_16saa.txt.trans', 'res_esarhaddon.txt.trans']

SIM_WORDS = {}

def noop(msg):
    pass

def confirm():
    print('Press "y" to continue, or "n" to quit')
    for line in sys.stdin:
        if line.strip() == 'y':
            return
        elif line.strip() == 'n':
            raise NotImplementedError
        print('Press "y" to continue, or "n" to quit')

def remove_vovels(s1, s2):
    vowels = ('a', 'e', 'i', 'o', 'u', 'y')
    s1_stripped = ''.join([l for l in s1 if l not in vowels]);
    s2_stripped = ''.join([l for l in s2 if l not in vowels]);
    if len(s1_stripped) > len(s2_stripped):
        s1_stripped, s2_stripped = s2_stripped, s1_stripped
    return s1_stripped, s2_stripped

def consonant_distance(s1, s2, debug=noop):
    debug('s1: {}, s2: {}'.format(s1, s2))
    s1_stripped, s2_stripped = remove_vovels(s1, s2)
    debug('str1: {}, str2: {}'.format(s1_stripped, s2_stripped))
    if len(s1_stripped) == 0 or len(s2_stripped) == 0:
        debug('100 - length 0')
        return 100
    delta = 0
    for i1, c1 in enumerate(s2_stripped):
        if not len(s1_stripped) > i1 + delta:
            debug('50 * diff - length')
            return 50 * (len(s2_stripped) - i1 - delta + 1)
        debug('C1: {}, C2: {}'.format(c1, s1_stripped[i1 + delta]))
        if s1_stripped[i1 + delta] == c1:
            continue
        elif c1 == 't' and delta == 0:
            delta = delta - 1
        elif s1_stripped[i1 + delta] == 't' and delta == 0:
            delta = delta + 1
            if not len(s1_stripped) > i1 + 1 + delta:
                debug('t was the last letter')
                return 0.1
        else:
            debug('different letter')
            return 100
    if delta > 1:
        debug('delta')
        return 10 * delta
    debug('similar')
    return 0.1  

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
    s1_stripped, s2_stripped = remove_vovels(s1, s2)
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
    #print('Storable: {}, distance: {}, words: {} - {}'.format(storable, distance, s1, s2))
    #confirm()
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

def hasNumbers(inputString):
    return any(char.isdigit() for char in inputString)

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
                    if len(word) < 2 or hasNumbers(word):
                        continue
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
            elif switch == 'consonant':
                dist = consonant_distance(w1, w2)
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
