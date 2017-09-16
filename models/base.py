import logging
from collections import defaultdict


class BaseModel(object):

    def __init__(self):
        pass


    def predict(self, X):
        prediction = []
        for sentID, sent in enumerate(X):
            sentAfter = self.predictSentence(sent)
            prediction.append(sentAfter)
        logging.info('Prediction finish')
        return prediction


    def predictSentence(self, sent):
        raise NotImplementedError()