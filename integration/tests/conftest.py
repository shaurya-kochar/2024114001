import pytest
from integration.code.game_manager import GameManager

@pytest.fixture
def gm():
    game = GameManager()
    return game
