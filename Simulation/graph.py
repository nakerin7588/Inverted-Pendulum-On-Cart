import pygame
import numpy as np

class graph:
    def __init__(self, x, y, width, height, title, x_label, y_label, y_range, time_window=5.0):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.title = title
        self.x_label = x_label
        self.y_label = y_label
        self.y_range = y_range
        self.time_window = time_window
        
        self.time_data = []
        self.value_data = []
        self.title_font = pygame.font.SysFont('Arial', 20, bold=True)  # Larger, bold font for title
        self.font = pygame.font.SysFont('Arial', 16)
        
        # Colors
        self.BLACK = (0, 0, 0)
        self.WHITE = (253, 254, 254)
        self.GREEN = (118, 215, 196)
        self.RED = (241, 148, 138)  # Add color for setpoint line
        
        # Initialize empty lists for data storage
        self.time_data = []
        self.value_data = []
        self.max_points = int(time_window * 100)  # Store 100 points per second
        
        self.setpoint = None
        
    def draw(self, screen, current_time, current_value):
        # Draw graph background
        pygame.draw.rect(screen, self.WHITE, (self.x, self.y, self.width, self.height))
        
        # Draw grid
        self._draw_grid(screen)
        
        # Draw axes
        self._draw_axes(screen)
        
        # Draw labels
        self._draw_labels(screen, current_value)
        
        # Update and clean data
        self._update_data(current_time, current_value)
        
        # Plot the data
        self._plot_data(screen)
        
    def _draw_grid(self, screen):
        grid_spacing_y = self.height / 6
        grid_spacing_x = self.width / 5
        
        # Draw horizontal grid lines and y-axis numbers
        for i in range(7):
            y_pos = self.y + i * grid_spacing_y
            y_value = self.y_range[1] - (i * (self.y_range[1] - self.y_range[0]) / 6)
            pygame.draw.line(screen, self.BLACK, (self.x, y_pos), 
                           (self.x + self.width, y_pos), 1)
            pygame.draw.line(screen, self.BLACK, (self.x - 5, y_pos), 
                           (self.x + 5, y_pos), 2)
            # Add y-axis numbers
            y_label = self.font.render(f'{y_value:.1f}', True, self.BLACK)
            screen.blit(y_label, (self.x - 45, y_pos - 10))
        
        # Draw vertical grid lines and x-axis numbers
        current_time = self.time_data[-1] if self.time_data else 0
        for i in range(6):
            x_pos = self.x + i * grid_spacing_x
            x_value = (current_time - self.time_window) + (i * self.time_window / 5)
            pygame.draw.line(screen, self.BLACK, (x_pos, self.y), 
                           (x_pos, self.y + self.height), 1)
            pygame.draw.line(screen, self.BLACK, (x_pos, self.y + self.height - 5), 
                           (x_pos, self.y + self.height + 5), 2)
            # Add x-axis numbers
            x_label = self.font.render(f'{x_value:.1f}', True, self.BLACK)
            screen.blit(x_label, (x_pos - 20, self.y + self.height + 10))
    
    def _draw_axes(self, screen):
        # Draw axes with thicker lines
        pygame.draw.line(screen, self.BLACK, (self.x, self.y + self.height), 
                        (self.x + self.width, self.y + self.height), 3)  # x-axis at bottom
        pygame.draw.line(screen, self.BLACK, (self.x, self.y), 
                        (self.x, self.y + self.height), 3)
        
        # Draw arrow heads
        pygame.draw.polygon(screen, self.BLACK, [
            (self.x + self.width, self.y + self.height),  # x-axis arrow at bottom
            (self.x + self.width - 10, self.y + self.height - 5),
            (self.x + self.width - 10, self.y + self.height + 5)
        ])
        pygame.draw.polygon(screen, self.BLACK, [
            (self.x, self.y),
            (self.x - 5, self.y + 10),
            (self.x + 5, self.y + 10)
        ])
    
    def _draw_labels(self, screen, current_value):
        # Draw title at top-center
        title = self.title_font.render(self.title, True, self.BLACK)
        title_x = self.x + (self.width - title.get_width()) // 2
        screen.blit(title, (title_x, self.y - 25))
        
        # Draw current value below title
        value_text = self.font.render(f'Current: {current_value:.2f}', True, self.BLACK)
        screen.blit(value_text, (self.x + 10, self.y + 10))
        
        # Draw x-label at bottom-right corner
        x_label = self.font.render(self.x_label, True, self.BLACK)
        x_label_pos = (self.x + self.width - x_label.get_width() - 10, 
                      self.y + self.height - x_label.get_height() - 5)
        screen.blit(x_label, x_label_pos)
        
        # Draw y-label at top-right corner
        y_label = self.font.render(self.y_label, True, self.BLACK)
        y_label_pos = (self.x + self.width - y_label.get_width() - 10, 
                      self.y + 10)
        screen.blit(y_label, y_label_pos)
    
    def _plot_data(self, screen):
        # Draw setpoint line if it exists
        if self.setpoint is not None:
            # Map setpoint to y coordinate
            y_range = self.y_range[1] - self.y_range[0]
            normalized_value = (self.setpoint - self.y_range[0]) / y_range
            y = self.y + (1 - normalized_value) * self.height
            
            # Draw horizontal line across graph
            pygame.draw.line(screen, self.RED, 
                           (self.x, int(y)), 
                           (self.x + self.width, int(y)), 
                           2)

        if len(self.time_data) > 1:
            current_time = self.time_data[-1]
            start_time = current_time - self.time_window
            y_range = self.y_range[1] - self.y_range[0]
            
            points = []
            for i in range(len(self.time_data)):
                # Map time to x coordinate
                x = self.x + ((self.time_data[i] - start_time) / self.time_window) * self.width
                
                # Map value to y coordinate
                normalized_value = (self.value_data[i] - self.y_range[0]) / y_range
                y = self.y + (1 - normalized_value) * self.height
                
                # Only add points within the graph boundaries
                if self.x <= x <= self.x + self.width:
                    points.append((int(x), int(y)))
            
            # Draw lines between points if we have at least 2 points
            if len(points) > 1:
                pygame.draw.lines(screen, self.GREEN, False, points, 2)

    def _update_data(self, current_time, current_value):
        # Add new data point
        self.time_data.append(current_time)
        self.value_data.append(current_value)
        
        # Remove old data points outside the time window
        while (len(self.time_data) > 0 and 
               self.time_data[0] < current_time - self.time_window):
            self.time_data.pop(0)
            self.value_data.pop(0)
            
        # Limit the number of points to prevent memory issues
        if len(self.time_data) > self.max_points:
            step = len(self.time_data) // self.max_points
            self.time_data = self.time_data[::step]
            self.value_data = self.value_data[::step]
            
    def set_setpoint(self, value):
        """Set the setpoint value to be displayed on the graph"""
        self.setpoint = value
