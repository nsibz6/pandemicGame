import random


# This doesn't feel like it fits very well here.

def set_game_difficulty():
    game_difficulty = input('What difficulty would you like to play the game at?:\n\nEasy, Medium, or Hard?')
    while game_difficulty not in ['Easy', 'Medium', 'Hard']:
        game_difficulty = input('Invalid input! Please try again.\n\nInput Easy, Medium or Hard.')
    if game_difficulty == 'Easy':
        return 4
    elif game_difficulty == 'Medium':
        return 5
    else:
        return 6


# Epidemic cards - increase infection rate, infects city with bottom world card, shuffles world discard pile and puts on top of world deck.

class Epidemic_Cards:
    def __init__(self, epidemic_cards):
        self.epidemic_deck = {}
        self.epidemic_cards = []
        for card in range(1, epidemic_cards + 1):
            self.epidemic_deck['Epidemic Card {0}'.format(card)] = Epidemic_Card()
            self.epidemic_cards.append('Epidemic Card {0}'.format(card))

    # Input some strings etc to make clearer what Epidemic card.use_card(x, y) is doing.

    def put_in_gameplay_deck(self, shuffled_player_deck):
        pile_size = len(shuffled_player_deck) // len(self.epidemic_cards)
        num_piles = len(shuffled_player_deck) // pile_size
        new_shuffled_player_deck = []
        cards_reshuffled = (num_piles * pile_size)
        for i in range(num_piles):
            add_epidemic_card = shuffled_player_deck[i * pile_size:(i + 1) * pile_size]
            add_epidemic_card.append(self.epidemic_cards.pop(0))
            random.shuffle(add_epidemic_card)
            new_shuffled_player_deck += add_epidemic_card
        shuffled_player_deck = shuffled_player_deck[cards_reshuffled:] + new_shuffled_player_deck
        return shuffled_player_deck


class Epidemic_Card:
    def use_card(self, infection_deck, world_map, card=0):
        world_map.counter += 1
        epidemic_city_card = infection_deck.shuffled_deck.pop(card)
        print('Epidemic in {0}.'.format(infection_card))
        epidemic_city = world_map.all_cities[epidemic_city_card]
        epidemic_city.infect_city(3, epidemic_city.colour)
        infection_deck.discard_pile.append(epidemic_city_card)
        infection_deck.shuffled_deck()
