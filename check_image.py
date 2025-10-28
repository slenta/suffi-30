import pygame
import os

pygame.init()
IMAGEPATH = os.path.join("platformer", "assets", "images")

# Load the image
image_path = os.path.join(IMAGEPATH, "ladder", "ladder_01.png")
print(f"Checking image: {image_path}")

try:
    image = pygame.image.load(image_path)
    print(f"Original image dimensions: {image.get_width()}x{image.get_height()} pixels")
except pygame.error as e:
    print(f"Error loading image: {e}")
except FileNotFoundError:
    print("Image file not found!")
    # List available files in the ladder directory
    ladder_dir = os.path.join(IMAGEPATH, "ladder")
    if os.path.exists(ladder_dir):
        print("\nFiles in ladder directory:")
        for file in os.listdir(ladder_dir):
            print(f"- {file}")