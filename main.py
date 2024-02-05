#!/usr/bin/python3

import sys

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
    
    def compare(self, card):
        return card == self.stringify()

class Hand:
    def __init__(self, cards) -> None:
        self.cards = cards

    def stringify_hand(self):
        string = ""
        for card in self.cards:
            string += f"{card.stringify()} "
        return string

    def remove(self, played):
        for card in self.cards:
            if card.compare(played):
                self.cards.remove(card)
                return


hand = None
turn = 0
player = ""
teammate = 0
trick = []
played = []
bids = [0, 0, 0, 0]
bidWinner = 0

while (line := input().split())[0] != "end":
    print(line, file=sys.stderr)

    match line[0]:
        case "player":
            player = line[1]
            teammate = int(player) + 2 % 4
            print(f"player number {player}, teammate {teammate}\n", file=sys.stderr)

        case "hand":
            hand = Hand([Card(card) for card in line[1:]])
            print(f"hand: {hand.stringify_hand()}\n", file=sys.stderr)

        case "bid":
            if line[1] == "?":
                print(0)
            else:
                bid = int(line[2])
                bids[int(line[1])] = bid
                if bid:
                    bidWinner = line[1]

        case "card":
            if line[1] == "?":
                print(0)
            else:
                turn = (turn + 1) % 4
                card = line[2]
                trick.append(card)
                print(f"trick: {trick}\n", file=sys.stderr)
                if not turn: #turn == 0
                    played.extend(trick)
                    trick = []
                if line[1] == player:
                    hand.remove(card)
                    print(f"hand: {hand.stringify_hand()}\n", file=sys.stderr)
    
