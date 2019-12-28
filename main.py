from goose3 import Goose
import re
from requests import get
import nltk
from plot_words import plot_map
from nltk.corpus import stopwords
from get_location import WordLocator 
import time
import pickle
# nltk.download()

REMOVE_STOP_WORDS = False
ROUND_PRECISION = 3
CUT_OFF = 100
TITLE = 'TEST'
# TEXT, ONLINE
INPUT_TYPE = 'TEXT'
FILENAME = 'texts/modestproposal.txt'
URL_LIST = ['https://www.cnn.com/2019/12/06/politics/trump-supreme-court-financial-documents-house-subpoena/index.html',
            'https://www.cnn.com/2019/12/07/politics/us-taliban-peace-talks-resume-doha-qatar/index.html',
            'https://www.cnn.com/travel/article/china-fake-meat-vegetarian-intl-hnk/index.html',
            'https://www.cnn.com/travel/article/world-champion-cheese-2019-rogue-river-blue-trnd/index.html',
            'https://www.cnn.com/2019/12/07/asia/north-korea-test-intl-hnk/index.html',
            'https://www.cnn.com/2019/12/07/middleeast/iraq-baghdad-protesters-killed-intl/index.html',
            'https://www.cnn.com/2019/12/04/entertainment/gabrielle-union-agt-investigation/index.html',
            'https://www.cnn.com/2019/12/04/entertainment/jason-momoa-apologizes-chris-pratt-trnd/index.html',
            'https://www.cnn.com/2019/12/06/us/florida-ups-shootout-frank-ordonez/index.html',
            'https://www.cnn.com/2019/12/06/us/75-foot-wave-california-bomb-cyclone-wxc-trnd/index.html']
     

def _cleanse_word(word):
    '''cleans word by filtering out non-letters'''
    return re.sub(r'[^\w]', '',  word.lower().strip())


def load_articles():
    # append all words from articles into a single string
    text = ''
    counter = 0
    for url in URL_LIST:
        response = get(url)
        extractor = Goose()
        article = extractor.extract(raw_html=response.content)
        text += article.cleaned_text
        counter += 1
        print("Article", counter, "out of", len(URL_LIST), "done.")
    return text


def get_text(): 
    text = ''
    if INPUT_TYPE == 'TEXT':
        print("TEXT input, grabbing text from text file") 
        with open(FILENAME, 'r',  encoding="utf8") as file:
            text = file.read().replace('\n', ' ')
    elif INPUT_TYPE == 'ONLINE':
        text = load_articles()
        # print("ONLINE input, attempting to grab text from pickle") 
        # try:
        #     text = pickle.load(open("text.pickle", "rb"))
        #     print("Successfully grabbed text from pickle")
        # except (OSError, IOError) as e:
        #     print("No pickle, grabbing text...")
        #     text = load_articles()
        #     pickle.dump(text, open("text.pickle", "wb"))
    return text


def tokenize_words(text):
    # tokenizes text and cleans each word
    words = []
    for t in nltk.word_tokenize(text):
        cleaned = _cleanse_word(t)
        if cleaned != '':
            words.append(cleaned)
    return words

def remove_stop_words(words):
    temp_words = words[:]
    sw = stopwords.words('english')
    for token in temp_words:
        if token in sw:
            words.remove(token)

def get_word_freq(words):
    # get frequency, returns list of tuples
    freq = nltk.FreqDist(words)
    freq_list = list(freq.items())
    # sort list by index 1 value and reverse it
    freq_list.sort(key=lambda tup: tup[1])
    freq_list.reverse()
    return freq_list

def normalize(word_list, code):
    normalized_list = []
    if code == 0:
        largest = word_list[0][1]
    elif code == 1:
        largest = word_list[len(word_list) - 1][1]
    for v, k in word_list:
        normalized_list.append((v, k / largest))
    return normalized_list

def main():
    start_time = time.time()
 
    text = get_text()
    words = tokenize_words(text)
    if REMOVE_STOP_WORDS:
        remove_stop_words(words)

    freq_list = get_word_freq(words)
    
    # params: list of words from article and the frequeny of words. Returns list of tuples containing words and its locations in text
    word_locator = WordLocator(words, freq_list)
    word_locations = word_locator.get_word_locations()
    avg_locations = word_locator.get_avg_locations()
    # print(word_locations)
    # print(avg_locations)
 
    # print("Total words read:", words_length)
    print("--- %s seconds ---" % (time.time() - start_time))
    
    plot_map(freq_list, len(words), TITLE, 'freq', CUT_OFF, ROUND_PRECISION)
    plot_map(avg_locations, len(words), TITLE, 'loc', CUT_OFF, ROUND_PRECISION)
    

if __name__ == "__main__":
    main()
