import pygame

pygame.init()
screen = pygame.display.set_mode((800, 600))

# Load the sprite sheet image
sprite_sheet = pygame.image.load("explosion.png")
# Define the dimensions of each animation frame
frame_width = 95
frame_height = 95

# Define the number of frames in each row and column of the sprite sheet
frames_per_row = 4
frames_per_column = 1

# Calculate the total number of frames
total_frames = frames_per_row * frames_per_column

# Create a list to store each individual frame
frames = []

# Extract each frame from the sprite sheet
for row in range(frames_per_column):
    for col in range(frames_per_row):
        x = col * frame_width
        y = row * frame_height
        rect = pygame.Rect(x, y, frame_width, frame_height)
        frame_image = pygame.Surface(rect.size).convert()
        frame_image.blit(sprite_sheet, (0, 0), rect)
        frames.append(frame_image)

current_frame = 0
animation_delay = 100  # Delay between frames in milliseconds
last_update = pygame.time.get_ticks()

running = True
clock = pygame.time.Clock()

while running:
    clock.tick(60)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Update the animation
    if pygame.time.get_ticks() - last_update > animation_delay:
        current_frame = (current_frame + 1) % total_frames
        last_update = pygame.time.get_ticks()

    # Draw the current frame
    screen.fill((255, 255, 255))
    screen.blit(frames[current_frame], (0, 0))
    pygame.display.flip()

pygame.quit()