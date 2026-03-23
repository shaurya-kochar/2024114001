class Shop:
    def __init__(self, inventory_module):
        self.inventory = inventory_module
        self.catalog = {
            "nitrous": {"price": 100, "type": "powerup"},
            "tires": {"price": 200, "type": "part"},
            "turbo": {"price": 300, "type": "powerup"}
        }

    def list_catalog(self):
        return self.catalog

    def buy_item(self, item_name):
        if item_name not in self.catalog:
            raise ValueError("Item not found in shop")
            
        price = self.catalog[item_name]["price"]
        self.inventory.update_cash(-price)
        self.inventory.add_item(item_name, 1)
        return True
