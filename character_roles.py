import random

# Create list of character objects. Enables them to be shuffled and dealt easily

class Character_Deck:
    def __init__(self):
        Quarantine_Specialist = Create_Quarantine_Specialist()
        Researcher = Create_Researcher()
        Scientist = Create_Scientist()
        Medic = Create_Medic()
        Contingency_Planner = Create_Contingency_Planner()
        Dispatcher = Create_Dispatcher()
        self.character_deck = [Quarantine_Specialist, Researcher,
                               Scientist, Medic, Contingency_Planner, Dispatcher]
        random.shuffle(self.character_deck)


# Different roles. Need to build any relevant special abilities into classes where relevant. In some instances will have to build special actions into the game play itself

class Create_Quarantine_Specialist:
    def __init__(self):
        self.value = 'Quarantine Specialist'

    def special_action(self):
        print('special action')

class Create_Researcher:
    def __init__(self):
        self.value = 'Researcher'

    def special_action(self):
        print('special action')

class Create_Scientist:
    def __init__(self):
        self.value = 'Scientist'

    def special_action(self):
        print('special action')


class Create_Medic:
    def __init__(self):
        self.value = 'Medic'

    def special_action(self):
        print('special action')


class Create_Contingency_Planner:
    def __init__(self):
        self.value = 'Contingency Planner'

    def special_action(self):
        print('special action')


class Create_Dispatcher:
    def __init__(self):
        self.value = 'Dispatcher'

    def special_action(self):
        print('special action')


class Create_Operations_Expert:
    def __init__(self):
        self.value = 'Operations Expert'

    def special_action(self):
        print('special action')