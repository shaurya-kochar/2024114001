import pytest
from unittest.mock import patch

from moneypoly.game import Game
from moneypoly.player import Player
from moneypoly.board import Board
from moneypoly.bank import Bank
from moneypoly.dice import Dice
from moneypoly.property import Property
from moneypoly.config import STARTING_BALANCE, GO_SALARY, JAIL_FINE

@pytest.fixture
def setup_game():
    """Initialise a basic 2-player game for integration testing."""
    game = Game(["Alice", "Bob"])
    return game

def test_initial_setup_integration(setup_game):
    """Test Game properly initializes and links Board, Bank, Dice, and Players."""
    game = setup_game
    assert len(game.players) == 2
    assert game.players[0].name == "Alice"
    assert game.players[1].name == "Bob"
    assert isinstance(game.board, Board)
    assert isinstance(game.bank, Bank)
    assert isinstance(game.dice, Dice)
    assert game.players[0].balance == STARTING_BALANCE

def test_move_updates_position_and_triggers_events(setup_game):
    """Test rolling dice moves player from Game through Dice to Board."""
    game = setup_game
    player = game.current_player()
    
    with patch('moneypoly.ui.safe_int_input', return_value=0), \
         patch('builtins.input', return_value='s'), \
         patch('moneypoly.dice.random.randint', side_effect=[1, 2]):
        game.play_turn()
        
    assert player.position == 3

def test_passing_go_adds_salary(setup_game):
    """Test moving past GO adds GO_SALARY to player balance."""
    game = setup_game
    player = game.current_player()
    player.position = 38
    
    with patch('builtins.input', return_value='s'), \
         patch('moneypoly.dice.Dice.roll', return_value=5):
        game._move_and_resolve(player, 5)

    assert player.balance == STARTING_BALANCE + GO_SALARY
    assert player.position == 3

def test_buying_property_integration(setup_game):
    """Test Game ↔ Player ↔ Property ↔ Bank interaction when buying."""
    game = setup_game
    player = game.players[0]
    prop = game.board.properties[0]  # Mediterranean
    
    assert prop.owner is None
    success = game.buy_property(player, prop)
    
    assert success is True
    assert prop.owner == player
    assert prop in player.properties
    assert player.balance == STARTING_BALANCE - prop.price

def test_paying_rent_integration(setup_game):
    """Test Game ↔ Player A ↔ Player B ↔ Property when paying rent."""
    game = setup_game
    owner_player = game.players[0]
    renting_player = game.players[1]
    prop = game.board.properties[1]  # Baltic
    
    game.buy_property(owner_player, prop)
    owner_initial_balance = owner_player.balance
    renter_initial_balance = renting_player.balance
    
    game.pay_rent(renting_player, prop)
    
    assert renting_player.balance == renter_initial_balance - prop.base_rent
    assert owner_player.balance == owner_initial_balance + prop.base_rent

def test_full_group_rent_multiplier(setup_game):
    """Test Rent multiplies when a player owns the whole group."""
    game = setup_game
    owner = game.players[0]
    renter = game.players[1]
    
    prop1 = game.board.properties[0]  # Mediterranean
    prop2 = game.board.properties[1]  # Baltic
    
    game.buy_property(owner, prop1)
    game.buy_property(owner, prop2)
    
    assert prop1.group.all_owned_by(owner) is True
    renter_initial = renter.balance
    owner_initial = owner.balance
    
    game.pay_rent(renter, prop1)
    expected_rent = prop1.base_rent * prop1.FULL_GROUP_MULTIPLIER
    assert renter.balance == renter_initial - expected_rent
    assert owner.balance == owner_initial + expected_rent

def test_mortgaging_property_integration(setup_game):
    """Test property mortgage interactions (Property ↔ Player ↔ Game)."""
    game = setup_game
    player = game.players[0]
    prop = game.board.properties[0]
    
    game.buy_property(player, prop)
    balance_before_mortgage = player.balance
    
    game.mortgage_property(player, prop)
    
    assert prop.is_mortgaged is True
    assert player.balance == balance_before_mortgage + prop.mortgage_value()

def test_unmortgaging_property_integration(setup_game):
    """Test lifting mortgage and deducting amounts correctly."""
    game = setup_game
    player = game.players[0]
    prop = game.board.properties[0]
    
    game.buy_property(player, prop)
    game.mortgage_property(player, prop)
    balance_before_unmortgage = player.balance
    expected_cost = int(prop.mortgage_value() * 1.1)
    
    game.unmortgage_property(player, prop)
    
    assert prop.is_mortgaged is False
    assert player.balance == balance_before_unmortgage - expected_cost

