import pytest
from unittest.mock import Mock, patch
from bk_street_fighter import BKStreetFighter, Fighter, AIPlayer

@pytest.fixture
def game():
    return BKStreetFighter()

@pytest.fixture
def fighter():
    return Fighter("Whopper", 100, 10)

@pytest.fixture
def ai_player():
    return AIPlayer()

def test_game_initialization(game):
    assert isinstance(game, BKStreetFighter)
    assert game.is_running == False
    assert len(game.fighters) == 2
    assert game.score == 0

def test_fighter_creation(fighter):
    assert fighter.name == "Whopper"
    assert fighter.health == 100
    assert fighter.attack_power == 10

def test_ai_player_creation(ai_player):
    assert isinstance(ai_player, AIPlayer)

@pytest.mark.parametrize("health,expected", [
    (100, 100),
    (50, 50),
    (0, 0),
    (-10, 0)
])
def test_fighter_health_bounds(health, expected):
    fighter = Fighter("Test", health, 10)
    assert fighter.health == expected

def test_game_start(game):
    game.start()
    assert game.is_running == True

def test_game_stop(game):
    game.start()
    game.stop()
    assert game.is_running == False

@patch('bk_street_fighter.pygame')
def test_game_render(mock_pygame, game):
    game.render()
    mock_pygame.display.flip.assert_called_once()

def test_collision_detection(game):
    fighter1 = Mock(rect=Mock(colliderect=Mock(return_value=True)))
    fighter2 = Mock()
    game.fighters = [fighter1, fighter2]
    
    assert game.check_collision(fighter1, fighter2)

def test_ai_player_move(ai_player, game):
    initial_position = ai_player.position
    ai_player.make_move(game)
    assert ai_player.position != initial_position

def test_score_increase(game):
    initial_score = game.score
    game.increase_score(10)
    assert game.score == initial_score + 10

@pytest.mark.parametrize("player_input,expected_action", [
    ('UP', 'jump'),
    ('DOWN', 'crouch'),
    ('LEFT', 'move_left'),
    ('RIGHT', 'move_right'),
    ('SPACE', 'attack'),
])
def test_player_input_handling(game, player_input, expected_action):
    with patch.object(game, expected_action) as mock_action:
        game.handle_input(player_input)
        mock_action.assert_called_once()

def test_game_over_condition(game):
    game.fighters[0].health = 0
    assert game.is_game_over() == True

def test_restart_game(game):
    game.start()
    game.fighters[0].health = 0
    game.score = 100
    game.restart()
    assert game.is_running == False
    assert game.score == 0
    assert all(fighter.health > 0 for fighter in game.fighters)