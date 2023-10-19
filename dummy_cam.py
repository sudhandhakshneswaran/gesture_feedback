import cv2
import pygame
import os
from pygame.locals import *
import pyglet

# Initialize Pygame
class Output:
    previous_file_count=0
    win = None

    def main():
        info = pygame.display.Info() # You have to call this before pygame.display.set_mode()
        screen_width,screen_height = info.current_w,info.current_h
        screen = pygame.display.set_mode((screen_width, screen_height))
        pygame.display.set_caption("TW Feedback")

        # Initialize the camera
        camera = cv2.VideoCapture(0)  # 0 represents the default camera

        # Define the font for displaying text (bold style)
        font = pygame.font.Font(None, 36)

        # Define the folder path for file counting
        folder_path = "feedback"

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
            frame = pygame.transform.scale(frame, (screen_width, screen_height))
            screen.blit(frame, (0, 0))

            # Count the files in the "feedback" folder
            feedback_folder_path = os.path.join(os.getcwd(), folder_path)
            if os.path.exists(feedback_folder_path) and os.path.isdir(feedback_folder_path):
                files = [f for f in os.listdir(feedback_folder_path) if os.path.isfile(os.path.join(feedback_folder_path, f))]
                file_count = len(files)
                if (file_count > Output.previous_file_count):
                    Output.previous_file_count = file_count
                   # Output.play_gif()
                file_text = f"Total Thumbs Up: {file_count}"
            else:
                file_text = f"Waiting for the Feedback"

            # Render and display the file count text in red with a bold style
            file_text_surface = font.render(file_text, True, (255, 0, 0))  # Red text
            screen.blit(file_text_surface, (10, 10))

            # Update the display
            pygame.display.flip()
            # camera.release()
            # pygame.quit()

    def play_gif():
        if Output.win is None:
            ag_file = "success_big.gif"
            animation = pyglet.resource.animation(ag_file)
            sprite = pyglet.sprite.Sprite(animation)

            # create a window and set it to the image size
            Output.win = pyglet.window.Window(width=sprite.width, height=sprite.height)

            # set window background color = r, g, b, alpha
            # each value goes from 0.0 to 1.0
            green = 0, 1, 0, 1
            pyglet.gl.glClearColor(*green)

            @Output.win.event
            def on_draw():
                Output.win.clear()
                sprite.draw()

            pyglet.clock.schedule_once(Output.close_pyglet, 5)
            print(pyglet.app)
            pyglet.app.run()

    def close_pyglet(dt):
        print("closing window")
        if Output.win:
            Output.win.close()
            Output.win = None

if __name__ == "__main__":
    os.environ['SDL_VIDEO_CENTERED'] = '1'
    pygame.init()
    Output.main()
