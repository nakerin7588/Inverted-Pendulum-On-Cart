import pygame
import numpy as np
from model import inverted_pendulum_dynamics, inverted_pendulum_kinematic

def map_meter_to_pixel(x):
    return x * 100
def map_pixel_to_meter(x):
    return x / 100

# Sizescreen
width = 1000 # Pixels
height = 600 # Pixels

pygame.init()
pygame.font.init()
font = pygame.font.SysFont('Arial', 24)
start_time = pygame.time.get_ticks()  # Get initial time in milliseconds

screen = pygame.display.set_mode((width, height))
clock = pygame.time.Clock()
pygame.display.set_caption("Simulation inverted pendulum on cart")

# Color code
Navy = (52, 73, 94)
Green = (118, 215, 196)
Blue = (52, 152, 219)
Orange = (240, 178, 122)
Red = (241, 148, 138)
White = (253, 254, 254)

# Variable Inverted Pendulum
cart_x = width // 2  # Position Cart on x (กลางหน้าจอ)
cart_y = height // 2  # Position Cart on y
cart_width = 100  # width Cart (m)
cart_height = 20  # height Cart (m)
cart_mass = 1.0  # mass Cart (kg)

pendulum_length = 100  # length in pixels (represents 1 meter)
pendulum_angle = np.pi / 4  # Initial angle set to pi radians (downwards)
pendulum_mass = 0.5  # mass Pendulum (kg)

gravity = 9.81  # gravitational acceleration (m/s^2)
time_step = 0.01  # Physics time step (s) - increased for better stability
frame_rate = 60    # Display refresh rate (Hz)
physics_time = 0.0 # Time accumulator for physics updates

state = [cart_x, 0.0, pendulum_angle, 0.0]  # Initial state: [x, x_dot, theta, theta_dot]

# ตั้งค่าให้หน้าจอไม่ปิดทันที
running = True

# Main Loop
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:  # ตรวจสอบว่าเรากดปิดหน้าต่างหรือไม่
            running = False
    
    # Calculate actual frame time
    dt = 1 / frame_rate
    physics_time += dt
    
    # Update physics with fixed time step
    while physics_time >= time_step:
        state = inverted_pendulum_dynamics(state=state, u=0.0, m=pendulum_mass, M=cart_mass, L=pendulum_length, g=gravity, dt=time_step)
        physics_time -= time_step
    
    cart_x = state[0]
    
    # Update Kinematic of Pendulum
    pendulum_x, pendulum_y = inverted_pendulum_kinematic(state=state, L=pendulum_length)
    
    # Map to pygame coordinate
    pendulum_y = cart_y - pendulum_y
    
    # Update simulation time
    current_time = (pygame.time.get_ticks() - start_time) / 1000.0  # Convert to seconds
    
    # Render graphics
    screen.fill(Navy)
    
    # Draw time in left corner
    time_text = font.render(f'Time: {current_time:.2f}s', True, White)
    screen.blit(time_text, (10, 10))
    

    # วาด Cart
    cart_rect = pygame.Rect(int(cart_x - cart_width // 2), int(cart_y - cart_height // 2), cart_width, cart_height)
    pygame.draw.rect(screen, Red, cart_rect)

    # วาด Pendulum
    pygame.draw.line(screen, Green, (int(cart_x), int(cart_y)), (int(pendulum_x), int(pendulum_y)), 5)  # วาดเส้น Pendulum
    pygame.draw.circle(screen, Orange, (int(pendulum_x), int(pendulum_y)), 10)  # วาดปลาย Pendulum
    
    # อัปเดตหน้าจอ
    pygame.display.flip()

# ออกจาก Pygame
pygame.quit()
