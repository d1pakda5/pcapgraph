# -*- coding: utf-8 -*-
# Copyright 2018 Ross Jacobs All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""Test manipulate_framebytes"""
import unittest
import os
import filecmp

from pcapgraph.manipulate_framebytes import parse_pcaps, write_file_bytes


class TestParsePackets(unittest.TestCase):
    """Test get_filenames.py.

    Note that one_packet.pcap and one_packet.pcapng have the exact same
    packet but saved separately with wireshark.

    Total file_bytes (lines of 16 bytes):
    b'\xd4\xc3\xb2\xa1\x02\x00\x04\x00\x00\x00\x00\x00\x00\x00\x00\x00'
    b'\x00\x00\x04\x00\x01\x00\x00\x00\xc00\xab[\x00\x00\n\x00'
    b'F\x00\x00\x00F\x00\x00\x00\x88\x15D\xab\xbf\xdd$w'
    b'\x03Q\x13D\x08\x00E\x00\x008\x0b]\x00\x00@\x11'
    b'\xc7\x98\n0\x12\x90\n\x80\x80\x80\xeab\x005\x00$'
    b'\xa4\x92\x9b\x13\x01\x00\x00\x01\x00\x00\x00\x00\x00\x00\x06a'
    b'mazon\x03com\x00\x00\x01\x00\x01\xc00'
    b'\xab[\xff\xff\n\x00b\x00\x00\x00b\x00\x00\x00\x88\x15'
    b'D\xab\xbf\xdd$w\x03Q\x13D\x08\x00E\x00\x00T'
    b'd\xf3@\x00@\x01\xa8\xe6\n0\x12\x90\x08\x08\x08\x08'
    b'\x08\x00\xe3Na"\x00\x01\xc00\xab[\x00\x00\x00\x00'
    b'\x7f.\n\x00\x00\x00\x00\x00\x10\x11\x12\x13\x14\x15\x16\x17'
    b'\x18\x19\x1a\x1b\x1c\x1d\x1e\x1f !"#$%&\''
    b'()*+,-./01234567'
    """

    def setUp(self):
        """Set up vars."""
        # Consists of 2 frames: 1 DNS query and 1 ICMP echo request
        if os.getcwd().endswith('tests'):
            os.chdir('..')
        self.expected_frame_list = [
            b'\x88\x15D\xab\xbf\xdd$w\x03Q\x13D\x08\x00E\x00\x008\x0b]\x00'
            b'\x00@\x11\xc7\x98\n0\x12\x90\n\x80\x80\x80\xeab\x005\x00$\xa4'
            b'\x92\x9b\x13\x01\x00\x00\x01\x00\x00\x00\x00\x00\x00\x06amazon'
            b'\x03com\x00\x00\x01\x00\x01',
            b'\x88\x15D\xab\xbf\xdd$w\x03Q\x13D\x08\x00E\x00\x00Td\xf3@\x00@'
            b'\x01\xa8\xe6\n0\x12\x90\x08\x08\x08\x08\x08\x00\xe3Na"\x00\x01'
            b'\xc00\xab[\x00\x00\x00\x00\x7f.\n\x00\x00\x00\x00\x00\x10\x11'
            b'\x12\x13\x14\x15\x16\x17\x18\x19\x1a\x1b\x1c\x1d\x1e\x1f'
            b' !"#$%&\'()*+,-./01234567'
        ]
        self.expected_timestamp_list = [
            b'\xc00\xab[\x00\x00\n\x00',
            b'\xc00\xab[\xff\xff\n\x00'
        ]

    def test_parse_pcap(self):
        """test parse_pcaps for pcap files."""
        filename = 'tests/files/in_order_packets.pcap'
        frame_list, timestamp_list = parse_pcaps(filename)
        self.assertListEqual(frame_list, self.expected_frame_list)
        self.assertListEqual(timestamp_list, self.expected_timestamp_list)

    def test_parse_pcapng(self):
        """test parse_pcaps for pcapng files."""
        filename = 'tests/files/in_order_packets.pcapng'
        frame_list, timestamp_list = parse_pcaps(filename)
        self.assertListEqual(frame_list, self.expected_frame_list)
        self.assertListEqual(timestamp_list, self.expected_timestamp_list)

    @staticmethod
    def test_write_file_bytes():
        """test write_file_bytes."""
        print(os.getcwd())
        filename = 'tests/files/in_order_packets.pcap'
        frame_list, timestamp_list = parse_pcaps(filename)
        temp_file = 'temp_delete.pcap'
        write_file_bytes(temp_file, frame_list, timestamp_list)
        filecmp.cmp(filename, temp_file)
        os.remove(temp_file)
