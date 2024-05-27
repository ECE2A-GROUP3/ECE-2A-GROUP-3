import sys
import pygame
import math
import random
import customtkinter as ctk

# Constants
WIDTH, HEIGHT = 1150, 800
BACKGROUND_COLOR = (30, 30, 30)  # Dark gray
WHITE = (255, 255, 255)
RED = (255, 100, 100)
BLUE = (100, 100, 255)
PARTICLE_RADIUS = 30
ELECTRIC_CONSTANT = 9e9  # Adjust as needed
FIELD_LINE_LENGTH = 90  # Length of field lines
FIELD_LINE_STEP = 25  # Step size for drawing field lines
MIN_DISTANCE = 5  # Minimum distance between particles with opposite charges
TIME_STEP = 0.1  # Time step for smoother animation


class Particle:
    def __init__(self, x, y, charge):
        self.x = x
        self.y = y
        self.charge = charge
        self.vx = random.uniform(-1, 1) * 2
        self.vy = random.uniform(-1, 1) * 2

    def draw(self, screen):
        if self.charge > 0:
            color = RED
        else:
            color = BLUE
        pygame.draw.circle(screen, color, (int(self.x), int(self.y)), PARTICLE_RADIUS)
        font = pygame.font.SysFont(None, 14)
        charge_text = font.render(f"{self.charge} C", True, WHITE)
        text_rect = charge_text.get_rect(center=(self.x, self.y))
        screen.blit(charge_text, text_rect)

    def calculate_force(self, other_particle):
        dx = other_particle.x - self.x
        dy = other_particle.y - self.y
        distance = max(math.sqrt(dx ** 2 + dy ** 2), 1)  # Avoid division by zero
        force_magnitude = ELECTRIC_CONSTANT * abs(self.charge * other_particle.charge) / (distance ** 2)
        angle = math.atan2(dy, dx)

        # Change direction of force if charges have opposite signs
        if self.charge * other_particle.charge < 0:
            force_x = force_magnitude * math.cos(angle)
            force_y = force_magnitude * math.sin(angle)
        else:
            force_x = -force_magnitude * math.cos(angle)
            force_y = -force_magnitude * math.sin(angle)

        return force_x, force_y

    def update_position(self, forces, particles):
        if not forces:  # Check if forces list is empty
            return

        total_force_x = sum(force[0] for force in forces)
        total_force_y = sum(force[1] for force in forces)

        # Adjust velocity based on the total force
        self.vx += total_force_x * TIME_STEP
        self.vy += total_force_y * TIME_STEP

        # Limit velocity to avoid particles from moving too fast
        self.vx = min(max(self.vx, -5), 5)
        self.vy = min(max(self.vy, -5), 5)

        # Update position
        new_x = self.x + self.vx * TIME_STEP
        new_y = self.y + self.vy * TIME_STEP

        # Limit position to screen boundaries
        new_x = min(max(new_x, 0), WIDTH)
        new_y = min(max(new_y, 0), HEIGHT)

        # Update position only if the new position respects the screen boundaries
        self.x = new_x
        self.y = new_y

        # Check if the distance between particles is less than the minimum distance for repulsion
        for other_particle in particles:
            if other_particle != self:
                dx = other_particle.x - self.x
                dy = other_particle.y - self.y
                distance = math.sqrt(dx ** 2 + dy ** 2)
                max_distance = MIN_DISTANCE + PARTICLE_RADIUS * 2  # Minimum distance + sum of radii
                if distance < max_distance:
                    # Compute the vector from other_particle to self
                    delta_x = self.x - other_particle.x
                    delta_y = self.y - other_particle.y

                    # Normalize the vector
                    magnitude = math.sqrt(delta_x ** 2 + delta_y ** 2)
                    delta_x /= magnitude
                    delta_y /= magnitude

                    # Scale the vector to the maximum distance
                    delta_x *= max_distance
                    delta_y *= max_distance

                    # Update the position to the final vector magnitude
                    self.x = other_particle.x + delta_x
                    self.y = other_particle.y + delta_y


