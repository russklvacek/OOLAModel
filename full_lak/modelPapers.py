import pandas as pd
import json
from pandas.io.json import json_normalize

import os.path
from gensim import corpora
from gensim.models import LsiModel
from gensim.models import LdaModel
from gensim.summarization import keywords 
from nltk.tokenize import RegexpTokenizer
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer
from gensim.models.coherencemodel import CoherenceModel
import matplotlib.pyplot as plt
import numpy as np
import pyLDAvis
import pyLDAvis.gensim

# Open and parse file 

def preprocess_data(doc_set):
    """
    Input  : document list
    Purpose: preprocess text (tokenize, removing stopwords, and stemming)
    Output : preprocessed text
    """
    # initialize regex tokenizer
    tokenizer = RegexpTokenizer(r'\w+')
    # create English stop words list
    en_stop = set(stopwords.words('english'))
    # Create p_stemmer of class PorterStemmer
    p_stemmer = PorterStemmer()
    # list for tokenized documents in loop
    texts = []
    keys = []
    # loop through document list
    
    for i in doc_set.Content:
        try: 
            #print(i)
            # clean and tokenize document string
            raw = i.lower()
            #print(raw)
            #print(keywords(raw).split("\n"))
            #keys.extend(keywords(raw).split("\n"))
            tokens = tokenizer.tokenize(raw)
            # remove stop words from tokens
            stopped_tokens = [i for i in tokens if not i in en_stop]
            # stem tokens
            stemmed_tokens = [p_stemmer.stem(i) for i in stopped_tokens]
            # add tokens to list
            texts.append(stemmed_tokens)
        except:
            continue
    return texts, keys

# with open('LAK_2019.json') as data_file:    
#     data = json.load(data_file)  
# df = json_normalize(data, 'papers', ['year'], record_prefix='papers_', errors='ignore')
#print(df)



def prepare_corpus(doc_clean):
    """
    Input  : clean document
    Purpose: create term dictionary of our corpus and Converting list of documents (corpus) into Document Term Matrix
    Output : term dictionary and Document Term Matrix
    """
    # Creating the term dictionary of our courpus, where every unique term is assigned an index. dictionary = corpora.Dictionary(doc_clean)
    dictionary = corpora.Dictionary(doc_clean)
    # Converting list of documents (corpus) into Document Term Matrix using dictionary prepared above.
    doc_term_matrix = [dictionary.doc2bow(doc) for doc in doc_clean]
    # generate LDA model
    return dictionary,doc_term_matrix

def create_gensim_lsa_model(doc_clean,number_of_topics,words):
    """
    Input  : clean document, number of topics and number of words associated with each topic
    Purpose: create LSA model using gensim
    Output : return LSA model
    """
    dictionary,doc_term_matrix=prepare_corpus(doc_clean)
    # generate LSA model
    lsamodel = LsiModel(doc_term_matrix, num_topics=number_of_topics, id2word = dictionary)  # train model
    print(lsamodel.print_topics(num_topics=number_of_topics, num_words=words))
    return lsamodel

def create_gensim_lda_model(doc_clean,number_of_topics):
    """
    Input  : clean document, number of topics and number of words associated with each topic
    Purpose: create LSA model using gensim
    Output : return LSA model
    """
    dictionary,doc_term_matrix=prepare_corpus(doc_clean)
    # generate LDA model
    ldamodel = LdaModel(doc_term_matrix, num_topics=number_of_topics, id2word = dictionary, alpha="auto", eval_every=5)  # train model
    #print(ldamodel.print_topics(num_topics=number_of_topics, num_words=words))
    #ldamodel.print_topics(-1)
    for i in range(0, ldamodel.num_topics-1):
        print(ldamodel.print_topic(i))
    return ldamodel, dictionary, doc_term_matrix

def compute_coherence_values(dictionary, doc_term_matrix, doc_clean, stop, start=2, step=3):
    """
    Input   : dictionary : Gensim dictionary
              corpus : Gensim corpus
              texts : List of input texts
              stop : Max num of topics
    purpose : Compute c_v coherence for various number of topics
    Output  : model_list : List of LSA topic models
              coherence_values : Coherence values corresponding to the LDA model with respective number of topics
    """
    coherence_values = []
    model_list = []
    for num_topics in range(start, stop, step):
        # generate LSA model
        model = LsiModel(doc_term_matrix, num_topics=num_topics, id2word = dictionary)  # train model
        model_list.append(model)
        coherencemodel = CoherenceModel(model=model, texts=doc_clean, dictionary=dictionary, coherence='c_v')
        coherence_values.append(coherencemodel.get_coherence())
    return model_list, coherence_values

def plot_graph(doc_clean,start, stop, step):
    dictionary,doc_term_matrix=prepare_corpus(doc_clean)
    model_list, coherence_values = compute_coherence_values(dictionary, doc_term_matrix, doc_clean,
                                                            stop, start, step)
    # Show graph
    x = range(start, stop, step)
    plt.plot(x, coherence_values)
    plt.xlabel("Number of Topics")
    plt.ylabel("Coherence score")
    plt.legend(("coherence_values"), loc='best')
    plt.savefig("full_lak_coherence_values.png")

    return np.argmax(coherence_values) + 1



df = pd.read_csv("lakPaperData.csv")
corpus, keywords = preprocess_data(df)
print(len(corpus))
#print(corpus)

start,stop,step=2,12,1
maximum = plot_graph(corpus,start,stop,step)
print(maximum)

# LSI Model
print("LSI Model")
number_of_topics = maximum
words=15
#document_list,titles=load_data("","articles.txt")
#clean_text=preprocess_data(document_list)
model=create_gensim_lsa_model(corpus, number_of_topics, words)

# LDA Model
print("\n LDA Model")
number_of_topics = maximum
words=15
#document_list,titles=load_data("","articles.txt")
#clean_text=preprocess_data(document_list)
lda_model, dictionary, corpus_out =create_gensim_lda_model(corpus, number_of_topics)

#print(keywords)
vis_file = open("full_lak_lda_vis.html", "w")
vis = pyLDAvis.gensim.prepare(lda_model, corpus_out, dictionary)
#pyLDAvis.display(vis)
pyLDAvis.save_html(vis, vis_file)