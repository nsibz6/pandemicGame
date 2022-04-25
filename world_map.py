from game_data import infection_rate, all_cities

class City:
  def __init__(self, city, colour, next_cities, all_cities):
    self.city = city
    self.colour = colour
    self.next_cities = next_cities[city]
    self.total_edges = len(self.next_cities)
    self.virus_info = {colour: [0, False] for colour in all_cities.keys()}
    self.players_in_city = []

  def add_city_edge(self, city):
    if city not in self.next_cities:
     self.next_cities.append(city)
     self.all_cities[city].next_cities.append(self.city)
     self.total_edges += 1
     self.all_cities[city].total_edges += 1

# function to delete city edges if required

  def delete_city_edge(self, city):
    if city in self.next_cities:
     self.next_cities.pop(city)
     self.all_cities[city].next_cities.pop(self.city)
     self.total_edges -= 1
     self.all_cities[city].total_edges -= 1

# function to allow the building of research centres. Also connects other research centres with each other to make traveling between them easier.

  def add_research_centre(self, world_map, city=None):
    if len(world_map.research_centres) < 6:
      if city == None:
        world_map.research_centres.append(self.city)
      else:
        world_map.research_centres.append(city)
      print('Showing updated research centres...\n\n {0}'.format(' '.join(world_map.research_centres)))
    else:
      print('You cannot build anymore research centres unless you first remove one, do you wish to continue?')
      make_choice = None
      while make_choice != 'Y' or make_choice != 'N':
        make_choice = input('input Y for Yes or N for No')
      if make_choice == 'N':
        return
      research_centre = None
      while research_centre not in world_map.research_centres:
        research_centre = input('Pick a valid research centre to remove: You can pick from {0}'.format(world_map.research_centres.keys()))
        if research_centre not in world_map.research_centres:
          print('Invalid choice: please try again')
      world_map.research_centres.pop(research_centre)
      add_research_centre(self, city)

# to show connections of a city. Useful for game play and testing.

  def show_connections(self):
    print(self.next_cities)

# vital function for end of every turn. Infect city and outbrek recursively call each other

  def infect_city(self, world_map, infection_num=1, colour=None):
    if not colour:
      colour = self.colour
    if colour in self.virus_info:
     self.virus_info[colour][0]+= infection_num
     world_map.game_status.viral_reserves[colour] -= infection_num
     if self.virus_info[colour][0] <= 3:
       world_map.game_status.check_game_status()
     if self.virus_info[colour][0] > 3:
       world_map.game_status.viral_reserves[colour] += (self.virus_info[colour][0] - 3)
       self.virus_info[colour][0] = 3
       if self.virus_info[colour][1] == False:
         self.virus_info[colour][1] = True
         self.outbreak(colour, world_map)

# outbreak function to be called when infection exceeds 3 of a single colour.

  def outbreak(self, colour, world_map):
    world_map.game_status.outbreak_counter -= 1
    world_map.game_status.check_game_status()
    for next_city in self.next_cities:
      world_map.all_cities[next_city].infect_city(world_map, 1, colour)

# Map of world. Contains all cities as well as other important game data. Higher orderobject that acts as a container for other objects.

class Map_of_World:
  def __init__(self, all_cities, game_status, infection_rate, starting_research_centre='Atlanta', counter=0):
    self.infection_rate = infection_rate
    self.counter = counter
    self.current_infection_rate = self.infection_rate[self.counter]
    self.research_centres =[starting_research_centre]
    self.all_cities = {city: City(city, colour, cities, all_cities) for colour, cities in all_cities.items() for city in cities}
    self.game_status = game_status

modern_world = Map_of_World(all_cities, False, infection_rate)

print(modern_world.all_cities)