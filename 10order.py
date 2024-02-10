#!/usr/bin/python3

import random

class Card:
    def __init__(self, name) -> None:
        self.suit = name[0]
        self.value = name[1]
        match self.value:
            case "5":
                self.points = 5
            case "T" | "A":
                self.points = 10
            case _:
                self.points = 0

    def stringify(self):
        return f"{self.suit}{self.value}"
    
    def equals(self, card):
        return card == self.stringify()


class Hand:
    def __init__(self, cards) -> None:
        self.cards = cards

    def stringify(self):
        string = ""
        for card in self.cards:
            string += f"{card.stringify()} "
        return string

    def remove(self, played):
        for card in self.cards:
            if card.equals(played):
                self.cards.remove(card)
                return
    
    def playable(self, trick):
        playable = []
        for card in self.cards:
            if card.suit == trick.required:
                playable.append(card)
        if not playable:
            playable = [card for card in self.cards]
        return playable
    

class Trick:
    def __init__(self) -> None:
        self.played = {}
        self.required = None

    def stringify(self):
        string = ""
        for player in self.played:
            string += f"{self.played[player].stringify()} "
        return string
    
    def getCards(self):
        return [self.played[player] for player in self.played]

    def add(self, player, card):
        if not self.played:
            self.required = card.suit
        self.played[player] = card

    def empty(self):
        self.played.clear()
        self.required = None        


hand = None
bid = 0
turn = 0
trick = Trick()

while (line := input().split())[0] != "end":

    match line[0]:
        case "player":
            player = line[1]

        case "hand":
            new_game = True
            hand = Hand([Card(card) for card in line[1:]])

        case "bid":
            if line[1] == "?":

                # Bid 1/3 times
                if random.random() < 0.33:
                    print(bid + 5 if bid else 50)
                else:
                    print(0)

            else:
                bid = int(line[2])

        case "card":

            #Play random playable card
            if line[1] == "?":
                print(random.choice(hand.playable(trick)).stringify())

            else:
                turn = (turn + 1) % 4
                card = line[2]
                trick.add(int(line[1]), Card(card))

                if not turn: #turn == 0
                    trick.empty()
                if line[1] == player:
                    hand.remove(card)
    