def calculate_field_at_point(particles, x, y):
    total_field_x = 0
    total_field_y = 0
    for particle in particles:
        dx = x - particle.x
        dy = y - particle.y
        distance = max(math.sqrt(dx ** 2 + dy ** 2), 1)  # Avoid division by zero
        field_magnitude = ELECTRIC_CONSTANT * particle.charge / (distance ** 2)
        angle = math.atan2(dy, dx)
        field_x = field_magnitude * math.cos(angle)
        field_y = field_magnitude * math.sin(angle)
        total_field_x += field_x
        total_field_y += field_y
    return total_field_x, total_field_y


def draw_field_lines(screen, particles):
    for x in range(0, WIDTH, FIELD_LINE_STEP):
        for y in range(0, HEIGHT, FIELD_LINE_STEP):
            field_x, field_y = calculate_field_at_point(particles, x, y)
            field_magnitude = math.sqrt(field_x ** 2 + field_y ** 2)
            if field_magnitude > 0:
                line_color = (150, 150, 150)  # Default color for field lines
                if field_x * field_y > 0:
                    line_color = (150, 150, 150)
                else:
                    line_color = (150, 150, 150)
                field_line_end_x = x + (field_x / field_magnitude) * FIELD_LINE_LENGTH
                field_line_end_y = y + (field_y / field_magnitude) * FIELD_LINE_LENGTH
                pygame.draw.line(screen, line_color, (x, y), (field_line_end_x, field_line_end_y), 1)
                if field_magnitude > 1:  # Only draw arrowhead if field strength is significant
                    # Calculate arrowhead points
                    arrowhead_size = 5
                    angle = math.atan2(field_y, field_x)
                    arrow_point1 = (
                        int(field_line_end_x - arrowhead_size * math.cos(angle - math.pi / 6)),
                        int(field_line_end_y - arrowhead_size * math.sin(angle - math.pi / 6))
                    )
                    arrow_point2 = (
                        int(field_line_end_x - arrowhead_size * math.cos(angle + math.pi / 6)),
                        int(field_line_end_y - arrowhead_size * math.sin(angle + math.pi / 6))
                    )
                    # Draw arrowhead
                    pygame.draw.polygon(screen, line_color, (arrow_point1, arrow_point2, (field_line_end_x, field_line_end_y)))


def add_particle(particle_list, charge, x, y):
    particle_list.append(Particle(x, y, charge))


def calculate_field_at_point(particles, x, y):
    total_field_x = 0
    total_field_y = 0
    for particle in particles:
        dx = x - particle.x
        dy = y - particle.y
        distance = max(math.sqrt(dx ** 2 + dy ** 2), 1)  # Avoid division by zero
        field_magnitude = ELECTRIC_CONSTANT * particle.charge / (distance ** 2)
        angle = math.atan2(dy, dx)
        field_x = field_magnitude * math.cos(angle)
        field_y = field_magnitude * math.sin(angle)
        total_field_x += field_x
        total_field_y += field_y
    return total_field_x, total_field_y

def draw_field_lines(screen, particles):
    for x in range(0, WIDTH, FIELD_LINE_STEP):
        for y in range(0, HEIGHT, FIELD_LINE_STEP):
            field_x, field_y = calculate_field_at_point(particles, x, y)
            field_magnitude = math.sqrt(field_x ** 2 + field_y ** 2)
            if field_magnitude > 0:
                line_color = (150, 150, 150)
                field_line_end_x = x + (field_x / field_magnitude) * FIELD_LINE_LENGTH
                field_line_end_y = y + (field_y / field_magnitude) * FIELD_LINE_LENGTH
                pygame.draw.line(screen, line_color, (x, y), (field_line_end_x, field_line_end_y), 1)
                if field_magnitude > 1:
                    arrowhead_size = 5
                    angle = math.atan2(field_y, field_x)
                    arrow_point1 = (
                        int(field_line_end_x - arrowhead_size * math.cos(angle - math.pi / 6)),
                        int(field_line_end_y - arrowhead_size * math.sin(angle - math.pi / 6))
                    )
                    arrow_point2 = (
                        int(field_line_end_x - arrowhead_size * math.cos(angle + math.pi / 6)),
                        int(field_line_end_y - arrowhead_size * math.sin(angle + math.pi / 6))
                    )
                    pygame.draw.polygon(screen, line_color, (arrow_point1, arrow_point2, (field_line_end_x, field_line_end_y)))

