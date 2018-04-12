from mysimilar import consonant_distance

def main():
    data = [
        ('mama', 'amma', 0.1),
        ('mam', 'mama', 0.1),
        ('mamam', 'mam', 100),
        ('tata', 'mata', 50),
        ('tama', 'tamta', 0.1),
        ('tata', 'mama', 100),
        ('abrakadabra', 'abra', 250),
        ('kamera', 'kameraman', 150)
    ]
    for s1, s2, expected in data:
        result = consonant_distance(s1, s2, print)
        print("'{}' : '{}' - is '{}' and expected is '{}'".format(s1, s2, result, expected))
        if result != expected:
            raise Exception('Different result than expected one')
    

if __name__ == "__main__":
    main() #sys.argv[1:]
