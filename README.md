# DigitalTwins
The repository has python scripts used to set-up network topologies in Comnetsemu and python notebooks to build traffic prediction models. <br> Below is a breakdown of the scripts to sep-up topologies and different scenario.
 - The [Linear_topology](https://github.com/johnsengendo/DigitalTwins/blob/main/linear_topology.py) python script creates a linear topology in Mininet with two nodes and two switches in between, and in it, I simulate traffic 
   transmissions using iperf that run for varying durations of 10 seconds, 20 seconds, 30 seconds, 40 seconds, 50 seconds, and 60 seconds.
 - The [multiple_flows](https://github.com/johnsengendo/DigitalTwins/blob/main/multiple_flows.py) script creates a scenario where we have mutiple flows in the network of two nodes communicating to each other. In it, I increase the 
   number of flows between the two nodes from one flow to five flows. And these flows run simultaneously. For example we can simulate two flows to run simultaneously, three flows, up to five flows, which can also be increased futher to 
   more flows.
 - The [increasing_BW](https://github.com/johnsengendo/DigitalTwins/blob/main/increasing_BW.py) script crates a scenario where the bandwidth is gradually increased from 0MBps by a factor of 10 until 1500Mbps. So as signal trasmission 
   takes place between the nodes, BW is increased.
 - The [expanded_topology](https://github.com/johnsengendo/DigitalTwins/blob/main/expanded_topology.py) helps to show how the liniear network topology can be expanded to a more complex topology, which can integrate SDN capabilities.

 A brief summary on the prediction models built is as below:<br>
[Window_size = 1](https://github.com/johnsengendo/DigitalTwins/blob/main/Trafic_prediction_4seconds_ahead_(window_size%3D1).ipynb) , [Window_size = 10](https://github.com/johnsengendo/DigitalTwins/blob/main/Trafic_prediction_4seconds_ahead_(window_size%3D10).ipynb) , [Window_size = 20](https://github.com/johnsengendo/DigitalTwins/blob/main/Trafic_prediction_4seconds_ahead_(window_size%3D20).ipynb) These prediction scripts demonstrate how a window_size, that is; how much past information can affect how an LSTM prediction model can accurately predicts the network traffic a few seconds in the future. And, as we can see from this [Summary on Window_size effect](https://github.com/johnsengendo/DigitalTwins/blob/main/Summary%20results%20of%20Window_size%20effect.pdf), the lower the window size, the more accurate the models can predict how much traffic will be transferred in the future.
