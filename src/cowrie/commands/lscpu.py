# Copyright (c) 2019 Nuno Novais <nuno@noais.me>
# All rights reserved.
# All rights given to Cowrie project

"""
virtual hardware related commands
 - lscpu
"""

from __future__ import absolute_import, division

from cowrie.shell.command import HoneyPotCommand

commands = {}


class command_lscpu(HoneyPotCommand):

    def start(self):
        self.vnd_id = 6  # TODO: Read from config
        self.model_id = 63 # TODO: Read from config

    def get_cpu(self):
        cpu_keys = ["Architecture", "CPU op-mode(s)", "CPU(s)", "On-line CPU(s) list", "Thread(s) per core",
                    "Core(s) per socket", "Socket(s)", "NUMA node(s)", "Vendor ID", "CPU family", "Model", "Model name",
                    "Stepping", "CPU MHz", "BogoMIPS", "Hypervisor vendor", "Virtualization type", "L1d cache",
                    "L1i cache", "L2 cache", "L3 cache", "NUMA node0 CPU(s)", "Flags"]
        cpu_file = 'cpu-{0}-{1}'.format(self.vnd_id,self.model_id)
        cpu_def = self.fs.open(CONFIG.get('honeypot', 'share_path') + '/arch/hwd/' + cpu_file).read()

commands['/usr/bin/lscpu'] = command_lscpu
commands['lscpu'] = command_lscpu
