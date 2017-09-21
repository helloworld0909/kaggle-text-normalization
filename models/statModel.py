import pickle
import logging
from collections import defaultdict
from models.base import BaseModel
from models.rules import Rules


class StatModel(BaseModel):

    def __init__(self, pklFreqDict):
        super(StatModel, self).__init__()
        self.freqDict = self.loadPklFreqDict(pklFreqDict)
        self.unchangedList = ['<self>', 'sil']
        self.notFoundToken = 0
        self.notFoundLabel = 0
        self.potentialError = 0

    @staticmethod
    def loadPklFreqDict(pklFreqDict):
        with open(pklFreqDict, 'rb') as pklFile:
            fd = pickle.load(pklFile)
            logging.info('Load pickle file finish')
            return fd

    def predictSentence(self, sent):
        sentAfter = []
        for row in sent:
            sentID, tokenID, label, token = row[:4]
            getToken = self.freqDict.get(token, {})
            getLabel = getToken.get(label, {})

            if not getToken:
                sentAfter.append((sentID, tokenID, token))
                self.notFoundToken += 1
            elif getToken and not getLabel:
                if len(getToken) > 1 or len(list(getToken.values())[0]) > 1:
                    self.potentialError += 1
                    logging.debug(token + '\t' + label)
                    logging.debug(str(dict(getToken)))

                afterFD = defaultdict(int)
                for labelFD in getToken.values():
                    for after, freq in labelFD.items():
                        afterFD[after] += freq
                after = max(afterFD.items(), key=lambda tf: tf[1])[0]

                if after in self.unchangedList:
                    sentAfter.append((sentID, tokenID, token))
                else:
                    sentAfter.append((sentID, tokenID, after))
                self.notFoundLabel += 1
                
            else:
                after = max(getLabel.items(), key=lambda tf: tf[1])[0]
                if after in self.unchangedList:
                    sentAfter.append((sentID, tokenID, token))
                else:
                    sentAfter.append((sentID, tokenID, after))
        return sentAfter


class BigramStatModel(StatModel):

    def __init__(self, *argv):
        super(BigramStatModel, self).__init__(*argv)

    def predictSentence(self, sent):
        sentAfter = []
        previousLabel = '</s>'
        for row in sent:
            sentID, tokenID, label, token = row[:4]
            getToken = self.freqDict.get(token, {})
            getLabel = getToken.get((previousLabel, label), {})
            if not getToken:
                sentAfter.append((sentID, tokenID, token))
                self.notFoundToken += 1
            elif getToken and not getLabel:
                if len(getToken) > 1 or len(list(getToken.values())[0]) > 1:
                    self.potentialError += 1
                    logging.debug(token + '\t' + label)
                    logging.debug(str(dict(getToken)))
                afterFD = defaultdict(int)
                for labelFD in getToken.values():
                    for after, freq in labelFD.items():
                        afterFD[after] += freq
                after = max(afterFD.items(), key=lambda tf: tf[1])[0]

                if after in self.unchangedList:
                    sentAfter.append((sentID, tokenID, token))
                else:
                    sentAfter.append((sentID, tokenID, after))
                self.notFoundLabel += 1
            else:
                after = max(getLabel.items(), key=lambda tf: tf[1])[0]
                if after in self.unchangedList:
                    sentAfter.append((sentID, tokenID, token))
                else:
                    sentAfter.append((sentID, tokenID, after))
            previousLabel = label
        return sentAfter
