import numpy as np

class energy_controller:
    """
    Energy-based Controller implementation for control systems.
    This controller regulates the system's energy to achieve desired behavior.
    """
    def __init__(self, m, M, L, k):
        # Dynamics parameters
        self.m = m  # Mass of the pendulum
        self.M = M  # Mass of the cart
        self.L = L  # Length of the pendulum
        
        # Controller gains
        self.k = k  # Proportional gain for energy control
        
        # State variables
        self.y = 0.0    # Output control signal (X_ddot)
        self.u = 0.0    # Control signal (force input to the system)
        self.e = 0.0    # Energy error (difference between current and desired energy)

    def update_controller(self, e, e_d, theta, theta_dot, theta_ddot, sat):
        """
        Updates the control signal based on energy regulation principle.
        
        Args:
            e (float): Current system energy
            e_d (float): Desired system energy
            theta (float): Current pendulum angle (in radians)
            theta_dot (float): Angular velocity of pendulum
            sat (float): Saturation limit for control signal
        
        Returns:
            float: Computed control signal (force input to the system)
        """
        # Calculate control signal:
        # - (e - e_d): Energy error
        # - theta_dot * cos(theta): Energy injection term
        # - sign: Ensures energy is only injected when needed
        # - k: Control gain to adjust response
        self.y = self.k * (e - e_d) * np.sign(theta_dot * np.cos(theta))
        
        # Saturate output to prevent excessive control signals
        # if self.y > sat:
        #     self.y = sat
        # elif self.y <= 0:
        #     self.y = 0
        
        # Calculate control signal (force input to the system)
        self.u = (self.m + self.M)*self.y + self.m*self.L*theta_ddot*np.cos(theta) - self.m*self.L*theta_dot**2*np.sin(theta)
        
        return self.y