class GameStatus:
    def __init__(self, all_cities, virus_cubes=24, outbreak_counter=7):
        self.viral_reserves = {colour: virus_cubes for colour in all_cities.keys()}
        self.outbreak_counter = outbreak_counter
        self.infect_city_status = True
        self.game_status = 'In Progress'

    def check_game_status(self):
        if self.outbreak_counter > 0:
            for colour, cubes in self.viral_reserves.items():
                if cubes <= 0:
                    self.game_status = 'GAME OVER:\n\nThere are no {0} cubes left!\n\nYOU HAVE LOST'.format(colour)
                    print(self.game_status)
                return
        self.game_status = 'GAME OVER:\n\nYou have had 7 or more outbreaks!\n\nYOU HAVE LOST'
        print(self.game_status)
