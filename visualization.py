import pygame
import numpy as np
from Controller.energy import energy_controller
from Controller.PID import PID_controller
import Simulation.model as model
import matplotlib.pyplot as plt  # Add this import

"""
   Pygame initialization 
"""
# Sizescreen
width = 1000 # Pixels
height = 600 # Pixels

pygame.init()
pygame.font.init()

screen = pygame.display.set_mode((width, height))

f = 100

timer = pygame.time.Clock()

font = pygame.font.SysFont('Arial', 24)
start_time = pygame.time.get_ticks()  # Get initial time in milliseconds
current_time = (pygame.time.get_ticks() - start_time) / 1000.0  # Convert to seconds
icon = pygame.image.load('Images/owl.png')
clock = pygame.time.Clock()
pygame.display.set_icon(icon)
pygame.display.set_caption("Simulation inverted pendulum on cart")

# Color code
Navy = (52, 73, 94)
Green = (118, 215, 196)
Blue = (52, 152, 219)
Orange = (240, 178, 122)
Red = (241, 148, 138)
White = (253, 254, 254)

"""
   Simulation variables
   
   Define 1 meter = 100 pixels
"""
# Variable Inverted Pendulum
cart_x_ = width // 2  # Position Cart on x in pixels
cart_y_ = height // 2  # Position Cart on y in pixels
cart_x = cart_x_ / 100  # Position Cart on x in meters
cart_y = cart_y_ / 100  # Position Cart on y in meters
cart_width = 100  # width Cart in pixels
cart_height = 20  # height Cart in pixels
cart_mass = 1  # mass Cart (kg)

pendulum_length = 100  # length in pixels (represents 1 meter)
pendulum_angle = np.pi  # Initial angle set to pi radians (downwards)
pendulum_mass = 0.5  # mass Pendulum (kg)

state = np.array([cart_x, 0.0, pendulum_angle, 0.0])  # Initial state: [x, x_dot, theta, theta_dot]

gravity = 9.8125  # gravitational acceleration (m/s^2)
dt = 1/f

# Initialize inverted pendulum model
inverted_pen = model.inverted_pendulum(m=pendulum_mass, M=cart_mass, L=pendulum_length/100, g=gravity, d=0.0, dt=dt)

pendulum_x, pendulum_y = inverted_pen.kinematic(state=state) # Initial position of pendulum
pendulum_x_ = pendulum_x * 100 # Position Pendulum on x in pixels
pendulum_y_ = cart_y_ - pendulum_y * 100 # Position Pendulum on y in pixels

pendulum_e = inverted_pen.pendulum_energy(state=state)  # Energy of the pendulum

# Variable Controller
u = 0.0  # Control input
u_sat = 100000.0  # Control input saturation limit

u_cp = 0.0 # Control input for cart position
u_cv = 0.0 # Control input for cart velocity

u_s = 0.0 # Control input for swingup/stabilize

cart_d = cart_x # Desired position of cart
pendulum_d = 0.0 # Desired angle of pendulum
energy_d = 2 * pendulum_mass * gravity * pendulum_length  # Desired energy of the system

controller_state = "swingup" # Initial controller state

# Initialize controller
swingup_controller = energy_controller(k=0.001)
stabilize_controller = PID_controller(kp=1.0, ki=0.0, kd=0.0)

cartpos_controller = PID_controller(kp=8.0, ki=0.0, kd=3.0)
cartvel_controller = PID_controller(kp=30.0, ki=5.0, kd=0.0)

# Add these lines before the main loop
velocity_data = []    # Store velocity values
setpoint_data = []    # Store setpoint values
time_data = []       # Store time values

# Main Loop
running = True
while running:
    timer.tick(f)
    # print(state[1])
    # print(f"Energy: {pendulum_e}")
    """
        Controller Update
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
    
    # if u > u_sat:
    #     u = u_sat
    # elif u < -u_sat:
    #     u = -u_sat
    
    # print(u)
    
    """
        Model Update
    """
    # Update dynamics of Pendulum
    state = inverted_pen.dynamics(state=state, u=u)
    cart_x = state[0]
    pendulum_angle = state[2]
    
    # Update Kinematic of Pendulum
    pendulum_x, pendulum_y = inverted_pen.kinematic(state=state)
    
    # Update Energy of Pendulum
    pendulum_e = inverted_pen.pendulum_energy(state=state)
    
    # Add these lines after state update
    velocity_data.append(state[1])   # Store current velocity
    setpoint_data.append(1)        # Store setpoint (constant at 1.0)
    time_data.append(current_time)   # Store current time
    
    # Map to pygame scale
    cart_x_ = cart_x * 100
    pendulum_x_ = pendulum_x * 100
    pendulum_y_ = pendulum_y * 100
    
    # Map to pygame coordinate
    pendulum_y_ = cart_y_ - pendulum_y_
    
    # Update simulation time
    current_time = (pygame.time.get_ticks() - start_time) / 1000.0  # Convert to seconds
    
    """
        Simulation update
    """
    # Render graphics
    screen.fill(Navy)
    
    # Draw time in left corner
    time_text = font.render(f'Time: {current_time:.2f}s', True, White)
    screen.blit(time_text, (10, 10))
    
    # Draw time in right corner
    e_text = font.render(f'E: {pendulum_e:.2f}s', True, White)
    screen.blit(e_text, (900, 10))
    
    # Draw time in right corner
    d_text = font.render(f'd: {pendulum_angle:.2f}s', True, White)
    screen.blit(d_text, (900, 50))
    
    # Draw time in right corner
    v_text = font.render(f'v: {state[1]:.2f}s', True, White)
    screen.blit(v_text, (900, 100))
    
    # Draw time in right corner
    x_text = font.render(f'x: {state[0]:.2f}s', True, White)
    screen.blit(x_text, (900, 150))
    
    
    # Check colission
    # ฝากแก้ด้วยให้มันแบบถ้าชนขอบแล้วมีอะไรสักอย่างเกิดขึ้น
    if cart_x_ - cart_width // 2 < 0 or cart_x_ + cart_width // 2 > width:
        running = False
    
    # Draw Cart
    cart_rect = pygame.Rect(int(cart_x_ - cart_width // 2), int(cart_y_ - cart_height // 2), cart_width, cart_height)
    pygame.draw.rect(screen, Red, cart_rect)

    # Draw Pendulum
    pygame.draw.line(screen, Green, (int(cart_x_), int(cart_y_)), (int(pendulum_x_), int(pendulum_y_)), 5)  # วาดเส้น Pendulum
    pygame.draw.circle(screen, Orange, (int(pendulum_x_), int(pendulum_y_)), 10)  # วาดปลาย Pendulum
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:  # Check that are we closing the window
            running = False
    
    # Update display
    pygame.display.flip()

# Replace the plotting code after the main loop
plt.figure(figsize=(10, 6))
plt.plot(time_data, velocity_data, label='Actual Velocity')
plt.plot(time_data, setpoint_data, '--', label='Setpoint')
plt.title('Cart Velocity over Time')
plt.xlabel('Time (s)')
plt.ylabel('Velocity (m/s)')
plt.grid(True)
plt.legend()
plt.show()

# Quit Pygame
pygame.quit()