class RaceManagement:
    def __init__(self, registration_module, inventory_module, results_module):
        self.registration = registration_module
        self.inventory = inventory_module
        self.results = results_module

    def setup_race(self, driver_name, car_name):
        if not self.validate_race_entry(driver_name, car_name):
            raise ValueError("Invalid race entry")
        return {"driver": driver_name, "car": car_name}

    def validate_race_entry(self, driver_name, car_name):
        members = self.registration.list_members()
        if driver_name not in members or members[driver_name] != "driver":
            return False
        if not self.inventory.has_car(car_name):
            return False
        return True

    def run_race(self, race_config):
        driver = race_config["driver"]
        car = race_config["car"]
        
        result = self.results.generate_results(driver, car)
        
        self.inventory.update_cash(result["prize"])
        if result["car_damaged"]:
            self.inventory.mark_car_damaged(car, True)
            
        return result
