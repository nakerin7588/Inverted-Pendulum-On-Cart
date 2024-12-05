import pygame
import numpy as np
from collections import deque

class graph:
    def __init__(self, x, y, width, height, title, x_label, y_label, y_range, time_window=5.0):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.title = title
        self.x_label = x_label
        self.y_label = y_label
        self.y_range = list(y_range)    # Convert to list for mutability
        self.time_window = time_window
        
        self.time_data = []
        self.value_data = []
        self.title_font = pygame.font.SysFont('Arial', 18, bold=True)  # Larger, bold font for title
        self.font = pygame.font.SysFont('Arial', 12)
        self.legend_font = pygame.font.SysFont('Arial', 12)  # Font for legend
        
        # Colors
        self.BLACK = (0, 0, 0)
        self.WHITE = (253, 254, 254)
        self.BLUE = (48, 61, 253)
        self.RED = (223, 12, 12)
        self.FRAME_BG = (240, 240, 240)  # Light gray background
        
        # Initialize empty lists for data storage
        self.time_data = []
        self.value_data = []
        self.max_points = int(time_window * 100)  # Store 100 points per second
        
        self.setpoint = None
        
        # Extract unit and name from y_label if it's in parentheses
        self.unit = ""
        self.y_name = y_label
        if "(" in y_label and ")" in y_label:
            self.unit = y_label[y_label.find("(")+1:y_label.find(")")]
            self.y_name = y_label[:y_label.find("(")].strip()  # Get name without unit and remove whitespace
        
        self.initial_y_range = y_range  # Store initial range
        self.auto_scale = True          # Enable auto-scaling by default
        self.scale_margin = 0.1         # 10% margin for auto-scaling
        self.show_all_history = False  # New flag for x-axis view mode
        self.all_time_data = []        # Store complete history
        self.all_value_data = []       # Store complete history
        
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
        
        # Draw legend after everything else
        self._draw_legend(screen)
        
    def _draw_grid(self, screen):
        grid_spacing_y = self.height / 6
        grid_spacing_x = self.width / 5
        
        # Find maximum width needed for y-axis labels
        max_width = 0
        for i in range(7):
            y_value = self.y_range[1] - (i * (self.y_range[1] - self.y_range[0]) / 6)
            y_label = self.font.render(f'{y_value:.2f}', True, self.BLACK)
            max_width = max(max_width, y_label.get_width())
        
        # Draw horizontal grid lines and y-axis numbers
        for i in range(7):
            y_pos = self.y + i * grid_spacing_y
            y_value = self.y_range[1] - (i * (self.y_range[1] - self.y_range[0]) / 6)
            pygame.draw.line(screen, self.BLACK, (self.x, y_pos), 
                           (self.x + self.width, y_pos), 1)
            pygame.draw.line(screen, self.BLACK, (self.x - 5, y_pos), 
                           (self.x + 5, y_pos), 2)
            # Right align y-axis numbers
            y_label = self.font.render(f'{y_value:.2f}', True, self.BLACK)
            label_height = y_label.get_height()
            screen.blit(y_label, (self.x - 10 - max_width, y_pos - label_height/2))
        
        # Draw vertical grid lines and x-axis numbers
        current_time = self.time_data[-1] if self.time_data else 0
        if self.show_all_history and self.all_time_data:
            start_time = self.all_time_data[0]
            time_range = current_time - start_time
        else:
            start_time = current_time - self.time_window
            time_range = self.time_window
            
        for i in range(6):
            x_pos = self.x + i * grid_spacing_x
            x_value = start_time + (i * time_range / 5)
            pygame.draw.line(screen, self.BLACK, (x_pos, self.y), 
                           (x_pos, self.y + self.height), 1)
            pygame.draw.line(screen, self.BLACK, (x_pos, self.y + self.height - 5), 
                           (x_pos, self.y + self.height + 5), 2)
            # Center x-axis numbers horizontally on the grid line
            x_label = self.font.render(f'{x_value:.2f}', True, self.BLACK)
            label_width = x_label.get_width()
            screen.blit(x_label, (x_pos - label_width/2, self.y + self.height + 10))
    
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
        
        # Draw value with frame, using y_name instead of "Current"
        value_text = self.font.render(f'{self.y_name}: {current_value:.2f} {self.unit}', True, self.BLACK)
        value_x = self.x + (self.width - value_text.get_width()) // 2
        value_y = self.y + self.height + 30
        
        # Draw frame background
        padding = 5
        frame_rect = pygame.Rect(
            value_x - padding,
            value_y - padding,
            value_text.get_width() + padding * 2,
            value_text.get_height() + padding * 2
        )
        pygame.draw.rect(screen, self.FRAME_BG, frame_rect)
        pygame.draw.rect(screen, self.BLACK, frame_rect, 1)  # Frame border
        
        # Draw value text with unit
        screen.blit(value_text, (value_x, value_y))
        
        # Draw x-label at right end of x-axis
        x_label = self.font.render(self.x_label, True, self.BLACK)
        x_label_pos = (self.x + self.width + 10,  # Move to right of axis
                      self.y + self.height - x_label.get_height()//2)  # Vertically center with axis
        screen.blit(x_label, x_label_pos)
        
        # Draw y-label at middle-left position
        y_label = self.font.render(self.y_label, True, self.BLACK)
        y_label_pos = (self.x - 75, 
                      self.y + (self.height // 2) - (y_label.get_height() // 2))
        screen.blit(y_label, y_label_pos)
    
    def _plot_data(self, screen):
        # Draw setpoint line if it exists
        if self.setpoint is not None:
            # Map setpoint to y coordinate
            y_range = self.y_range[1] - self.y_range[0]
            normalized_value = (self.setpoint - self.y_range[0]) / y_range
            y = self.y + (1 - normalized_value) * self.height
            
            # Only draw setpoint line if it's within graph boundaries
            if self.y <= y <= self.y + self.height:
                pygame.draw.line(screen, self.RED, 
                               (self.x, int(y)), 
                               (self.x + self.width, int(y)), 
                               2)

        if len(self.time_data) > 1:
            current_time = self.time_data[-1]
            if self.show_all_history and self.all_time_data:
                start_time = self.all_time_data[0]
                plot_time_data = self.all_time_data
                plot_value_data = self.all_value_data
            else:
                start_time = current_time - self.time_window
                plot_time_data = self.time_data
                plot_value_data = self.value_data
                
            time_range = current_time - start_time
            y_range = self.y_range[1] - self.y_range[0]
            
            points = []
            prev_point = None
            
            for i in range(len(plot_time_data)):
                # Map time to x coordinate
                x = self.x + ((plot_time_data[i] - start_time) / time_range) * self.width
                
                # Map value to y coordinate
                normalized_value = (plot_value_data[i] - self.y_range[0]) / y_range
                y = self.y + (1 - normalized_value) * self.height
                
                # Clip point to graph boundaries
                x = max(self.x, min(x, self.x + self.width))
                y = max(self.y, min(y, self.y + self.height))
                
                current_point = (int(x), int(y))
                
                # Only add point if it or previous point is within the graph boundaries
                if (self.x <= x <= self.x + self.width and self.y <= y <= self.y + self.height):
                    if prev_point and not (self.x <= prev_point[0] <= self.x + self.width and 
                                         self.y <= prev_point[1] <= self.y + self.height):
                        # Add previous point to connect lines properly
                        points.append(prev_point)
                    points.append(current_point)
                prev_point = current_point
            
            # Draw lines between points if we have at least 2 points
            if len(points) > 1:
                pygame.draw.lines(screen, self.BLUE, False, points, 2)

    def _update_data(self, current_time, current_value):
        # Store in complete history
        self.all_time_data.append(current_time)
        self.all_value_data.append(current_value)
        
        # Always update time_data and value_data
        self.time_data.append(current_time)
        self.value_data.append(current_value)
        
        if self.show_all_history:
            # In show all mode, time_data and value_data mirror all_time_data and all_value_data
            self.time_data = self.all_time_data
            self.value_data = self.all_value_data
        else:
            # In sliding window mode, keep only recent data
            while (len(self.time_data) > 0 and 
                   self.time_data[0] < current_time - self.time_window):
                self.time_data.pop(0)
                self.value_data.pop(0)
            
            # Limit the number of points to prevent memory issues
            if len(self.time_data) > self.max_points:
                step = len(self.time_data) // self.max_points
                self.time_data = self.time_data[::step]
                self.value_data = self.value_data[::step]

        # Auto-scale y-axis if needed
        if self.auto_scale and len(self.value_data) > 0:
            min_val = min(self.value_data)
            max_val = max(self.value_data)
            
            # Calculate margins
            range_size = max_val - min_val
            margin = range_size * self.scale_margin
            
            # Update range if value is outside current range
            if min_val < self.y_range[0] or max_val > self.y_range[1]:
                self.y_range[0] = min_val - margin
                self.y_range[1] = max_val + margin
            
            # If range becomes too small, center around the current value
            if range_size < 0.1:
                center = (min_val + max_val) / 2
                self.y_range[0] = center - 0.05
                self.y_range[1] = center + 0.05

        # Remove old data points outside the time window if not showing all history
        if not self.show_all_history:
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

    def set_auto_scale(self, enable):
        """Enable or disable auto-scaling of y-axis"""
        self.auto_scale = enable
        if not enable:
            self.y_range = list(self.initial_y_range)

    def reset_scale(self):
        """Reset y-axis to initial range"""
        self.y_range = list(self.initial_y_range)

    def set_show_all_history(self, show_all):
        """Toggle between showing all history or sliding window"""
        self.show_all_history = show_all
        if not show_all:
            # Reset the sliding window data without clearing history
            current_time = self.all_time_data[-1] if self.all_time_data else 0
            self.time_data = []
            self.value_data = []
            # Rebuild sliding window data from recent points
            for i in range(len(self.all_time_data)):
                if self.all_time_data[i] > current_time - self.time_window:
                    self.time_data.append(self.all_time_data[i])
                    self.value_data.append(self.all_value_data[i])
    
    def reset(self):
        """Clear all data points from the graph"""
        self.time_data = []
        self.value_data = []
        self.values = 0.0

    def clear_data(self):
        """Clear all stored data"""
        self.time_data = deque(maxlen=int(self.time_window * 100))
        self.value_data = deque(maxlen=int(self.time_window * 100))
        self.all_time_data = []
        self.all_value_data = []
    
    def _draw_legend(self, screen):
        # Legend box properties
        padding = 5
        box_width = 100
        box_height = 40
        line_length = 20
        
        # Position legend in top-right corner of graph
        legend_x = self.x + self.width - box_width - padding
        legend_y = self.y + padding
        
        # Draw legend background
        pygame.draw.rect(screen, self.FRAME_BG, 
                        (legend_x, legend_y, box_width, box_height))
        pygame.draw.rect(screen, self.BLACK, 
                        (legend_x, legend_y, box_width, box_height), 1)
        
        # Draw setpoint line and label
        y_pos = legend_y + padding + 5
        pygame.draw.line(screen, self.RED, 
                        (legend_x + padding, y_pos),
                        (legend_x + padding + line_length, y_pos), 2)
        text = self.legend_font.render("Setpoint", True, self.BLACK)
        screen.blit(text, (legend_x + padding + line_length + 5, y_pos - 5))
        
        # Draw real-time data line and label
        y_pos += 20
        pygame.draw.line(screen, self.BLUE, 
                        (legend_x + padding, y_pos),
                        (legend_x + padding + line_length, y_pos), 2)
        text = self.legend_font.render(self.y_name, True, self.BLACK)
        screen.blit(text, (legend_x + padding + line_length + 5, y_pos - 5))
