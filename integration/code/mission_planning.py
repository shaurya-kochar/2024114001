class MissionPlanning:
    def __init__(self, crew_management, inventory_module):
        self.crew = crew_management
        self.inventory = inventory_module

    def assign_mission(self, mission_type):
        if mission_type == "rescue":
            if not self.crew.check_roles(["driver", "strategist"]):
                raise ValueError("Mission failed: Missing required roles (driver, strategist)")
            return "Rescue mission successful!"
            
        elif mission_type == "repair":
            if not self.can_repair():
                raise ValueError("Cannot repair: Need mechanic and damaged car")
            
            # Auto-repair the first damaged car
            damaged_cars = self.inventory.get_damaged_cars()
            self.inventory.mark_car_damaged(damaged_cars[0], False)
            return f"Repaired {damaged_cars[0]} successfully!"
            
        elif mission_type == "delivery":
            if not self.crew.check_roles(["driver"]):
                raise ValueError("Mission failed: Missing driver")
            self.inventory.update_cash(200)
            return "Delivery successful! Earned $200"
            
        raise ValueError("Unknown mission type")

    def can_repair(self):
        has_mechanic = self.crew.check_roles(["mechanic"])
        has_damaged_cars = len(self.inventory.get_damaged_cars()) > 0
        return has_mechanic and has_damaged_cars
