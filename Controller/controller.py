import numpy as np
from energy import energy_controller
from PID import PID_controller

class controller:
    """
    
    """
    def __init__(self, k):
        self.k = k  # Proportional gain for energy control
        
        # State variables
        self.y = 0.0    # Output control signal
        self.e = 0.0    # Energy error (difference between current and desired energy)
        
    def update_controller(self, e, e_d, theta, theta_dot, sat):
        """
        """
        if (abs(0 - pendulum_angle) <= np.deg2rad(5)):  # Stabilization condition: pole near upright
            # Use stabilization controller
            controller_state = "stabilize"
            e = pendulum_d - pendulum_angle
            u_s = stabilize_controller.update_controller(e, sat=10.0)
            # print(f"Stabilize controller in used u_s={u_s}")
        else :  # Swing-up condition: pole is far from upright
            # Use swing-up controller
            controller_state = "swingup"
            u_s = swingup_controller.update_controller(e=pendulum_e, e_d=energy_d, theta=pendulum_angle, theta_dot=state[3], sat=30)
            print(f"Swing-up controller in used u_s={u_s}")
    
        # Update cart position controller
        u_cp = cartpos_controller.update_controller(cart_d - cart_x, sat=30.0)
        
        # # Update cart velocity controller
        # u_cv = cartvel_controller.update_controller(0 - state[1], sat=15.0)
        
        # Update control input
        u = u_s + u_cp + u_cv
        
        return u