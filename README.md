# Chapter 1 : Inverted-Pendulum-On-Cart
This final project is in FRA333(Kinematics of Robotics System) This project exprain process of Inverted-Pendulum-On-Cart. By using simulation from PyGame.

<p align="center"><img src="Images/init_simulation.png" alt="initial simulation" /></p>

## Key components of the project include:
- **Modeling** : Dynamics model of the cart-pendulum system.
- **Controller** : 
    - *Swing-up Controller* : A control strategy applied at the start to add energy to the pendulum, enabling it to swing from the downward position to the upright position.
    - *Stabilized* : Implementation of a PID controller to keep the pendulum stabilized in the upright position.
- **Simulation** : A simulation to visualize the movement of the cart and pendulum and evaluate the performance of the controller.

# Chapter 2 : Concepts and Theories

1. **Inverted Pendulum on Cart**

    This is an under-actuated mechanical system with highly non-linear dynamics. It consists of a pendulum attached to a cart, where the pendulum can swing freely. The main objective of designing a control system for this setup is to swing the pendulum from the downward position to an upright position and maintain its balance. This is achieved by controlling the horizontal movement of the cart, which is the only available input for stabilizing the pendulum.

2. **Dynamics modeling of Inverted pendulum on cart**
    - FBD Inverted pendulum on cart

        <p align="center"><img src="Images/Dynamics-model.png" alt="initial simulation" /></p>

    - **F** = External force applied to the cart (N)
    - **θ** = Angle of the pendulum (rad)
    - **M** = Mass of the cart (kg)
    - **m** = Mass of the pendulum (kg)
    - **l** = Length of the pendulum (m)
    - **g** = Acceleration due to gravity (m/s²)


-  Kinematic equation of Inverted pendulum on cart

$$x_m = x + l \sin(\theta)$$

$$\dot{x_m} = \dot{x} + l \dot{\theta} \cos(\theta)$$

$$y_m = l \cos(\theta)$$

$$\dot{y_m} = -l \dot{\theta} \sin(\theta)$$

- Calculate Dynamics equation by Lagrangian

    $$L = T - V$$

    - **L** = Lagrangian (No unit)
    - **T** = Kinetic Energy (J)
    - **V** = Potential Energy (J)

- The total kinetic energy of the system :

$$T = \frac{1}{2} (M + m) \dot{x}^2 + m l \dot{x} \dot{\theta} \cos(\theta) + \frac{1}{2} m l^2 \dot{\theta}^2$$

- The potential energy of the system :
    
$$V = m g l \cos(\theta)$$

- So Lagrangian of the system :
    
$$L = \frac{1}{2} (M + m) \dot{x}^2 + m l \dot{x} \dot{\theta} \cos(\theta) + \frac{1}{2} m l^2 \dot{\theta}^2 - m g l \cos(\theta)$$

- Summary 
    - Equation of Motion for the Cart :

        $$\ddot{x} = \frac{F + m l \dot{\theta}^2 \sin(\theta) - m g \cos(\theta) \sin(\theta)}{M + m \sin^2(\theta)}$$

    - Equation of Motion for the Pendulum :

        $$\ddot{\theta} = \frac{g \sin(\theta) - \ddot{x} \cos(\theta)}{l}$$

**3. Energy-based control**

This focuses on adjusting the energy of the system to control its dynamics.
- Nonlinear Equations in Terms of Force :
    
$$F = (M + m \sin^2(\theta)) \ddot{x} - m l \dot{\theta}^2 \sin(\theta) + m g \cos(\theta) \sin(\theta)$$

- Control Law (Energy-Based Control) :
    
$$u = \ddot{x}$$

- Total Energy of the Pendulum :
    
$$E = \frac{1}{2} m l^2 \dot{\theta}^2 + m g l (1 + \cos(\theta))$$

- Energy Required to Reach the Equilibrium
    
$$E_d = m g l (1 + \cos(0)) = 2 m g l$$

- Controller Design
    
$$u = k \dot{\theta} \cos(\theta) \tilde{E}, \quad k > 0$$

- The controller design is divided into 2 phases
    - Phases 1 add Energy if $E<E_d$
    - Phases 2 Remove Energy if $E>E_d$
    - Get 
    
    $$u = sat_{u_{max}} \left( k(E - E_d) \text{Sign}(\dot{\theta} \cos(\theta)) \right)$$

    In this equation $u = \ddot{x}$ , But this system is controlled by force, so we need to calculate backwards to convert the control input into force for control the cart.

# Chapter 3 : Methodology

## 1. System Diagram

After we done research about dynamics of inverted pendulum and control strategy. We considerated to create our system diagram to guide us to complete our project.

<p align="center"><img src="Images/SystemDiagram.png" alt="system diagram" /></p>

## 2. Modeling for simulation

From dynamics model that we got. We have create the model that simulate with python by using dynamics & kinematic model of inverted pendulum on cart.

<p align="center"><img src="Images/OnlyDynamics.gif" alt="system diagram" /></p>

## 3. Controller design

After we got dynamics simulation of our inverted pendulum on cart. We decided to desire controller of our project that reference from system diagram.

Controller desire step:

