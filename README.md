# Inverted-Pendulum-On-Cart
This final project is in FRA333(Kinematics of Robotics System) This project exprain process of Inverted-Pendulum-On-Cart. By using simulation from PyGame.

Key components of the project include:
- **Modeling** : Dynamics model of the cart-pendulum system.
- **Controller** : 
    - *Swing-up Controller* : A control strategy applied at the start to add energy to the pendulum, enabling it to swing from the downward position to the upright position.
    - *Stabilized* : Implementation of a PID controller to keep the pendulum stabilized in the upright position.
- **Simulation** : A simulation to visualize the movement of the cart and pendulum and evaluate the performance of the controller.


# Installation Instructions

# Equation



# Usage

To run the simulation follow these steps :
### 1. Clone the Repository
First, clone the project repository to your computer :
```bash
git clone https://github.com/nakerin7588/Inverted-Pendulum-On-Cart.git
cd Inverted-Pendulum-On-Cart
```
### 2.Install Dependencies
Make sure you have Python installed. Then install the required libraries.

1. Pygame

    ```bash
    pip3 install pygame
    ```
2. numpy
    ```bash
    pip3 install numpy
    ```

### 3.Run the Simulation
Execute the main script to launch the simulation :
```bash
python visualization.py
```

### 4. Start and Control the Simulation
* **Start Simulation**
    
    After the simulation window appears, you will see a *Start button*. Click on it to begin the simulation.
    - Initially, the *swing-up controller* will be applied to add energy to the pendulum, attempting to swing it up to an upright position.
    - Next the *PID controller* will attempt to stabilize the pendulum by controlling the cart's movement.

* **Stop Simulation**
    
    While the simulation is running, you can press the *Stop button* to pause the simulation anytime.

### 5.Exit the Simulation
To exit the simulation, only close the PyGame window.

# Knowledge



