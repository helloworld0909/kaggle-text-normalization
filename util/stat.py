import logging
import pickle
from collections import defaultdict


nameList = ['output-000{:0>2}-of-00100'.format(i) for i in range(1)]


def dd():
    return defaultdict(int)

def ddd():
    return defaultdict(dd)

def generateFreqDict(filenameList):

    freqDict = defaultdict(ddd)
    for filename in filenameList:
        with open(filename, 'r', encoding='utf-8') as inputFile:
            for line in inputFile:
                if line.startswith('<eos>') or not line.strip():
                    continue
                line = line.strip('\n').split('\t')
                label, token, after = line
                freqDict[token][label][after] += 1
        logging.info('{} finish'.format(filename))
    with open('freqDict.pkl', 'wb') as pklFile:
        pickle.dump(freqDict, pklFile, -1)
    logging.info('VocabSize: {}'.format(len(freqDict)))


if __name__ == '__main__':

    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
        datefmt='%a, %d %b %Y %H:%M:%S',
    )

    generateFreqDict(nameList)