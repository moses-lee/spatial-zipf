import operator

class WordCounter(object):
    ''' Word counting object, counts frequency of words'''
    def __init__(self, text):
        self.text = text
        self.word_freq = dict()
        self._count_words()
        self.words_length = len(text)


    def _count_words(self):
        '''creates dictionary, with words being keys and number of occurrences as values'''
        for word in self.text:
            if word != '' and word != ' ':
                if word in self.word_freq:
                    self.word_freq[word] += 1
                else:
                    self.word_freq.update( {word : 1} )


    def get_word_frequency(self):
        ''' converts dictionary and returns in as orted tuple, also returns total word length'''
        return sorted(self.word_freq.items(), key=lambda x: x[1], reverse=True), self.words_length

                

