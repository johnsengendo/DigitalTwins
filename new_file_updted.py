import os
import re
import time
import threading
from mininet.topo import Topo
from mininet.net import Mininet
from mininet.cli import CLI
from mininet.log import setLogLevel

class LinearTopology(Topo):
    def __init__(self):
        Topo.__init__(self)
        # Adding nodes to the topology
        switch1 = self.addSwitch('s1')
        switch2 = self.addSwitch('s2')
        host1 = self.addHost('h1')
        host2 = self.addHost('h2')

        # Adding links between the nodes
        self.addLink(host1, switch1)
        self.addLink(switch1, switch2)
        self.addLink(switch2, host2)

def run_iperf_flow(h1, h2_ip, server_port, duration, interval, results_file, bandwidth="10m"):
    result_file = f"/tmp/iperf_flow_{server_port}.txt"
    h1.popen(f'iperf -c {h2_ip} -p {server_port} -i {interval} -t {duration} -b {bandwidth} > {result_file}', shell=True)
    time.sleep(duration + 1)  # Waiting for the iperf process to finish

    with open(result_file, 'r') as f:
        result = f.read()

    os.remove(result_file)  # Removing the temporary result file

    results_file.write(f"Flow Result:\n{result}\n")
    results_file.write("-----\n")

    match = re.search(r'(\d+\.\d+)-(\d+\.\d+) sec\s+(\d+\.\d+) MBytes\s+(\d+\.\d+) Mbits/sec', result)
    if match:
        start_time = float(match.group(1))
        end_time = float(match.group(2))
        duration = end_time - start_time
        transferred_data = float(match.group(3))
        bandwidth = float(match.group(4))

        results_file.write(f"Duration: {duration} seconds\n")
        results_file.write(f"Transferred Data: {transferred_data} MBytes\n")
        results_file.write(f"Bandwidth: {bandwidth} Mbits/sec\n")

def create_linear_topology():
    topo = LinearTopology()
    net = Mininet(topo=topo)
    net.start()

    num_flows = 5

    with open('five_flows_data_updated', 'a') as results_file:
        durations = [10]
        intervals = [0.5]
        num_runs = 3

        for duration, interval in zip(durations, intervals):
            for j in range(num_runs):
                # Starting the iperf servers on host 2 for each flow
                servers = []
                for flow_id in range(num_flows):
                    server_port = 5000 + flow_id
                    server = net.get('h2').popen(f'iperf -s -p {server_port}')
                    servers.append(server)
                    time.sleep(1)

                h2_ip = net.get('h2').IP()

                # Creating and starting threads for running iperf flows in parallel
                threads = []
                for flow_id in range(num_flows):
                    server_port = 5000 + flow_id
                    bandwidth = "1m" if flow_id < 4 else "10m"  # Four flows with zero bandwidth
                    thread = threading.Thread(target=run_iperf_flow, args=(net.get('h1'), h2_ip, server_port, duration, interval, results_file, bandwidth))
                    thread.start()
                    threads.append(thread)

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
