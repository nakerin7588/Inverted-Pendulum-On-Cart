import numpy as np
from Controller.energy import energy_controller
from Controller.PID import PID_controller

class controller:
    """
    A hybrid controller for an inverted pendulum on a cart that switches between energy-based swing-up
    and PID stabilization control modes.
    
    The controller has two states:
    - SWINGUP: Uses energy control to swing the pendulum up
    - STABILIZE: Uses PID control to stabilize the pendulum and control cart position
    
    Args:
        k_e (float): Energy controller gain
        kp_s (float): Proportional gain for stabilization
        kd_s (float): Derivative gain for stabilization
        kp_p (float): Proportional gain for position control
        ki_p (float): Integral gain for position control
        kd_p (float): Derivative gain for position control
        theta_range (float): Angle range for switching to stabilization (degrees)
        m (float): Pendulum mass
        M (float): Cart mass
        L (float): Pendulum length
    """
    def __init__(self, k_e, kp_s, kd_s, kp_p, ki_p, kd_p, theta_range, m, M, L):
        # Controller initialization
        self.e_controller = energy_controller(m, M, L, k_e) # Energy controller
        self.s_controller = PID_controller(kp_s, 0.0, kd_s) # Stabilize controller
        self.p_controller = PID_controller(kp_p, ki_p, kd_p) # Position controller
        
        # Controller variables
        self.u = 0.0
        self.theta_range = theta_range # Range of theta for stabilization in degree
        self.state = "STABILIZE" # Controller state [SWINGUP, STABILIZE]
    
    def update_controller_state(self, th, e, e_d):
        """
        Update the controller state based on pendulum angle.
        
        Args:
            th (float): Current pendulum angle (radians)
            e (float): Current energy
            e_d (float): Desired energy
            
        Returns:
            str: New controller state ("STABILIZE" or "SWINGUP")
        """
        return "STABILIZE" if abs(th) < np.deg2rad(self.theta_range) else "SWINGUP"
    
    def update_controller(self, e, e_d, theta, theta_dot, theta_ddot, theta_d, x , x_d):
        """
        Update the control input based on current state and measurements.
        
        Args:
            e (float): Current system energy
            e_d (float): Desired energy
            theta (float): Current pendulum angle (radians)
            theta_dot (float): Angular velocity
            theta_ddot (float): Angular acceleration
            theta_d (float): Desired angle
            x (float): Current cart position
            x_d (float): Desired cart position
            
        Returns:
            float: Control input force to be applied to the cart
        """
        self.state = self.update_controller_state(theta, e, e_d)
        
        if self.state == "STABILIZE":
            self.u = self.s_controller.update_controller(theta - theta_d, 1000.0) + self.p_controller.update_controller(x - x_d, 1000.0)
            
        else:
            self.state = "SWINGUP"
            self.u = self.e_controller.update_controller(e, e_d, theta, theta_dot, theta_ddot, 1000.0) - self.p_controller.update_controller(x - x_d, 1000.0)
        
        # print(f"Current controller state is {self.state} and Control input is {self.u}")
        
        return self.u