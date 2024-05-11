from mininet.topo import Topo
from mininet.net import Mininet
from mininet.cli import CLI
from mininet.log import setLogLevel
import time
import threading
import re
import os

class LinearTopology(Topo):
    def __init__(self):
        Topo.__init__(self)
        switch1 = self.addSwitch('s1')
        switch2 = self.addSwitch('s2')
        host1 = self.addHost('h1')
        host2 = self.addHost('h2')
        self.addLink(host1, switch1)
        self.addLink(switch1, switch2)
        self.addLink(switch2, host2)

def run_iperf_flow(h1, h2_ip, server_port, duration, interval, results_file, bandwidth='10m'):
    result_file = f"/tmp/iperf_flow2_{server_port}.txt"
    h1.popen(f'iperf -c {h2_ip} -p {server_port} -i {interval} -t {duration} -b {bandwidth} -d > {result_file}', shell=True)
    time.sleep(duration + 1)
    with open(result_file, 'r') as f:
        result = f.read()
    os.remove(result_file)
    results_file.write(f"Flow Result:\n{result}\n-----\n")
    match = re.search(r'(\d+\.\d+)-(\d+\.\d+) sec\s+(\d+\.\d+) MBytes\s+(\d+\.\d+) Mbits/sec', result)
    if match:
        duration = float(match.group(2)) - float(match.group(1))
        transferred_data = float(match.group(3))
        bandwidth = float(match.group(4))
        results_file.write(f"Duration: {duration} seconds\n")
        results_file.write(f"Transferred Data: {transferred_data} MBytes\n")
        results_file.write(f"Average Bandwidth: {bandwidth} Mbits/sec\n")
    print(result)

def create_linear_topology():
    topo = LinearTopology()
    net = Mininet(topo)
    net.start()
    num_flows = 2
    with open('five_flows_data', 'a') as results_file:
        flow_configs = [(60, 0, '10m'), (5, 5, '500m')]  # Increased bandwidth for the second flow
        intervals = [0.5]
        num_runs = 3
        for duration, interval in zip([10], intervals):
            for j in range(num_runs):
                servers = [net.get('h2').popen(f'iperf -s -p {5000 + flow_id}') for flow_id in range(num_flows)]
                time.sleep(1)
                h2_ip = net.get('h2').IP()
                threads = []
                for flow_id, (flow_duration, start_delay, bandwidth) in enumerate(flow_configs):
                    thread = threading.Thread(target=run_iperf_flow_with_delay, args=(net.get('h1'), h2_ip, 5000 + flow_id, flow_duration, interval, results_file, start_delay, bandwidth))
                    thread.start()
                    threads.append(thread)
                for thread in threads:
                    thread.join()
                for server in servers:
                    server.terminate()
            results_file.write(f"End of {duration} seconds run\n-----\n")
    CLI(net)
    net.stop()

def run_iperf_flow_with_delay(h1, h2_ip, server_port, duration, interval, results_file, start_delay, bandwidth):
    time.sleep(start_delay)
    run_iperf_flow(h1, h2_ip, server_port, duration, interval, results_file, bandwidth)

if __name__ == '__main__':
    setLogLevel('info')
    create_linear_topology()