1. We desired swing-up controller using Energy-based control that use total energy of pendulum to control this system. Because dynamics model of this is non-linear system, So we can't use only PID controller to control position of pendulum. Additionally, we also use PID to control position of cart to make sure cart will still on center.

2. After we can swing the pendulum to upright position we decided to control stability of pendulum to make sure that pendulum will still on upright position. So we decided to use PID controller because we estimate stabilize state was linear. Additionally, we add position controller as same as swing-up controller to make sure that cart will still on center.

3. Fine tune step. We tuning gain of controller with trial and error method, because we want to focus on dynamics desire step so we didn't want to use other method.

<p align="center"><img src="Images/runSim_Kine.gif" alt="runSim_Kine" /></p>

## 4. Simulation

1. Start simulation

<p align="center"><img src="Images/GIFstart.gif" alt="/GIFstart" /></p>

2. Stop/Pause simulation

<p align="center"><img src="Images/GIFstop.gif" alt="GIFstop" /></p>

3. Reset simulation

<p align="center"><img src="Images/GIFreset.gif" alt="GIFreset" /></p>

# Chapter 4 : Results and Analysis
## 4.1 Overview

This chapter presents the results of the simulation and its comparison with theoretical results calculated using Matlab. The goal is to validate the accuracy of the simulation by analyzing the consistency of the results.

## 4.2 Simulation Setup

Both Matlab and Python simulations were run with the following parameters:

- **Cart Mass (\(M\))**: 0.135 kg
- **Pendulum Mass (\(m\))**: 0.1 kg
- **Pendulum Length (\(l\))**: 0.5 m
- **Gravitational Acceleration (\(g\))**: 9.80665 m/s²
- **Simulation Time (\(T\))**: 10 s

## 4.3 Results from Matlab

<div align="center"><img src="Images/matlab.png" alt="runSim_Kine" /></div>

Graph from matlab:

1. Position of cart
<div align="center"><img src="Images/cart_mat.png" alt="runSim_Kine" /></div>

2. Angular of pendulum
<div align="center"><img src="Images/Angula_mat.png" alt="runSim_Kine" /></div>

## 4.4 Results from Simulation

<div align="center"><img src="Images/10.0_sim.png" alt="runSim_Kine" /></div>

Graph from simulation:

<div align="center"><img src="Images/graph_sim.png" alt="runSim_Kine" /></div>

# Chapter 5 : Summary

This project successfully simulated and controlled the **Inverted Pendulum on a Cart** system, addressing the challenges of swing-up and stabilization. The outcomes from the Python simulation were validated against Matlab results, providing confidence in the correctness and performance of the system.

## Key Insights

1. **Validation with Matlab**: 

   - Python’s results closely aligned with Matlab, confirming the theoretical correctness of the Python simulation.

2. **Swing-Up Control**: 

    - The energy based controller perform that, this system can swing the pendulum upright position while this system is non-linear.

3. **Stabilization Control**:

   - The PID controller maintained the pendulum in the upright position with acceptable performance in both platforms.
   - Matlab showed superior stabilization with faster settling time and minimal overshoot.

# Usage

Our project was develop with Ubuntu22.04, so every command is for ubuntu.

## Dependencies

To use this project. You need to have all of dependencies for this project.

⚠️**warning**: Make sure you have python version > 3.10 already.

1. pygame

    ```
    pip3 install pygame
    ```

2. numpy

    ```
    pip3 install numpy
    ```

## Installation

1. Clone this repository

    Clone this repository via this command below into your workspace or download it and extract file into your workspace.

    ```
    git clone https://github.com/nakerin7588/Inverted-Pendulum-On-Cart.git
    cd Inverted-Pendulum-On-Cart
    ```

2. Run the Simulation

    Execute the `visualization.py` via this command below.

    ⚠️**warning**: Make sure you are in root folder of your workspcae.

    ```
    python3 .\visualization.py
    ```

## Simulation's features

<p align="center"><img src="Images/Result.png" alt="system diagram" /></p>

* **Start Simulation**
    
    After the simulation window appears, you will see a *Start button*. Click on it to begin the simulation.
    - Initially, the *swing-up controller* will be applied to add energy to the pendulum, attempting to swing it up to an upright position.
    - Next the *Stabilize controller* will attempt to stabilize the pendulum by controlling the cart's movement.

* **Stop Simulation**
    
    While the simulation is running, you can press the *Stop button* to pause the simulation anytime.

* **Reset Simulation**
    
    While the simulation is pausing, you can press the *Reset button* to reset the simulation.

# References

- [INVERTED PENDULUM (Model Based Control Design for Swing-up & Balance the Inverted Pendulum)](https://drive.google.com/file/d/1W2v3wKXBVW4FohB33kTv8iBEiOFgoS8d/view)

- [Swing-up Control of an Inverted Pendulum by Energy-Based Methods](https://www.researchgate.net/publication/3811174_Swing-up_Control_of_an_Inverted_Pendulum_by_Energy-Based_Methods)

- [Cart-pole system : Equations of motion](https://courses.ece.ucsb.edu/ECE594/594D_W10Byl/hw/cartpole_eom.pdf)

- [NON-LINEAR SWING-UP AND STABILIZING CONTROL OF AN INVERTED PENDULUM SYSTEM](https://ieeer8.org/wp-content/uploads/downloads/2011/12/bugeja.pdf)