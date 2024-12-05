import pygame
import numpy as np
from Controller.controller import controller
from Controller.energy import energy_controller
from Controller.PID import PID_controller
import Simulation.model as model
import Simulation.button as button
from collections import deque
from Simulation.graph import graph

"""
Pygame initialization 
"""
# Initial window size
width = 1240  # Pixels
height = 600  # Pixels
initial_size = (width, height)
is_fullscreen = False

base_width = 1000  # Base width for scaling calculations
button_base_scale = 0.125  # Original button scale

pygame.init()
pygame.font.init()

screen = pygame.display.set_mode(initial_size, pygame.RESIZABLE)

f = 100

timer = pygame.time.Clock()

font = pygame.font.SysFont('Arial', 24)
current_time = 0.0
icon = pygame.image.load('Images/owl.png')
clock = pygame.time.Clock()
pygame.display.set_icon(icon)
pygame.display.set_caption("Simulation inverted pendulum on cart")


start_img = pygame.image.load('Images/start.png').convert_alpha()
stop_img = pygame.image.load('Images/stop.png').convert_alpha()
reset_img = pygame.image.load('Images/reset.png').convert_alpha()

start_x = (width // 2) - 310
start_y = 480
stop_x = (width // 2) - 15
stop_y = 480
reset_x = (width // 2) + 310
reset_y = 480

start_button = button.Button(start_x, start_y, start_img, 0.125)
stop_button = button.Button(stop_x, stop_y, stop_img, 0.125)
reset_button = button.Button(reset_x, reset_y, reset_img, 0.125)

# Color code
Navy = (69, 125, 142)
Green = (118, 215, 196)
Blue = (52, 152, 219)
Orange = (240, 178, 122)
Red = (241, 148, 138)
White = (253, 254, 254)
Black = (0, 0, 0)

"""
Simulation variables

Define 1 meter = 100 pixels
"""
is_start = False

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

cart_d = cart_x # Desired position of cart
pendulum_d = 0.0 # Desired angle of pendulum
energy_d = 2 * pendulum_mass * gravity * pendulum_length  # Desired energy of the system

# Initialize controller
controller = controller(k_e=13.5, kp_s=15.0, kd_s=100.0, kp_p=5.0, ki_p=0.0, kd_p=100.0, theta_range=25, m=pendulum_mass, M=cart_mass, L=pendulum_length/100)

"""
Graph variables
"""
angle_graph = graph(
    x=width - 700,
    y=50,
    width=250,
    height=150,
    title="Pendulum Angle",
    x_label="Time (s)",
    y_label="θ (rad)",
    y_range=(-np.pi, np.pi),
    time_window=5.0
)

position_graph = graph(
    x=width - 320,
    y=50,
    width=250,
    height=150,
    title="Cart Position",
    x_label="Time (s)",
    y_label="x (m)",
    y_range=(0, width/100),
    time_window=5.0
)

energy_graph = graph(
    x=width - 1080,
    y=50,
    width=250,
    height=150,
    title="Pendulum Energy",
    x_label="Time (s)",
    y_label="E (J)",
    y_range=(0, 2 * energy_d),
    time_window=5.0
)

energy_graph.set_setpoint(energy_d)  # Set desired energy
angle_graph.set_setpoint(pendulum_d)  # Set desired angle
position_graph.set_setpoint(cart_d)   # Set desired position

switch_graph = False

# Add small font for graph instructions
small_font = pygame.font.SysFont('Arial', 16)

"""
Additional function
"""
x_offset = 0
y_offset = 0

def update_offset(new_width, new_height):
    global x_offset, y_offset, width, height
    global cart_x_, cart_y_, cart_x, cart_y, cart_d
    global pendulum_x_, pendulum_y_, pendulum_x, pendulum_y
    global state
    global start_button, stop_button, reset_button  # Added reset_button
    
    if new_width != width:
        x_offset  += (new_width - width) // 2
        y_offset += (new_height - height) // 2
        
        width = new_width
        height = new_height
        
        # Update cart position
        cart_x_ = (cart_x * 100) + x_offset
        cart_y_ = height // 2

        # Update pendulum position
        pendulum_x_ = (pendulum_x * 100) + x_offset
        pendulum_y_ = pendulum_y * 100
        pendulum_y_ = cart_y_ - pendulum_y_
        
        # Calculate new scale based on window width
        new_scale = (new_width / base_width) * button_base_scale
        
        # Update button positions and scale
        start_button.update_offset(start_x + x_offset, start_y + y_offset, new_scale)
        stop_button.update_offset(stop_x + x_offset, stop_y + y_offset, new_scale)
        reset_button.update_offset(reset_x + x_offset, reset_y + y_offset, new_scale)
        
        # Update graph position
        angle_graph.x = (width // 2) - 310
        position_graph.x = (width // 2) - 15
        energy_graph.x = (width // 2) + 310

def reset_simulation():
    global is_start, switch_graph
    global x_offset, y_offset
    global cart_x, cart_y, pendulum_angle, state, current_time
    global cart_x_, pendulum_x_, pendulum_y_, pendulum_x, pendulum_y, pendulum_e
    global u, controller
    
    is_start = False
    switch_graph = False
    collision_detected = False
    
    # Reset variables to initial values
    pendulum_angle = np.deg2rad(180)
    cart_x = cart_d
    pendulum_angle = np.pi
    state = np.array([cart_x, 0.0, 0.0, pendulum_angle, 0.0, 0.0])
    current_time = 0.0
    cart_x_ = (cart_x * 100) + x_offset
    cart_y_ = height // 2
    
    # Update positions
    pendulum_x, pendulum_y = inverted_pen.kinematic(state=state)
    pendulum_x_ = (pendulum_x * 100) + x_offset
    pendulum_y_ = pendulum_y * 100
    pendulum_y_ = cart_y_ - pendulum_y_
    
    # Reset controller
    u = 0.0
    controller.reset()
    
    # Reset graphs
    angle_graph.clear_data()
    position_graph.clear_data()
    energy_graph.clear_data()
    angle_graph.reset()
    position_graph.reset()
    energy_graph.reset()

"""
Main Loop
"""
running = True
sim_state = 0
collision_detected = False  # Add this new variable

while running:
    timer.tick(f)
    """
    Start/Stop/Reset Button
    """
    if start_button.draw(screen):
        is_start = True
        sim_state = 1
    if stop_button.draw(screen):
        sim_state = 0
    if reset_button.draw(screen) and sim_state == 0:  # Only allow reset when stopped
        reset_simulation()
        switch_graph = False
        energy_graph.set_show_all_history(False)
        angle_graph.set_show_all_history(False)
        position_graph.set_show_all_history(False)
        collision_detected = False

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
        cart_x_ = (cart_x * 100) + x_offset
        pendulum_x_ = (pendulum_x * 100) + x_offset
        pendulum_y_ = pendulum_y * 100
        
        # Map to pygame coordinate
        pendulum_y_ = cart_y_ - pendulum_y_
        
        # Update simulation time
        current_time += dt
        
    """
    Simulation update
    """
    # Render graphics
    screen.fill(Navy)
    
    # Draw time in left corner
    time_text = font.render(f'Time: {current_time:.2f} s', True, Black)
    screen.blit(time_text, (10, 10))
    
    # Draw graphs    
    angle_graph.draw(screen, current_time, pendulum_angle)
    position_graph.draw(screen, current_time, cart_x)
    energy_graph.draw(screen, current_time, pendulum_e)
    
    # Draw s-key instructions below each graph
    hint_text = small_font.render("Press s-key to switch graph mode.", True, Black)
    screen.blit(hint_text, (width - 250, 5))

    # Check collision
    if cart_x_ - cart_width // 2 < 0 or cart_x_ + cart_width // 2 > width:
        collision_detected = True
        sim_state = 0  # Stop simulation

    # Draw collision message if detected
    if collision_detected:
        collision_text = font.render("Collision detected. Please reset simulation", True, Red)
        text_rect = collision_text.get_rect(center=(width//2, height//2))
        screen.blit(collision_text, text_rect)
    
    # Draw Cart
    cart_rect = pygame.Rect(int(cart_x_ - cart_width // 2), int(cart_y_ - cart_height // 2), cart_width, cart_height)
    pygame.draw.rect(screen, Red, cart_rect)

    # Draw Pendulum
    pygame.draw.line(screen, Green, (int(cart_x_), int(cart_y_)), (int(pendulum_x_), int(pendulum_y_)), 5)
    pygame.draw.circle(screen, Orange, (int(pendulum_x_), int(pendulum_y_)), 10)
    
    start_button.draw(screen)
    stop_button.draw(screen)
    reset_button.draw(screen)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_F11:
                is_fullscreen = not is_fullscreen
                if is_fullscreen:
                    screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
                else:
                    screen = pygame.display.set_mode(initial_size, pygame.RESIZABLE)
                update_offset(*screen.get_size())
            if event.key == pygame.K_s:
                if switch_graph:
                    switch_graph = False
                    energy_graph.set_show_all_history(False)
                    angle_graph.set_show_all_history(False)
                    position_graph.set_show_all_history(False)
                else:
                    if is_start:
                        switch_graph = True
                        energy_graph.set_show_all_history(True)
                        angle_graph.set_show_all_history(True)
                        position_graph.set_show_all_history(True)
                    
        elif event.type == pygame.VIDEORESIZE and not is_fullscreen:
            screen = pygame.display.set_mode((event.w, event.h), pygame.RESIZABLE)
            update_offset(*screen.get_size())
        elif event.type == pygame.WINDOWMAXIMIZED:
            update_offset(*screen.get_size())
        elif event.type == pygame.WINDOWRESTORED:
            update_offset(*screen.get_size())
    
    # Update display
    pygame.display.flip()

# Quit Pygame
pygame.quit()