def add_particle(particle_list, charge, x, y):
    particle_list.append(Particle(x, y, charge))

def create_input_fields():
    root = ctk.CTk()
    root.title("Particle Input")
    root.geometry("400x1000")

    charges = []
    xs = []
    ys = []

    charge_entries = []
    x_entries = []
    y_entries = []

    def process_input():
        nonlocal charges, xs, ys
        charges = []
        xs = []
        ys = []
        for i in range(3):
            charge = charge_entries[i].get()
            x = x_entries[i].get()
            y = y_entries[i].get()

            if charge and x and y:
                charges.append(float(charge))
                xs.append(float(x))
                ys.append(float(y))
        root.destroy()

    # Adding description and instructions on the left side
    description_frame = ctk.CTkFrame(root)
    description_frame.pack(pady=10, padx=20, fill="x")

    description_label = ctk.CTkLabel(description_frame, text="Electrostatic Simulator\n\nEnter charges and positions\nfor up to 3 particles.\n\nCharges can be positive or negative.\nPositions should be within the screen bounds.", justify="left")
    description_label.pack(pady=10)

    input_frame = ctk.CTkFrame(root)
    input_frame.pack(pady=1, padx=20, fill="both", expand=True)

    for i in range(3):
        frame = ctk.CTkFrame(input_frame)
        frame.pack(pady=5, fill="x")

        charge_label = ctk.CTkLabel(frame, text=f"Charge {i + 1} :", anchor="w")
        charge_label.pack(fill="x", padx=5, pady=1)
        charge_entry = ctk.CTkEntry(frame)
        charge_entry.pack(fill="x", padx=5, pady=1)

        x_label = ctk.CTkLabel(frame, text=f"X {i + 1} :", anchor="w")
        x_label.pack(fill="x", padx=5, pady=1)
        x_entry = ctk.CTkEntry(frame)
        x_entry.pack(fill="x", padx=5, pady=1)

        y_label = ctk.CTkLabel(frame, text=f"Y {i + 1} :", anchor="w")
        y_label.pack(fill="x", padx=5, pady=1)
        y_entry = ctk.CTkEntry(frame)
        y_entry.pack(fill="x", padx=5, pady=1)

        charge_entries.append(charge_entry)
        x_entries.append(x_entry)
        y_entries.append(y_entry)

    button_frame = ctk.CTkFrame(root)
    button_frame.pack(pady=20, fill="x")

    ok_button = ctk.CTkButton(button_frame, text="OK", command=process_input)
    ok_button.pack(pady=10)

    root.mainloop()

    return charges, xs, ys





