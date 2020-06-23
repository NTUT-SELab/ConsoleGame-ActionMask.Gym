import PySimpleGUI as sg
import sys
import threading
import subprocess
import webbrowser
import time
sys.path.append('./')

from examples.controller import PacmanGame, GalaxianGame, BombermanGame, MagicKeyGame


class UI:

    def __init__(self):
        sg.theme('DarkAmber')
        self.sg = sg
        self.layout()
        window2_active = False
        train_active = False

        while True:
            ev1, vals1 = self.window.Read(timeout=100)
            if ev1 in (None, 'Cancel'):  # if user closes window or clicks cancel
                break
            if ev1 == 'Play' and not window2_active:
                window2_active = True
                self.window.Hide()
                self.play(vals1[0])
                while True:
                    ev2, vals2 = self.window2.Read()
                    if ev2 in (None, 'Cancel'):  # if user closes window or clicks cancel
                        self.window2.close()
                        window2_active = False
                        self.window.UnHide()
                        break

            if ev1 == 'Train' and not train_active:
                self.train()
                self.window.Hide()
                sg.popup('Opened in browser, close it?')
                self.window.UnHide()
                self.close()

        self.window.close()

    def layout(self):
        self.window = sg.Window(
            'ConsoleGame-ActionMask',
            [[sg.Combo(['Pacman', 'Galaxian', 'Bomberman', 'MagicKey'], default_value='Pacman')],
             [sg.Button('Play'), sg.Button('Train')]]
        )

    def play(self, game='Pacman'):
        if game == 'Pacman':
            game = PacmanGame()
            self.text_box = sg.Text(str(game.state_cache), font='Courier 10', key='-BOX-')
            self.text_score = sg.Text('Your score is 0                           ', key='-SCORE-')
            self.window2 = sg.Window('PacmanGame', [[self.text_box], [self.text_score]])
            threading.Thread(target=game.play, args=(self.text_box, self.text_score), daemon=True).start()
        elif game == 'Galaxian':
            game = GalaxianGame()
            self.text_box = sg.Text(str(game.map_to_string()), font='Courier 10', key='-BOX-')
            self.text_score = sg.Text('Your score is 0                           ', key='-SCORE-')
            self.window2 = sg.Window('Galaxian', [[self.text_box], [self.text_score]])
            threading.Thread(target=game.play, args=(self.text_box, self.text_score), daemon=True).start()
        elif game == 'Bomberman':
            game = BombermanGame()
            self.text_box = sg.Text(str(game.state), font='Courier 10', key='-BOX-')
            self.text_score = sg.Text('Your score is 0                           ', key='-SCORE-')
            self.window2 = sg.Window('BombermanGame', [[self.text_box], [self.text_score]])
            threading.Thread(target=game.play, args=(self.text_box, self.text_score), daemon=True).start()
        elif game == 'MagicKey':
            game = MagicKeyGame()
            self.text_box = sg.Text(str(game.map_to_string()), font='Courier 10', key='-BOX-')
            self.text_score = sg.Text('Your score is 0                           ', key='-SCORE-')
            self.window2 = sg.Window('MagicKey', [[self.text_box], [self.text_score]])
            threading.Thread(target=game.play, args=(self.text_box, self.text_score), daemon=True).start()

    def train(self, game="Pacman"):
        if game == "Pacman":
            subprocess.Popen(
                'bash ./scripts/run_docker_train.sh python examples/Pacman/PPO2/run_action_mask_env.py', shell=True
            )
        elif game == 'Galaxian':
            pass

        time.sleep(3)
        webbrowser.open("http://localhost:6006")

    def close(self):
        subprocess.Popen('bash -c ./scripts/stop_docker.sh', shell=True)


if __name__ == '__main__':
    UI()
