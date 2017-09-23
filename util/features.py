import nltk

class FeatureFactory(object):

    def __init__(self):
        self.featureFuncList = [
            self.pos_tag,
            self.string_normal,
        ]

        self.pos_tagger = nltk.pos_tag

    def getFeatures(self, tokenSeq):
        featureSeqs = []
        for featureFunc in self.featureFuncList:
            featureSeq = featureFunc(tokenSeq)
            assert len(featureSeq) == len(tokenSeq)
            featureSeqs.append(featureSeq)
        return featureSeqs

    def pos_tag(self, text_seq):
        return tuple(zip(*self.pos_tagger(text_seq)))[1]

    def string_normal(self, text_seq):
        return tuple(map(lambda w: self.normalization(w), text_seq))

    @staticmethod
    def normalization(word):
        normal_word = ''
        for char in word:
            if char.isupper():
                normal_word += 'A'
            elif char.islower():
                normal_word += 'a'
            elif char.isdigit():
                normal_word += '1'
            else:
                normal_word += '0'
        return normal_word

    def generateCoNLL(self, filename, outputName):
        with open(filename, 'r', encoding='utf-8') as inputFile:
            with open(outputName, 'w', encoding='utf-8') as outputFile:
                tokenSeq = []
                labelSeq = []

                for line in inputFile:
                    if line.startswith('<eos>') or not line.strip():
                        featureSeqs = self.getFeatures(tokenSeq)

                        for i in range(len(tokenSeq)):
                            write_line = tokenSeq[i] + '\t' + '\t'.join(map(lambda f: str(f[i]), featureSeqs)) + '\t' + \
                                         labelSeq[i] + '\n'
                            outputFile.write(write_line)

                        outputFile.write('\n')

                        tokenSeq = []
                        labelSeq = []
                    else:
                        label, token, after = line.strip('\n').split('\t')
                        tokenSeq.append(token)
                        labelSeq.append(labelSeq)

if __name__ == '__main__':
    featureFactory = FeatureFactory()
    featureFactory.generateCoNLL('../data/en_with_types/output-00001-of-00100', 'en_train_01.txt')