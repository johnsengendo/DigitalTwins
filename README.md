# DigitalTwins
The repository has python scripts used to set-up network topologies in ComNetsEmu and python notebooks to build traffic prediction models. <br> Below is the topology setup and a description of different scenario.
![Linear topology](https://github.com/johnsengendo/DigitalTwins/blob/main/Network_setup.png)
 - The [Linear_topology](https://github.com/johnsengendo/DigitalTwins/blob/main/linear_topology.py) python script creates a linear topology shown above in Mininet with two nodes and two switches in between, and in it, I simulate traffic 
   transmissions using iperf that run for varying durations of 10 seconds, 20 seconds, 30 seconds, 40 seconds, 50 seconds, and 60 seconds.
 - The [multiple_flows](https://github.com/johnsengendo/DigitalTwins/blob/main/multiple_flows.py) script creates a scenario using the same topology above where we have mutiple flows in the network of two nodes communicating to each other. In it, I increase the 
   number of flows between the two nodes from one flow to five flows. And these flows run simultaneously. For example we can simulate two flows to run simultaneously, three flows, up to five flows, which can also be increased futher to 
   more flows.
 - The [increasing_BW](https://github.com/johnsengendo/DigitalTwins/blob/main/increasing_BW.py) script crates a scenario where the bandwidth is gradually increased from 0MBps by a factor of 10 until 1500Mbps. So as signal trasmission 
   takes place between the nodes, BW is increased.
 - The [expanded_topology](https://github.com/johnsengendo/DigitalTwins/blob/main/expanded_topology.py) helps to show how the liniear network topology can be expanded to a more complex topology, which can integrate SDN capabilities.

 A brief summary on the prediction models built is as below:<br>
- These prediction models [Window_size = 1](https://github.com/johnsengendo/DigitalTwins/blob/main/Prediction_LSTM_model(Window_size_%3D1).ipynb), [Window_size = 6](https://github.com/johnsengendo/DigitalTwins/blob/main/Prediction_LSTM_model(Window_size_%3D6).ipynb), [Window_size = 10](https://github.com/johnsengendo/DigitalTwins/blob/main/Prediction_LSTM_model(Window_size_%3D10).ipynb) which consider the senario of increasing BW between two nodes communicating to each other demonstrate how the varying window size affects the accuracy of predicting the future, which is a key aspect in achieving synchronization digital twins.
- [Window_size = 1](https://github.com/johnsengendo/DigitalTwins/blob/main/Trafic_prediction_4seconds_ahead_(window_size%3D1).ipynb) , [Window_size = 10](https://github.com/johnsengendo/DigitalTwins/blob/main/Trafic_prediction_4seconds_ahead_(window_size%3D10).ipynb) , [Window_size = 20](https://github.com/johnsengendo/DigitalTwins/blob/main/Trafic_prediction_4seconds_ahead_(window_size%3D20).ipynb) These as well demonstrate how the window size can affect the prediction. They take into the consideration of an iperf  run for different durations(10seconds, 20Seconds, 30Seconds, 40Seconds, 50Seconds & 60Seconds) when the nodes are communicating between themselves. I provide a brief summary [here](https://github.com/johnsengendo/DigitalTwins/blob/main/Summary%20results%20of%20Window_size%20effect.pdf)

**PID Integration:**<br>
In this section, I demonstrate how to integrate a PID to improve predictions made by models which is a key aspect in Digital Twins synchronization.  This is achieved by using predictions made by an LSTM model.
![PID](https://github.com/johnsengendo/DigitalTwins/blob/main/PID_Integration.png)

In the first senario, two nodes are simulated to communicate as BW is increased gradually. The models (note books) below demostrate how we can improve predictiond with a PID.
- Predictions 1 Second ahead [note book](https://github.com/johnsengendo/DigitalTwins/blob/main/Prediction_Model(1Seconds_ahead)_with_PID_Integration.ipynb)
- Predictions 10 Seconds ahead [note book](https://github.com/johnsengendo/DigitalTwins/blob/main/Prediction_Model(10Seconds_ahead)_with_PID_Integration.ipynb)
- Predictions 60 Seconds ahead [note book](https://github.com/johnsengendo/DigitalTwins/blob/main/Prediction_Model(60Seconds_ahead)_with_PID_Integration.ipynb)

Here in the second senario, the duration of trasmission between the nodes is varied. Below are models showing how we integrate the PID to improve transfered traffic predictions afew seconds ahead.
- Predictions 1 Second ahead [note book](https://github.com/johnsengendo/DigitalTwins/blob/main/Trafic_prediction_single_flow_1second_ahead_PID_(window_size%3D1).ipynb)
- Predictions 10 Seconds ahead [note book](https://github.com/johnsengendo/DigitalTwins/blob/main/Trafic_prediction_single_flow_10seconds_ahead_PID_(window_size%3D1).ipynb)
- Predictions 60 Seconds ahead [note book](https://github.com/johnsengendo/DigitalTwins/blob/main/Trafic_prediction_single_flow_60seconds_ahead_PID_(window_size%3D1).ipynb)

Here in the third senario, a very noisy senario is emulated where two simultaneous flows are initiated between the nodes and a 5% packet loss is introduced in the link connecting the 2 switches. Below are models showing how we integrate the PID to improve transfered traffic predictions afew seconds ahead.
- Predictions 1 Second ahead [note book](https://github.com/johnsengendo/DigitalTwins/blob/main/Prediction_Model_for_noisy_senario_with_PID_Integration_(1seconds_ahead).ipynb)
- Predictions 10 Seconds ahead [note book](https://github.com/johnsengendo/DigitalTwins/blob/main/Prediction_Model_for_noisy_senario_with_PID_Integration_(10seconds_ahead).ipynb)
- Predictions 60 Seconds ahead [note book](https://github.com/johnsengendo/DigitalTwins/blob/main/Prediction_Model_for%20noisy_senario_with_PID_Integration_(60seconds_ahead).ipynb)
