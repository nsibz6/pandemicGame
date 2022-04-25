import random
from game_data import all_cities

class Infection_Deck:
  def __init__(self, all_cities):
    self.infection_cards = {city: colour for colour, cities in all_cities.items() for city in cities}
    self.shuffled_deck = [city for colour, cities in all_cities.items() for city in cities]
    self.discard_pile = []
    self.out_of_the_game = []
    random.shuffle(self.shuffled_deck)

# To view out of the game cards

  def view_out_of_game_cards(self):
    return self.out_of_the_game

# Function exists so deck can be tested. WILL NOT BE OPTION FOR PLAYERS.

  def view_deck(self):
    for card in self.shuffled_deck:
      print(card.city)

# Shuffle infection discard pile and put back into infection deck.

  def shuffle_deck(self):
    random.shuffle(self.discard_pile)
    self.shuffled_deck += self.discard_pile
    self.discard_pile = []

  def draw_infection_card(self):
    if not self.shuffled_deck:
      print('Final card has been drawn, now shuffling discard...')
      self.shuffle_deck()
    drawn_card = self.shuffled_deck.pop()
    self.discard_pile.append(drawn_card)
    return drawn_card


# test_deck = Infection_Deck(all_cities)

# print(test_deck.shuffled_deck)
