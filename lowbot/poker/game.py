from lowbot.poker.deck import *
from lowbot.poker.hands import Hand


DRAW = 100
TERMINAL = 111
ONGOING = 112
CAP = 113
NUM_PLAYERS = 2


class Game(object):

    def __init__(self, num_cards=13, num_suits=4, num_draws=0, hand_size=5, cap=3):
        self.History = "r"
        self.Deck = Deck(num_cards=num_cards, num_suits=num_suits)
        self.Hands = []
        self.NumDraws = num_draws
        self.DrawCount = 0
        self.LastCard = 0
        self.Pots = [0.5, 1.]
        self.State = ONGOING
        self.Cap = cap
        self.Winner = -1
        self.Bet = 1

        self._deal_cards(hand_size)

    def get_current_player(self):
        last_round = self.History.split("-")[-1]
        plays = len(''.join(i for i in last_round if not i.isdigit()))
        player = 1 - (plays % 2)
        return player

    def get_winner(self):
        return self.Winner

    def perform_action(self, action, indices=None):

        last_round = self.History.split("-")[-1]
        plays = len(''.join(i for i in last_round if not i.isdigit()))
        player = 1 - (plays % 2)

        if action == "f":
            self.History += "f"
        elif action == "c":
            self.Pots[player] = self.Pots[1-player]
            self.History += "c"
        elif action == "r":
            self.Pots[player] = self.Pots[1-player] + self.Bet
            self.History += "r"
        elif action == "d":
            cards = self.Deck.Cards[self.LastCard:self.LastCard + len(indices)]
            self.LastCard += len(indices)
            self.Hands[player].draw(indices, cards)
            self.History += "d" + str(len(indices))

        self._update_state()

    def get_legal_actions(self):

        if self.State == DRAW:
            return "d"
        elif self.State == TERMINAL:
            return ""
        elif self.State == ONGOING:
            return "fcr"
        elif self.State == CAP:
            return "fc"

    def _deal_cards(self, hand_size):
        self.Deck.shuffle()
        self.Hands = [Hand(self.Deck.Cards[0:hand_size]), Hand(self.Deck.Cards[hand_size:2*hand_size])]
        self.LastCard += 2*hand_size

    def _update_state(self):
        # WARNING: ONLY WORK PROPERLY WHEN TRIGGERED AFTER ACTION

        last_round = self.History.split("-")[-1]
        plays = len(''.join(i for i in last_round if not i.isdigit()))
        player = 1 - (plays % 2)
        old_state = self.State

        if "d" in last_round:
            if last_round.count("d") == NUM_PLAYERS:
                self.State = ONGOING
            else:
                self.State = DRAW

        else:
            if last_round[-1] == "f":
                self.State = TERMINAL
                self.Winner = player

            elif plays > 1:
                if last_round[-1] == "c":
                    if plays == 2 and self.DrawCount == 0:
                        self.State = ONGOING
                    else:
                        if self.DrawCount < self.NumDraws:
                            self.State = DRAW
                        else:
                            self.State = TERMINAL
                            better_hand = self.Hands[player].compare(self.Hands[1-player])
                            if better_hand == 1:
                                self.Winner = player
                            elif better_hand == -1:
                                self.Winner = 1 - player
                            else:
                                self.Winner = 2

                elif last_round[-1] == "r":
                    if last_round.count("r") < self.Cap:
                        self.State = ONGOING
                    else:
                        self.State = CAP

            else:
                self.State = ONGOING

        if (self.State - old_state)**2 > 25:
            self.History += "-"
            if self.State == DRAW:
                self.DrawCount += 1

