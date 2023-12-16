from libraries.AI.genetic_helpers import *
import numpy as np
from copy import copy, deepcopy
import random

class v1():
    def __init__(self, genotype=None, aggregate='wsum', num_features=9, mutate=True, noise_sd=0.2, mutation_strength=0.1):
        # init my AI
        if genotype is None:
            self.genotype = np.array([random.uniform(-1, 1) for _ in range(num_features)])
        else:
            if not mutate:
                self.genotype = genotype
            else:
                # mutate given genotype
                mutation = np.array([np.random.normal(1, noise_sd) for _ in range(num_features)])
                if len(genotype) == len(mutation):
                    self.genotype = genotype * mutation
                else:
                    min_len = min(len(genotype), len(mutation))
                    self.genotype = genotype[:min_len] * mutation[:min_len]

        self.score = 0.0
        self.rel = 0.0
        self.aggregate = aggregate

    def scoreMove(self, board, aggregate='wsum'):        
        #scores the current move
        peaks = get_peaks(board)
        highestPeak = np.max(peaks)
        holes = get_holes(peaks, board)
        wells = get_wells(peaks)

        ratingVal = {
            'aggregateHeight': np.sum(peaks),
            'nHoles': np.sum(holes),
            'bumps': get_bumpiness(peaks),
            'nPits': np.count_nonzero(np.count_nonzero(board, axis=0) == 0),
            'mWells': np.max(wells),
            'nColHoles': np.count_nonzero(np.array(holes) > 0),
            'rowTrans': get_row_transition(board, highestPeak),
            'colTrans': get_col_transition(board, peaks),
            'cleared': np.count_nonzero(np.mean(board, axis=1))
        }

        weights = self.genotype
        
        if self.aggregate=='wsum':
            weights /= np.sum(weights)

        ratings = np.array([*ratingVal.values()], dtype=float)
        aggregateRating = np.dot(ratings, weights)

        return aggregateRating

        # only linear will work right now, need to extend genotype for exponents to add more
        # aggregate_funcs = {
        #     'lin': lambda gene, ratings: np.dot(ratings, gene),
        #     'exp': lambda gene, ratings: np.dot(np.array([ratings[i]**gene[i] for i in range(len(ratings))]), gene),
        #     'disp': 0
        # }

        # ratings = np.array([*rating_funcs.values()], dtype=float)
        # aggregate_rating = aggregate_funcs[aggregate](self.genotype, ratings)

        # return aggregate_rating

    def get_best_move(self, board, piece):
        #gets best move
        bX = -1000
        mX = -1000
        bP = None
        for i in range(4):
            if piece is None:
                return 
            piece = piece.get_next_rotation()
            for x in range(board.width):
                try:
                    y = board.drop_height(piece, x)
                except:
                    continue

                board_copy = deepcopy(board.board)
                for pos in piece.body:
                    board_copy[y + pos[1]][x + pos[0]] = True

                np_board = bool_to_np(board_copy)
                c = self.scoreMove(np_board)

                if c > mX:
                    mX = c
                    bX = x
                    bP = piece
                    
        return bX, bP
