Streamcrab
==========

Streamcrab is a quasi-realtime twitter sentiment analyzer

This is the second version of the tool.
Most obvious change - well it is re-written from scratch.

Full changelog and Docs will follow.


Requirements
------------

- python 2.7
- python2.7-dev
- mongodb server

    # debian like systems:
    apt-get install python2.7 python2.7-dev mongodb-server


Installation
------------

    python setup.py develop
    python toolbox/setup-app.py


Configure
---------

copy smm/config.default.py to smm/config.py

    cp smm/config.default.py smm/config.py

Edit smm/config.py according to your needs

    nano smm/config.py



Testing
-------

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


Training and testing corpora
----------------------------


    http://mpqa.cs.pitt.edu/
    http://nlp.stanford.edu/sentiment/index.html
    http://www.cs.uic.edu/~liub/FBS/sentiment-analysis.html#datasets
    http://www.cs.york.ac.uk/semeval-2013/semeval2013.tgz ?