def test_rent_not_paid_on_mortgaged_property(setup_game):
    """Test that rent is 0 if property is mortgaged."""
    game = setup_game
    owner = game.players[0]
    renter = game.players[1]
    prop = game.board.properties[1]
    
    game.buy_property(owner, prop)
    game.mortgage_property(owner, prop)
    
    renter_initial = renter.balance
    owner_initial = owner.balance
    
    game.pay_rent(renter, prop)
    
    assert renter.balance == renter_initial
    assert owner.balance == owner_initial

def test_going_to_jail_integration(setup_game):
    """Test going to jail from Go To Jail tile."""
    game = setup_game
    player = game.current_player()
    player.position = 29
    
    game._move_and_resolve(player, 1)
    
    assert player.jail["in_jail"] is True
    assert player.position == 10

def test_paying_to_leave_jail(setup_game):
    """Test paying fine to leave jail."""
    game = setup_game
    player = game.current_player()
    
    player.go_to_jail()
    assert player.jail["in_jail"] is True
    initial_balance = player.balance
    
    with patch('moneypoly.ui.confirm', return_value=True), \
         patch('builtins.input', return_value='s'), \
         patch('moneypoly.dice.random.randint', side_effect=[1, 3]):
        game._handle_jail_turn(player)
        
    assert player.jail["in_jail"] is False
    assert player.balance == initial_balance - JAIL_FINE

def test_chance_card_effect_integration(setup_game):
    """Test drawing a chance card updates player cash (Game ↔ Cards ↔ Player)."""
    game = setup_game
    player = game.current_player()
    initial_balance = player.balance
    
    card = {"description": "Bank pays you $50", "action": "collect", "value": 50}
    game._apply_card(player, card)
    
    assert player.balance == initial_balance + 50

def test_trade_between_players(setup_game):
    """Test Game trading mechanism between Player A and Player B."""
    game = setup_game
    seller = game.players[0]
    buyer = game.players[1]
    prop = game.board.properties[0]
    
    game.buy_property(seller, prop)
    seller_bal_before = seller.balance
    buyer_bal_before = buyer.balance
    
    game.trade(seller, buyer, prop, 100)
    
    assert prop.owner == buyer
    assert prop not in seller.properties
    assert prop in buyer.properties
    
    assert seller.balance == seller_bal_before + 100
    assert buyer.balance == buyer_bal_before - 100

def test_bankruptcy_eliminates_player(setup_game):
    """Test check_bankruptcy removes player and clears properties."""
    game = setup_game
    player = game.players[0]
    prop = game.board.properties[0]
    
    game.buy_property(player, prop)
    player.balance = -10
    
    assert player.is_bankrupt()
    game._check_bankruptcy(player)
    
    assert getattr(player, "is_eliminated", False) is True
    assert player not in game.players
    assert prop.owner is None
    assert prop not in player.properties

def test_game_winner_detection(setup_game):
    """Test finding winner when other players are bankrupt."""
    game = setup_game
    player1 = game.players[0]
    player2 = game.players[1]
    
    player1.balance = -10
    game._check_bankruptcy(player1)
    
    winner = game.find_winner()
    assert winner == player2

def test_auction_property_integration(setup_game):
    """Test auctioning property to highest bidder."""
    game = setup_game
    prop = game.board.properties[0]
    
    with patch('moneypoly.ui.safe_int_input', side_effect=[50, 60, 0]):
        game.auction_property(prop)
        
    assert prop.owner == game.players[1]
    assert prop in game.players[1].properties
    assert game.players[1].balance == STARTING_BALANCE - 60

def test_tax_payment_integration(setup_game):
    """Test landing on Income Tax tile deducts money."""
    game = setup_game
    player = game.current_player()
    initial_balance = player.balance
    
    player.position = 3
    with patch('builtins.input', return_value='s'):
        game._move_and_resolve(player, 1)
    
    assert player.balance == initial_balance - 200

def test_landing_on_unowned_property_menu_integration(setup_game):
    """Test interactive menu when landing on unowned property."""
    game = setup_game
    player = game.current_player()
    
    player.position = 0
    # Moves to index 1 is "Mediterranean Ave", which is position 1, index 0
    with patch('builtins.input', return_value='b'):
        game._move_and_resolve(player, 1)
    
    prop = game.board.properties[0]
    assert prop.owner == player
    assert player.balance == STARTING_BALANCE - prop.price
