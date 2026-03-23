# Call Graph Summary

```text
main()
└── GameManager.__init__()
    ├── Registration.__init__()
    ├── CrewManagement.__init__()
    ├── Inventory.__init__()
    ├── Results.__init__()
    ├── RaceManagement.__init__()
    ├── Shop.__init__()
    ├── PowerUps.__init__()
    └── MissionPlanning.__init__()

GameManager.handle_register_member(name, role)
└── Registration.register_member(name, role)

GameManager.handle_assign_crew_role(name, role)
├── Registration.list_members()
└── CrewManagement.assign_role(name, role)

GameManager.handle_buy_item(item_name)
└── Shop.buy_item(item_name)
    ├── Inventory.update_cash(amount)
    └── Inventory.add_item(item_name, quantity)

GameManager.handle_use_powerup(powerup_name)
└── PowerUps.use_power_up(powerup_name)
    ├── Inventory.items.get()
    └── Inventory.remove_item(powerup_name, quantity)

GameManager.handle_run_race(driver_name, car_name)
└── RaceManagement.setup_race(driver_name, car_name)
    ├── Registration.list_members()
    └── Inventory.has_car(car_name)
└── RaceManagement.run_race(race_config)
    ├── Results.generate_results(driver, car)
    ├── Inventory.update_cash(prize)
    └── Inventory.mark_car_damaged(car, status)

GameManager.handle_assign_mission(mission_type)
└── MissionPlanning.assign_mission(mission_type)
    ├── CrewManagement.check_roles(required_roles)
        └── Registration.list_members()
    ├── MissionPlanning.can_repair()
        ├── CrewManagement.check_roles()
        └── Inventory.get_damaged_cars()
    ├── Inventory.get_damaged_cars()
    ├── Inventory.mark_car_damaged(car, False)
    └── Inventory.update_cash(amount)
```
