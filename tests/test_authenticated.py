#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for `exmoapi.authenticated` package."""

import unittest

import tests.test_public
from exmoapi.core.api import Credential
from exmoapi.authenticated import AuthenticatedApi


class TestAuthenticatedApi(tests.test_public.TestPublicApi):
    """Tests for `exmoapi.authenticated.api` module."""

    def setUp(self):
        """Set up test fixtures, if any."""
        self.pairs = ('BTC_USD', 'BTC_RUB', 'USD_RUB')
        self.limit = 200
        # exmo: testapiuser
        credential = Credential(
            api_key='K-2585e13a2ed7dcf4aaf869e40a7a6507eda3cd2e',
            api_secret='S-e5ab0dd485c7b9c92ba8d4111bedc400138b443e')
        self.api = AuthenticatedApi(credential.key, credential.secret)

    def tearDown(self):
        """Tear down test fixtures, if any."""

    def test_query_user_info(self):
        """Test query `order_book`."""
        ui = self.api.user_info()
        self.assertIsInstance(ui.get('balances'), dict)

    def test_query_order_create(self):
        """Test query `order_create`."""
        pair = 'USD_RUB'
        quantity = 1.0
        price = 57.0
        typ = 'buy'
        try:
            self.api.order_create(pair, quantity, price, typ)
        except Exception as e:
            self.assertEqual(str(e), 'Error 50054: Insufficient funds')

    def test_query_order_cancel(self):
        """Test query `order_cancel`."""
        order_id = 0
        try:
            self.api.order_cancel(order_id)
        except Exception as e:
            self.assertEqual(str(e), f"Error 50173: Order was not found '#{order_id}'")

    def test_query_user_open_orders(self):
        """Test query `user_open_orders`."""
        orders = self.api.user_open_orders()
        self.assertEqual(orders, {})

    def test_query_user_trades(self):
        """Test query `user_trades`."""
        pair = 'BTC_USD'
        trades = self.api.user_trades(pair=pair)
        self.assertEqual(trades.get(pair), [])

    def test_query_user_cancelled_orders(self):
        """Test query `user_cancelled_orders`."""
        orders = self.api.user_cancelled_orders()
        self.assertIsInstance(orders, dict)
        self.assertEqual(orders, {})

    def test_query_order_trades(self):
        """Test query `order_trades`."""
        order_id = 0
        try:
            self.api.order_trades(order_id)
        except Exception as e:
            self.assertEqual(str(e), f"Error 50304: Order was not found '{order_id}'")

    def test_query_required_amount(self):
        """Test query `required_amount`."""
        pair = 'BTC_USD'
        quantity = 1.0
        amount = self.api.required_amount(pair, quantity)
        self.assertGreater(amount.get('avg_price'), 0.0)

    def test_query_deposit_address(self):
        """Test query `deposit_address`."""
        addresses = self.api.deposit_address()
        self.assertIsInstance(addresses, dict)

    def test_query_withdraw_crypt(self):
        """Test query `withdraw_crypt`."""
        amount = 0.0
        currency = 'BTC'
        address = '1Jvu3g8DAe69jT2yQb9vfEvchvFJuQdABj'
        try:
            withdraw = self.api.withdraw_crypt(amount, currency, address)
            self.assertIn('result', withdraw.keys())
        except Exception as e:
            self.assertEqual(str(e), "Error 10519: API method is not allowed")

    def test_query_withdraw_get_txid(self):
        """Test query `withdraw_get_txid`."""
        task_id = 0
        try:
            self.api.withdraw_get_txid(task_id)
        except Exception as e:
            self.assertEqual(str(e), f"Error 10193: Withdrawal task not found {task_id}")
