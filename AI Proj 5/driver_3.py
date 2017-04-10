# IMDB sentiment analysiser
# Jake Lee Attempt 1
# EdX (ColumbiaX): Artificial Intelligence

from os import listdir
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.linear_model import SGDClassifier
from sklearn.feature_extraction.text import TfidfVectorizer
import string

train_path = "../resource/asnlib/public/aclImdb/train/" # use terminal to ls files under this directory
test_path = "../resource/asnlib/public/imdb_te.csv" # test data for grade evaluation

# train_path = "aclImdb/train/" # use terminal to ls files under this directory
# test_path = "imdb_te.csv" # test data for grade evaluation

sw = open("stopwords.en.txt", "r", encoding="utf8")
stopwords = sw.read()
sw.close()
stopwords = stopwords.split("\n")


def process(string_set):
    words = string_set
    words = words.replace("<br />", " ")
    words = words.rstrip()
    replace = str.maketrans(string.punctuation, ' '*len(string.punctuation))
    words = words.translate(replace)
    words = words.lower()
    words = words.split()
    words = [word for word in words if word not in stopwords]
    words = ' '.join(words)

    return words


def imdb_data_preprocess(inpath, outpath="./", name="imdb_tr.csv", mix=False):
    fo = open(name, "w", encoding='utf8')
    fo.write("row_number,text,polarity\n")

    count = 0
    for text in listdir(inpath + "pos"):
        fi = open(inpath + "pos/" + text, "r", encoding='utf8')
        text = process(fi.read())
        fo.write(str(count) + "," + text + ",1" + "\n")
        count += 1
        fi.close()

    for text in listdir(inpath + "neg"):
        fi = open(inpath + "neg/" + text, "r", encoding='utf8')
        text = process(fi.read())
        fo.write(str(count) + "," + text + ",0" + "\n")
        count += 1
        fi.close()




if "__main__" == __name__:
    imdb_data_preprocess(train_path)

    training = pd.read_csv("imdb_tr.csv")
    test_set = pd.read_csv(test_path, encoding="ISO-8859-1")
    test_set['text'] = test_set['text'].apply(process)

    # UNIGRAM
    count_vec = CountVectorizer(stop_words=stopwords)
    transform_train = count_vec.fit_transform(training['text'])
    classifier = SGDClassifier(loss="hinge", penalty="l1")
    classifier.fit(transform_train, training['polarity'])

    # Output classification for test set
    transform_test = count_vec.transform(test_set['text'])
    results = classifier.predict(transform_test)
    with open("unigram.output.txt", "w") as f:
        for result in results:
            f.write(str(result) + "\n")


    # BIGRAM
    count_vec = CountVectorizer(stop_words=stopwords, ngram_range=(1, 2))
    transform_train = count_vec.fit_transform(training['text'])
    classifier = SGDClassifier(loss="hinge", penalty="l1")
    classifier.fit(transform_train, training['polarity'])

    # Output classification for test set
    transform_test = count_vec.transform(test_set['text'])
    results = classifier.predict(transform_test)
    with open("bigram.output.txt", "w") as f:
        for result in results:
            f.write(str(result) + "\n")


    # Unigram TdIdf
    count_vec = TfidfVectorizer(stop_words=stopwords)
    transform_train = count_vec.fit_transform(training['text'])
    classifier = SGDClassifier(loss="hinge", penalty="l1")
    classifier.fit(transform_train, training['polarity'])

    # Output classification for test set
    transform_test = count_vec.transform(test_set['text'])
    results = classifier.predict(transform_test)
    with open("unigramtfidf.output.txt", "w") as f:
        for result in results:
            f.write(str(result) + "\n")


    # BIGRAM TdIdf
    count_vec = TfidfVectorizer(stop_words=stopwords, ngram_range=(1, 2))
    transform_train = count_vec.fit_transform(training['text'])
    classifier = SGDClassifier(loss="hinge", penalty="l1")
    classifier.fit(transform_train, training['polarity'])

    # Output classification for test set
    transform_test = count_vec.transform(test_set['text'])
    results = classifier.predict(transform_test)
    with open("bigramtfidf.output.txt", "w") as f:
        for result in results:
            f.write(str(result) + "\n")




