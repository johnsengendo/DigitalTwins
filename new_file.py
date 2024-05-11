from mininet.topo import Topo
from mininet.net import Mininet
from mininet.cli import CLI
from mininet.log import setLogLevel
from mininet.link import TCLink
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

        # Adding links between the nodes with packet loss
        self.addLink(host1, switch1, cls=TCLink, loss=5)  # 5% packet loss
        self.addLink(switch1, switch2, cls=TCLink, loss=5)  # Additional link between switches also with packet loss
        self.addLink(switch2, host2, cls=TCLink, loss=5)

# Function to run iperf remains largely the same, we can modify it later if needed

def create_linear_topology():
    topo = LinearTopology()

    # Starting the Mininet network with link TCLink for packet loss simulation
    net = Mininet(topo, link=TCLink)

    # Starting the network
    net.start()

    # Defining the number of parallel flows
    num_flows = 5  # Changed from 1 to 5

    # Opening a file in append mode to write the results
    with open('Increase_in_BW', 'a') as results_file:
        durations = [10]  # Durations over which iperf is run
        intervals = [0.5]  # Intervals at which data is captured for each duration
        num_steps = 150  # Number of steps (after each step, the bandwidth is increased by a factor of 10)

        for duration, interval in zip(durations, intervals):
            for step in range(1, num_steps + 1):
                # Starting the iperf servers on host2 
                servers = []
                for flow_id in range(num_flows):
                    server_port = 5000 + flow_id
                    server = net.get('h2').popen(f'iperf -s -p {server_port}')
                    servers.append(server)
                    time.sleep(1)

                # Getting the IP address of h2
                h2_ip = net.get('h2').IP()

                # Calculating dynamic bandwidth for this step
                bandwidth = step * 10  # Increasing bandwidth by 10 Mbps for each step

                # Creating and starting threads for each iperf flow
                threads = []
                for flow_id in range(num_flows):
                    server_port = 5000 + flow_id
                    thread = threading.Thread(target=run_iperf_flow, args=(net.get('h1'), h2_ip, server_port, duration, interval, results_file, f"{bandwidth}M"))
                    thread.start()
                    threads.append(thread)

                # Waiting for all threads to finish
                for thread in threads:
                    thread.join()

                # Stopping the iperf servers
                for server in servers:
                    server.terminate()

                results_file.write(f"End of step {step}, Bandwidth: {bandwidth} Mbps\n")
                results_file.write("-----\n")

    # Opening the Mininet command line interface
    CLI(net)
    # Stopping the network once the CLI is closed
    net.stop()

if __name__ == '__main__':
    setLogLevel('info')
    create_linear_topology()
