# importing mininet libraries 
from mininet.topo import Topo
from mininet.net import Mininet
from mininet.cli import CLI
from mininet.log import setLogLevel
import time
import threading
import random
import re
import os

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

def run_iperf_flow(h1, h2_ip, server_port, duration, interval, results_file):
    result_file = f"/tmp/iperf_flow_{server_port}.txt"
    h1.popen(f'iperf -c {h2_ip} -p {server_port} -i {interval} -t {duration} -b 10m -d > {result_file}', shell=True)
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
        results_file.write(f"Average Bandwidth: {bandwidth} Mbits/sec\n")
        results_file.write(f"Direction: {'uplink'}\n")

    print(result)

def create_linear_topology():
    topo = LinearTopology()
    net = Mininet(topo)
    net.start()

    results_file = open('five_flows_data', 'a')

    # Starting continuous flow
    continuous_flow_thread = threading.Thread(target=run_iperf_flow, args=(net.get('h1'), net.get('h2').IP(), 5001, 800, 1, results_file))
    continuous_flow_thread.start()

    # Introduce delay before starting the second flow
    time.sleep(40)
    # Starting second flow with a specific short duration
    second_flow_thread = threading.Thread(target=run_iperf_flow, args=(net.get('h1'), net.get('h2').IP(), 5002, 10, 1, results_file))
    second_flow_thread.start()
    second_flow_thread.join()  # Ensure this thread completes before starting random flows

    # Starting random flows after some delay
    time.sleep(5)  # Wait for a few seconds after second flow
    for _ in range(3):  # Example: Start 3 random flows
        random_duration = random.randint(5, 15)
        random_interval = random.choice([0.5, 1, 1.5])
        random_port = random.randint(5003, 6000)
        random_flow_thread = threading.Thread(target=run_iperf_flow, args=(net.get('h1'), net.get('h2').IP(), random_port, random_duration, random_interval, results_file))
        random_flow_thread.start()
        time.sleep(random.randint(1, 5))  # Random delay before starting the next flow

    # Wait for the continuous flow to finish
    continuous_flow_thread.join()

    results_file.close()
    CLI(net)
    net.stop()

if __name__ == '__main__':
    setLogLevel('info')
    create_linear_topology()
