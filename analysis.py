import logging
import pickle
from collections import defaultdict
import numpy as np
from util.stat import ddd, dd   # For loading pickle file


def loadPklFreqDict(pklFreqDict):
    with open(pklFreqDict, 'rb') as pklFile:
        fd = pickle.load(pklFile)
        logging.info('Load pickle file finish')
        return fd


def ambiguousTrans(freqDict):
    ambiguousTransDict = defaultdict(ddd)
    totalCount = 0
    for token, tokenFD in freqDict.items():
        for label, labelFD in tokenFD.items():
            if len(labelFD) >= 2:
                allTrans = sorted(labelFD.items(), key=lambda tf: tf[1], reverse=True)
                nTrans = np.array(list(map(lambda tf: tf[1], allTrans)))
                totalCount += nTrans[1:].sum()

                ambiguousTransDict[token][label] = labelFD
                logging.debug('\t'.join([token, label, str(allTrans)]))

    with open('data/ambigousTrans.pkl', 'wb') as pklFile:
        pickle.dump(ambiguousTransDict, pklFile, -1)
    logging.info('Potential error rate: {}'.format(totalCount / 1000000000))
    logging.info('AmbiguousTrans finish')


def ambiguousLabel(freqDict, threshold=1000):
    ambiguousLabelDict = defaultdict(ddd)

    totalDiffCount = 0
    for token, tokenFD in freqDict.items():
        if len(tokenFD) >= 2:

            allLabel = sorted(tokenFD.items(), key=lambda lf: sum(lf[1].values()), reverse=True)

            topLabel = allLabel[0][0]
            topLabelFD = tokenFD[topLabel]
            topLabelAfter = max(topLabelFD.items(), key=lambda lf: lf[1])[0]

            diffCount = 0
            for label, _ in allLabel[1:]:
                labelFD = tokenFD[label]
                for after, freq in labelFD.items():
                    if after != topLabelAfter:
                        diffCount += freq

            if diffCount >= threshold:
                ambiguousLabelDict[token] = tokenFD
                logging.info('\t'.join([token, str(dict(tokenFD))]))
                totalDiffCount += diffCount

    with open('data/ambigousLabel.pkl', 'wb') as pklFile:
        pickle.dump(ambiguousLabelDict, pklFile, -1)
    logging.info('Total diff count: {}'.format(totalDiffCount))
    logging.info('ambigousLabel finish')

if __name__ == '__main__':

    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
        datefmt='%a, %d %b %Y %H:%M:%S',
    )

    fd = loadPklFreqDict('data/freqDict.pkl')
    # ambiguousTrans(fd)
    # ambiguousLabel(fd, threshold=1000)
    print(dict(fd['-']))

