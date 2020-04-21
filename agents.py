#################################################################################
#
# agents.py
#
# Player class is inherited by game players
#
# Human's choose their moves via the command line
#
# RandomAgent's choose their moves at random from the available moves
#
# IntelligentAgent's will use a neural network to predict the best next move
#
#################################################################################
import random
from model import NNet
import numpy as np


class Player:
    def __init__(self, number):
        """

        :param number: players token number, what they place on the board
        """
        self.number = number
        self.turns = []

    def choose_move(self, available, board_state):
        pass

    def learn(self, states, policies, winners):
        pass

    def add_winners(self, win):
        for turn in self.turns:
            turn += [win]


class Human(Player):
    def choose_move(self, available, board_state):
        """
        Retrieves user input, verifies column number has an available space, and places that piece
        :param available:
        :param board_state:
        :return: none, but place pieces in board
        """

        print(f"Can place a piece at: {available}")
        choice = int(input("Column: "))
        while choice not in available:
            print("That column is full")
            choice = int(input("Column: "))
        return choice - 1, [1 / 7, 1 / 7, 1 / 7, 1 / 7, 1 / 7, 1 / 7, 1 / 7]


class RandomAgent(Player):
    def choose_move(self, available, board_state):
        return int(random.choice(available))-1, [(1 / len(available)) if i in available else 0 for i in range(1, 8)]


class IntelligentAgent(Player):
    def __init__(self, number):
        self.network = NNet()
        self.trained = False
        super().__init__(number)

    def choose_move(self, available, board_state):
        if self.trained:
            results = self.network.model.predict([(np.array(board_state)).reshape((1, 6, 7))])
            policy_output, value = results
            # print(f"Policy: {policy_output}")
            # print(f"Value: {value}")
            policy = policy_output[0]
            for item in np.argsort(policy)[::-1]:
                if item+1 in available:
                    choice = item
                    break
            if (choice + 1) not in available:
                print(f"Snapshot: {choice}, {available}")
                # raise ValueError
                choice = int(random.choice(available)) - 1
                print("net chose a move that is unavailable")
                # TODO: figure out how to prevent network from choosing unavailable move
            return choice, policy
        else:
            choice = int(random.choice(available)) - 1
            return choice, [(1 / len(available)) if i in available else 0 for i in range(1, 8)]

    def learn(self, states, policies, winners):
        self.network.train_on_batch(states, policies, winners)
        if self.trained is False:
            self.trained = True
            print("HAS BEEN TRAINED")
