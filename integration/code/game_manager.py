from .registration import Registration
from .crew_management import CrewManagement
from .inventory import Inventory
from .race_management import RaceManagement
from .results import Results
from .mission_planning import MissionPlanning
from .power_ups import PowerUps
from .shop import Shop

class GameManager:
    def __init__(self):
        self.registration = Registration()
        self.crew = CrewManagement(self.registration)
        self.inventory = Inventory()
        self.results = Results()
        self.race = RaceManagement(self.registration, self.inventory, self.results)
        self.mission = MissionPlanning(self.crew, self.inventory)
        self.power_ups = PowerUps(self.inventory)
        self.shop = Shop(self.inventory)

    def run(self):
        print("StreetRace Manager initialized.")

    def handle_register_member(self, name, role):
        return self.registration.register_member(name, role)

    def handle_assign_mission(self, mission_type):
        return self.mission.assign_mission(mission_type)

    def handle_add_inventory(self, item_name, quantity):
        self.inventory.add_item(item_name, quantity)

    def handle_update_cash(self, amount):
        self.inventory.update_cash(amount)

    def handle_buy_item(self, item_name):
        return self.shop.buy_item(item_name)

    def handle_run_race(self, driver_name, car_name):
        config = self.race.setup_race(driver_name, car_name)
        return self.race.run_race(config)

    def handle_assign_skill(self, name, level):
        return self.crew.assign_skill(name, level)

    def print_state(self):
        return {
            "members": self.registration.list_members(),
            "inventory": self.inventory.items,
            "cash": self.inventory.cash,
            "cars": self.inventory.cars
        }
