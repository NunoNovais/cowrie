# Copyright (c) 2019 Nuno Novais <nuno@noais.me>
# All rights reserved.
# All rights given to Cowrie project

"""
virtual hardware related commands
 - nproc
"""

from __future__ import absolute_import, division

import getopt

from cowrie.shell.command import HoneyPotCommand

commands = {}


class command_nproc(HoneyPotCommand):

    def help(self):
        output = (
            'Usage: nproc [OPTION]...',
            'Print the number of processing units available to the current process,',
            'which may be less than the number of online processors',
            '',
            '      --all      print the number of installed processors',
            '      --ignore=N  if possible, exclude N processing units',
            '      --help     display this help and exit',
            '      --version  output version information and exit',
            '',
            'GNU coreutils online help: <http://www.gnu.org/software/coreutils/>',
            'Full documentation at: <http://www.gnu.org/software/coreutils/nproc>',
            'or available locally via: info ''(coreutils) nproc invocation'''
        )
        for l in output:
            self.write(l + '\n')

    def version(self):
        output = (
            'nproc (GNU coreutils) 8.28',
            'Copyright (C) 2017 Free Software Foundation, Inc.',
            'License GPLv3+: GNU GPL version 3 or later <http://gnu.org/licenses/gpl.html>.',
            'This is free software: you are free to change and redistribute it.',
            'There is NO WARRANTY, to the extent permitted by law.'
            ''
            'Written by Giuseppe Scrivano.'
        )
        for l in output:
            self.write(l + '\n')

    def start(self):
        try:
            opts, args = getopt.getopt(self.args, '',
                                       ['all', 'ignore=', 'help', 'version'])
        except getopt.GetoptError as err:
            self.write("lscpu: invalid option -- \'{0}\'\n".format(err.opt))
            self.write("Try 'lscpu --help' for more information.\n")
            self.exit()
            return

        ignore = 0
        if len(opts):
            only_opts = [x for x, _ in opts]
            if '--help' in only_opts:
                self.version()
                self.exit()
                return
            elif '--version' in only_opts:
                self.write("lscpu from util-linux 2.32\n")
                self.exit()
                return
            elif '--ignore' in only_opts:
                ignore = dict(opts)['--ignore']
                if not ignore.isdigit():
                    self.write("nproc: invalid number: '{0}'\n".format(ignore))
                    self.exit()

        cpu = self.protocol.user.server.realm.platform.cpu
        nproc = cpu['Socket(s)'] * cpu['Core(s) per socket'] - int(ignore)
        self.write("{0}\n".format(nproc))
        self.exit()


commands['/usr/bin/nproc'] = command_nproc
commands['nproc'] = command_nproc
