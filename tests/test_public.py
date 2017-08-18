#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for `exmoapi.public` package."""

import unittest

from exmoapi.public import PublicApi


class TestPublicApi(unittest.TestCase):
    """Tests for `exmoapi.public.api` module."""
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
        self.assertTrue(all(map(lambda el: len(el.get('ask')) <= self.limit >= len(el.get('bid')),
                                order_book.values())))

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
