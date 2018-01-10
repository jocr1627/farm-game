from utils.get_is_valid_placement import get_is_valid_placement
from utils.resolve_ownership import resolve_ownership

class Cultivate:
  card_costs = { "water": 3 }
  name = "Cultivate"

  def __init__(self, player_id, points):
    self.player_id = player_id
    self.points = points

  def execute(self, game_state):
    board = game_state.board
    player = game_state.players[self.player_id]

    for key,value in self.card_costs.items():
      player.hand.discard(key, value)

    for x,y in self.points:
      board.get_tile(x, y).is_fertile = True

    resolve_ownership(game_state)
    player.turn_actions.append(self)

  def is_possible(self, game_state, should_enforce_hand):
    board = game_state.board
    player = game_state.players[self.player_id]
    are_points_valid = all(
      map(
        lambda item: (
          board.has_tile(item[0], item[1])
          and not board.get_tile(item[0], item[1]).is_fertile
          and get_is_valid_placement(board.get_tile(item[0], item[1]), board, is_fertile=True)
        ),
        self.points
      )
    )

    all_relevant_tiles = [board.get_tile(x, y) for x,y in self.points if board.has_tile(x, y)]
    
    for x,y in self.points:
      all_relevant_tiles += board.get_neighbors(x, y)
    
    non_null_owner_ids = [tile.owner_id for tile in all_relevant_tiles if tile.owner_id is not None]
    first_non_null_owner_id = non_null_owner_ids[0] if len(non_null_owner_ids) > 0 else None
    all_owners_are_equal = all(
      map(
        lambda tile: tile.owner_id is None or tile.owner_id == first_non_null_owner_id,
        all_relevant_tiles
      )
    )

    return (
      (
        not should_enforce_hand
        or all(map(lambda item: player.hand.get_count(item[0]) >= item[1], self.card_costs.items()))
      )
      and are_points_valid
      and all_owners_are_equal
    )
  
  def undo(self, game_state):
    board = game_state.board
    player = game_state.players[self.player_id]

    for key,value in self.card_costs.items():
      player.hand.draw(key, value)

    for x,y in self.points:
      board.get_tile(x, y).is_fertile = False

    resolve_ownership(game_state)
    player.turn_actions.pop()
