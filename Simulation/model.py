import numpy as np

class inverted_pendulum:
    def __init__(self, m: float = 0.2, M: float = 1.0, L: float = 0.5, g: float = 9.8125, d: float = 0.0, dt: float = 0.01):
        # Validate parameters
        if m <= 0 or M <= 0 or L <= 0 or g <= 0 or dt <= 0:
            raise ValueError("Physical parameters must be positive")
            
        self.m = m  # Mass of the pendulum (kg)
        self.M = M  # Mass of the cart (kg)
        self.L = L  # Length of the pendulum (m)
        self.g = g  # Acceleration due to gravity (m/s^2)
        self.d = d  # Damping coefficient
        self.dt = dt  # Time step for simulation (s)

    def dynamics(self, state: np.ndarray, u: float, disturbance: float = 0.0) -> np.ndarray:
        """
        Compute the dynamics of an inverted pendulum on a cart.

        Parameters:
        state (np.ndarray): The state vector [x, x_dot, theta, theta_dot]
        u (float): The control input (force applied to the cart)
        disturbance (float): External force applied to the pendulum

        Returns:
        np.ndarray: Updated state vector [x, x_dot, theta, theta_dot]
        """
        if len(state) != 4:
            raise ValueError("State must be a vector of length 4")
            
        x, x_dot, theta, theta_dot = state
        
        sin_theta = np.sin(theta)
        cos_theta = np.cos(theta)
        
        # Remove incorrect length scaling
        x_ddot = (u + disturbance + (self.m * self.L * theta_dot**2 * sin_theta) - 
                 (self.m * self.g * sin_theta * cos_theta)) / (self.M + (self.m * sin_theta**2))
        theta_ddot = (self.g * sin_theta - x_ddot * cos_theta) / self.L
        
        # Update states with proper time scaling
        x_dot += x_ddot * self.dt
        x += x_dot * self.dt
        theta_dot += theta_ddot * self.dt
        theta += theta_dot * self.dt
        theta = (theta + np.pi) % (2 * np.pi) - np.pi
        # theta = np.mod(theta, 2 * np.pi)
        
        return np.array([x, x_dot, theta, theta_dot])

    def kinematic(self, state: np.ndarray) -> np.ndarray:
        """
        Compute the kinematic positions of the cart and pendulum endpoints.

        Parameters:
        state (np.ndarray): The state vector [x, x_dot, theta, theta_dot]

        Returns:
        np.ndarray: Updated kinematic positions [pendulum_x, pendulum_y]
        """
        x, _, theta, _ = state
        
        # Pendulum end position
        pendulum_x = x + (self.L * np.sin(theta))
        pendulum_y = self.L * np.cos(theta)
        
        return np.array([pendulum_x, pendulum_y])
    
    def pendulum_energy(self, state: np.ndarray) -> float:
        """
        Compute the total pendulum energy of the system.

        Parameters:
        state (np.ndarray): The state vector [x, x_dot, theta, theta_dot]

        Returns:
        float: Total pendulum energy of the system
        """
        x, x_dot, theta, theta_dot = state
        
        cos_theta = np.cos(theta)
        
        # Total pendulum energy of the system
        energy = (0.5 * self.m * self.L**2 * theta_dot**2) + (self.m * self.g * self.L * (1 + cos_theta))
        
        return energy