# DigitalTwins
The repository has python scripts used to set-up network topologies in Comnetsemu.
The LinearTopology Python script creates a linear topology in Mininet with two nodes and two switches in between, and in it, I simulate a traffic transmission using iperf that runs at varying durations of 10 seconds, 20 seconds, 30 seconds, 40 seconds, 50 seconds, and 60 seconds.
The Multiflow script creates a scenario where we have mutiple flows in the network of two nodes communicating to each other. In it, I increase the number of flows between the two nodes from one flow to five flows. And these flows run simultaneously, for example we can simulate two flows to run simultaneously, three flows, up to five flows, which can also be increased futher to more flows.
The increasing bandwidth script crates a scenario where the bandwidth is gradually increased from 0MBps by a factor of 10 until 1500Mbps. So as signal trasmission takes place between the nodes, BW is increased.
The expanded topology helps to show how the liniear network topology can be expanded to a more complex topology, which can integrate SDN capabilities.
