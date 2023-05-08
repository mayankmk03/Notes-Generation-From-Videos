import string
import gensim
from gensim import corpora
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
from nltk import pos_tag
from nltk.stem.wordnet import WordNetLemmatizer


class LDAKeywords():

    def __init__(self) -> None:
        self.lemma = WordNetLemmatizer()
        self.word_stemmer = PorterStemmer()

    def __clean(self, text: str) -> str:

        stop = set(stopwords.words('english'))
        exclude = set(string.punctuation)

        stop_free = ' '.join(
            [word for word in text.lower().split() if word not in stop])
        punc_free = ''.join(ch for ch in stop_free if ch not in exclude)

        normalized = ' '.join([self.lemma.lemmatize(word)
                              for word in punc_free.split()])
        stemmed_words = self.word_stemmer.stem(normalized.lower())

        sent = pos_tag(stemmed_words.split())
        sent_clean = [x for (x, y) in sent if y in ('NNS', 'NNPS', 'NN')]

        return sent_clean

    def __get_text(self) -> str:
        text = ""
        with open('transcript.txt', 'r') as f:
            text = f.read()

        return text

    def __get_term_matrix_and_dict(self) -> tuple:

        prompttext = self.__get_text()
        new_words = self.__clean(prompttext)

        dictionary = corpora.Dictionary([new_words])
        doc_term_matrix = [dictionary.doc2bow(doc) for doc in [new_words]]

        return (doc_term_matrix, dictionary)

    def get_keywords(self) -> str:
        lda = gensim.models.ldamodel.LdaModel

        doc_term_matrix, dictionary = self.__get_term_matrix_and_dict()

        num_topics = 10
        ldamodel = lda(doc_term_matrix, num_topics=num_topics,
                       id2word=dictionary, passes=50, minimum_probability=0)
        topic_num = 0
        topic_words = ldamodel.show_topic(topic_num)

        keywords=''
        for idx, word in enumerate(topic_words):
            keywords=keywords+str(idx + 1) +'. '+word[0].capitalize()+'\n'

        return keywords


if __name__ == "__main__":

    lda = LDAKeywords()
    # returns a tuple list of tuples with each tuple consisting of the word and its weight

    topics = lda.get_keywords()

    # for idx, word in enumerate(topics):
    #     print(idx + 1, word[0].capitalize())
