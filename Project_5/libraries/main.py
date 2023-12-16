from libraries.game import Game
import sys
import os

def main():
    for i in range(2):
        print(i)
        g = Game(sys.argv[1])
        dropped, rows = g.run_no_visual()
    # g = Game(sys.argv[1])
    g.run_no_visual()
    g.run()


if __name__ == "__main__":
    main()
