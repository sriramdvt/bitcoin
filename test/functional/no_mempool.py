#!/usr/bin/env python3
# Copyright (c) 2015-2020 The Bitcoin Core developers
# Distributed under the MIT software license, see the accompanying
# file COPYING or http://www.opensource.org/licenses/mit-license.php.
"""Test a node with the -nomempool option.

- Test that getnetworkhashps RPC works when -nomempool is set
- Test that generatetoaddress RPC does not work when -nomempool is set
- Test that getblocktemplate RPC does not work when -nomempool is set
"""
from decimal import Decimal

from test_framework.test_framework import BitcoinTestFramework
from test_framework.util import (
    assert_raises_rpc_error,
)
from test_framework.blocktools import (
    NORMAL_GBT_REQUEST_PARAMS,
)

class NoMempoolTest (BitcoinTestFramework):
    def set_test_params(self):
        self.num_nodes = 1
        self.setup_clean_chain = True
        self.extra_args = [["-nomempool"]]

    def run_test (self):
        node = self.nodes[0]

        # `getnetworkhashps` does not ensure that a mempool exists, this should not throw an error
        node.getnetworkhashps()

        # The `generatetoaddress` RPC function called by node.generate ensures
        # that a mempool exists, by calling `EnsureMemPool`
        assert_raises_rpc_error(-33, "Mempool disabled or instance not found", node.generate, 101)

        # The `getblocktemplate` RPC function ensures that a mempool exists, by calling `EnsureMemPool`
        assert_raises_rpc_error(-33, "Mempool disabled or instance not found", node.getblocktemplate, NORMAL_GBT_REQUEST_PARAMS)

if __name__ == '__main__':
    NoMempoolTest().main ()
