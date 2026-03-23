# MoneyPoly Call Graph Summary

The call graph visualizes the hierarchical interactions among Python modules within the MoneyPoly application during its execution lifecycle. 

Below is a structured interaction summary:

## Call Graph Execution Path

main() [main.py]
└── Game.run() [game.py]
    ├── ui.print_banner() [ui.py]
    ├── Game.play_turn() [game.py]
    │   ├── ui.print_banner() [ui.py]
    │   ├── Player.is_bankrupt() [player.py]
    │   ├── Game._check_bankruptcy() [game.py]
    │   │   ├── Bank.receive_properties() [bank.py]
    │   │   └── Player.properties.clear() [player.py]
    │   ├── Game.interactive_menu() [game.py]
    │   │   ├── ui.safe_int_input() [ui.py]
    │   │   ├── ui.print_standings() [ui.py]
    │   │   ├── ui.print_board_ownership() [ui.py]
    │   │   ├── Game.mortgage_property() / unmortgage_property() [game.py]
    │   │   └── Game.interactive_trade() [game.py]
    │   ├── Game._handle_jail_turn() [game.py]
    │   │   ├── ui.confirm() [ui.py]
    │   │   ├── Player.leave_jail() [player.py]
    │   │   ├── Dice.roll() [dice.py]
    │   │   └── Game._move_and_resolve() [game.py]
    │   ├── Dice.roll() [dice.py]
    │   │   ├── random.randint() [Python Standard]
    │   │   ├── Dice.is_doubles() [dice.py]
    │   │   └── Dice.total() [dice.py]
    │   ├── Dice.describe() [dice.py]
    │   ├── Game._move_and_resolve() [game.py]
    │   │   ├── Player.move() [player.py]
    │   │   ├── Board.get_tile() [board.py]
    │   │   ├── Game._handle_property_tile() [game.py]
    │   │   │   ├── Property.mortgage_value() [property.py]
    │   │   │   ├── Game.buy_property() [game.py]
    │   │   │   ├── Game.auction_property() [game.py]
    │   │   │   └── Game.pay_rent() [game.py]
    │   │   │       ├── Property.calculate_rent() [property.py]
    │   │   │       │   └── PropertyGroup.all_owned_by() [property.py]
    │   │   │       └── Player.pay() / Player.receive() [player.py]
    │   │   ├── Game._handle_chance_tile() [game.py]
    │   │   │   ├── random.choice() [Python Standard]
    │   │   │   └── Game._apply_card() [game.py]
    │   │   │       ├── Player.receive() / pay() / go_to_jail() [player.py]
    │   │   │       └── Game._move_and_resolve() [game.py]
    │   │   └── Game._handle_special_tile() [game.py]
    │   │       ├── Player.pay() [player.py]
    │   │       └── Player.go_to_jail() [player.py]
    │   └── Game.advance_turn() [game.py]
    ├── ui.print_standings() [ui.py]
    └── Game.find_winner() [game.py]

## Node Interactions Snapshot

1. **main**: Program entry. Instantiates `Game`.
2. **Game**: Core controller orchestrating turns. Talks to `Player`, `Board`, `Dice`, `Bank`, and `UI`.
3. **Player**: State container tracking balance, properties, and jail status. Manipulated heavily by `Game`.
4. **Board**: Initialises and holds properties, tiles, property groups. Evaluated by `Game`.
5. **Property / PropertyGroup**: Calculates rents using full group multipliers and mortgage state. Interacts with `Player` owners.
6. **Dice**: Generates random numbers, tracks doubles. Returns numeric totals for `Game`.
7. **Bank**: Temporary storage for properties unowned or surrendered during bankruptcy.
8. **UI**: Helper functions abstracting interaction prints/prompts (`confirm`, `safe_int_input`, etc).
