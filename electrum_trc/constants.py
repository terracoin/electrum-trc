# -*- coding: utf-8 -*-
#
# Electrum - lightweight Bitcoin client
# Copyright (C) 2018 The Electrum developers
#
# Permission is hereby granted, free of charge, to any person
# obtaining a copy of this software and associated documentation files
# (the "Software"), to deal in the Software without restriction,
# including without limitation the rights to use, copy, modify, merge,
# publish, distribute, sublicense, and/or sell copies of the Software,
# and to permit persons to whom the Software is furnished to do so,
# subject to the following conditions:
#
# The above copyright notice and this permission notice shall be
# included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
# NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS
# BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN
# ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN
# CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import os
import gzip
import json

from .logging import get_logger
from .util import inv_dict


_logger = get_logger(__name__)


def read_json(filename, default):
    path = os.path.join(os.path.dirname(__file__), filename)
    try:
        with open(path, 'r') as f:
            r = json.loads(f.read())
    except:
        r = default
    return r


def read_json_gz(filename, default):
    path = os.path.join(os.path.dirname(__file__), filename)
    try:
        with gzip.open(path, 'rb') as f:
            data = f.read()
            r = json.loads(data.decode('utf-8'))
    except:
        _logger.info(f'file not found: {filename}')
        r = default
    return r


GIT_REPO_URL = "https://github.com/terracoin/electrum-trc"
GIT_REPO_ISSUES_URL = f"{GIT_REPO_URL}/issues"


CHUNK_SIZE = 2016


class AbstractNet:

    @classmethod
    def max_checkpoint(cls) -> int:
        return max(0, len(cls.CHECKPOINTS) * CHUNK_SIZE - 1)


class BitcoinMainnet(AbstractNet):

    TESTNET = False
    WIF_PREFIX = 0x80
    ADDRTYPE_P2PKH = 0
    ADDRTYPE_P2SH = 5
    GENESIS = "00000000804bbc6a621a9dbb564ce469f492e1ccf2d70f8a6b241e26a277afa2"
    DEFAULT_PORTS = {'t': '50001', 's': '50002'}
    DEFAULT_SERVERS = read_json('servers.json', {})
    CHECKPOINTS = read_json_gz('checkpoints.json.gz', [])

    XPRV_HEADERS = {
        'standard':    0x0488ade4,  # xprv
    }
    XPRV_HEADERS_INV = inv_dict(XPRV_HEADERS)
    XPUB_HEADERS = {
        'standard':    0x0488b21e,  # xpub
    }
    XPUB_HEADERS_INV = inv_dict(XPUB_HEADERS)
    #DRKV_HEADER = 0x02fe52f8  # drkv
    #DRKP_HEADER = 0x02fe52cc  # drkp
    BIP44_COIN_TYPE = 83
    DIP3_ACTIVATION_HEIGHT = None

    AUXPOW_CHAIN_ID = 0x0032
    AUXPOW_START_HEIGHT = 833000


class BitcoinTestnet(AbstractNet):

    TESTNET = True
    WIF_PREFIX = 0xef
    ADDRTYPE_P2PKH = 111
    ADDRTYPE_P2SH = 196
    GENESIS = "00000000a48f093611895d7452e456b646d213d238e86dc2c0db7d15fe6c555d"
    DEFAULT_PORTS = {'t': '51001', 's': '51002'}
    DEFAULT_SERVERS = read_json('servers_testnet.json', {})
    CHECKPOINTS = read_json_gz('checkpoints_testnet.json.gz', [])

    XPRV_HEADERS = {
        'standard':    0x04358394,  # tprv
    }
    XPRV_HEADERS_INV = inv_dict(XPRV_HEADERS)
    XPUB_HEADERS = {
        'standard':    0x043587cf,  # tpub
    }
    XPUB_HEADERS_INV = inv_dict(XPUB_HEADERS)
    BIP44_COIN_TYPE = 1
    DIP3_ACTIVATION_HEIGHT = None

    AUXPOW_CHAIN_ID = 0x0001
    AUXPOW_START_HEIGHT = 0


class BitcoinRegtest(BitcoinTestnet):

    GENESIS = "5424a2e7fce169e6b9841d0b543a9c53ba111f3b31921b9fd768baa8ead4a8d2"
    DEFAULT_SERVERS = read_json('servers_regtest.json', {})
    CHECKPOINTS = []


# don't import net directly, import the module instead (so that net is singleton)
net = BitcoinMainnet


def set_mainnet():
    global net
    net = BitcoinMainnet


def set_testnet():
    global net
    net = BitcoinTestnet


def set_regtest():
    global net
    net = BitcoinRegtest
