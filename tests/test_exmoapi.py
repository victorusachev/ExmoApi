#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for `exmoapi` package."""

import unittest

from exmoapi.core import CoreApi
from exmoapi.public import PublicApi


class TestCoreApi(unittest.TestCase):
    """Tests for `exmoapi.core` module."""

    def setUp(self):
        """Set up test fixtures, if any."""

    def tearDown(self):
        """Tear down test fixtures, if any."""

    def test_nonce(self):
        api = CoreApi()
        nonce_sequence = (api.next_nonce for _ in range(10))
        last = 0
        for nonce in nonce_sequence:
            self.assertTrue(nonce > last)
            last = nonce

    def test_connection(self):
        """Test connection."""
        api = CoreApi()
        ok = api.ping()
        self.assertTrue(ok, True)


class TestExmoapi(unittest.TestCase):
    """Tests for `exmoapi` package."""

    def setUp(self):
        """Set up test fixtures, if any."""
        self.pairs = ('BTC_USD', 'BTC_RUB', 'USD_RUB')
        self.limit = 200
        self.api = PublicApi()

    def tearDown(self):
        """Tear down test fixtures, if any."""

    def test_query_trades(self):
        """Test query `trades`"""
        trades = self.api.trades(self.pairs)

        self.assertIsInstance(trades, dict)
        self.assertTrue(set(trades.keys()), set(self.pairs))

    def test_query_order_book(self):
        """Test query `order_book`"""
        order_book = self.api.order_book(pairs=self.pairs, limit=self.limit)

        self.assertIsInstance(order_book, dict)
        self.assertTrue(set(order_book.keys()), set(self.pairs))
        self.assertTrue(all(map(lambda el: len(el.get('ask')) <= self.limit >= len(el.get('bid')), order_book.values())))

    def test_query_ticker(self):
        """Test query `ticker`"""
        ticker = self.api.ticker()

        self.assertIsInstance(ticker, dict)
        self.assertTrue(set(self.pairs).issubset(set(ticker.keys())))

    def test_query_pair_settings(self):
        """Test query `pair_settings`"""
        pair_settings = self.api.pair_settings()

        self.assertIsInstance(pair_settings, dict)
        self.assertTrue(set(self.pairs).issubset(set(pair_settings.keys())))

    def test_query_currency(self):
        """Test query `currency`"""
        all_currencies = self.api.currency()

        self.assertIsInstance(all_currencies, list)
        self.assertTrue(len(all_currencies) > 0)

        currencies = {currency for pair in self.pairs for currency in pair.split('_')}
        self.assertTrue(currencies.issubset(all_currencies))
