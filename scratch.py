import cv2
import pygame
import os
import threading
from pygame.locals import *
import pyglet

# Initialize Pygame
pygame.init()

class Output:
    win = None
    def __init__(self):
        win = None

    @staticmethod
    def play_gif():
        if Output.win is None:
            ag_file = "success.gif"
            animation = pyglet.resource.animation(ag_file)
            sprite = pyglet.sprite.Sprite(animation)

            # Create a window and set it to the image size
            Output.win = pyglet.window.Window(width=sprite.width, height=sprite.height)

            # Set window background color = r, g, b, alpha
            # Each value goes from 0.0 to 1.0
            green = 0, 1, 0, 1
            pyglet.gl.glClearColor(*green)

            @Output.win.event
            def on_draw():
                Output.win.clear()
                sprite.draw()

            pyglet.clock.schedule_once(Output.close_pyglet, 5)
            pyglet.app.run()

    @staticmethod
    def close_pyglet(dt):
        print("Closing window")
        if Output.win:
            Output.win.close()
            Output.win = None

    @staticmethod
    def main():
        screen_width, screen_height = 800, 600
        screen = pygame.display.set_mode((screen_width, screen_height))
        pygame.display.set_caption("Camera and File Count")

        # Initialize the camera
        camera = cv2.VideoCapture(0)  # 0 represents the default camera

        # Define the font for displaying text (bold style)
        font = pygame.font.Font(None, 36)

        # Define the folder path for file counting
        folder_path = "feedback"

        # Global variable to track the previous file count
        previous_file_count = 0

        # Function to count files in the "feedback" folder
        def count_files():
            feedback_folder_path = os.path.join(os.getcwd(), folder_path)
            if os.path.exists(feedback_folder_path) and os.path.isdir(feedback_folder_path):
                files = [f for f in os.listdir(feedback_folder_path) if os.path.isfile(os.path.join(feedback_folder_path, f))]
                return len(files)
            else:
                return 0

        # Function to check for file count change and play GIF
        def check_and_play_gif():
            nonlocal previous_file_count
            while True:
                file_count = count_files()
                if file_count != previous_file_count:
                    previous_file_count = file_count
                    Output.play_gif()

        # Start a thread to check for file count change and play GIF
        file_count_thread = threading.Thread(target=check_and_play_gif)
        file_count_thread.daemon = True
        file_count_thread.start()

        # Main game loop
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == QUIT:
                    running = False

            # Capture a frame from the camera
            ret, frame = camera.read()

            frame = cv2.rotate(frame, cv2.ROTATE_90_COUNTERCLOCKWISE)

            # Convert the frame to a Pygame surface
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            frame = pygame.surfarray.make_surface(frame)

            # Clear the screen
            screen.fill((0, 0, 0))

            # Display the camera frame
            screen.blit(frame, (0, 0))

            # Count the files in the "feedback" folder and display the count
            file_count = count_files()
            file_text = f"Total files in '{folder_path}': {file_count}"

            # Render and display the file count text in red with a bold style
            file_text_surface = font.render(file_text, True, (255, 0, 0))  # Red text
            screen.blit(file_text_surface, (10, 10))

            # Update the display
            pygame.display.flip()

        # Release the camera and quit Pygame
        camera.release()
        pygame.quit()

if __name__ == "__main__":
    Output.main()
