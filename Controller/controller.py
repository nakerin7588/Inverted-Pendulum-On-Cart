import numpy as np
from Controller.energy import energy_controller
from Controller.PID import PID_controller

class controller:
    """
    
    """
    def __init__(self, k_e, kp_s, kd_s, kp_p, kd_p, k_v, theta_range, m, M, L):
        # Controller initialization
        self.e_controller = energy_controller(m, M, L, k_e) # Energy controller
        self.s_controller = PID_controller(kp_s, 0.0, kd_s) # Stabilize controller
        self.p_controller = PID_controller(kp_p, 0.0, kd_p) # Position controller
        self.v_controller = PID_controller(k_v, 0.0, 0.0) # Velocity controller
        
        # Controller variables
        self.u = 0.0
        self.theta_range = theta_range # Range of theta for stabilization in degree
        self.state = "STABILIZE" # Controller state [SWINGUP, STABILIZE]
    
    def update_controller_state(self, th, e, e_d):
	    return "STABILIZE" if abs(th) < np.deg2rad(self.theta_range) else "SWINGUP"
    
    def update_controller(self, e, e_d, theta, theta_dot, theta_ddot, theta_d, x, x_dot , x_d):
        """
        """
        # if self.state == "GO_CENTER":
        #     if abs(theta) < np.deg2rad(self.theta_range):
        #         self.state = "STABILIZE"
        #     elif abs(x_d - x) <= 1e-2:
        #         self.state = "SWINGUP"
        #     else:
        #         self.u = self.p_controller.update_controller(x_d - x, 1000.0)
        
        # elif self.state == "SWINGUP":
        #     if abs(theta) < np.deg2rad(self.theta_range):
        #         self.state = "STABILIZE"
        #     elif abs(x_d - x) <= 0.05:
        #         self.u = self.e_controller.update_controller(e, e_d, theta, theta_dot, theta_ddot, 1000.0)
        #     else:
        #         self.state = "GO_CENTER"
            
        # elif self.state == "STABILIZE":
        #     if abs(theta) > np.deg2rad(self.theta_range):
        #         self.state = "GO_CENTER"
        #     else:
        #         self.u = -self.s_controller.update_controller(theta_d - theta, 1000.0)
        #         self.u -= self.p_controller.update_controller(x_d - x, 1000.0)
        
        self.state = self.update_controller_state(theta, e, e_d)
        
        if self.state == "STABILIZE":
            self.u = self.s_controller.update_controller(theta - theta_d, 1000.0) + self.p_controller.update_controller(x - x_d, 1000.0)
            
        else:
            self.state = "SWINGUP"
            self.u = self.e_controller.update_controller(e, e_d, theta, theta_dot, theta_ddot, 1000.0)
        
        print(f"Current controller state is {self.state} and Control input is {self.u}")
        
        return self.u