![alt text](https://github.com/iareust/train_schedule_optimization/blob/master/architecture.png)

# Cleaned Code Repository of the Bachelor Thesis 
Code Repository for the Bachelor Thesis on "Train Schedule Optimization with focus on Robustness"

The src Folder contains all relevant components. It is structured in the following 6 submodules
- experiments: Jupyter notebook containing the implementation of the genetic algorithms as well as the experiment setups and results
- gym-train-env: A gym environment which was used to test reinfocement learning agent. But because the optimization method was changed to genetic optimization, those environments were not finished. They can be used as a basis for a future project involving RL Agents.
- log_viewer: The Jupyter Notebook of the Log viewer which was used to present the random number experiment in the intermediat presentation.
- model: The implementation of the components which were described in the documentation.
- simulation: Implementation of the behaviour for the components decribed in the model


## Usage of Train Simulator
The usage of the train network simulator is demonstrated in this section with a given example train network and
two predefined timetables. 

### Example Train Network and Train Timetable (Line AB and BA)
```
  +-----------+                    +-----------+ 
  |           |                    |           | 
  | Station A +--------------------+ Station C | 
  |           |                    |           | 
  +-----------+                    +-----------+ 
```

| Station | Arrival Time (Time/Simulation Time) | Station | Arrival Time (Time/Simulation Time) | Description    |
|---------|-------------------------------------|---------|-------------------------------------|----------------|
|    A    | 00:10 / 0010                        | B       | 00:05 / 0005                        |                |
|    B    | 00:25 / 0025                        | A       | 00:15 / 0015                        |                |               | End dwelling   |
|    B    | 01:30 / 0090                        | A       | 01:10 / 0070                        |                |
|    A    | 01:45 / 0105                        | B       | 01:25 / 0085                        |                |

### Evaluating a Timetable
Import the simulator module and network architecture. If there is no predefined network architecture for your problem
you can create on in the /src/simulation/networks file.

```Python
from src.simulation.simulator import Simulator
from src.simulation.networks import DebugNetwork
```

To evaluate timetables, you have to first instantiate the Simulator with the given network architecture
```python
sim = Simulator(DebugNetwork)
``` 

The simulator can now be used to evaluate a timetable:
```python
timetable = [[10,25,90,105],[5,15,70,85]]
sim.evaluate_timetable(timetable)
```
This automatically performs 12 simulations for the three scenarios (4 each):
- Train Increase
- Passenger Increase
- Train Breakdown

The returned results contain the performance of the network for each scenario, as well as the timetable
which was provided.

```python
{'passenger_increase': {'1': 2.37734693877551,
  '2': 2.37734693877551,
  '4': 2.37734693877551,
  '8': 2.37734693877551,
  'reward_total': 9.50938775510204},
 'trains_increase': {'1': 2.37734693877551,
  '2': 2.4054879075447912,
  '3': 2.3862420779295235,
  '4': 1.050675729560095,
  'reward_total': 8.21975265380992},
 'trains_delay': {'5': 1.6823481143668793,
  '30': 2.374356371936044,
  '60': 2.408574858259782,
  '120': 1.545365510890001,
  'reward_total': 8.010644855452707},
 'timetables': [[10, 25, 90, 105], [5, 15, 70, 85]]}
```

If you only want to conduct a single simulation on the network, you can use the simulate method:
```python
env = sim.simulate(time_tables=timetable, 
            connections_per_h=1,
            passenger_increase_factor=1,
            force_train_stop_time=0,
            plot=False)
```

This command returns a train environment, which can then be used to evaluate the performance rewards
of this network.
```python
reward_early = env.get_reward_early_arrival()
reward_handled = env.get_reward_handled()
reward_delay = env.get_reward_delay(tolarance_per_line=5, num_lines=2)
```
