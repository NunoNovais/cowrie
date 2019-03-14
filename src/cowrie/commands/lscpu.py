# Copyright (c) 2019 Nuno Novais <nuno@noais.me>
# All rights reserved.
# All rights given to Cowrie project

"""
virtual hardware related commands
 - lscpu
"""

from __future__ import absolute_import, division

import getopt

from cowrie.shell.command import HoneyPotCommand

commands = {}


class command_lscpu(HoneyPotCommand):

    def help(self):
        output = (
            'Usage:',
            ' lscpu [options]',
            '',
            'Display information about the CPU architecture.',
            '',
            'Options:',
            ' -a, --all               print both online and offline CPUs (default for -e)',
            ' -b, --online            print online CPUs only (default for -p)',
            ' -c, --offline           print offline CPUs only',
            ' -J, --json              use JSON for default or extended format',
            ' -e, --extended[=<list>] print out an extended readable format',
            ' -p, --parse[=<list>]    print out a parsable format',
            ' -s, --sysroot <dir>     use specified directory as system root',
            ' -x, --hex               print hexadecimal masks rather than lists of CPUs',
            ' -y, --physical          print physical instead of logical IDs',
            '',
            ' -h, --help              display this help',
            ' -V, --version           display version',
            '',
            'Available output columns:',
            '           CPU  logical CPU number',
            '          CORE  logical core number',
            '        SOCKET  logical socket number',
            '          NODE  logical NUMA node number',
            '          BOOK  logical book number',
            '        DRAWER  logical drawer number',
            '         CACHE  shows how caches are shared between CPUs',
            '  POLARIZATION  CPU dispatching mode on virtual hardware',
            '       ADDRESS  physical address of a CPU',
            '    CONFIGURED  shows if the hypervisor has allocated the CPU',
            '        ONLINE  shows if Linux currently makes use of the CPU',
            '        MAXMHZ  shows the maximum MHz of the CPU',
            '        MINMHZ  shows the minimum MHz of the CPU',
            '',
            'For more details see lscpu(1).'
        )
        for l in output:
            self.write(l + '\n')

    def start(self):
        try:
            opts, args = getopt.getopt(self.args, 'abcJepe:p:s:xyhV',
                                       ['all', 'online', 'offline', 'json', 'extended=', 'parse=', 'sysroot', 'hex',
                                        'physical', 'help', 'version'])
        except getopt.GetoptError as err:
            self.write("lscpu: invalid option -- \'{0}\'\n".format(err.opt))
            self.write("Try 'lscpu --help' for more information.\n")
            self.exit()
            return
        # "lscpu: options --all, --online and --offline may only be used with options --extended or --parse."
        only_opts = [x for x, _ in opts]
        if len(opts):
            if set(only_opts).issubset(set(['-h', '--help'])):
                self.help()
                self.exit()
                return
            elif set(only_opts).issubset(set(['-V', '--version'])):
                self.write("lscpu from util-linux 2.32\n")
                self.exit()
                return
            elif set(only_opts).issubset(set(['-a', '--all', '-b', '--online'])) and not set(only_opts).issubset(
                    set(['-e', '--extended', '-p', '--parse'])):
                self.write("lscpu: options --all, --online and --offline " +
                           "may only be used with options --extended or --parse.\n")
                self.exit()
                return
            elif set(only_opts).issubset(set(['-c', '--offline'])):
                if not set(only_opts).issubset(set(['-e', '--extended', '-p', '--parse'])):
                    self.write("lscpu: options --all, --online and --offline " +
                               "may only be used with options --extended or --parse.\n")
                self.exit()
                return

            if set(only_opts).issubset(set(['-J', '--json'])) and not set(only_opts).issubset(
                    set(['-e', '--extended', '-p', '--parse'])):
                cpu = self.protocol.user.server.realm.platform.cpu
                lscpu = '{\n   "lscpu": [\n'
                for i in list(cpu.keys())[:23]:
                    lscpu += '      {{"field" : {0}, "data" : {1}}}\n'.format(i, cpu[i])
                lscpu += '   ]\n}\n'
                self.write(lscpu)
                self.exit()
            else:
                if set(only_opts).issubset(set(['-e', '--extended'])):
                    # TODO
                    pass
                elif set(only_opts).issubset(set(['-p', '--parse'])):
                    self.write("# The following is the parsable format, which can be fed to other\n")
                    self.write("# programs. Each different item in every column has an unique ID\n")
                    self.write("# starting from zero.\n")
                    # TODO
                    pass
        else:
            cpu = self.protocol.user.server.realm.platform.cpu
            for i in list(cpu.keys())[:23]:
                line = '{0: <20} {1}\n'.format("{0}:".format(i), cpu[i])
                self.write(line)
            self.exit()


commands['/usr/bin/lscpu'] = command_lscpu
commands['lscpu'] = command_lscpu
