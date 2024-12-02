class PID:
    """
    PID Controller implementation for control systems.
    Implements a discrete-time PID controller with anti-windup protection.
    """
    def __init__(self, kp, ki, kd):
        # Controller gains
        self.kp = kp  # Proportional gain
        self.ki = ki  # Integral gain
        self.kd = kd  # Derivative gain
        
        # State variables
        self.y_n = 0.0    # Current output
        self.y_n_1 = 0.0  # Previous output
        self.e_n = 0.0    # Current error
        self.e_n_1 = 0.0  # Previous error
        self.e_n_2 = 0.0  # Error from two steps ago

    def update_pid(self, error, pid_sat):
        """
        Updates PID controller output based on error input.
        
        Args:
            error: Current error (setpoint - measured_value)
            pid_sat: Output saturation limits (±pid_sat)
        
        Returns:
            float: Controller output
        """
        e_n = error  # Current error sample

        # Anti-windup logic:
        # Only update controller if:
        # 1. Output is not saturated, or
        # 2. Error is trying to reduce the output
        if not ((self.y_n >= pid_sat and e_n > 0) or (self.y_n <= -pid_sat and e_n < 0)):
            # PID equation in discrete form:
            self.y_n += ((self.kp + self.ki + self.kd) * e_n) - ((self.kp + (2 * self.kd)) * self.e_n_1) + (self.kd * self.e_n_2)

        # Update error history for next iteration
        self.e_n_2 = self.e_n_1
        self.e_n_1 = e_n
        self.e_n = e_n

        # Saturate output to prevent excessive control signals
        if self.y_n > pid_sat:
            self.y_n = pid_sat
        elif self.y_n < -pid_sat:
            self.y_n = -pid_sat

        return self.y_n