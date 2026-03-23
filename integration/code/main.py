from game_manager import GameManager

def show_menu():
    print("Welcome to StreetRace Manager")
    print("1. Register Member")
    print("2. Assign Mission")
    print("3. Run Race")
    print("4. Buy Item")
    print("5. State")
    print("6. Exit")

def execute_choice(game, choice):
    if choice == "1":
        name = input("Name: ")
        role = input("Role: ")
        print(game.handle_register_member(name, role))
    elif choice == "2":
        mission_type = input("Mission type: ")
        print(game.handle_assign_mission(mission_type))
    elif choice == "3":
        driver = input("Driver: ")
        car = input("Car: ")
        print(game.handle_run_race(driver, car))
    elif choice == "4":
        item = input("Item: ")
        print(game.handle_buy_item(item))
    elif choice == "5":
        print(game.print_state())

def main():
    game = GameManager()
    game.run()
    while True:
        show_menu()
        choice = input("> ")
        if choice == "6":
            break
        try:
            execute_choice(game, choice)
        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    main()
