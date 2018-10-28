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
"""Test pcap_math.py."""

import unittest
import filecmp
import os

from pcapgraph.pcap_math import PcapMath
from pcapgraph import get_tshark_status


class TestPcapMath(unittest.TestCase):
    """Test pcap_math.py. Expected to be run from project root."""
    def setUp(self):
        """Make sure that tshark is in PATH."""
        # If testing from ./tests, change to root directory (useful in PyCharm)
        if os.getcwd().endswith('tests'):
            os.chdir('..')
        # Add the wireshark folder to PATH for this shell.
        get_tshark_status()
        self.set_obj = PcapMath(['examples/simul1.pcap',
                                 'examples/simul2.pcap',
                                 'examples/simul3.pcap'])

    def test_union_pcap(self):
        """Test union_pcap using the pcaps in examples."""
        self.set_obj.union_pcap()
        self.assertTrue(
            filecmp.cmp('union.pcap', 'examples/set_ops/union.pcap'))
        os.remove('union.pcap')

    def test_intersect_pcap(self):
        """Test union_pcap using the pcaps in examples."""
        # This will generate intersect.pcap in tests/
        self.set_obj.intersect_pcap()
        # The generated file should be the same as examples/union.pcap
        self.assertTrue(
            filecmp.cmp('intersect.pcap', 'examples/set_ops/intersect.pcap'))
        # examples/intersect.pcap is from all 3 simul pcaps, so using
        # 2 of 3 should fail as the generated intersection will be different.
        two_thirds = PcapMath(['examples/simul1.pcap', 'examples/simul2.pcap'])
        two_thirds.intersect_pcap()
        self.assertFalse(
            filecmp.cmp('intersect.pcap', 'examples/set_ops/intersect.pcap'))
        os.remove('intersect.pcap')

    def test_difference_pcap(self):
        """Test the difference_pcap method with multiple pcaps."""
        diff1and3 = PcapMath(['examples/simul1.pcap', 'examples/simul3.pcap'])
        diff_filename = diff1and3.difference_pcap()
        self.assertTrue(
            filecmp.cmp(diff_filename, 'examples/set_ops/'
                        'diff_simul1-simul3.pcap'))
        os.remove('diff_simul1.pcap')

    def test_symmetric_difference(self):
        """Test the symmetric difference method with muliple pcaps."""
        self.set_obj.symmetric_difference_pcap()
        # The generated file should be the same as examples/union.pcap
        self.assertTrue(
            filecmp.cmp('symdiff_simul1.pcap',
                        'examples/set_ops/symdiff_simul1.pcap'))
        self.assertTrue(
            filecmp.cmp('symdiff_simul3.pcap',
                        'examples/set_ops/symdiff_simul3.pcap'))
        os.remove('symdiff_simul1.pcap')
        os.remove('symdiff_simul2.pcap')
        os.remove('symdiff_simul3.pcap')

    def test_get_minmax_common_frames(self):
        """Test get_minmax_common against expected frame outputs"""
        min_frame = '881544abbfdd2477035113440800450000547baf40004001922a0a3' \
                    '01290080808080800ae46628b0001e830ab5b0000000088cd0c0000' \
                    '000000101112131415161718191a1b1c1d1e1f20212223242526272' \
                    '8292a2b2c2d2e2f3031323334353637'
        max_frame = '247703511344881544abbfdd0800452000542bbc00007901e8fd080' \
                    '808080a301290000082a563110001f930ab5b00000000a9e80d0000' \
                    '000000101112131415161718191a1b1c1d1e1f20212223242526272' \
                    '8292a2b2c2d2e2f3031323334353637'
        actual_min_frame, actual_max_frame = \
            self.set_obj.get_minmax_common_frames()
        self.assertEqual(min_frame, actual_min_frame)
        self.assertEqual(max_frame, actual_max_frame)

    def test_bounded_interface_pcap(self):
        """Test the bounded_interface_pcap using pcaps in examples."""
        self.set_obj.bounded_intersect_pcap()
        # All 3 simul time-bound intersections should be the same and also
        # equal to the intersect.pcap. This is due to the traffic being the
        # same and there being no infixed traffic from other sources.
        self.assertTrue(
            filecmp.cmp('bounded_intersect-simul1.pcap',
                        'examples/set_ops/intersect.pcap'))
        self.assertTrue(
            filecmp.cmp('bounded_intersect-simul2.pcap',
                        'examples/set_ops/intersect.pcap'))
        self.assertTrue(
            filecmp.cmp('bounded_intersect-simul3.pcap',
                        'examples/set_ops/intersect.pcap'))
        os.remove('bounded_intersect-simul1.pcap')
        os.remove('bounded_intersect-simul2.pcap')
        os.remove('bounded_intersect-simul3.pcap')
