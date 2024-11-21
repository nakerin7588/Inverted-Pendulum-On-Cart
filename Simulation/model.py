import numpy as np

def inverted_pendulum_dynamics(state, u, disturbance=0.0, m=0.2, M=1.0, L=0.5, g=9.8125, d=0.1, dt=0.01):
    """
    Compute the dynamics of an inverted pendulum on a cart.

    Parameters:
    state (array): The state vector [x, x_dot, theta, theta_dot]
    u (float): The control input (force applied to the cart)
    disturbance (float): External force applied to the pendulum (default: 0.0 N)
    m (float): Mass of the pendulum (default: 0.2 kg)
    M (float): Mass of the cart (default: 1.0 kg)
    L (float): Length of the pendulum (default: 0.5 m)
    g (float): Acceleration due to gravity (default: 9.81 m/s^2)
    d (float): Damping coefficient (default: 0.1)

    Returns:
    array: the state vector [x, x_dot, theta, theta_dot]
    """
    x, x_dot, theta, theta_dot = state

    # # Scale the length for pixels to meters conversion (assuming 100 pixels = 1 meter)
    L = L / 100.0
    
    sin_theta = np.sin(theta)
    cos_theta = np.cos(theta)
    
    # Update state with scaled parameters
    x_ddot = (u + (m * L * theta_dot**2 * sin_theta) - (m * g * sin_theta * cos_theta)) / (M + (m * sin_theta**2))
    theta_ddot = (g * sin_theta - x_ddot * cos_theta) / L
    
    # Update states with proper time scaling
    x_dot += x_ddot * dt
    x += x_dot * dt
    theta_dot += theta_ddot * dt
    theta += theta_dot * dt
    
    return np.array([x, x_dot, theta, theta_dot])

def inverted_pendulum_kinematic(state, L=0.5):
    """
    Compute the kinematic positions of the cart and pendulum endpoints.

    Parameters:
    state (array): The state vector [x, x_dot, theta, theta_dot]
    L (float): Length of the pendulum (default: 0.5 m)
    
    Returns:
    tuple: (cart_pos, pendulum_pos) where each is a 2D position [x, y]
    """
    x, _, theta, _ = state

    sin_theta = np.sin(theta)
    cos_theta = np.cos(theta)
    
    # Pendulum end position relative to cart
    pendulum_x = x + (L * sin_theta)
    pendulum_y = L * cos_theta  # Ensure the y-coordinate is inverted for Pygame
    
    return pendulum_x, pendulum_y