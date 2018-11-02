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
"""Test draw_graph.py."""

import unittest

from pcapgraph.draw_graph import *
from tests import setup_testenv, DEFAULT_CLI_ARGS


class TestManipulateFrames(unittest.TestCase):
    """Test manipulate_framse"""

    def setUp(self):
        """set directory to project root."""
        setup_testenv()
        self.args = DEFAULT_CLI_ARGS

    def test_draw_graph(self):
        raise NotImplemented

    def test_remove_or_open_files(self):
        raise NotImplemented

    def test_get_graph_vars_from_files(self):
        raise NotImplemented

    def test_generate_graph(self):
        raise NotImplemented

    def test_set_horiz_bar_colors(self):
        raise NotImplemented

    def test_set_xticks(self):
        raise  NotImplemented

    def test_export_graph(self):
        raise NotImplemented

    def test_make_text_not_war(self):
        raise NotImplemented
