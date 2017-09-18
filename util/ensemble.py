import logging
from collections import defaultdict

def votingEnrich(filenameList):
    inputFileList = []
    for filename in filenameList:
        inputFileList.append(open(filename, 'r', encoding='utf-8'))
    with open('data/en_test_enrich.txt', 'w', encoding='utf-8') as outputFile:
        for lines in zip(*inputFileList):
            lines = list(map(lambda line: line.strip('\n').split('\t'), lines))

            labels = list(map(lambda line: line[2], lines))
            fd = defaultdict(int)
            for label in labels:
                fd[label] += 1
            votedLabel = max(fd.items(), key=lambda kv: kv[1])[0]
            votedLine = list(lines[0])
            votedLine[2] = votedLabel
            outputFile.write('\t'.join(votedLine) + '\n')

    for inputFile in inputFileList:
        inputFile.close()
    logging.info('Voting finish')


if __name__ == '__main__':
    votingEnrich(['data/enrich_0.99870.txt', 'data/enrich_0.99890.txt', 'data/enrich_0.99886.txt'])