def draw_info_panel(screen, particles):
    info_panel_width = 400
    info_panel_height = HEIGHT
    info_panel_bg_color = (50, 50, 50)
    info_panel_text_color = WHITE
    border_color = (100, 100, 100)  # Border color
    font = pygame.font.SysFont(None, 20)

    # Draw background rectangle for the info panel
    pygame.draw.rect(screen, info_panel_bg_color, (WIDTH, 0, info_panel_width, info_panel_height))

    # Draw border around the info panel
    pygame.draw.rect(screen, border_color, (WIDTH, 0, info_panel_width, info_panel_height), 2)

    # Draw title
    title_font = pygame.font.SysFont(None, 24)
    title_text = title_font.render("ELECTROSTATIC  SIMULATOR", True, WHITE)
    title_text_rect = title_text.get_rect(center=(WIDTH + info_panel_width / 2, 30))
    screen.blit(title_text, title_text_rect)

    # Draw text for each particle's properties
    text_y = 70  # Adjusted starting Y position
    for i, particle in enumerate(particles):
        # Draw border around each particle's information
        pygame.draw.rect(screen, border_color, (WIDTH + 10, text_y - 5, info_panel_width - 20, 50), 1)

        charge_text = f"Particle {i + 1} Charge: {particle.charge} C"
        charge_surface = font.render(charge_text, True, info_panel_text_color)
        screen.blit(charge_surface, (WIDTH + 20, text_y))

        position_text = f"Position: ({int(particle.x)}, {int(particle.y)})"
        position_surface = font.render(position_text, True, info_panel_text_color)
        screen.blit(position_surface, (WIDTH + 20, text_y + 20))

        # Add any additional information here
        # For example, you can include velocity, acceleration, or any other relevant information

        text_y += 90# Increase the spacing between particle information

    # Draw buttons
    button_font = pygame.font.SysFont(None, 20)
    button_width = 100
    button_height = 30
    button_color = (70, 70, 70)
    pygame.draw.rect(screen, button_color, (WIDTH + info_panel_width / 2 - button_width / 2, HEIGHT - 80, button_width, button_height))
    pygame.draw.rect(screen, button_color, (WIDTH + info_panel_width / 2 - button_width / 2 - 120, HEIGHT - 80, button_width, button_height))
    pygame.draw.rect(screen, button_color, (WIDTH + info_panel_width / 2 - button_width / 2 + 120, HEIGHT - 80, button_width, button_height))
    pygame.draw.rect(screen, button_color, (WIDTH + info_panel_width / 2 - button_width / 2, HEIGHT - 40, button_width, button_height))


    pause_text = button_font.render("Pause", True, WHITE)
    start_text = button_font.render("Reset", True, WHITE)
    reset_text = button_font.render("Run", True, WHITE)
    close_text = button_font.render("Close", True, WHITE)


    screen.blit(pause_text, (WIDTH + info_panel_width / 2 - button_width / 2 + 20, HEIGHT - 70))
    screen.blit(start_text, (WIDTH + info_panel_width / 2 - button_width / 2 - 100, HEIGHT - 70))
    screen.blit(reset_text, (WIDTH + info_panel_width / 2 - button_width / 2 + 140, HEIGHT - 70))
    screen.blit(close_text, (WIDTH + info_panel_width / 2 - button_width / 2 + 20, HEIGHT - 30))


def run_simulation():
    charges, xs, ys = create_input_fields()  # Get input before initializing Pygame
    pygame.init()
    screen = pygame.display.set_mode((WIDTH + 400, HEIGHT))  # Adjusted screen width
    clock = pygame.time.Clock()

    particles = [Particle(x, y, charge) for charge, x, y in zip(charges, xs, ys)]
    paused = False  # Flag to control pause/resume state
    while True:
        screen.fill(BACKGROUND_COLOR)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:  # Pause/Resume simulation
                    paused = not paused
                elif event.key == pygame.K_r:  # Reset simulation
                    charges, xs, ys = create_input_fields()
                    particles = [Particle(x, y, charge) for charge, x, y in zip(charges, xs, ys)]
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Left mouse button clicked
                    mouse_x, mouse_y = event.pos
                    if WIDTH + 120 <= mouse_x <= WIDTH + 220 and HEIGHT - 80 <= mouse_y <= HEIGHT - 50:
                        paused = True
                    elif WIDTH + 240 <= mouse_x <= WIDTH + 340 and HEIGHT - 80 <= mouse_y <= HEIGHT - 50:
                        paused = False
                    elif WIDTH + 0 <= mouse_x <= WIDTH + 100 and HEIGHT - 80 <= mouse_y <= HEIGHT - 50:
                        charges, xs, ys = create_input_fields()
                        particles = [Particle(x, y, charge) for charge, x, y in zip(charges, xs, ys)]
                    elif WIDTH + 120 <= mouse_x <= WIDTH + 220 and HEIGHT - 40 <= mouse_y <= HEIGHT - 10:
                        exit()
                        return

        if not paused:
            # Calculate forces
            forces = []
            for i, particle in enumerate(particles):
                particle_forces = []
                for j, other_particle in enumerate(particles):
                    if i != j:  # Don't calculate force with itself
                        force_x, force_y = particle.calculate_force(other_particle)
                        particle_forces.append((force_x, force_y))

                forces.append(particle_forces)

            # Update particle positions
            for particle, force in zip(particles, forces):
                particle.update_position(force, particles)

        # Draw electric field lines
        draw_field_lines(screen, particles)

        # Draw particles
        for particle, force in zip(particles, forces):
            particle.draw(screen)

        # Draw information panel
        draw_info_panel(screen, particles)

        pygame.display.flip()
        clock.tick(60)

if __name__ == "__main__":
    run_simulation()

