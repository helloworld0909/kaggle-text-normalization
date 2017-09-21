import logging
import pickle
import re
from collections import defaultdict


def dd():
    return defaultdict(int)


def ddd():
    return defaultdict(dd)


class TranslateRule(object):

    def __init__(self):
        self.alphabet = 'abcdefghijklmnopqrstuvwxyz'
        self.trigger = re.compile('_letter')
        self.translate = {'{}_letter'.format(c): c for c in self.alphabet}
        self.translate['_letter'] = ''
        self.whitespaces = re.compile(' +')

    def apply(self, raw, label):
        if re.search(self.trigger, raw):
            for before, after in self.translate.items():
                raw = raw.replace(before, after)
            raw = self.whitespaces.sub(' ', raw)

        raw = raw.strip(' ')

        if label == 'ELECTRONIC"':
            raw = raw.replace('dot c o m', 'dot com')
            raw = raw.replace('s l a s h', 'slash')
            raw = raw.replace('c o l o n', 'colon')
            raw = raw.replace('d a s h', 'dash')
            raw = raw.replace(' h a s h ', ' hash ')

        return raw


def generateFreqDict(filenameList):

    freqDict = defaultdict(ddd)
    translateRule = TranslateRule()
    for filename in filenameList:
        with open(filename, 'r', encoding='utf-8') as inputFile:
            for line in inputFile:
                if line.startswith('<eos>') or not line.strip():
                    continue
                line = line.strip('\n').split('\t')
                label, token, after = line

                after = translateRule.apply(after, label)

                freqDict[token][label][after] += 1
        logging.info('{} finish'.format(filename))
    with open('freqDict.pkl', 'wb') as pklFile:
        pickle.dump(freqDict, pklFile, -1)
    logging.info('VocabSize: {}'.format(len(freqDict)))


def generateBigramFreqDict(filenameList):
    bigramFreqDict = defaultdict(ddd)
    translateRule = TranslateRule()
    for filename in filenameList:
        with open(filename, 'r', encoding='utf-8') as inputFile:
            previousLabel = '</s>'
            for line in inputFile:
                if line.startswith('<eos>') or not line.strip():
                    previousLabel = '</s>'
                    continue
                line = line.strip('\n').split('\t')
                label, token, after = line

                after = translateRule.apply(after, label)

                bigramFreqDict[token][tuple((previousLabel, label))][after] += 1
                previousLabel = label
        logging.info('{} finish'.format(filename))
    with open('bigramFreqDict.pkl', 'wb') as pklFile:
        pickle.dump(bigramFreqDict, pklFile, -1)
    logging.info('VocabSize: {}'.format(len(bigramFreqDict)))


def fixFreqDict(filename):
    with open(filename, 'rb') as pklFile:
        freqDict = pickle.load(pklFile)
        logging.info('Load pickle file finish')
    for tokenFD in freqDict.values():
        for labelFD in tokenFD.values():
            for after, freq in labelFD.items():
                if after.startswith(' '):
                    labelFD.pop(after)
                    labelFD[after.strip(' ')] = freq
                if after.startswith('h t t p'):
                    labelFD.pop(after)
                    after = after.replace('dot c o m', 'dot com')
                    after = after.replace('s l a s h', 'slash')
                    after = after.replace('c o l o n', 'colon')
                    after = after.replace('d a s h', 'dash')
                    after = after.replace(' h a s h ', ' hash ')
                    labelFD[after] = freq
    with open('freqDict.pkl', 'wb') as pklFile:
        pickle.dump(freqDict, pklFile, -1)
    logging.info('VocabSize: {}'.format(len(freqDict)))


def generateCoNLL(filename, outputName):
    with open(filename, 'r', encoding='utf-8') as inputFile:
        with open(outputName, 'w', encoding='utf-8') as outputFile:
            for line in inputFile:
                if line.startswith('<eos>') or not line.strip():
                    outputFile.write('\n')
                    continue
                label, token, after = line.strip('\n').split('\t')
                outputFile.write(token + '\t' + label + '\n')


if __name__ == '__main__':

    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
        datefmt='%a, %d %b %Y %H:%M:%S',
    )

    nameList = ['../en_with_types/output-000{:0>2}-of-00100'.format(i) for i in range(100)]
    # generateBigramFreqDict(nameList)
    # generateCoNLL('../en_with_types/output-00001-of-00100', 'en_train_CoNLL1.txt')
    fixFreqDict('data/bigramFreqDict.pkl')
