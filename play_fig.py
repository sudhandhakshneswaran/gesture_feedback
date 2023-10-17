import pyglet


class playGig:
    def main(self):
        self.lock = threading.Lock()
        ag_file = "success.gif"
        play(self)
        
    def play(self):
        animation = pyglet.resource.animation(ag_file)
        sprite = pyglet.sprite.Sprite(animation)

        # create a window and set it to the image size
        win = pyglet.window.Window(width=sprite.width, height=sprite.height)

        # set window background color = r, g, b, alpha
        # each value goes from 0.0 to 1.0
        green = 0, 1, 0, 1
        pyglet.gl.glClearColor(*green)

        @win.event
        def on_draw():
            win.clear()
            sprite.draw()

        def close_pyglet(self, dt):
                pyglet.app.exit()

        pyglet.clock.schedule_once(close_pyglet, 5)
        pyglet.app.run()    

if __name__ == "__main__":
    playGig.main()