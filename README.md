Streamcrab
==========

Streamcrab is a quasi-realtime twitter sentiment analyzer

This is the second version of the tool, and it is rewritten completely from previous version
(still available in legacy branch)

Features and Changes from previous version
----------------------------------------

- Supports MaxEnt and Bayes classifiers (defaults to MaxEnt)
- Simplified tweets collection (see `Collecting raw Tweets`)
- Simplified trainer (see `Train classifier`)
- Build in HTTP server & Frontend (gevent, gevent-socketio, Flask)
- Unittests tested
- Utilization of multi-core systems
- Scalable (in theory :)


Requirements
------------

- python 2.7
- python2.7-dev
- mongodb server


Debian like systems:

    apt-get install python2.7 python2.7-dev mongodb-server


Checkout
--------
Checkout latest streamcrab branch from github


    git clone git@github.com:cyhex/streamcrab.git ./streamcrab
    cd streamcrab


Configure
---------
copy smm/config.default.py to smm/config.py and edit smm/config.py according to your needs

    cp smm/config.default.py smm/config.py
    nano smm/config.py


Installation & Setup
--------------------
Download and install required libs and data

    python setup.py develop
    python toolbox/setup-app.py



Testing
-------
Run unittests

    python -m unittest discover tests


Collecting raw Tweets
---------------------
The base of data training is an assumption that tweets with happy emoticons :) are positive and tweets
with sad :( emoticons have negative sentiment polarity

Wether this assumption is correct or not is outside the scope of this document.

Collect 2000 'happy' tweets

    python toolbox/collect-tweets.py happy 2000

Collect 2000 'sad' tweets

    python toolbox/collect-tweets.py sad 2000

for more options see

    python toolbox/collect-classifier.py --help


Train classifier
----------------
Create and save new classifier trained from collected tweets

    python toolbox/train-classifier.py maxEntTestCorpus 2000

for more options see

    python toolbox/train-classifier.py --help



Show stats
----------
Show detailed info on collected Tweets and saved classifiers

    python toolbox/show-classifiers.py

Its worth mention that `Training data size` is the size of the trained classifier after it has been
serialized (pickled) whit protocol=1 actual Memory Usage may vary...



Interactive shell
-----------------
You can directly interact with the trained classifier and get verbose output on how the score is calculated
replace `maxEntTestCorpus` with desired classifier name see `Show stats` to display available classifiers

    python toolbox/shell-classifier.py maxEntTestCorpus

You should see:

    exit: ctrl+c

    Loaded maxEntTestCorpus
    Classify:

Type something and hit enter:

    Classify: today is a bad day for this nation

    Classification: negative with 53.29%

    Feature                                          negativ positiv
    ----------------------------------------------------------------
    bad==1 (1)                                         0.074
    today==1 (1)                                       0.027
    day==1 (1)                                         0.008
    bad==1 (1)                                                -0.178
    nation==1 (1)                                              0.139
    today==1 (1)                                              -0.035
    day==1 (1)                                                -0.007
    -----------------------------------------------------------------
    TOTAL:                                             0.109  -0.081
    PROBS:                                             0.533   0.467



for more options see

    python toolbox/shell-classifier.py --help


Training and testing results
----------------------------
Tested against http://www.cs.york.ac.uk/semeval-2013/semeval2013.tgz  Task2
twitter-test-GOLD-A.csv and twitter-test-GOLD-B.csv (ie Gold-A Gold-B) ca. 4000 tweets per file

Test results for different Classifier/Tokenizer:

    TrainedClassifier: maxEnt_20000
    -------------------------------
    ID: 52a5dbe2638dbf2aca991e0e
    Date: 2013-12-09 15:04:02+00:00
    Cutoff : -0.02
    Classifier : MaxentClassifier
    Tokenizer : StopTwitterProcessor
    Sample_size : 40000
    Training data size 1.82 (MB)

    Gold-A: 0.694
    Gold-B: 0.748


    TrainedClassifier: maxEnt_POS_20000
    -----------------------------------
    ID: 52a611ca638dbf34c3168f48
    Date: 2013-12-09 18:54:02+00:00
    Cutoff : -0.02
    Classifier : MaxentClassifier
    Tokenizer : StopPosTwitterProcessor
    Sample_size : 40000
    Training data size 2.69 (MB)

    Gold-A: 0.676
    Gold-B: 0.751


    TrainedClassifier: bayes_20000
    ------------------------------
    ID: 52a61363638dbf35c63ea01e
    Date: 2013-12-09 19:00:51+00:00
    Cutoff : -0.02
    Classifier : NaiveBayesClassifier
    Tokenizer : StopTwitterProcessor
    Sample_size : 40000
    Training data size 10.93 (MB)

    Gold-A: 0.684
    Gold-B: 0.718


    TrainedClassifier: bayes_POS_20000
    ----------------------------------
    ID: 52a6160b638dbf365cea35c3
    Date: 2013-12-09 19:12:11+00:00
    Cutoff : -0.02
    Classifier : NaiveBayesClassifier
    Tokenizer : StopPosTwitterProcessor
    Sample_size : 40000
    Training data size 13.76 (MB)

    Gold-A: 0.681
    Gold-B: 0.714


    TrainedClassifier: maxEnt_100000
    --------------------------------
    ID: 52a71b3e638dbf0a0ec69ea7
    Date: 2013-12-10 13:46:38+00:00
    Cutoff : 0.001
    Classifier : MaxentClassifier
    Tokenizer : StopTwitterProcessor
    Sample_size : 200000
    Training data size 5.84 (MB)

    Gold-A: 0.687
    Gold-B: 0.766




Todo
----

- Test accuracy of BIG datasets (1M Tweets+)
- Test accuracy with ngrams
- Implement queue.full() check in smm.classifier.pool.QueueFeeder
- Implement KeyboardInterrupt, SystemExit in start-server.py


Links, Sources etc
------------------

- http://mpqa.cs.pitt.edu/
- http://nlp.stanford.edu/sentiment/index.html
- http://www.cs.uic.edu/~liub/FBS/sentiment-analysis.html#datasets
- http://www.cs.york.ac.uk/semeval-2013/semeval2013.tgz ?

