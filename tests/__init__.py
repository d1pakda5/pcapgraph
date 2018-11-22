#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""Shared vars/functions for test classes."""

import os

from pcapgraph import get_tshark_status


def setup_testenv():
    """Set up PATH and current working directory."""
    get_tshark_status()
    # If testing from ./tests, change to root directory (useful in PyCharm)
    if os.getcwd().endswith('tests'):
        os.chdir('..')


DEFAULT_CLI_ARGS = {
    '--anonymize': False,
    '--bounded-intersection': False,
    '--difference': False,
    '--exclude-empty': False,
    '--help': False,
    '--intersection': False,
    '--inverse-bounded': False,
    '--most-common-frames': False,
    '--output': [],
    '--show-packets': False,
    '--strip-l2': False,
    '--strip-l3': False,
    '--symmetric-difference': False,
    '--union': False,
    '--verbose': False,
    '--version': False,
    '-w': False,
    '<file>': [],
}

EXPECTED_UNION_STDOUT = """Count: 3
Frame hex: 881544abbfdd2477035113440800450000547baf40004001922a0a301290080808080800ae46628b0001e830ab5b0000000088cd0c0000000000101112131415161718191a1b1c1d1e1f202122232425262728292a2b2c2d2e2f3031323334353637
    1   0.000000 10.48.18.144 → 8.8.8.8      ICMP 98 Echo (ping) request  id=0x628b, seq=1/256, ttl=64

Count: 3
Frame hex: 881544abbfdd247703511344080045000038204000004011b2b50a3012900a808080badc00350024cb35a3f60100000100000000000006616d617a6f6e03636f6d0000010001
    1   0.000000 10.48.18.144 → 10.128.128.128 DNS 70 Standard query 0xa3f6 A amazon.com

Count: 3
Frame hex: 247703511344881544abbfdd080045000068f7f9400040119acb0a8080800a3012900035badc00541ec2a3f68180000100030000000006616d617a6f6e03636f6d0000010001c00c00010001000000150004b02067cdc00c00010001000000150004cdfbf267c00c00010001000000150004b02062a6
    1   0.000000 10.128.128.128 → 10.48.18.144 DNS 118 Standard query response 0xa3f6 A amazon.com A 176.32.103.205 A 205.251.242.103 A 176.32.98.166

Count: 3
Frame hex: 247703511344881544abbfdd080045200054efc60000790124f3080808080a3012900000b646628b0001e830ab5b0000000088cd0c0000000000101112131415161718191a1b1c1d1e1f202122232425262728292a2b2c2d2e2f3031323334353637
    1   0.000000      8.8.8.8 → 10.48.18.144 ICMP 98 Echo (ping) reply    id=0x628b, seq=1/256, ttl=121

Count: 3
Frame hex: 881544abbfdd2477035113440800450000547bfa4000400191df0a301290080808080800742962930001e930ab5b00000000c1e20c0000000000101112131415161718191a1b1c1d1e1f202122232425262728292a2b2c2d2e2f3031323334353637
    1   0.000000 10.48.18.144 → 8.8.8.8      ICMP 98 Echo (ping) request  id=0x6293, seq=1/256, ttl=64

Count: 3
Frame hex: 881544abbfdd247703511344080045000038208b00004011b26a0a3012900a808080eaea003500246994d5890100000100000000000006616d617a6f6e03636f6d0000010001
    1   0.000000 10.48.18.144 → 10.128.128.128 DNS 70 Standard query 0xd589 A amazon.com

Count: 3
Frame hex: 247703511344881544abbfdd080045000068f7fc400040119ac80a8080800a3012900035eaea0054bd23d5898180000100030000000006616d617a6f6e03636f6d0000010001c00c00010001000000140004b02062a6c00c00010001000000140004b02067cdc00c00010001000000140004cdfbf267
    1   0.000000 10.128.128.128 → 10.48.18.144 DNS 118 Standard query response 0xd589 A amazon.com A 176.32.98.166 A 176.32.103.205 A 205.251.242.103

Count: 3
Frame hex: 247703511344881544abbfdd080045200054f17a00007901233f080808080a30129000007c2962930001e930ab5b00000000c1e20c0000000000101112131415161718191a1b1c1d1e1f202122232425262728292a2b2c2d2e2f3031323334353637
    1   0.000000      8.8.8.8 → 10.48.18.144 ICMP 98 Echo (ping) reply    id=0x6293, seq=1/256, ttl=121

Count: 3
Frame hex: 881544abbfdd2477035113440800450000547c4e40004001918b0a3012900808080808008e09629f0001ea30ab5b00000000a6f60c0000000000101112131415161718191a1b1c1d1e1f202122232425262728292a2b2c2d2e2f3031323334353637
    1   0.000000 10.48.18.144 → 8.8.8.8      ICMP 98 Echo (ping) request  id=0x629f, seq=1/256, ttl=64

To view the content of these packets, subtract the count lines,
add and save to <textfile>, and then run

text2pcap <textfile> out.pcap
wireshark out.pcap

"""

EXPECTED_STRIPPED_PCAP = {
    'tests/files/test.pcap': {
        'frames': [
            '0000  45 20 00 54 2b bc 00 00 ff 01 13 37 0a 01 01 01\n'
            '0010  0a 02 02 02 00 00 82 a5 63 11 00 01 f9 30 ab 5b\n'
            '0020  00 00 00 00 a9 e8 0d 00 00 00 00 00 10 11 12 13\n'
            '0030  14 15 16 17 18 19 1a 1b 1c 1d 1e 1f 20 21 22 23\n'
            '0040  24 25 26 27 28 29 2a 2b 2c 2d 2e 2f 30 31 32 33\n'
            '0050  34 35 36 37            \n'
        ],
        'timestamps': ['1537945792.667334000']
    }
}
