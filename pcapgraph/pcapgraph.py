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
"""PcapGraph:
    Create bar graphs out of packet captures.

USAGE:
    pcapgraph [-abdeisuvwx23] (<file>)... [--output <format>]...
    pcapgraph (-V | --version)
    pcapgraph (-h | --help)

DESCRIPTION:
    Analyze packet captures with graphs and set operations. Graphs will show
    the temporal overlap of packets. Set operations can help with flow-based
    troubleshooting across multiple interfaces or devices.
    The default behavior for output is a graph (hence the name).

    Official documentation: https://pcapgraph.readthedocs.io/

OPTIONS:
    SET OPERATIONS:
      -b, --bounded-intersection
                            Bounded intersection of packets.
      -d, --difference      First packet capture minus packets in all
                            succeeding packet captures.
      -e, --inverse-bounded
                            Shortcut for applying `-b` to a group of pcaps and
                            then subtracting the intersection from each.
      -s, --symmetric-difference
                            Packets unique to each packet capture.
                            (see Set Operations > symmetric difference).
      -u, --union           All unique packets across all pcaket captures.
                            (see Set Operations > union).
      -i, --intersection    All packets that are shared by all packet captures
                            (see Set Operations > intersection).

    OUTPUT OPTIONS:
      -a, --anonymize       Anonymize packet capture file names with fictional
                            place names and devices.
      -o, --output <format>
                            Output results as a file with format type.
      -w                    Open pcaps in Wireshark after creation.
                            (shortcut for --output pcap --output wireshark)
      -x, --exclude-empty   eXclude generated pcaps from being saved if empty.
      -2, --strip-l2        Remove layer2 bits and encode raw IP packets.
                            Use if pcaps track flows across layer 3 boundaries
                            or L2 frame formats differ between pcaps (e.g. An
                            AP will have Ethernet/Wi-Fi interfaces that encode
                            802.3/802.11 frames).
      -3, --strip-l3        Remove IP header and encode dummy ethernet/IP
                            headers. Use if pcaps track flows across IPv4 NAT.
                            -3 implies -2. This flag is IPv4 only as IPv6
                            should not have NAT.

    MISC OPTIONS:
      -h, --help            Show this screen.
      -v, --verbose         Provide more context to what pcapgraph is doing.
      -V, --version         Show PcapGraph's version.

INPUT:
    *<file>...*

    One or more files or directories. When PcapGraph detects a
    directory, it will go one level deep to find packet captures.
    This program can read all files that can be read by tshark.

    packet capture:
        `pcapng, pcap, cap, dmp, 5vw, TRC0, TRC1,
        enc, trc, fdc, syc, bfr, tr1, snoop`

OUTPUT:
    *[--output <format>]...*

    If no format is specified, a graph is printed to the screen and stdout.
    Image formats are those supported by matplotlib on your system. You can see
    which ones are available by running this in your python interpreter:

      ``matplotlib.pyplot.gcf().canvas.get_supported_filetypes()``

    pcap and pcapng require a set operation for there to be packets to save.
    generate-pcaps creates the pcaps simul1 through 3 used in documentation.
    wireshark opens the pcaps from a set operation in the wireshark GUI.

    image:
        `eps, jpeg, jpg, pdf, pgf, png,
        ps, raw, rgba, svg, svgz, tif, tiff`

    text:
        `txt`

    packet capture:
        `pcap, pcapng, generate-pcaps, wireshark`

EXAMPLE USAGE:
  1. Gut check whether a group of pcaps were taken at the same time::
      ::

        $ pcapgraph file1.pcap file2.pcap file3.pcap

                   ASCII of matplotlib graph
                    ______________________
        file1.pcap  |           MMMMM    |    Let A = 2018 Sep 26, 09:10:52
                    |           MMMMM    |    Let F = 2018 Sep 26, 09:30:36
                    |                    |
        file2.pcap  |             HHHHHH |    A and F are the first and last
                    |             HHHHHH |    frames according to timestamp.
                    |                    |
        file3.pcap  | WWWWW              |    B-E are then equally spaced
                    | WWWWW              |    xticks between A and F.
                    |____________________|
                    A   B   C   D   E   F

      Opens a matplotlib graph to visualize packet captures. Sometimes when
      packet captures are taken on multiple devices, they are started and
      stopped at different times. If troubleshooting requires traffic to be
      the same, then use this tool to quickly determine whether additional
      packet captures are necessary.

  2. Intersection to track traffic across multiple interfaces::
      ::

        $ pcapgraph --intersect --strip-l2 file1.pcap file2.pcap --output pcap

      Imagine that you are troubleshooting inter-vlan issues on a router
      and both ports are configured as access on different vlans.
      If you take a packet capture on each interface, frames coming in one
      port and going out the other will be different because the src/dst MAC
      and VLAN tag will change. Using intersect with strip L2 will remove
      frame headers so that common traffic can be found.

  3. Intersection to find common traffic across a natting firewall::
      ::

         $ pcapgraph --intersect --strip-l3 file1.pcap file2.pcap --output pcap

      Imagine that you are troubleshooting an issue on a natting firewall and
      you are looking at traffic on lan and wan ports. Using strip-l3 with
      intersect will find all common traffic, even though NAT changes various
      values. strip-l3 replaces all l3 fields that would change with generic
      values. Export this traffic as pcap to review in wireshark.

      Note that traffic will look like the following in wireshark:

      ::

        <RAW IP>  10.0.0.1 ->  10.0.0.2  ICMP echo reply    DATA1
        <RAW IP>  10.0.0.1 ->  10.0.0.2  UDP  16298 -> 53   DATA2
        <RAW IP>  10.0.0.1 ->  10.0.0.2  TCP  28274 -> 80   DATA3

  4. Difference between traffic on a switchport and the uplink:
      ::

          $ pcapgraph --difference switch_uplink.pcap switchport3.pcap

      Find all packets in switch_uplink.pcap that are also in switchport3.pcap
      and remove them. This might be helpful if you know that all traffic
      coming out of switchport3 is noise for what you are looking for.
      Difference is generally helpful as another means to filter pcaps.

  5. Union to help diagnose a broadcast storm:
      ::

          $ pcapgraph --union pcap_dir/

      Union, without an output format defaults to a matplotlib graph and
      text to stdout. This text will contain the ASCII hexdump of the 10
      most common packets along with their count. Knowing what the MAC
      (and potentially IP) of the causative packets may be helpful in
      identifying a switching loop.

      Use spanning tree and set a root bridge once you have figured it out.

  6. Find unique traffic in the same timeframe across all pcaps:
      ::

          $ pcapgraph file1.pcap file2.pcap --inverse-bounded -w

      Assume that you are looking at two packet captures: file1.pcap that has
      pings to a remote destination and file2.pcap that should have those
      pings, but doesn't. You know that there will be other traffic on this
      link like TCP, HTTP, etc. Normally, you might find an ip.id of a packet
      early in one packet capture and search for it in the other with
      'ip.id==0xabcd' for example. Then find the latest packet in both using
      the same method and then filter both packet captures by frame number.
      This funciton automates that process.

      Finds all traffic in the bounding intersection that is unique
      to each packet capture and opens all of them in wireshark.

SET OPERATIONS:
    All set operations require packet captures and do the following:

    1. Find all unique packets by their ASCII hexdump value.
    2. Strip L2 and L3 headers if those options are specified
    3. Apply the operation and generate a list of packets.
    4. Reencode the packets in a pcap using text2pcap.

    difference:
        Remove all packets that are present in one pcap from another.

    intersection:
        Find all packets that two pcaps have in common.

    union:
        Find all unique packets found in all provided pcaps.

    symmetric difference:
        Find all packets that are unique to each pcap.

    bounded (time intersection):
        Find the first and last frames in the frame intersection of all pcaps
        according to their timestamp Use these two frames as upper and lower
        limts to return all frames in each pcap that are between these two
        frames. This can help to identify traffic that sholud be in both packet
        captures, but is in only one.

    inverse bounded (time intersection):
        Finds which packets are unique to each packet capture in a given time
        frame and saves each as a packet capture.

SEE ALSO:
    pcapgraph (https://pcapgraph.readthedocs.io):
        Comprehensive documentation for this program.

    wireshark (https://www.wireshark.org/):
        Read packet captures to troubleshoot networks.

    wireshark utils (https://www.wireshark.org/docs/man-pages/):
        CLI utils that contain or enhance wireshark functionality. These were
        used in PcapGraph: editcap, mergecap, reordercap, text2pcap, tshark

    pyshark (https://kiminewt.github.io/pyshark/):
        Python wrapper for tshark.

    scapy (https://scapy.readthedocs.io/en/latest/):
        Python program to manipulate frames.

    matplotlib (https://matplotlib.org/):
        Python package to plot 2D graphs.
"""
import docopt

import pcapgraph.manipulate_frames as mf
import pcapgraph.get_filenames as gf
import pcapgraph.draw_graph as dg
import pcapgraph.pcap_math as pm
from . import get_tshark_status


def run():
    """Main function that contains the major moving parts:

    1. Verify tshark
    2. Get filenames from CLI args
    3. Get a per-pcap frame list to be graphed/exported
           frame dict form: {<file/operation>: {frame: timestamp, ...}, ...}
    4. Draw the graph/export files
    """
    get_tshark_status()
    args = docopt.docopt(__doc__)
    filenames = sorted(gf.parse_cli_args(args))
    options = {
        'strip-l2': args['--strip-l2'],
        'strip-l3': args['--strip-l3'],
        'pcapng': 'pcapng' in args['--output']
    }
    pcap_math = pm.PcapMath(filenames, options)
    all_filenames = pcap_math.parse_set_args(args)
    pcaps_frame_dict = mf.get_pcap_frame_dict(all_filenames)
    if args['-w']:
        args['--output'].extend(['wireshark', 'pcap'])
    dg.draw_graph(pcaps_frame_dict, filenames, args['--output'])


if __name__ == '__main__':
    run()
