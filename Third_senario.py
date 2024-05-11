from mininet.topo import Topo
from mininet.net import Mininet
from mininet.cli import CLI
from mininet.log import setLogLevel
import time
import threading
import re

class LinearTopology(Topo):
    def __init__(self):
        super().__init__()
        switch1 = self.addSwitch('s1')
        switch2 = self.addSwitch('s2')
        host1 = self.addHost('h1')
        host2 = self.addHost('h2')

        self.addLink(host1, switch1)
        self.addLink(switch1, switch2)
        self.addLink(switch2, host2)

def run_iperf_flow(h1, h2_ip, server_port, duration, interval, results_file):
    cmd = f'iperf -c {h2_ip} -p {server_port} -i {interval} -t {duration} -b 10m -d'
    result = h1.cmd(cmd)
    results_file.write(f"Flow Result for port {server_port}:\n{result}\n")
    results_file.write("-----\n")

def burst_signal(h1, h2_ip, server_port, burst_duration, burst_bandwidth):
    cmd = f'iperf -c {h2_ip} -p {server_port} -t {burst_duration} -b {burst_bandwidth}'
    h1.cmd(cmd)

def create_linear_topology():
    topo = LinearTopology()
    net = Mininet(topo)
    net.start()

    num_flows = 1
    durations = [10]
    intervals = [0.5]

    with open('iperf_results.txt', 'w') as results_file:
        h2 = net.get('h2')
        h2_ip = h2.IP()

        for duration, interval in zip(durations, intervals):
            servers = [h2.popen(f'iperf -s -p {5000 + i}') for i in range(num_flows)]
            time.sleep(1)

            threads = [threading.Thread(target=run_iperf_flow, args=(net.get('h1'), h2_ip, 5000 + i, duration, interval, results_file)) for i in range(num_flows)]
            burst_thread = threading.Thread(target=burst_signal, args=(net.get('h1'), h2_ip, 5100, 5, '100m'))

            for thread in threads:
                thread.start()
            time.sleep(5)  # Wait for 5 seconds before starting the burst signal
            burst_thread.start()
            burst_thread.join()

            for thread in threads:
                thread.join()

            for server in servers:
                server.terminate()
            results_file.write(f"End of {duration} seconds run\n")
            results_file.write("-----\n")

    CLI(net)
    net.stop()

if __name__ == '__main__':
    setLogLevel('info')
    create_linear_topology()
