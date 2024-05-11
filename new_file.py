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

        # Adding nodes to the topology
        switch1 = self.addSwitch('s1')
        switch2 = self.addSwitch('s2')
        host1 = self.addHost('h1')
        host2 = self.addHost('h2')

        # Adding links between the nodes
        self.addLink(host1, switch1)
        self.addLink(switch1, switch2)
        self.addLink(switch2, host2)

# Rest of the code...

def run_iperf_flow(h1, h2_ip, server_port, duration, interval, results_file, bandwidth):
    # Modify the bandwidth parameter in the iperf command
    h1.popen(f'iperf -c {h2_ip} -p {server_port} -i {interval} -t {duration} -b {bandwidth}m -d > {result_file}', shell=True)

    # Rest of the code...

def create_linear_topology():
    # Creating an instance of the linear topology defined at the start
    topo = LinearTopology()

    # Starting the Mininet network
    net = Mininet(topo)

    # Starting the network
    net.start()

    # Defining the number of parallel flows(this can be changed)
    num_flows = 3

    # Opening results file
    with open('five_flows_data.txt', 'a') as results_file:

        durations = [5, 10]  # durations over which iperf is run
        intervals = [0.5, 0.5]  # intervals at which data is captured for each duration e.g at 0.5Sec for a duration of 10
        num_runs = 1  # number or repetitions for which the iperf is run for each duration
        bandwidths = [8, 2]  # bandwidths for each flow

        for duration, interval, bandwidth in zip(durations, intervals, bandwidths):
            for j in range(num_runs):
                # Starting the iperf servers on host 2 for each flow
                servers = []
                for flow_id in range(num_flows):
                    server_port = 5000 + flow_id
                    server = net.get('h2').popen(f'iperf -s -p {server_port}')
                    servers.append(server)
                    time.sleep(1)

                # Getting the IP address of h2
                h2_ip = net.get('h2').IP()

                # Starting the first flow with 80% of the link bandwidth
                if flow_id == 0:
                    thread = threading.Thread(target=run_iperf_flow, args=(net.get('h1'), h2_ip, server_port, duration, interval, results_file, bandwidth))
                    thread.start()
                    threads.append(thread)

                # Starting the second flow with the remaining 20% of the link bandwidth
                elif flow_id == 1:
                    thread = threading.Thread(target=run_iperf_flow, args=(net.get('h1'), h2_ip, server_port, duration + 5, interval, results_file, bandwidth))
                    thread.start()
                    threads.append(thread)

                # Waiting for the first flow to finish before starting the next iteration
                if flow_id == 0:
                    for thread in threads:
                        thread.join()

                # Stopping the iperf servers
                for server in servers:
                    server.terminate()

            results_file.write(f"End of {duration} seconds run\n")
            results_file.write("-----\n")

    # Opening the Mininet command line interface
    CLI(net)
    # Stopping the network once the CLI is closed
    net.stop()
if __name__ == '__main__':
    setLogLevel('info')
    create_linear_topology()
