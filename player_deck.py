import random
from game_data import all_cities


# player deck class, city cards & event cards. Epidemic cards created separately to be added to the deck later.

class playerDeck:
    def __init__(self, all_cities):
        self.player_deck = {city: colour for colour, cities in all_cities.items() for city in cities}
        self.shuffled_deck = [city for colour, cities in all_cities.items() for city in cities]
        self.discard_pile = []
        new_event_deck = eventCards()
        self.player_deck.update(new_event_deck.event_deck)
        self.shuffled_deck += [event_card for event_card in new_event_deck.event_deck.keys()]
        random.shuffle(self.shuffled_deck)

    def view_deck(self):
        for card in self.shuffled_deck:
            print(card)

    def draw_card(self, player_hand, num=1):
        for card in range(num):
            drawn_card = self.shuffled_deck.pop()
            player_hand.append(drawn_card)
            print('You have drawn {0}.'.format(drawn_card))


# Event cards - single use cards that have special abilities

class eventCards:
    def __init__(self):
        self.event_deck = {'Resilient Population': resilientPopulation(), 'One Quiet Night': oneQuietNight(),
                           'Airlift': airlift(), 'Forecast': forecast(), 'Government Grant': governmentGrant()}

# Removes one world card from the game; therefore city can no longer be flipped during infection phase.

class resilientPopulation:
    def use_card(self, discard_pile, out_of_the_game, card_to_discard=None):
        if not discard_pile:
            return print(
                'You can only use this card if there are cards in the infection discard pile:\n\nPlease take another action.')
        if not card_to_discard:
            print('You may choose to permanently remove one of the following infection cards from the game:\n')
            for card in discard_pile:
                print(card)
        print('Please make a selection or enter N if you wish to exit.')
        while card_to_discard not in discard_pile:
            card_to_discard = input()
            if card_to_discard == 'N':
                return
            if card_to_discard not in discard_pile:
                print('Invalid entry! Please select a card in the infection discard pile.')
        print('You have discarded {0}!'.format(card_to_discard))
        out_of_the_game.append(discard_pile.remove(card_to_discard))


# Prevents any cards being flipped for one infection phase.

class oneQuietNight:
    def use_card(self, game_status):
        game_status.infect_city_status = False
        print('\n\nYou have used One Quiet Night, no cards will be drawn during the next infection phase!')


# Move a player from any city to any other city.
# Currently when use card called by player, is not called with player parameter so is getting error message.

class airlift:
    def use_card(self, player, world_map):
        if player.player_name in world_map.all_cities[player.current_city].players_in_city:
            world_map.all_cities[player.current_city].players_in_city.pop(player.player_name)
            print('Please choose a valid city to move to:')
        for city in world_map.all_cities:
            print(city)
        pick_city = input()
        if pick_city in world_map.all_cities:
            world_map.all_cities[pick_city].players_in_city.append(player.player_name)
            player.current_city = pick_city


# Look at top 6 world cards and rearrange in order of your choice.
# Quite a complex algorithm. Look for potential ways to simplify. Have reduced amount of code with respect to informing the player of what order each new card is they are inputting.

class forecast:
    # instantiated with empty list to store player's reorder decision
    def __init__(self):
        self.new_order = []

    # function to enable player to choose which card to put 1st, 2nd, 3rd, 4th, 5th and 6th
    def select_new_order(self, temp_top_6):
        print(
            '\nStarting with the first card you will draw in the infection phase and ending with the 6th card to be drawn, you can now rearrange the top 6 cards\n')
        select_card = None
        for i in range(1, 6 + 1):
            while select_card not in temp_top_6:
                select_card = input(
                    '\nPlease input one of the cards to be the card number {0} in the new order.\n'.format(i))
                if select_card not in temp_top_6:
                    print('\nInvalid choice!\n')
            self.new_order.append(select_card)
            temp_top_6.remove(select_card)
            print('\nCards left to choose from.\n')
            for card in temp_top_6:
                print(card)
        return self.new_order

    # function that enables player to confirm they are happy with new order. If yes amends deck, if no restarts the process. NOTE: have not included functionality to allow players to simply quit otherwise would enable them to view top 6 cards for free without using the card.
    def final_decision(self, final_choice, final_amend, infection_deck):
        if final_choice == 'N':
            print('\nRestarting the process now...\n')
            final_amend = []
            self.new_order = []
            self.use_card(infection_deck)
        else:
            infection_deck = infection_deck[:-6] + final_amend
            self.new_order = []
            # print(shuffled_world_deck)

    # use card function. This is what is called by players when they play the card and it calls the above two functions within it. Presents cards from 1st drawn to last drawn.
    def use_card(self, infection_deck):
        temp_top_6 = infection_deck[-6:]
        print('\nCards in order, first to last:\n')
        for city in range(len(temp_top_6)):
            print(temp_top_6[0 - (city + 1)])
        self.select_new_order(infection_deck, temp_top_6)
        # print(new_order)
        final_amend = []
        for i in range(len(self.new_order)):
            final_amend.append(self.new_order[0 - (i + 1)])
        print('\nFrom first to last this is the order in which the infection cards will now be drawn:\n')
        for card in range(len(final_amend)):
            print(final_amend[0 - (card + 1)])
        final_choice = None
        while final_choice not in ('N', 'Y'):
            final_choice = input('\nAre you happy with that order? Input Y for Yes or N for No\n')
            if final_choice not in ('N', 'Y'):
                print('\nInvalid input, must be Y for Yes or N for No: Please try again:\n')
        self.final_decision(final_choice, final_amend, infection_deck)


# creates research centre anywhere on map
# Further updates made on the original on Pandemic Decks. Ensure you copy this logic over.

class governmentGrant:
    def check_city(self, select_city, world_map):
        while select_city in world_map.research_centres.keys() or select_city not in world_map.all_cities:
            select_city = input(
                'You must ensure your input is a city in the list that does not already have a research centre:\n\nTry again')
        return world_map.all_cities[select_city].add_research_centre()

    def use_card(self, world_map):
        print('Add a research centre to a city of your choice that does not already have a research centre:')
        for city in all_cities:
            if city not in world_map.research_centres.keys():
                print(city)
        select_city = input()
        self.check_city(select_city, world_map)
