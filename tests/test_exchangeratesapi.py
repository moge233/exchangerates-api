#!/usr/bin/env python3

'''
tests/test_exchangeratesapi.py

Main testing module for the exchangeratesapi package.

classes:
    TestExchangeRatesIO(unittest.TestCase)

'''

from datetime import date
from http.client import HTTPResponse
from json import loads
from unittest import TestCase

from exchangeratesapi import ExchangeRatesIO


class TestExchangeRatesIO(TestCase):

    def setUp(self):
        self.xchg = ExchangeRatesIO('usd')

    def test_class_type(self):
        self.assertIsInstance(self.xchg, ExchangeRatesIO)

    def test_base_currency_descriptor(self):
        with self.assertRaises(TypeError):
            self.xchg.base_currency = 15
        with self.assertRaises(ValueError):
            self.xchg.base_currency = 'Bad String'

    def test__request(self):
        response = self.xchg._request('http://httpbin.org/get')
        self.assertIsInstance(response, HTTPResponse)
        self.assertEqual(response.status, 200)

    def test__build_url(self):
        test_url = 'https://api.exchangeratesapi.io/latest'
        expected_url = 'https://api.exchangeratesapi.io/latest?base=EUR&foo=bar'
        self.assertEqual(expected_url, self.xchg._build_url(test_url,
                                                        **{'base' : 'EUR',
                                                           'foo' : 'bar'}))

    def test_latest(self):
        response = self.xchg.latest()
        self.assertIsInstance(response, HTTPResponse)
        self.assertEqual(response.status, 200)
        content = response.read()
        self.assertIsInstance(content, bytes)
        content_j = loads(content)
        self.assertEqual('USD', content_j['base'])

    def test_latest_base(self):
        response = self.xchg.latest(base='EUR')
        self.assertIsInstance(response, HTTPResponse)
        self.assertEqual(response.status, 200)
        content = response.read()
        self.assertIsInstance(content, bytes)
        content_j = loads(content)
        self.assertEqual('EUR', content_j['base'])

    def test_latest_json(self):
        response = self.xchg.latest(parse_json=True)
        self.assertIsInstance(response, dict)
        self.assertIn('base', response.keys())
        self.assertIn('date', response.keys())
        self.assertIn('rates', response.keys())
        self.assertEqual(self.xchg.base_currency, response['base'])

    def test_latest_symbols(self):
        response = self.xchg.latest(symbols=('JPY', 'EUR'))
        self.assertIsInstance(response, HTTPResponse)
        self.assertEqual(response.status, 200)
        content = response.read()
        self.assertIsInstance(content, bytes)

        with self.assertRaises(TypeError):
            response = self.xchg.historical(date(2012, 9, 12),
                                            symbols=['USD', 'GBP'])

    def test_historical(self):
        response = self.xchg.historical(date(2012, 9, 12))
        self.assertIsInstance(response, HTTPResponse)
        self.assertEqual(response.status, 200)
        content = response.read()
        self.assertIsInstance(content, bytes)

        with self.assertRaises(AttributeError):
            response = self.xchg.historical('2012-09-12')

    def test_historical_base(self):
        response = self.xchg.historical(date(2012, 9, 12), base='EUR')
        self.assertIsInstance(response, HTTPResponse)
        self.assertEqual(response.status, 200)
        content = response.read()
        self.assertIsInstance(content, bytes)

    def test_historical_json(self):
        response = self.xchg.historical(date(2012, 9, 12), parse_json=True)
        self.assertIsInstance(response, dict)
        self.assertIn('base', response.keys())
        self.assertIn('date', response.keys())
        self.assertIn('rates', response.keys())
        self.assertEqual(self.xchg.base_currency, response['base'])

    def test_historical_range(self):
        response = self.xchg.historical(date(2012, 9, 12),
                                        end=date(2012, 9, 20))
        self.assertIsInstance(response, HTTPResponse)
        self.assertEqual(response.status, 200)
        content = response.read()
        self.assertIsInstance(content, bytes)
        content_j = loads(content)
        self.assertEqual(self.xchg.base_currency, content_j['base'])

        with self.assertRaises(AttributeError):
            response = self.xchg.historical(date(2012, 9, 20),
                                            end='2012-09-23')

    def test_historical_range_json(self):
        response = self.xchg.historical(date(2012, 9, 12),
                                        end=date(2012, 9, 20),
                                        parse_json=True)
        self.assertIsInstance(response, dict)
        self.assertIn('base', response.keys())
        self.assertIn('start_at', response.keys())
        self.assertIn('end_at', response.keys())
        self.assertIn('rates', response.keys())

    def test_historical_symbols(self):
        response = self.xchg.historical(date(2012, 9, 12),
                                        symbols=('USD', 'GBP'))
        self.assertIsInstance(response, HTTPResponse)
        self.assertEqual(response.status, 200)
        content = response.read()
        self.assertIsInstance(content, bytes)

        with self.assertRaises(TypeError):
            response = self.xchg.historical(date(2012, 9, 12),
                                            symbols=['USD', 'GBP'])
