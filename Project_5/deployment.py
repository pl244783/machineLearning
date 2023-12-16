from versionHistory.v1 import v1
from multiprocessing import Pool
from libraries.game import Game
import random
import numpy as np
import joblib

def runGame():
    i = joblib.load('v1/5/v1g00009.joblib')
    game = Game(mode="tetrisAI", agent=i)
    dropped, cleared = game.run()
    #print(f'Dropped: {dropped}, Cleared: {cleared}')

runGame()