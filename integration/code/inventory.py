class Inventory:
    def __init__(self):
        self.items = {}
        self.cash = 1000
        self.cars = {}

    def add_item(self, item_name, quantity=1):
        self.items[item_name] = self.items.get(item_name, 0) + quantity

    def remove_item(self, item_name, quantity=1):
        if self.items.get(item_name, 0) < quantity:
            raise ValueError("Not enough items in inventory")
        self.items[item_name] -= quantity

    def update_cash(self, amount):
        if self.cash + amount < 0:
            raise ValueError("Not enough cash")
        self.cash += amount

    def add_car(self, car_name):
        self.cars[car_name] = {"damaged": False}
        
    def mark_car_damaged(self, car_name, status=True):
        if car_name in self.cars:
            self.cars[car_name]["damaged"] = status
            
    def has_car(self, car_name):
        if car_name not in self.cars:
            return False
        return not self.cars[car_name]["damaged"]
        
    def get_damaged_cars(self):
        return [c for c, obj in self.cars.items() if obj["damaged"]]
