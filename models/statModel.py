import pickle
import logging
from models.base import BaseModel
from models.rules import Rules


class StatModel(BaseModel):

    def __init__(self, pklFreqDict):
        super(StatModel, self).__init__()
        self.freqDict = self.loadPklFreqDict(pklFreqDict)
        self.unchangedList = ['<self>', 'sil']
        self.notFoundToken = 0
        self.notFoundLabel = 0

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
                sentAfter.append((sentID, tokenID, token))
                self.notFoundLabel += 1
            else:
                after = max(fd.items(), key=lambda tf: tf[1])[0]
                if after in self.unchangedList:
                    sentAfter.append((sentID, tokenID, token))
                else:
                    sentAfter.append((sentID, tokenID, after))
        return sentAfter
