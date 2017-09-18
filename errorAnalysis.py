import logging
from models.statModel import StatModel
from util.corpus import Corpus
from util.stat import ddd, dd   # For loading pickle file

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
    datefmt='%a, %d %b %Y %H:%M:%S',
)

_, X = Corpus.loadCSVData('data/en_train.csv')
model = StatModel('data/freqDict.pkl')
prediction = model.predict(X)

for sentPre, sentGold in zip(prediction, X):
    for rowPre, rowGold in zip(sentPre, sentGold):
        if rowPre[-1] != rowGold[-1]:
            print(rowPre[-1] + '\t' + rowGold[-1])