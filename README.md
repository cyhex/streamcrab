SMM
==========

SMM is a real-time, multi-lingual twitter sentiment analyzer. Based on Naive Bayes classifier as demonstrated on http://smm.streamcrab.com


### Origins

This project is based on several researches including my own in the field of Opinion Mining and Text Analysis

### Usage

Install python 2.6

Install NLTK

Install all NLTK Corpora ( needed langid, Porter Stemmer, wordnet, stopwords )

Start the classification daemon:

	cd {smm}/tracker
	python moodClassifierd.py debug

Wait few minutes till you see:

	starting debug mode...
	OK

In another terminal, run connection test:

	cd {smm}/tracker/tests
	python moodClientServerTest.py

If all is good you should see:

	[{'text': u'this is some text', 'x_mood': 0.0, 'x_lang': 'en'}]


### Classification daemon
By default, the classification daemon (moodClassifierd.py) listens on all IPs on port 6666.

Classification daemon can be started in following modes:

	# start and detach from terminal
	moodClassifierd.py start

	# stop detached daemon
	moodClassifierd.py stop

	# start in debug mode (prints log to stdout)
	moodClassifierd.py debug


### Classification daemon client

	lib/moodClassifierClient.py

is a TCP client for Classification daemon, for more info and usage look at the source code in:

	lib/moodClassifierClient.py
	tests/moodClientServerTest.py


### Training data
This is perhaps the most important part, as it is responsible for accuracy of the results. SMM comes with a small training dataset and its good mostly for testing the system.

For good results it is important to build a better data set.


### Build Training Dataset

The first part of building the data set is collecting raw data, that can be done using

	python collector/trainer/twitterCollector.py

You need to adjust twitterCollector.py file for your needs.


Second step is to classify the data, that can be done with:

	python collector/trainer/tweetClassifier.py

You need to adjust tweetClassifier.py file for your needs.

### How to build your own dataset
for my test I used smilies to determine the initial user sentiment, then the most non informative features are removed in order to slim down the DB and speedup the overall performance.
However for production systems that most likely wont be good enough.

One way would be to classify the texts by hand using crowd sourcing or something similar.
An alternative would be to search for genre specific texts with classifications (ie. Movies reviews on IMDB; assuming its legal) and compiling a dataset out of it.

It is also worth mentioning that positive dataset should be as close as possible in quantity and quality to the negative dataset for obvious reasons...


### How to test your own datasets

Rule number one:  Please do remember that testing a single tweet/text will not yield anything useful. In fact you would need to use test classes to check your dataset performance. From my experience, tests with around 300k tweets most likely to give a proper overview of your datasets performance.

For general testing a tests/accuracyTest2.py gives a good overview of the system performance. In fact you can also use it to get in-depth analysis of your dataset performance:

		MD.classifier.show_most_informative_features(n=100)


For more info read:

http://nltk.github.com/api/nltk.classify.html#module-nltk.classify.naivebayes

http://nltk.googlecode.com/svn/trunk/doc/howto/classify.html



### Licensing
GPLv3
