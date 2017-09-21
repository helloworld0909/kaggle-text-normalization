import logging
from models.statModel import StatModel
from util.corpus import Corpus
from util.stat import ddd, dd   # For loading pickle file
from util.ensemble import votingEnrich

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
    datefmt='%a, %d %b %Y %H:%M:%S',
)

votingEnrich([
    'data/enrich_0.99890.txt',
    'data/enrich_0.99889.txt',
    'data/enrich_0.99886.txt',
    'data/enrich_0.99892.txt',
    'data/enrich_0.99901.txt'
])
X = Corpus.loadEnrichData('data/en_test_enrich.txt')
model = StatModel('data/freqDict.pkl')
prediction = model.predict(X)
logging.info('Not found token rate: {}'.format(model.notFoundToken / 1088565.0))
logging.info('Found token but not found label rate: {}'.format(model.notFoundLabel / 1088565.0))
logging.info('Potential error rate: {}'.format(model.potentialError / 1088565.0))
Corpus.writePrediction(prediction, 'submission.csv')

