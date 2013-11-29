from unittest import TestCase
from smm.classifier.textprocessing import TwitterMixin

__author__ = 'gx'


class TestTwitterMixin(TestCase):

    def test_remove_usernames(self):
        text = "hello @username xxx"
        result = TwitterMixin.remove_usernames(text).split()
        expect = "hello xxx".split()
        self.assertEqual(expect, result)

    def test_remove_hashtags(self):
        text = "hello #hashtag xxx"
        result = TwitterMixin.remove_hashtags(text).split()
        expect = "hello xxx".split()
        self.assertEqual(expect, result)

    def test_remove_urls(self):
        text = "hello http://cyhex.com xxx"
        result = TwitterMixin.remove_urls(text).split()
        expect = "hello xxx".split()
        self.assertEqual(expect, result)


    def test_remove_numbers(self):
        text = "hello 12456 xxx"
        result = TwitterMixin.remove_numbers(text).split()
        expect = "hello xxx".split()
        self.assertEqual(expect, result)

    def test_char_fold(self):
        text = "hello loooooooool"
        result = TwitterMixin.char_fold(text).split()
        expect = "hello lool".split()
        self.assertEqual(expect, result)

    def test_word_map(self):
        text = "hello :) :( not xxx"
        result = TwitterMixin.word_map(text).split()
        expect = "hello __h__ __s__ __not__ xxx".split()
        self.assertEqual(expect, result)