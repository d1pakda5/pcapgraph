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
"""Test get_filenames.py."""

import unittest

import pcapgraph.get_filenames as gf
from tests import setup_testenv, DEFAULT_CLI_ARGS


class TestGetFilenames(unittest.TestCase):
    """Test get_filenames.py."""
    setup_testenv()
    args = DEFAULT_CLI_ARGS

    def test_parse_cli_args(self):
        """Test parse_cli_args,get_filenames_from_directories,get_filenames"""
        self.args['--version'] = True
        # Version should exit.
        with self.assertRaises(SystemExit):
            gf.parse_cli_args(self.args)
        self.args['--version'] = False

        # Not testing generating_pcaps as it could fail depending on whether
        # the default interface is the one that traffic is going through.

        # directory and file should be properly detected as such and parsed.
        self.args['<file>'] = ['tests/files/test.pcap', 'tests/files/test_dir']
        expected_results = [
            'tests/files/test_dir/test_dir.pcap', 'tests/files/test.pcap'
        ]
        self.assertEqual(expected_results, gf.parse_cli_args(self.args))

    def test_get_filenames_from_directories(self):
        raise NotImplemented

    def test_get_filenames(self):
        raise NotImplemented
