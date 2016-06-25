#!/usr/bin/env python2
__author__ = 'Michael Niewoehner <c0d3z3r0>'
__email__ = 'mniewoeh@stud.hs-offenburg.de'

import smbus, argparse, time


# SMBUS data
# noline
# port 0: 08-02-fd-01-fe-01-fe-88-77	-> 0x02, 0x01, 0x01
# port 1: 08-02-fd-00-ff-01-fe-88-77	-> 0x02, 0x00, 0x01
#
# universal
# port 0: 06-03-fc-01-fe-66-99		    -> 0x03, 0x01
# port 1: 06-03-fc-00-ff-66-99		    -> 0x03, 0x00
#
# bridge
# port 0: 08-02-fd-01-fe-00-ff-88-77	-> 0x02, 0x01, 0x00
# port 1: 08-02-fd-00-ff-00-ff-88-77	-> 0x02, 0x00, 0x00

modes = {'b': [0x02, None, 0x00],
         'n': [0x02, None, 0x01],
         'u': [0x03, None]
         }


def calcChecksums(cmd):
    cmd_cs = []
    for c in cmd:
        cmd_cs.extend([c, 0xff-c])
    l = len(cmd_cs)+2
    l += l << 4
    cmd_cs.extend([l, 0xff-l])
    return cmd_cs


def setMode(mode):
    s = smbus.SMBus(0)

    cmd = modes[mode]
    cmd_0 = list(cmd)
    cmd_1 = list(cmd)
    cmd_0[1] = 0x01
    cmd_1[1] = 0x00

    s.write_block_data(0x24, 0x55, calcChecksums(cmd_0))
    time.sleep(0.1)
    s.write_block_data(0x24, 0x55, calcChecksums(cmd_1))

    s.close()


def main():
    parser = argparse.ArgumentParser(description='rbMode')
    group = parser.add_mutually_exclusive_group()
    group.add_argument('--list', '-l', action='store_true', help='Show modes')
    group.add_argument('mode', nargs='?',
                       help='Modes: n(oline)|b(ridge)|u(niversal)')
    args = parser.parse_args()

    if args.list:
        print("""\
Brigde mode (b):    Connects LAN and WAN port directly
Universal mode (u): Use LAN and WAN as normal network interfaces
Noline mode (n):    Physically disconnect both ports""")
    elif args.mode:
        if modes.has_key(args.mode):
            print("Setting mode to " +
                  {'b': 'bridge', 'n': 'noline', 'u': 'universal'}[args.mode])
            setMode(args.mode)
        else:
            parser.print_help()
    else:
        parser.print_help()


if __name__ == '__main__':
    main()
