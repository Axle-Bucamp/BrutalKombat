import pytest
import pygame
from unittest.mock import Mock, patch
from bk_street_fighter import BKStreetFighter, Fighter, AIPlayer, load_character_asset, select_character

@pytest.fixture
def mock_pygame():
    with patch('pygame.image.load') as mock_load:
        mock_load.return_value = Mock(spec=pygame.Surface)
        yield mock_load

@pytest.fixture
def game():
    return BKStreetFighter()

@pytest.fixture
def fighter():
    return Fighter("Test Fighter", 100, 10)

@pytest.fixture
def ai_player():
    return AIPlayer("AI Fighter", 100, 10)

def test_load_character_asset(mock_pygame):
    asset = load_character_asset("burger_king")
    mock_pygame.assert_called_once_with("assets/burger_king.png")
    assert isinstance(asset, pygame.Surface)

@pytest.mark.parametrize("character_name", ["burger_king", "ronald", "colonel"])
def test_select_character(mock_pygame, character_name):
    character = select_character(character_name)
    assert isinstance(character, Fighter)
    assert character.name == character_name
    mock_pygame.assert_called_once_with(f"assets/{character_name}.png")

def test_ai_basic_logic(ai_player, fighter):
    ai_player.update(fighter)
    assert ai_player.action in ["move", "attack", "defend"]

def test_game_with_ai_players(game):
    game.start_game()
    assert len(game.players) == 2
    assert all(isinstance(player, AIPlayer) for player in game.players)

@pytest.mark.parametrize("player_health, opponent_health, expected_action", [
    (20, 80, "defend"),
    (80, 20, "attack"),
    (50, 50, "move"),
])
def test_ai_strategy(ai_player, fighter, player_health, opponent_health, expected_action):
    ai_player.health = player_health
    fighter.health = opponent_health
    ai_player.update(fighter)
    assert ai_player.action == expected_action

def test_game_over_condition(game):
    game.start_game()
    game.players[0].health = 0
    game.update()
    assert game.is_game_over
    assert game.winner == game.players[1]

def test_character_asset_loading_error():
    with pytest.raises(FileNotFoundError):
        load_character_asset("nonexistent_character")

def test_ai_player_initialization():
    ai = AIPlayer("AI Fighter", 100, 10)
    assert ai.name == "AI Fighter"
    assert ai.health == 100
    assert ai.attack_power == 10
    assert ai.action is None

def test_multiple_rounds(game):
    game.start_game()
    for _ in range(3):  # Simulate 3 rounds
        while not game.is_game_over:
            game.update()
        game.reset_round()
    assert game.round_number == 3

if __name__ == "__main__":
    pytest.main()