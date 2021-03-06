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
"""Save file."""

import subprocess as sp
import os


def convert_to_pcaptext(raw_packet, timestamp=''):
    """Convert the raw pcap hex to a form that text2cap can read from stdin.

    hexdump and xxd can do this on unix-like platforms, but not on Windows.

    `tshark -r <file> -T json -x` produces the "in" and text2pcap
    requires the "out" formats as shown below:

    Per Text2pcap documentation:
    "Text2pcap understands a hexdump of the form generated by od -Ax -tx1 -v."

    In format::

      247703511344881544abbfdd0800452000542bbc00007901e8fd080808080a301290000
      082a563110001f930ab5b00000000a9e80d0000000000101112131415161718191a1b1c
      1d1e1f202122232425262728292a2b2c2d2e2f3031323334353637

    Out format::

      0000  24 77 03 51 13 44 88 15 44 ab bf dd 08 00 45 20
      0010  00 54 2b bc 00 00 79 01 e8 fd 08 08 08 08 0a 30
      0020  12 90 00 00 82 a5 63 11 00 01 f9 30 ab 5b 00 00
      0030  00 00 a9 e8 0d 00 00 00 00 00 10 11 12 13 14 15
      0040  16 17 18 19 1a 1b 1c 1d 1e 1f 20 21 22 23 24 25
      0050  26 27 28 29 2a 2b 2c 2d 2e 2f 30 31 32 33 34 35
      0060  36 37

    NOTE: Output format doesn't need an extra \\n between packets. So in the
    above example, the next line could be 0000  00 ... for the next packet.

    Args:
        raw_packet (str): The ASCII hexdump seen above in 'In'
        timestamp (str): An optional packet timestamp that will precede
            the 0000 line of the packet hex.
    Returns:
        formatted_string (str): Packet in ASCII hexdump format like `Out` above
    """
    # init vars
    formatted_string = ''
    hex_chars_per_line = 32
    hex_chars_per_byte = 2
    num_chars = len(raw_packet)

    if timestamp:
        formatted_string += str(timestamp) + '\n'
    # Parse the string into lines and each line into space-delimited bytes.
    for line_sep in range(0, num_chars, hex_chars_per_line):
        raw_line = raw_packet[line_sep:line_sep + hex_chars_per_line]
        line = ''
        for byte_sep in range(0, hex_chars_per_line, hex_chars_per_byte):
            line += raw_line[byte_sep:byte_sep + hex_chars_per_byte] + ' '
        line = line[:-1]  # get rid of trailing space
        line_sep_hex = line_sep // 32 * 10  # Offsets need to be in hex.
        formatted_string += '{:>04d}'.format(line_sep_hex) + '  ' + line + '\n'

    return formatted_string


def reorder_packets(pcap):
    """Union causes packets to be ordered incorrectly, so reorder properly.

    Reorder packets, save to 2nd file. After this is done, replace initial
    file with reordered one. Append temporary file with '_'.

    Args:
        pcap (str): Filename of packet capture. Should end with '_', which
            can be stripped off so that we can reorder to a diff file.
    """
    pcap_filename_parts = os.path.splitext(pcap)
    temp_pcap = pcap_filename_parts[0] + '2' + pcap_filename_parts[1]
    reorder_packets_cmds = ['reordercap', pcap, temp_pcap]
    reorder_sp = sp.Popen(reorder_packets_cmds, stdout=sp.PIPE, stderr=sp.PIPE)
    reorder_sp.communicate()
    reorder_sp.kill()
    os.replace(temp_pcap, pcap)


def save_pcap(pcap_dict, name, options):
    """Save a packet capture given ASCII hexdump using `text2pcap`

    Args:
        pcap_dict (dict): List of pcaps of frames to timestamps. Format:
            {<frame>: <timestamp>, ...}
        name (str): Type of operation and name of savefile
        options (dict): Whether to encode with L2/L3 headers.
    """
    pcap_text = ''
    for frame in pcap_dict:
        frame_timestamp = pcap_dict[frame]
        pcap_text += convert_to_pcaptext(frame, frame_timestamp)
    save_pcap_cmds = ['text2pcap', '-', '-t', '%s.']
    if options['strip-l2'] or options['strip-l3']:
        # 101 is the link-type for raw-ip (IPv4 & IPv6)
        save_pcap_cmds += ['-l', '101']
    if options['pcapng']:  # If output type is pcapng
        save_pcap_cmds += ['-n']
        name += 'ng'
    save_pcap_cmds += [name]
    save_pcap_sp = sp.Popen(
        save_pcap_cmds, stdin=sp.PIPE, stdout=sp.PIPE, stderr=sp.PIPE)
    save_pcap_sp.communicate(input=pcap_text.encode())
    save_pcap_sp.kill()
    reorder_packets(name)
