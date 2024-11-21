import pygame
import math
#import Simulation.dynamic_model as dynamic_model

# Sizescreen
width = 800
height = 400

pygame.init()
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Simulation inverted pendulum on cart")

# Color code
Navy = (52, 73, 94)
Green = (118, 215, 196)
Blue = (52, 152, 219)
Orange = (240, 178, 122)
Red = (241, 148, 138)

# Variable Inverted Pendulum
cart_x = width // 2  # Position Cart on x (กลางหน้าจอ)
cart_y = height // 2  # Position Cart on y
cart_width = 100  # width Cart (m)
cart_height = 20  # height Cart (m)

pendulum_length = 150  # ความยาวของ Pendulum (m)
pendulum_angle = math.pi / 4  # มุมเริ่มต้น pi/4 Radian(rad) / 45 degree
angular_velocity = 0  # ความเร็วเชิงมุมเริ่มต้น (rad)
angular_acceleration = 0  # ความเร่งเชิงมุมเริ่มต้น (rad/s^2)
gravity = 9.8125  # แรงโน้มถ่วง (m/s^2)
time_step = 0.02  # Δt (s)

# ตั้งค่าให้หน้าจอไม่ปิดทันที
running = True

# Game Loop
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:  # ตรวจสอบว่าเรากดปิดหน้าต่างหรือไม่
            running = False

    # อัปเดต Dynamics ของ Pendulum
    angular_acceleration = -gravity / pendulum_length * math.sin(pendulum_angle)  # สมการการเคลื่อนที่
    angular_velocity += angular_acceleration * time_step
    pendulum_angle += angular_velocity * time_step

    # เติมพื้นหลังให้เป็นสี Navy
    screen.fill(Navy)

    # วาด Cart
    cart_rect = pygame.Rect(cart_x - cart_width // 2, cart_y - cart_height // 2, cart_width, cart_height)
    pygame.draw.rect(screen, Red, cart_rect)

    # วาด Pendulum
    pendulum_x = cart_x + pendulum_length * math.sin(pendulum_angle)
    pendulum_y = cart_y + pendulum_length * math.cos(pendulum_angle)
    pygame.draw.line(screen, Green, (cart_x, cart_y), (pendulum_x, pendulum_y), 5)  # วาดเส้น Pendulum
    pygame.draw.circle(screen, Orange, (int(pendulum_x), int(pendulum_y)), 10)  # วาดปลาย Pendulum

    # อัปเดตหน้าจอ
    pygame.display.flip()

    # จำกัดเฟรมเรต
    pygame.time.delay(int(time_step * 1000))

# ออกจาก Pygame
pygame.quit()
