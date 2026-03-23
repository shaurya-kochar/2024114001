class PowerUps:
    def __init__(self, inventory_module):
        self.inventory = inventory_module

    def has_power_up(self, power_up_name):
        return self.inventory.items.get(power_up_name, 0) > 0

    def use_power_up(self, power_up_name):
        if not self.has_power_up(power_up_name):
            raise ValueError("Power up not available in inventory")
            
        self.inventory.remove_item(power_up_name, 1)
        return f"Used {power_up_name}!"
