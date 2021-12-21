import itertools
import threading
import sys
import time


def loading(function):
    def wrapper():
        done = False

        def animate():
            """Animated ASCII loading in termminal"""
            SPEED = 1  # Int 1 - 10
            LINE = '\rLoading '

            frames = [
                ["⡏ ", "⡗ ", "⡧ ", "⣇ ", "⣸ ", "⢼ ", "⢺ ", "⢹ "],
                ['bq', 'dp', 'qb', 'pd'],
                ['bo', 'do', 'ob', 'od', 'oq', 'op', 'qo', 'po'],
                ["⣷", "⣯", "⣟", "⡿", "⢿", "⣻", "⣽", "⣾"],
            ]

            CHOICE = 0  # Int 0 - 3
            for frame in itertools.cycle(frames[CHOICE]):

                if done:
                    break
                sys.stdout.write(LINE + frame)
                sys.stdout.flush()
                time.sleep(1 / SPEED / 10)
            sys.stdout.write('\rDone!' + ' ' * (len(LINE) + 2))

        thread = threading.Thread(target=animate)
        thread.start()

        function()

        done = True
    return wrapper
