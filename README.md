SMM
==========

SMM is a real-time, multi-lingual twitter sentiment analyzer. Based on Naive Bayes classifier as demonstrated on http://smm.streamcrab.com


### Origins

This project is based on several researches including my own in the field of Opinion Mining and Text Analysis

### Usage

Install python 2.6/2.7

Install NLTK 

Install Corpora, I think the only one that you need is the Languages, but I am not sure...


Start the classification daemon:
	
	cd tracker
	python moodClassifierd.py debug

Wait few minutes till you see:

	starting debug mode...
	OK

Run connection test:

	python tests/moodClientServerTest.py

If all is good you should see:

	[{'text': u'this is some text', 'x_mood': 0.0, 'x_lang': 'en'}]


### Classification daemon
By default classification daemon (moodClassifierd.py) listens on all IPs on port 6666.

Classification daemon can be started in following modes:

	# start and detach from terminal
	moodClassifierd.py start
	
	# stop detached daemon
	moodClassifierd.py stop

	# start in debug mode (prints log to stdout)
	moodClassifierd.py debug
	

### Classification daemon client

	lib/moodClassifierClient.py

Is a TCP client for Classification daemon, for more info and usage look at the source code in:

	lib/moodClassifierClient.py
	tests/moodClientServerTest.py


### Training data
It perhaps the most important part, as it is responsible for accuracy of the results. SMM comes with a small training dataset and its good mostly for testing the system.

For good results it is impotent to build a better data set.


### Build Training Dataset

The first part of building the data set is collecting raw data, that can be done using

	python collector/trainer/twitterCollector.py 

You need to adjust twitterCollector.py file for your needs.


Second step is to classify the data, that can be done with:

	python collector/trainer/tweetClassifier.py

You need to adjust tweetClassifier.py file for your needs.

### Licensing
GPLv3
	