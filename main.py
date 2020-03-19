from goose3 import Goose
import re
from requests import get
import nltk
from plot_words import plot_map
from nltk.corpus import stopwords
from get_location import WordLocator
import time
import pickle
import sys
from os import listdir
from os.path import isfile, join
import itertools
import threading

# nltk.download()

REMOVE_STOP_WORDS = False
SAVE_PLOT = True
# precision for graph
ROUND_PRECISION = 3
# percentage cutoff on the number of words in the plot. set to -1 for no cut off
# affects linear regression
WORD_CUT_OFF = 20
# input source: TEXT, ONLINE
INPUT_TYPE = 'TEXT'
# fill with links, if chosen ONLINE for input_type
URL_LIST = []


def _cleanse_word(word):
    '''cleans word by filtering out non-letters'''
    return re.sub(r'[^\w]', '',  word.lower().strip())


def load_articles():
    '''grabs articles from online sources'''
    text = ""
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
    '''gets text from the texts folder'''
    text = ""
    title = ""
    if INPUT_TYPE == 'TEXT':
        print("TEXT input, grabbing text from text file")
        path = "texts/"
        files_list = [f for f in listdir(path) if isfile(join(path, f))]
        print("Pick File to Analyze (Input Number): ")

        for i in range(len(files_list)):
            print('[' + str(i + 1) + '] ' + files_list[i])
        selection = int(input())
        title = files_list[selection - 1]
        print("Picked: " + title)
        with open(path + title, 'r',  encoding="utf8") as file:
            text = file.read().replace('\n', ' ')
    elif INPUT_TYPE == 'ONLINE':
        # TODO: get url titles instead of generic "online"
        title = "online"
        text = load_articles()
    return text, title


def tokenize_words(text):
    '''tokenizes text and cleans each word'''
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
    '''params: all words as string. returns: list of tuples based on frequency'''
    # get frequency, returns list of tuples
    freq = nltk.FreqDist(words)
    freq_list = list(freq.items())
    # sort list by index 1 value and reverse it
    freq_list.sort(key=lambda tup: tup[1])
    freq_list.reverse()
    return freq_list


# def normalize(word_list, code):
#     '''normalizes slope of average distances'''
#     normalized_list = []
#     if code == 0:
#         largest = word_list[0][1]
#     elif code == 1:
#         largest = word_list[len(word_list) - 1][1]
#     for v, k in word_list:
#         normalized_list.append((v, k / largest))
#     return normalized_list

def get_slope(word_list):
    ''' params: gets list of tuples with words and average distance '''
    ''' returns list of tuples with words and their slops based on average distance'''
    slope_list = []
    length = len(word_list)
    for i in range(length):
        if (i < length - 1):
            slope = word_list[i + 1][1] - word_list[i][1]
            slope_list.append((i, slope))
    return slope_list


def loading():
    spinner = itertools.cycle(['-', '/', '|', '\\'])
    while True:
        sys.stdout.write(next(spinner))   
        sys.stdout.flush()
        time.sleep(0.1)              
        sys.stdout.write('\b')
                  


def main():
    start_time = time.time()

    # grabs text, whether from online or the texts folder. returns total tet in string and title
    text, title = get_text()
    words = tokenize_words(text)
    # t1 = threading.Thread(target=loading) 
    # t1.start() 

    if REMOVE_STOP_WORDS:
        remove_stop_words(words)

    freq_list = get_word_freq(words)

    # @param: list of words from article and the frequency of words. Returns list of tuples containing words and its locations in text
    word_locator = WordLocator(words, freq_list)
    word_locations = word_locator.get_word_locations()
    avg_locations = word_locator.get_avg_locations()

    slope_list = get_slope(avg_locations)

    # t1.join()
    print("Total words read:", len(words))
    print("--- %s seconds ---" % (time.time() - start_time))

    # @params: source, length of the words, graph title, type of graph, whether to save or not, how many words on x axis, rounding
    # type of graphs: freq(word frequencies), avg_dist (average distance between each word), sloped_avg (slopes of avg distances)
    plot_map(freq_list, len(words), title, "freq", SAVE_PLOT, WORD_CUT_OFF, ROUND_PRECISION)
    plot_map(avg_locations, len(words), title, "avg_dist", SAVE_PLOT, WORD_CUT_OFF, ROUND_PRECISION)
    plot_map(slope_list, len(words), title, "sloped_avg", SAVE_PLOT, WORD_CUT_OFF, ROUND_PRECISION)


if __name__ == "__main__":
    main()
