import pygame
import numpy as np
from Controller.controller import controller
from Controller.energy import energy_controller
from Controller.PID import PID_controller
import Simulation.model as model
import matplotlib.pyplot as plt
import button

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


start_img = pygame.image.load('Images/start.png').convert_alpha()
stop_img = pygame.image.load('Images/stop.png').convert_alpha()

start_button = button.Button(250, 450, start_img, 0.125)
stop_button = button.Button(700, 450, stop_img, 0.125)

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
cart_width = 60  # width Cart in pixels
cart_height = 20  # height Cart in pixels
cart_mass = 0.135  # mass Cart (kg)

pendulum_length = 0.5  # length in meters
pendulum_angle = np.deg2rad(180)  # Initial angle set to pi radians (downwards)
pendulum_mass = 0.1  # mass Pendulum (kg)

state = np.array([cart_x, 0.0, 0.0, pendulum_angle, 0.0, 0.0])  # Initial state: [x, x_dot, x_ddot, theta, theta_dot, theta_ddot]

gravity = 9.8125  # gravitational acceleration (m/s^2)
dt = 1/f

# Initialize inverted pendulum model
inverted_pen = model.inverted_pendulum(m=pendulum_mass, M=cart_mass, L=pendulum_length, g=gravity, d=0.0, dt=dt)

pendulum_x, pendulum_y = inverted_pen.kinematic(state=state) # Initial position of pendulum
pendulum_x_ = pendulum_x * 100 # Position Pendulum on x in pixels
pendulum_y_ = cart_y_ - pendulum_y * 100 # Position Pendulum on y in pixels

pendulum_e = inverted_pen.pendulum_energy(state=state)  # Energy of the pendulum

# Variable Controller
u = 0.0  # Control input
u_sat = 100000.0  # Control input saturation limit

cart_d = cart_x # Desired position of cart
pendulum_d = 0.0 # Desired angle of pendulum
energy_d = 2 * pendulum_mass * gravity * pendulum_length  # Desired energy of the system

# Initialize controller
controller = controller(k_e=20.0, kp_s=100.0, kd_s=800.0, kp_p=5.0, ki_p=0.0, kd_p=100.0, theta_range=25, m=pendulum_mass, M=cart_mass, L=pendulum_length/100)

# Main Loop
running = True
sim_state = 0
while running:
    timer.tick(f)
    """
    Start/Stop Button
    """
    if start_button.draw(screen):
        sim_state = 1
    if stop_button.draw(screen):
        sim_state = 0

    if sim_state == 1:
        """
        Controller Update
        """
        u = controller.update_controller(e=pendulum_e, e_d=energy_d, theta=pendulum_angle, theta_dot=state[4], theta_ddot=state[5], theta_d=pendulum_d, x=state[0], x_d=cart_d)
       
        """
        Model Update
        """
        # Update dynamics of Pendulum
        state = inverted_pen.dynamics(state=state, u=u)
        cart_x = state[0]
        pendulum_angle = state[3]
        
        # Update Kinematic of Pendulum
        pendulum_x, pendulum_y = inverted_pen.kinematic(state=state)
        
        # Update Energy of Pendulum
        pendulum_e = inverted_pen.pendulum_energy(state=state)
    
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
    
    # Draw Energy in right corner
    e_text = font.render(f'E: {pendulum_e:.2f}s', True, White)
    screen.blit(e_text, (900, 10))
    
    # Draw degree in right corner
    d_text = font.render(f'd: {pendulum_angle:.2f}s', True, White)
    screen.blit(d_text, (900, 50))
    
    # Draw velocity in right corner
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
    
    start_button.draw(screen)
    stop_button.draw(screen)

    for event in pygame.event.get():
            if event.type == pygame.QUIT:  # Check that are we closing the window
                running = False
    # Update display
    pygame.display.flip()

# Quit Pygame
pygame.quit()