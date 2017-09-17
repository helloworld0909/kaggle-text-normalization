import logging


class Rules(object):

    def __init__(self):
        self.transList = [
            str.maketrans("₀₁₂₃₄₅₆₇₈₉", "0123456789"),
            str.maketrans("⁰¹²³⁴⁵⁶⁷⁸⁹", "0123456789"),
            str.maketrans("፬", "4"),
        ]


    def predictToken(self, token, label):
        if label == 'LETTERS':
            after = filter(str.isalpha, token)
            after = map(str.lower, after)
            after = ' '.join(after)
            return after

        else:
            return token





