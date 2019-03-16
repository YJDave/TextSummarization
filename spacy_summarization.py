# NLP Pkgs
import spacy 
nlp = spacy.load('en')
# Pkgs for Normalizing Text
from spacy.lang.en.stop_words import STOP_WORDS
from string import punctuation
# Import Heapq for Finding the Top N Sentences
from heapq import nlargest
import matplotlib
matplotlib.use('TkAgg')
from matplotlib import pyplot as plt
import mpld3
import numpy as np


def text_summarizer(raw_docx):
    raw_text = raw_docx
    docx = nlp(raw_text)
    stopwords = list(STOP_WORDS)
    # Build Word Frequency # word.text is tokenization in spacy
    word_frequencies = {}  
    for word in docx:  
        if word.text not in stopwords:
            if word.text not in word_frequencies.keys():
                word_frequencies[word.text] = 1
            else:
                word_frequencies[word.text] += 1


    print("word_frequencies\n", word_frequencies)

    # BAR CHART: Display bar charts of different words
    objects = tuple(word_frequencies.keys())
    y_pos = np.arange(len(objects))
    performance = list(word_frequencies.values())

    fig, ax = plt.subplots()
    ax.bar(y_pos, performance, align='center', alpha=0.5, color="r")
    plt.xticks(y_pos, objects, rotation='vertical')
    plt.ylabel('No of occurences')
    plt.title('Words Frequency')
    chart_html1 = mpld3.fig_to_html(fig)
    # mpld3.show()

    # SCATTER CAHRT: Display bar charts of different words
    x = [i for i in range(1, len(objects)+1)]
    y = performance
    labels = list(objects)

    fig2, ax2 = plt.subplots()
    ax2.plot(x, y, 'ro')
    # You can specify a rotation for the tick labels in degrees or with keywords.
    plt.xticks(x, labels, rotation='vertical')
    # Pad margins so that markers don't get clipped by the axes
    plt.margins(0.2)
    # Tweak spacing to prevent clipping of tick-labels
    plt.ylabel('No of occurences')
    plt.title('Words Frequency')
    plt.subplots_adjust(bottom=0.15)
    chart_html2 = mpld3.fig_to_html(fig2)
    # # plt.show()
    # mpld3.show()

    # fig3, ax3 = plt.subplots()
    # objects3 = objects[1:10]
    # y_pos3 = np.arange(len(objects3))
    # performance3 = 
    # ax3.bar(y_pos3, performance3, align='center', alpha=0.5)
    # plt.margins(0.2)
    # plt.ylabel('No of occurences')
    # plt.title('Most Frequent Words')
    # plt.subplots_adjust(bottom=0.15)
    # chart_html3 = mpld3.fig_to_html(fig3)


    maximum_frequncy = max(word_frequencies.values())
    print("maximum_frequncy\n", maximum_frequncy)

    for word in word_frequencies.keys():  
        word_frequencies[word] = (word_frequencies[word]/maximum_frequncy)
    # Sentence Tokens
    sentence_list = [ sentence for sentence in docx.sents ]

    # Sentence Scores
    sentence_scores = {}  
    for sent in sentence_list:  
        for word in sent:
            if word.text.lower() in word_frequencies.keys():
                if len(sent.text.split(' ')) < 30:
                    if sent not in sentence_scores.keys():
                        sentence_scores[sent] = word_frequencies[word.text.lower()]
                    else:
                        sentence_scores[sent] += word_frequencies[word.text.lower()]


    print("sentence_scores\n", sentence_scores)
    summarized_sentences = nlargest(5, sentence_scores, key=sentence_scores.get)
    final_sentences = [ w.text for w in summarized_sentences ]
    summary = ' '.join(final_sentences)
    return summary, [chart_html1, chart_html2]
