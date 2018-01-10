from actions.Burn import Burn
from actions.Cultivate import Cultivate
from actions.Destroy import Destroy
from actions.Fertilize import Fertilize
from actions.Lock import Lock
from actions.Move import Move
from actions.Place import Place
from actions.Settle import Settle
from actions.Shift import Shift
from utils.get_is_valid_placement import get_is_valid_placement

def add_first_cultivate(player_id, game_state, possible_actions, should_enforce_hand):
  board = game_state.board
  points = []

  for tile in board.get_tiles():
    is_valid_placement = get_is_valid_placement(tile, board, is_fertile=True)
    neighbors = board.get_neighbors(tile.x, tile.y)
    neighbors_owned_and_fertile = map(
      lambda neighbor: (neighbor.is_fertile and neighbor.owner_id == player_id) or (neighbor.x, neighbor.y) in points,
      neighbors
    )
    neighbors_are_friendly_or_neutral = map(
      lambda neighbor: (neighbor.owner_id is None or neighbor.owner_id == player_id),
      neighbors
    )

    if (
      not tile.is_fertile
      and is_valid_placement
      and (
        tile.owner_id == player_id
        or (tile.owner_id is None and any(neighbors_owned_and_fertile))
      )
      and all(neighbors_are_friendly_or_neutral)
    ):
      points.append((tile.x, tile.y))

      if len(points) == 4:
        break
    
  if len(points) == 4:
    action = Cultivate(player_id, points)

    if action.is_possible(game_state, should_enforce_hand):
      possible_actions.append(action)

def get_is_potential_bottleneck(tile, board):
  neighbors = board.get_neighbors(tile.x, tile.y)
  num_fertilized_neighbors = len([neighbor for neighbor in neighbors if neighbor.is_fertile])

  return num_fertilized_neighbors > len(neighbors) - 4 and num_fertilized_neighbors < 4 

def get_is_next_to_settlement(tile, board):
  neighbors = board.get_neighbors(tile.x, tile.y) + [tile]

  return any(map(lambda neighbor: neighbor.is_settled, neighbors))

def get_should_burn(tile, board):
  return get_is_potential_bottleneck(tile, board) or get_is_next_to_settlement(tile, board)

def get_should_destroy(player_id, tile, board):
  return tile.is_settled and tile.owner_id != player_id

def get_should_fertilize(player_id, tile, board):
  tiles = board.get_neighbors(tile.x, tile.y) + [tile]

  return any(map(lambda tile: tile.owner_id == player_id, tiles))

def get_should_lock(player_id, tile, board):
  return tile.is_fertile and tile.is_settled and tile.owner_id == player_id

def get_should_shift(tile, board):
    return get_is_potential_bottleneck(tile, board) or get_is_next_to_settlement(tile, board)

def get_possible_actions(player_id, game_state, should_enforce_hand):
  player = game_state.players[player_id]
  possible_actions = []
  turn_actions = player.turn_actions
  num_cards_used = sum([sum(action.card_costs.values()) for action in turn_actions])

  if should_enforce_hand and num_cards_used >= 3:
    return possible_actions

  board = game_state.board
  tiles = board.get_tiles()

  for tile in tiles:
    action = Burn(player_id, tile.x, tile.y)

    if action.is_possible(game_state, should_enforce_hand) and get_should_burn(tile, board):
      possible_actions.append(action)

    action = Destroy(player_id, tile.x, tile.y)

    if action.is_possible(game_state, should_enforce_hand) and get_should_destroy(player_id, tile, board):
      possible_actions.append(action)
    
    action = Fertilize(player_id, tile.x, tile.y)

    if action.is_possible(game_state, should_enforce_hand) and get_should_fertilize(player_id, tile, board):
      possible_actions.append(action)

    action = Lock(player_id, tile.x, tile.y)

    if action.is_possible(game_state, should_enforce_hand) and get_should_lock(player_id, tile, board):
      possible_actions.append(action)

    action = Settle(player_id, tile.x, tile.y)

    if action.is_possible(game_state, should_enforce_hand):
      possible_actions.append(action)

    for i in range(-1, 2):
      for j in range(-1, 2):
        if i == j:
          continue

        adjX = tile.x + i
        adjY = tile.y + j
        action = Place(player_id, adjX, adjY)

        if action.is_possible(game_state, should_enforce_hand):
          possible_actions.append(action)

        action = Shift(player_id, tile.x, tile.y, adjX, adjY)

        if action.is_possible(game_state, should_enforce_hand) and get_should_shift(tile, board):
          possible_actions.append(action)

  add_first_cultivate(player_id, game_state, possible_actions, should_enforce_hand)
  
  return possible_actions
