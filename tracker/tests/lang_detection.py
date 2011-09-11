# -*- coding: utf-8 -*-

import unittest
from tracker.lib.supportedLangs import supportedLangs
from tracker.lib.lang_detection import LangDetect
class TestLang(unittest.TestCase):


    def testDetect(self):
        
        texts = [
             (u"The quick brown",'en'),
             (u"Le renard brun rapide saute par-dessus le chien paresseux",'fr'),
             (u"@Ja_Nina HERRLICH :) ich hab nix auf planeten gefunden..deine version klingt absolut logisch :D",'de'),
             (u"En Google somos plenamente conscientes de la confianza que los usuarios depositan ",'es'),
             (u"Noi di Google siamo perfettamente consapevoli della fiducia che riponi in noi e della ",'it'),
             (u'русский язык','ru'),
             (u'','other')
        ]
        
        ld = LangDetect(languages = supportedLangs)
        r1 = []
        r2 = []
        for text,lang in texts:
            res =  ld.detect(text)
            r1.append(res[0])
            r2.append(lang)
        assert r1==r2


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()