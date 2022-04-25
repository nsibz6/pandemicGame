class Create_Player:
    def __init__(self, world_map, player_name, num_cards, player_deck, character_deck, player_num=0,
                 current_city='Atlanta', num_actions=1):
        self.num = player_num
        self.name = player_name
        self.num_actions = num_actions
        self.character_class = character_deck.character_deck.pop()
        self.current_city = current_city
        self.hand = draw_player_card(player_deck, num_cards) + ['Forecast', 'Government Grant']
        world_map.all_cities[self.current_city].players_in_city.append(self.name)

    def give_card(self, player_dict):
        print('Please choose a player (other than yourself!) to give a city card to.')
        other_players = []
        for num, player in player_dict:
            if player.name is not self.name:
                print(player.name)
                other_players.append(player.name)
        player = input()
        while player.name not in other_players:
            input('Invalid choice, please try again!')

    def take_card(self, card, player):
        pass

    def special_action(self, player_class):
        pass

    def remove_virus_cube(self, colour=None):
        total_virus_cubes = 0
        print('The current city your are in has the following number of virus cubes of each colour:')
        for colour, cube in world_map.all_cities[self.current_city].virus_info.items():
            print(colour, cube[0])
            total_virus_cubes += cube[0]
        if total_virus_cubes == 0:
            return print(
                'The current city you are in is not infected and therefor you cannot take this action:\n\n Please take another action.')
        colour = input(
            'Please select a colour virus cube to remove. Please note you cannot pick a colour where there are 0 virus cubes.')
        if world_map.all_cities[self.current_city].virus_info[colour][0] < 1:
            print('invalid selection please try again')
            self.remove_virus_cube(colour)
        world_map.all_cities[self.current_city].virus_info[colour][0] -= 1
        world_map.game_status.viral_reserves[colour] += 1
        self.num_actions -= 1

    def build_research_centre(self, card):
        pass

    # different ways of moving.
    # move to adjacent city.

    def move_drive_ferry(self, world_map, choice=None):
        if choice == None:
            print('you may move to an adjacent city for 1 action:\nYou are currently in {0}, you may move to:'.format(
                self.current_city))
            for city in world_map.all_cities[self.current_city].next_cities:
                print(city)
            choice = input('Do you wish to continue? If so input a valid city to move to: Otherwise insert N for No')
            if choice in world_map.all_cities[self.current_city].next_cities:
                world_map.all_cities[self.current_city].players_in_city.remove(self.name)
                world_map.all_cities[choice].players_in_city.append(self.name)
                self.current_city = choice
                self.num_actions -= 1

    # discard city card and fly directly to that city.

    def move_direct_flight(self, world_map, gameplay_deck):
        city_cards = []
        for card in self.hand:
            if card in world_map.all_cities:
                print(card)
                city_cards.append(card)
        if len(city_cards) > 0:
            print(
                'You may discard a city card to travel to that city for 1 action:\nYou are currently in {0},you may move to any of the above cities.\n\nPlease input a valid city to move to or type N to exit this action.'.format(
                    self.current_city))
        else:
            return print(
                'You do not have any city cards which you can use for this action.\n Please choose another action!')
        choice = input()
        while choice not in city_cards:
            if choice == 'N':
                return print('You have chosen to end this action.')
            choice = input('\nInvalid selection, please try again!')
        world_map.all_cities[self.current_city].players_in_city.remove(self.name)
        world_map.all_cities[choice].players_in_city.append(self.name)
        self.current_city = choice
        self.num_actions -= 1
        gameplay_deck.discard_pile.append(self.hand.remove(choice))

    # fly to any city if you discard card for city you are in.

    def move_chartered_flight(self, world_map, gameplay_deck, choice=0):
        if self.current_city in self.hand:
            if choice == None:
                print(
                    'You may travel to any other city on the map for 1 action:\nYou are currently in {0},you may move to:'.format(
                        self.current_city))
            for city in world_map.all_cities:
                if city != self.current_city:
                    print(city)
            choice = input('Do you wish to continue? If so input a valid city to move to: Otherwise insert N for No')
            if choice in world_map.all_cities:
                world_map.all_cities[self.current_city].players_in_city.remove(self.name)
                world_map.all_cities[choice].players_in_city.append(self.name)
                self.current_city = choice
                self.num_actions -= 1
                gameplay_deck.discard_pile.append(self.hand.remove(choice))

    # fly from a city with a research centre to any other city with a research centre.

    def move_shuttle_flight(self, choice=0):
        if self.current_city in world_map.research_centres:
            if choice == None:
                print(
                    'You may travel to any other city which also has a research centre for 1 action:\nYou are currently in {0},you may move to:'.format(
                        self.current_city))
            for city in world_map.research_centres:
                print(city)
            choice = input('Do you wish to continue? If so input a valid city to move to: Otherwise insert N for No')
            if choice in world_map.research_centres:
                world_map.all_cities[self.current_city].players_in_city.remove(self.name)
                world_map.all_cities[choice].players_in_city.append(self.name)
                self.current_city = choice
                self.num_actions -= 1

    # Play event cards.

    def use_card(self, player_dict, player_deck):
        player_event_cards = []
        for player_num, player in player_dict.items():
            for card in player.hand:
                if card not in player_event_cards and (
                        card == 'Resilient Population' or card == 'One Quiet Night' or card == 'Airlift' or card == 'Forecast' or card == 'Government Grant'):
                    player_event_cards.append(card)
        if not player_event_cards:
            print('There are no available event cards to play:\n\nPlease take another action')
            return
        print(
            'You may play any of the below available event cards:\n\nAs event cards can be played out of sequence you may play cards from other players hands if you agree to do so as a team.\n\n')
        print(player_event_cards, "\n\n")
        choice = input('Which card do you want to play?')
        if choice == 'Forecast':
            return player_deck.player_deck[choice].use_card()
        elif choice in player_event_cards:
            player_deck.player_deck[choice].use_card()
            for player_num, player in player_dict.items():
                if choice in player.hand:
                    player.hand.remove(choice)
                    break


# draw player cards.

def draw_player_card(shuffled_player_deck, epidemic_deck=None, num_cards=2):
    drawn_cards = []
    for card in range(num_cards):
        drawn_cards.append(shuffled_player_deck.shuffled_deck.pop())
        if 'Epidemic Card' in drawn_cards[-1]:
            epidemic_deck.epidemic_deck[drawn_cards[-1]].use_card(shuffled_world_deck, world_discard_pile)
    return drawn_cards