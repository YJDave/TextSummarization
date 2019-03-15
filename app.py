from __future__ import unicode_literals
from flask import Flask,render_template,url_for,request

from spacy_summarization import text_summarizer
from gensim.summarization import summarize
from nltk_summarization import nltk_summarizer
import time
import spacy
nlp = spacy.load('en')
app = Flask(__name__)

# Web Scraping Pkg
from bs4 import BeautifulSoup
# from urllib.request import urlopen
from urllib.request import urlopen

# Sumy Pkg
from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.lex_rank import LexRankSummarizer

# Sumy 
def sumy_summary(docx):
	parser = PlaintextParser.from_string(docx,Tokenizer("english"))
	lex_summarizer = LexRankSummarizer()
	summary = lex_summarizer(parser.document,3)
	summary_list = [str(sentence) for sentence in summary]
	result = ' '.join(summary_list)
	return result


# Reading Time
def readingTime(mytext):
	total_words = len([ token.text for token in nlp(mytext)])
	estimatedTime = total_words/200.0
	return estimatedTime

# Fetch Text From Url
def get_text(url):
	page = urlopen(url)
	soup = BeautifulSoup(page)
	fetched_text = ' '.join(map(lambda p:p.text,soup.find_all('p')))
	return fetched_text

@app.route('/')
def index():
	return render_template('index.html')


@app.route('/analyze',methods=['GET','POST'])
def analyze():
	start = time.time()
	if request.method == 'POST':
		rawtext = request.form['rawtext']
		final_reading_time = readingTime(rawtext)
		final_summary, chart_html_array = text_summarizer(rawtext)
		summary_reading_time = readingTime(final_summary)
		end = time.time()
		final_time = end-start
	return render_template('index.html',ctext=rawtext,final_summary=final_summary,
		final_time=final_time,final_reading_time=final_reading_time,summary_reading_time=summary_reading_time,
		chart_html_array=chart_html_array)

@app.route('/analyze_url',methods=['GET','POST'])
def analyze_url():
	start = time.time()
	if request.method == 'POST':
		raw_url = request.form['raw_url']
		rawtext = get_text(raw_url)
		final_reading_time = readingTime(rawtext)
		final_summary, chart_html_array = text_summarizer(rawtext)
		summary_reading_time = readingTime(final_summary)
		end = time.time()
		final_time = end-start
	return render_template('index.html',ctext=rawtext,final_summary=final_summary,final_time=final_time,
		final_reading_time=final_reading_time,summary_reading_time=summary_reading_time,
		chart_html_array=chart_html_array)



@app.route('/compare_summary')
def compare_summary():
	return render_template('compare_summary.html')

@app.route('/comparer',methods=['GET','POST'])
def comparer():
	start = time.time()
	if request.method == 'POST':
		rawtext = request.form['rawtext']
		final_reading_time = readingTime(rawtext)
		final_summary_spacy, charts = text_summarizer(rawtext)
		summary_reading_time = readingTime(final_summary_spacy)
		# Gensim Summarizer
		final_summary_gensim = summarize(rawtext)
		summary_reading_time_gensim = readingTime(final_summary_gensim)
		# NLTK
		final_summary_nltk = nltk_summarizer(rawtext)
		summary_reading_time_nltk = readingTime(final_summary_nltk)
		# Sumy
		final_summary_sumy = sumy_summary(rawtext)
		summary_reading_time_sumy = readingTime(final_summary_sumy) 

		end = time.time()
		final_time = end-start

		import matplotlib
		matplotlib.use('TkAgg')
		from matplotlib import pyplot as plt
		import mpld3

		fig, ax = plt.subplots()
		model_names = ("SPACY", "GENSIM", "NLTK", "SUMY LEXRANK")
		summary_time_cmp = [summary_reading_time, summary_reading_time_gensim,
							summary_reading_time_nltk, summary_reading_time_sumy]
		ax.bar([0,1,2,3], summary_time_cmp, align='center', alpha=0.5)
		plt.xticks([0,1,2,3], model_names, rotation='vertical')
		plt.ylabel('Time in minute')
		plt.title('Time comparision between different models')
		chart_html1 = mpld3.fig_to_html(fig)

	return render_template('compare_summary.html',ctext=rawtext,final_summary_spacy=final_summary_spacy,
		final_summary_gensim=final_summary_gensim,final_summary_nltk=final_summary_nltk,final_time=final_time,
		final_reading_time=final_reading_time,summary_reading_time=summary_reading_time,
		summary_reading_time_gensim=summary_reading_time_gensim,final_summary_sumy=final_summary_sumy,
		summary_reading_time_sumy=summary_reading_time_sumy,summary_reading_time_nltk=summary_reading_time_nltk,
		chart_html_array=[chart_html1])



@app.route('/about')
def about():
	return render_template('index.html')

if __name__ == '__main__':
	app.run(debug=True)