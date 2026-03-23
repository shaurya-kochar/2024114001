import pytest
from integration.code.game_manager import GameManager

@pytest.fixture
def gm():
    game = GameManager()
    return game

def test_register_and_assign_role(gm):
    gm.handle_register_member("Alice", "driver")
    assert gm.registration.list_members().get("Alice") == "driver"

def test_assign_driver_to_race_success(gm):
    gm.handle_register_member("Bob", "driver")
    gm.inventory.add_car("CarA")
    result = gm.handle_run_race("Bob", "CarA")
    assert result["driver"] == "Bob"

def test_assign_driver_to_race_failure_no_car(gm):
    gm.handle_register_member("Charlie", "driver")
    with pytest.raises(ValueError, match="Invalid race entry"):
        gm.handle_run_race("Charlie", "NoCar")

def test_assign_non_driver_to_race(gm):
    gm.handle_register_member("Dave", "mechanic")
    gm.inventory.add_car("CarB")
    with pytest.raises(ValueError, match="Invalid race entry"):
        gm.handle_run_race("Dave", "CarB")

def test_mission_rescue_success(gm):
    gm.handle_register_member("Eve", "strategist")
    gm.handle_register_member("Frank", "driver")
    result = gm.handle_assign_mission("rescue")
    assert "successful" in result

def test_mission_rescue_failure(gm):
    gm.handle_register_member("Grace", "strategist")
    with pytest.raises(ValueError, match="Missing required roles"):
        gm.handle_assign_mission("rescue")

def test_race_updates_inventory_cash_and_car_damage(gm):
    gm.handle_register_member("Heidi", "driver")
    gm.inventory.add_car("CarC")
    initial_cash = gm.inventory.cash
    
    result = gm.handle_run_race("Heidi", "CarC")
    if result["won"]:
        assert gm.inventory.cash == initial_cash + 500
    else:
        assert gm.inventory.cash == initial_cash

def test_repair_mission_success(gm):
    gm.handle_register_member("Ivan", "mechanic")
    gm.inventory.add_car("CarD")
    gm.inventory.mark_car_damaged("CarD", True)
    
    gm.handle_assign_mission("repair")
    assert gm.inventory.has_car("CarD") is True

def test_repair_mission_failure_no_mechanic(gm):
    gm.inventory.add_car("CarE")
    gm.inventory.mark_car_damaged("CarE", True)
    with pytest.raises(ValueError, match="Need mechanic and damaged car"):
        gm.handle_assign_mission("repair")

def test_repair_mission_failure_no_damaged_car(gm):
    gm.handle_register_member("Judy", "mechanic")
    gm.inventory.add_car("CarF")
    with pytest.raises(ValueError, match="Need mechanic and damaged car"):
        gm.handle_assign_mission("repair")

def test_shop_buy_item_success(gm):
    initial_cash = gm.inventory.cash
    gm.handle_buy_item("nitrous")
    assert gm.inventory.cash == initial_cash - 100
    assert gm.power_ups.has_power_up("nitrous") is True

def test_shop_buy_item_insufficient_funds(gm):
    gm.inventory.cash = 0
    with pytest.raises(ValueError, match="Not enough cash"):
        gm.handle_buy_item("turbo")

def test_power_up_use(gm):
    gm.handle_buy_item("nitrous")
    result = gm.power_ups.use_power_up("nitrous")
    assert "Used nitrous" in result
    assert gm.power_ups.has_power_up("nitrous") is False

def test_power_up_use_unowned(gm):
    with pytest.raises(ValueError, match="not available"):
        gm.power_ups.use_power_up("turbo")

def test_delivery_mission_success(gm):
    gm.handle_register_member("Karl", "driver")
    initial_cash = gm.inventory.cash
    result = gm.handle_assign_mission("delivery")
    assert "successful" in result
    assert gm.inventory.cash == initial_cash + 200

def test_delivery_mission_failure_no_driver(gm):
    with pytest.raises(ValueError, match="Missing driver"):
        gm.handle_assign_mission("delivery")
