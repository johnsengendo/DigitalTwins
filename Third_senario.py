# importing mininet libraries 
from mininet.topo import Topo
from mininet.net import Mininet
from mininet.cli import CLI
from mininet.log import setLogLevel
import time
import threading
import random
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
    h1.popen(f'iperf -c {h2_ip} -p {server_port} -i {interval} -t {duration} -b 10M > {result_file}', shell=True)
    time.sleep(duration + 2)  # Wait for iperf to finish
    
    with open(result_file, 'r') as f:
        result = f.read()
    os.remove(result_file)  # Removing the temporary result file

    results_file.write(f"Flow Result for port {server_port}:\n{result}\n")
    results_file.write("-----\n")
    print(result)  # Print the result to console

def create_linear_topology():
    topo = LinearTopology()
    net = Mininet(topo)
    net.start()

    main_flow_file = open('/tmp/main_flow_results.txt', 'w')  # File to store main flow results

    # Starting continuous main flow
    main_flow_thread = threading.Thread(target=run_iperf_flow, args=(net.get('h1'), net.get('h2').IP(), 5001, 400, 1, main_flow_file))
    main_flow_thread.start()

    # Delay before starting the second short flow
    time.sleep(50)
    second_flow_thread = threading.Thread(target=run_iperf_flow, args=(net.get('h1'), net.get('h2').IP(), 5002, 10, 1, main_flow_file))
    second_flow_thread.start()
    second_flow_thread.join()

    # Start random short flows after the second flow
    for _ in range(5):  # Starting 5 random short flows
        random_duration = random.randint(5, 15)
        random_port = random.randint(5003, 5010)
        random_flow_thread = threading.Thread(target=run_iperf_flow, args=(net.get('h1'), net.get('h2').IP(), random_port, random_duration, 1, main_flow_file))
        random_flow_thread.start()
        time.sleep(random.randint(5, 15))  # Random delay before the next flow

    main_flow_thread.join()  # Wait for the main flow to complete
    main_flow_file.close()

    CLI(net)
    net.stop()

if __name__ == '__main__':
    setLogLevel('info')
    create_linear_topology()
