#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for `exmoapi.core` package."""

import unittest

from exmoapi.core import CoreApi


class TestCoreApi(unittest.TestCase):
    """Tests for `exmoapi.core.api` module."""

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
