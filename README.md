Streamcrab
==========

Streamcrab is a quasi-realtime twitter sentiment analyzer

This is the second version of the tool, and it is rewritten completely from previous version
(still available in legacy branch)

Changes from previous version
-----------------------------

- Supports MaxEnt and Bayes classifiers (defaults to MaxEnt)
- Simplified tweets collection (see `Collecting raw Tweets`)
- Simplified trainer (see `Train classifier`)
- Build in HTTP Server & frontend based on gevent and Flask
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
see : https://github.com/cyhex/streamcrab/blob/master/docs/acurracy_tests.md


Todo
----

- Test accuracy of BIG datasets (1M Tweets+)
- Test accuracy with ngrams
- Implement queue.full() check in smm.classifier.pool.QueueFeeder


Links, Sources etc
------------------

- http://mpqa.cs.pitt.edu/
- http://nlp.stanford.edu/sentiment/index.html
- http://www.cs.uic.edu/~liub/FBS/sentiment-analysis.html#datasets
- http://www.cs.york.ac.uk/semeval-2013/semeval2013.tgz ?

