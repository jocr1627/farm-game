from utils.get_is_continuous import get_is_continuous
from utils.get_is_valid_placement import get_is_valid_placement
from utils.resolve_ownership import resolve_ownership

class Shift:
  card_costs = { "air": 1 }
  name = "Shift"

  def __init__(self, player_id, x, y, targetX, targetY):
    self.player_id = player_id
    self.targetX = targetX
    self.targetY = targetY
    self.x = x
    self.y = y

  def execute(self, game_state):
    board = game_state.board
    player = game_state.players[self.player_id]

    for key,value in self.card_costs.items():
      player.hand.discard(key, value)

    board.swap_tiles(self.x, self.y, self.targetX, self.targetY)
    resolve_ownership(game_state)
    player.turn_actions.append(self)

  def is_possible(self, game_state, should_enforce_hand):
    board = game_state.board
    player = game_state.players[self.player_id]
    is_continuous = get_is_continuous(board)
    tile = board.get_tile(self.x, self.y)
    target_tile = board.get_tile(self.targetX, self.targetY)
    is_valid_placement = False
    is_valid_target_placement = False

    if tile is not None:
      tile_owner_id = tile.owner_id if tile.is_settled else None
      is_valid_placement = get_is_valid_placement(tile, board, owner_id=tile_owner_id, x=self.targetX, y=self.targetY)
    if target_tile is not None:
      target_tile_owner_id = target_tile.owner_id if target_tile.is_settled else None
      is_valid_target_placement = get_is_valid_placement(target_tile, board, owner_id=target_tile_owner_id, x=self.x, y=self.y)

    return (
      (
        not should_enforce_hand
        or all(map(lambda item: player.hand.get_count(item[0]) >= item[1], self.card_costs.items()))
      )
      and board.has_tile(self.x, self.y)
      and not tile.is_locked
      and (target_tile is None or not target_tile.is_locked)
      and abs(self.targetX - self.x) <= 1
      and abs(self.targetY - self.y) <= 1
      and (self.x != self.targetX or self.y != self.targetY)
      and is_continuous
      and is_valid_placement
      and is_valid_target_placement
    )
  
  def undo(self, game_state):
    player = game_state.players[self.player_id]

    for key,value in self.card_costs.items():
      player.hand.draw(key, value)

    game_state.board.swap_tiles(self.x, self.y, self.targetX, self.targetY)
    resolve_ownership(game_state)
    player.turn_actions.pop()
