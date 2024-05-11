from mininet.topo import Topo
from mininet.net import Mininet
from mininet.node import OVSController
from mininet.cli import CLI
from mininet.log import setLogLevel
import time
import threading

class SimpleTopology(Topo):
    def build(self):
        switch = self.addSwitch('s1')
        host1 = self.addHost('h1')
        host2 = self.addHost('h2')
        self.addLink(host1, switch)
        self.addLink(switch, host2)

def run_continuous_flow(net, duration=60):
    h1, h2 = net.get('h1'), net.get('h2')
    h2.cmd('iperf -s -p 5001 &')  # Start a server on a background
    output_file = "/tmp/continuous_flow_results.txt"
    h1.cmdPrint(f'iperf -c {h2.IP()} -p 5001 -t {duration} > {output_file}')
    print(f"Continuous flow results stored in {output_file}")

def run_temporary_flow(net):
    h1, h2 = net.get('h1'), net.get('h2')
    h2.cmd('iperf -s -p 5002 &')  # Start another server on a different port
    h1.cmdPrint('iperf -c {} -p 5002 -t 5'.format(h2.IP()))

def run_random_flows(net):
    import random
    h1, h2 = net.get('h1'), net.get('h2')
    for i in range(10):  # Number of random flows
        duration = random.randint(1, 10)  # Duration between 1 and 10 seconds
        port = 5003 + i  # Different port for each flow
        h2.cmd('iperf -s -p {} &'.format(port))
        time.sleep(random.randint(1, 5))  # Random start time delays
        h1.cmdPrint('iperf -c {} -p {} -t {}'.format(h2.IP(), port, duration))
        time.sleep(duration + 1)  # Wait for flow to finish

def start_experiment():
    topo = SimpleTopology()
    net = Mininet(topo=topo, controller=OVSController)
    net.start()

    # Start the continuous flow
    threading.Thread(target=run_continuous_flow, args=(net,)).start()

    # Start the temporary flow
    threading.Thread(target=run_temporary_flow, args=(net,)).start()

    # Start random smaller flows
    threading.Thread(target=run_random_flows, args=(net,)).start()

    time.sleep(60)  # Run the network for 60 seconds or as needed
    CLI(net)  # Optional: can start CLI for interactive commands
    net.stop()

if __name__ == '__main__':
    setLogLevel('info')
    start_experiment()
