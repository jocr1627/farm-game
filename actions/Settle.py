from utils.get_is_valid_placement import get_is_valid_placement
from utils.resolve_ownership import resolve_ownership

class Settle:
  card_costs = { "earth": 2 }
  name = "Settle"

  def __init__(self, player_id, x, y):
    self.player_id = player_id
    self.x = x
    self.y = y

  def execute(self, game_state):
    player = game_state.players[self.player_id]
    tile = game_state.board.get_tile(self.x, self.y)

    for key,value in self.card_costs.items():
      player.hand.discard(key, value)
  
    tile.is_settled = True
    tile.owner_id = self.player_id
    resolve_ownership(game_state)
    player.turn_actions.append(self)

  def is_possible(self, game_state, should_enforce_hand):
    board = game_state.board
    player = game_state.players[self.player_id]
    tile = board.get_tile(self.x, self.y)
    is_valid_placement = tile is not None and get_is_valid_placement(tile, board, owner_id=player.id)

    return (
      (
        not should_enforce_hand
        or all(map(lambda item: player.hand.get_count(item[0]) >= item[1], self.card_costs.items()))
      )
      and board.has_tile(self.x, self.y)
      and board.get_tile(self.x, self.y).owner_id is None
      and is_valid_placement
    )
  
  def undo(self, game_state):
    player = game_state.players[self.player_id]
    tile = game_state.board.get_tile(self.x, self.y)

    for key,value in self.card_costs.items():
      player.hand.draw(key, value)

    tile.is_settled = False
    tile.owner_id = None
    resolve_ownership(game_state)
    player.turn_actions.pop()
