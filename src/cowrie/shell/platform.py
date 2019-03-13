# Copyright (c) 2019 Nuno Novais <nuno@noais.me>
# All rights reserved.
# All rights given to Cowrie project

from __future__ import absolute_import, division

from cowrie.core.config import CONFIG


class Factory(object):
    def __init__(self):
        self.cpu = self.get_cpu(CONFIG.getint('honeypot', 'cpu_cnd_id', fallback=6),
                                CONFIG.getint('honeypot', 'cpu_model_id', fallback=63))
        self.mem_size = CONFIG.getint('honeypot', 'mem_size', fallback=8192)  # in Mb

        self.set_cpu_size(CONFIG.getint('honeypot', 'cpu_sockets', fallback=1),
                          CONFIG.getint('honeypot', 'cpu_cores', fallback=4),
                          CONFIG.getint('honeypot', 'numa_cpus', fallback=8))
        self.set_cpu_hyper(CONFIG.get('honeypot', 'cpu_hypervisor', fallback="None"))
        self.create_proc_cpuinfo()

    def get_cpu(self, cpu_vnd_id, cpu_model_id):
        cpu = {}
        cpu_keys = ["Architecture", "CPU op-mode(s)", "CPU(s)", "On-line CPU(s) list", "Thread(s) per core",
                    "Core(s) per socket", "Socket(s)", "NUMA node(s)", "Vendor ID", "CPU family", "Model", "Model name",
                    "Stepping", "CPU MHz", "BogoMIPS", "Hypervisor vendor", "Virtualization type", "L1d cache",
                    "L1i cache", "L2 cache", "L3 cache", "NUMA node0 CPU(s)", "Flags", "stepping", "apicid",
                    "initial apicid", "fpu", "fpu_exception", "cpuid level", "wp", "bugs", "clflush size",
                    "cache_alignment", "address sizes", "power management", "microcode"]
        try:
            cpu_file = 'cpu-{0}-{1}'.format(cpu_vnd_id, cpu_model_id)
            with open(CONFIG.get('honeypot', 'share_path') + '/arch/hwd/' + cpu_file) as fp:
                for line in fp:
                    tokens = line.split(':')
                    if tokens[0] in cpu_keys:
                        cpu[tokens[0]] = tokens[1].strip()
            # Fix cpu so we don't break later, even if the info will be incorrect
            for k in cpu_keys:
                if k not in cpu:
                    cpu[k] = ''
        except Exception:
            pass
        finally:
            return cpu

    def set_cpu_size(self, sockets, cores_socket, numa_cpus):
        self.cpu['Socket(s)'] = sockets
        self.cpu['Core(s) per socket'] = cores_socket
        self.cpu['CPU(s)'] = sockets * cores_socket
        self.cpu['On-line CPU(s) list'] = '0-{}'.format((sockets * cores_socket) - 1)
        self.cpu['NUMA node0 CPU(s)'] = '0-{}'.format((min(sockets, numa_cpus) * cores_socket) - 1)

    def set_cpu_hyper(self, hyper):
        hyper_list = ["None", "Xen", "KVM", "Microsoft", "VMware", "IBM", "Linux-VServer", "User-mode Linux",
                      "Innotek GmbH", "Hitachi", "Parallels", "Oracle", "OS/400", "pHyp", "Unisys s-Par",
                      "Windows Subsystem for Linux"]
        if hyper in hyper_list:
            self.cpu['Hypervisor vendor'] = hyper
        else:
            self.cpu['Hypervisor vendor'] = "None"

    def create_proc_cpuinfo(self):
        cpuinfo_vars = {}
        proc_cpuinfo_putput = [["processor", None], ["vendor_id", "Vendor ID"], ["cpu family", "CPU family"],
                               ["model", "Model"], ["model name", "Model name"], ["stepping", "Stepping"],
                               ["microcode", "microcode"], ["cpu MHz", "CPU MHz"], ["cache size", "L3 cache"],
                               ["physical id", None], ["siblings", None], ["core id", None],
                               ["cpu cores", "Core(s) per socket"], ["apicid", None], ["initial apicid", None],
                               ["fpu", "fpu"], ["fpu_exception", "fpu_exception"], ["cpuid level", "cpuid level"],
                               ["wp", "wp"], ["flags", "Flags"], ["bugs", "bugs"], ["bogomips", "BogoMIPS"],
                               ["clflush size", "clflush size"], ["cache_alignment", "cache_alignment"],
                               ["address sizes", "address sizes"], ["power management", "power management"]]

        with open(CONFIG.get('honeypot', 'contents_path') + '/proc/cpuinfo', "w") as fp:
            for cpu in range(int(self.cpu['Socket(s)'])):
                for core in range(int(self.cpu['Core(s) per socket'])):
                    cpuinfo_vars['processor'] = cpu * core + core
                    cpuinfo_vars['physical id'] = cpu
                    cpuinfo_vars['siblings'] = self.cpu['Core(s) per socket']
                    cpuinfo_vars['core id'] = cpuinfo_vars['processor']
                    cpuinfo_vars['apicid'] = cpuinfo_vars['processor']
                    cpuinfo_vars['initial apicid'] = cpuinfo_vars['processor']

                    for k, v in proc_cpuinfo_putput:
                        if v is None:
                            vl = cpuinfo_vars[k]
                        else:
                            vl = self.cpu[v]
                        line = '{0: <16}: {1}\n'.format(k, vl)
                        fp.write(line)
                    fp.write("\n")
