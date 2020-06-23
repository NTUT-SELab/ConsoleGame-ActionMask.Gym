from env.Pacman.base_env import BaseEnv as PacmanBaseEnv
from env.Galaxian.base_env import BaseEnv as GalaxianBaseEnv
from env.Bomberman.base_env import BaseEnv as BombermanBaseEnv
from env.MagicKey.base_env import BaseEnv as MagicKeyBaseEnv
import threading
import time


class BombermanGame(BombermanBaseEnv):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def play(self, textBox, textScore):
        self.action = 4

        threading.Thread(target=self.listener, daemon=True).start()
        self.stop = False

        self.reset()
        self.pause = False

        while (not self.is_done()):
            if self.stop:
                break

            if not self.pause:
                self.step(self.action)
                self.action = 4
                textBox.update(str(self.state))
                textScore.update('Your score is ' + str(self.state.score))
            else:
                textScore.update('Pause')

            time.sleep(0.5)

        if self.state.is_win():
            textScore.update(f'You Win, score: {self.state.score}')
        else:
            textScore.update(f'Game Over, score: {self.state.score}')

        print("Your score: {}".format(self.state.score))

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
            elif key == Key.space:
                self.action = 5
            elif key == Key.esc:
                self.pause = not self.pause
            elif key == Key.delete:
                self.stop = True
                return False

        with Listener(on_press=on_press) as li:
            li.join()


class PacmanGame(PacmanBaseEnv):

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


class GalaxianGame(GalaxianBaseEnv):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.reset()

    def play(self, textBox, textScore):
        self.action = None

        threading.Thread(target=self.listener, daemon=True).start()
        self.stop = False
        self.reset()
        self.pause = False

        while (not self.is_done()):
            if self.stop:
                break

            if not self.pause:
                self.step(self.action)
                textBox.update(str(self.map_to_string()))
                textScore.update('Your score is ' + str(self.score))
            else:
                textScore.update('Pause')
            time.sleep(0.5)

        if self.is_done():
            textScore.update(f'Game Over, score: {self.score}')

        print("Your score: {}".format(self.score))

    def listener(self):
        from pynput.keyboard import Listener, Key

        def on_press(key):
            if key == Key.left:
                self.action = 0
            elif key == Key.right:
                self.action = 1
            elif key == Key.esc:
                self.pause = not self.pause
            elif key == Key.delete:
                self.stop = True
                return False

        with Listener(on_press=on_press) as li:
            li.join()


class MagicKeyGame(MagicKeyBaseEnv):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.reset()

    def play(self, textBox, textScore):
        self.action = -1

        threading.Thread(target=self.listener, daemon=True).start()
        self.stop = False
        self.reset()
        self.pause = False

        while (not self.is_done()):
            if self.stop:
                break

            if not self.pause:
                self.step(self.action)
                textBox.update(str(self.map_to_string()))
                textScore.update('Your score is ' + str(self.score))
            else:
                textScore.update('Pause')
            time.sleep(0.5)

        if self.is_done():
            textScore.update(f'Game Over, score: {self.score}')

        print("Your score: {}".format(self.score))

    def listener(self):
        from pynput.keyboard import Listener, Key

        def on_press(key):
            try:
                if key.char == '1':
                    self.action = 26
                elif 90 >= ord(key.char.upper()) >= 65:
                    self.action = ord(key.char.upper()) - 65
            except Exception:
                self.action = -1

            if key == Key.esc:
                self.pause = not self.pause
            elif key == Key.delete:
                self.stop = True
                return False

        with Listener(on_press=on_press) as li:
            li.join()
