import logging
import pickle
from collections import defaultdict
from util.stat import ddd, dd   # For loading pickle file


def loadPklFreqDict(pklFreqDict):
    with open(pklFreqDict, 'rb') as pklFile:
        fd = pickle.load(pklFile)
        logging.info('Load pickle file finish')
        return fd


def ambiguousTrans(freqDict, threshold=0.1):
    ambiguousTransDict = defaultdict(ddd)
    for token, tokenFD in freqDict.items():
        for label, labelFD in tokenFD.items():
            if len(labelFD) >= 2:
                allTrans = sorted(labelFD.items(), key=lambda tf: tf[1])
                top2Trans = allTrans[-2:]
                if top2Trans[0][1] / top2Trans[1][1] > threshold:
                    ambiguousTransDict[token][label] = labelFD
                    logging.info('\t'.join([token, label, str(allTrans)]))

    with open('ambigousTrans.pkl', 'wb') as pklFile:
        pickle.dump(ambiguousTransDict, pklFile, -1)
    logging.info('AmbiguousTrans finish')


if __name__ == '__main__':

    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
        datefmt='%a, %d %b %Y %H:%M:%S',
    )

    fd = loadPklFreqDict('data/freqDict.pkl')
    ambiguousTrans(fd, threshold=0.1)



