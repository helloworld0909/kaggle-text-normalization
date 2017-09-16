import logging
import csv
from collections import defaultdict


class Corpus(object):

    def __init__(self):
        pass


    @staticmethod
    def loadEnrichData(filePath):

        sentences = defaultdict(list)
        with open(filePath, 'r', encoding='utf-8') as inputFile:
            for line in inputFile:
                row = line.strip('\n').split('\t')
                row[0] = int(row[0])
                row[1] = int(row[1])
                sentences[row[0]].append(row)
            sentences = sorted(sentences.values(), key=lambda kv: kv[0][0])
        print('Sentences: {}'.format(len(sentences)))

        return sentences

    @staticmethod
    def loadCSVData(filePath):

        sentences = defaultdict(list)
        with open(filePath, 'r', encoding='utf-8') as csvfile:
            reader = csv.reader(csvfile, delimiter=',', quotechar='"')
            schema = reader.__next__()

            for row in reader:
                row[0] = int(row[0])
                row[1] = int(row[1])
                sentences[row[0]].append(row)

            sentences = sorted(sentences.values(), key=lambda kv: kv[0][0])
        print('Sentences: {}'.format(len(sentences)))

        return schema, sentences

    @staticmethod
    def yieldTrainData(filePath):
        with open(filePath, 'r', encoding='utf-8') as csvfile:
            reader = csv.reader(csvfile, delimiter=',', quotechar='"')
            _ = reader.__next__()
            X = []
            y = []
            for row in reader:
                sentID = int(row[0])
                tokenID = int(row[1])
                after = row[4]
                if tokenID == 0 and X:
                    yield X, y
                    X = []
                    y = []
                row[0] = sentID
                row[1] = tokenID
                X.append(tuple(row[:4]))
                y.append(after)


    @staticmethod
    def writePrediction(prediction, filePath):
        with open(filePath, 'w', encoding='utf-8', newline='') as csvfile:
            writer = csv.writer(csvfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_NONNUMERIC)
            writer.writerow(["id","after"])

            for sent in prediction:
                for row in sent:
                    ID = '{}_{}'.format(row[0], row[1])
                    writer.writerow([ID, row[2]])







if __name__ == '__main__':
    corpus = Corpus()
    _, sents = corpus.loadCSVData('data/en_test.csv')
    with open('data/en_test_CoNLL.txt', 'w', encoding='utf-8') as output_file:
        print(sents[0])
        for sentence in sents:
            X_trans = list(map(lambda t: t[-1], sentence))
            output_file.write('\n'.join(X_trans))
            output_file.write('\n\n')
