import sys
from actions.Burn import Burn
from actions.Cultivate import Cultivate
from actions.Destroy import Destroy
from actions.Fertilize import Fertilize
from actions.Lock import Lock
from actions.Move import Move
from actions.Place import Place
from actions.Settle import Settle
from actions.Shift import Shift
from utils.get_possible_actions import get_possible_actions
from Board import Board
from GameState import GameState
from Player import Player
from Tile import Tile

def simulate_game(game_state, should_draw=False, should_print=False):
  while not game_state.get_is_over():
    for player_id in game_state.players.keys():
      game_state.players[player_id].take_turn(game_state, should_print)

    if should_draw:
      game_state.board.draw()

    game_state.turn_number += 1
  
  return game_state

def get_scores(game_state):
  scores_by_player_id = {}
  
  for player in game_state.players.values():
    scores_by_player_id[player.id] = 0

  for tile in game_state.board.get_tiles():
    if tile.is_fertile and tile.owner_id is not None:
      scores_by_player_id[tile.owner_id] += 1

  return scores_by_player_id

starting_board = Board()
starting_board.set_tile(Tile(0, 0))

starting_card_counts = {
  "air": 1,
  "earth": 1,
  "fire": 1,
  "water": 1
}

def get_action_priority_list_1():
  return [Lock, Cultivate, Fertilize, Settle, Place, Move, Shift, Destroy, Burn]

def get_action_priority_list_2():
  return [Destroy, Burn, Move, Shift, Settle, Cultivate, Fertilize, Lock, Place]

def get_action_priority_list_3():
  return [Place, Settle, Cultivate, Fertilize, Move, Shift, Destroy, Burn, Lock]

num_players = 3
players = {}
max_depths = [
  2,
  2,
  2
]

for i in range(num_players):
  player = Player(starting_card_counts, get_action_priority_list_1, max_depths[i])
  players[player.id] = player

options = {
  "board": starting_board,
  "get_is_over": lambda game_state: game_state.turn_number >= 10,
  "get_possible_actions": get_possible_actions,
  "get_scores": get_scores,
  "players": players
}
initial_game_state = GameState(options)

mode = sys.argv[1] if len(sys.argv) > 1 else None
should_draw = (mode == 'draw')
should_print = (mode == 'draw') or (mode == 'print')

final_game_state = simulate_game(initial_game_state, should_draw, should_print)
scores_by_player_id = get_scores(final_game_state)

for player in final_game_state.players.values():
  print(player.hand.card_counts)

print(scores_by_player_id)
