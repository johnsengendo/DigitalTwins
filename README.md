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
- These prediction models [Window_size = 1](https://github.com/johnsengendo/DigitalTwins/blob/main/Prediction_LSTM_model(Window_size_%3D1).ipynb), [Window_size = 6](https://github.com/johnsengendo/DigitalTwins/blob/main/Prediction_LSTM_model(Window_size_%3D6).ipynb), [Window_size = 10](https://github.com/johnsengendo/DigitalTwins/blob/main/Prediction_LSTM_model(Window_size_%3D10).ipynb) which consider the senario of increasing BW between two nodes communicating to each other demonstrate how the varying window size affects the accuracy of predicting the future, which is a key aspect in achieving synchronization digital twins.
- [Window_size = 1](https://github.com/johnsengendo/DigitalTwins/blob/main/Trafic_prediction_4seconds_ahead_(window_size%3D1).ipynb) , [Window_size = 10](https://github.com/johnsengendo/DigitalTwins/blob/main/Trafic_prediction_4seconds_ahead_(window_size%3D10).ipynb) , [Window_size = 20](https://github.com/johnsengendo/DigitalTwins/blob/main/Trafic_prediction_4seconds_ahead_(window_size%3D20).ipynb) These as well demonstrate how the window size can affect the prediction. They take into the consideration of an iperf  run for different durations(10seconds, 20Seconds, 30Seconds, 40Seconds, 50Seconds & 60Seconds) when the nodes are communicating between themselves. I provide a brief summary [here](https://github.com/johnsengendo/DigitalTwins/blob/main/Summary%20results%20of%20Window_size%20effect.pdf)

PID Integration:<br>
In this section, I demonstrate how we integrate a PID that aids in improving transferred traffic predictions made by an LSTM model. In this section, I present three notebooks. [Notebook one](https://github.com/johnsengendo/DigitalTwins/blob/main/Prediction_Model(10Seconds_ahead)_with_PID_Integration.ipynb), showing how we use the PID to improve predictions of one second into the future. [Notebook two](https://github.com/johnsengendo/DigitalTwins/blob/main/Prediction_Model(10Seconds_ahead)_with_PID_Integration.ipynb), showing how the PID improves our predictions 10 seconds in the future. And [notebook three](https://github.com/johnsengendo/DigitalTwins/blob/main/Prediction_Model(60Seconds_ahead)_with_PID_Integration.ipynb), showing how as well the PID can improve predictions of the transferred traffic one minute into the future. In this case, I considered data where I capture the transferred traffic and the throughput between two nodes as the bandwidth is increased gradually.
