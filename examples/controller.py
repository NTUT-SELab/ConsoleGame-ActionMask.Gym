from env.Pacman.base_env import BaseEnv
import threading
import time


class PacmanGame(BaseEnv):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def play(self, textBox, textScore):
        self.action = 3

        threading.Thread(target=self.listener, daemon=True).start()
        self.stop = False

        self.reset()
        self.pause = False

        while (not self.is_done()):
            if self.stop:
                break

            if not self.pause:
                self.step(self.action)
                textBox.update(str(self.state_cache))
                textScore.update('Your score is ' + str(self.state_cache.score))
            else:
                textScore.update('Pause')
            time.sleep(0.5)

        if self.state_cache.isWin():
            textScore.update(f'You Win, score: {self.state_cache.score}')
        else:
            textScore.update(f'Game Over, score: {self.state_cache.score}')

        print("Your score: {}".format(self.state_cache.score))

    def listener(self):
        from pynput.keyboard import Listener, Key

        def on_press(key):
            if key == Key.up:
                self.action = 0
            elif key == Key.down:
                self.action = 1
            elif key == Key.right:
                self.action = 2
            elif key == Key.left:
                self.action = 3
            elif key == Key.esc:
                self.pause = not self.pause
            elif key == Key.delete:
                self.stop = True
                return False

        with Listener(on_press=on_press) as li:
            li.join()
