
Training and testing results
----------------------------

Tested against http://www.cs.york.ac.uk/semeval-2013/semeval2013.tgz  Task2
twitter-test-GOLD-A.csv and twitter-test-GOLD-B.csv (ie Gold-A Gold-B) ca. 4000 tweets per file

Gold-A and Gold-B are only used for testing and are not part of training set.

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


    TrainedClassifier: maxEnt_swn
    Trained from SentiWordNet_3.0.0 corpus
    Sample site ca. 110,000
    --------------------------------
    ID: 52ab58a7638dbf682f166132
    Date: 2013-12-13 18:57:43+00:00
    Cutoff : -0.02
    Classifier : MaxentClassifier
    Tokenizer : StopTwitterProcessor
    Sample_size : NA
    Training data size 1.56 (MB)

    Gold-A: 0.593
    Gold-B: 0.612


    TrainedClassifier: maxent_20000
    -------------------------------
    ID: 52ac628b638dbf56a51be635
    Date: 2013-12-14 13:52:11+00:00
    Cutoff : -0.02
    Classifier : MaxentClassifier
    Tokenizer : StopBigramTwitterProcessor
    Sample_size : 40000
    Training data size 11.13 (MB)

    Gold-A: 0.662
    Gold-B: 0.625


    TrainedClassifier: maxent_100000
    --------------------------------
    ID: 52ac7369638dbf56dc3dc10f
    Date: 2013-12-14 15:04:09+00:00
    Cutoff : -0.02
    Classifier : MaxentClassifier
    Tokenizer : StopBigramTwitterProcessor
    Sample_size : 200000
    Training data size 47.49 (MB)

    Gold-A: 0.620
    Gold-B: 0.639

    TrainedClassifier: maxent_stemm_100000
    --------------------------------------
    ID: 52aeaf62638dbf1336cbfe03
    Date: 2013-12-16 07:44:34+00:00
    Cutoff : -0.02
    Classifier : MaxentClassifier
    Tokenizer : StopStemmTwitterProcessor
    Sample_size : 200000
    Training data size 8.46 (MB)
    Gold-A: 0.712
    Gold-B: 0.785


    TrainedClassifier: maxent_stemm_300000
    --------------------------------------
    ID: 52aec78c638dbf17e4e2c166
    Date: 2013-12-16 09:27:40+00:00
    Cutoff : -0.02
    Classifier : MaxentClassifier
    Tokenizer : StopStemmTwitterProcessor
    Sample_size : 600000
    Training data size 19.29 (MB)
    Gold-A: 0.720
    Gold-B: 0.784

    TrainedClassifier: maxent_stemm_400000
    --------------------------------------
    ID: 52af0286638dbf19d4741616
    Date: 2013-12-16 13:39:18+00:00
    Cutoff : -0.02
    Classifier : MaxentClassifier
    Tokenizer : StopStemmTwitterProcessor
    Sample_size : 800000
    Training data size 23.97 (MB)
    Gold-A: 0.721
    Gold-B: 0.780

    TrainedClassifier: maxent_stemm_500000
    --------------------------------------
    ID: 52af5e35638dbf1d5d25919f
    Date: 2013-12-16 20:10:29+00:00
    Cutoff : -0.02
    Classifier : MaxentClassifier
    Tokenizer : StopStemmTwitterProcessor
    Sample_size : 1000000
    Training data size 28.40 (MB)
    Gold-A: 0.721
    Gold-B: 0.784


Notes:
------

Switching to FreqDist for feature extraction yields structure like {feature: nCount} gives worse results then
{feature : exists } - That is something that i find strange...

