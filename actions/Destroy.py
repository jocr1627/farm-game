from utils.get_is_continuous import get_is_continuous
from utils.resolve_ownership import resolve_ownership

class Destroy:
  card_costs = { "fire": 3 }
  name = "Destroy"

  def __init__(self, player_id, x, y):
    self.player_id = player_id
    self.x = x
    self.y = y

  def execute(self, game_state):
    board = game_state.board
    player = game_state.players[self.player_id]

    for key,value in self.card_costs.items():
      player.hand.discard(key, value)
    
    self.tile = board.get_tile(self.x, self.y)
    board.remove_tile(self.x, self.y)
    resolve_ownership(game_state)
    player.turn_actions.append(self)

  def is_possible(self, game_state, should_enforce_hand):
    board = game_state.board
    player = game_state.players[self.player_id]
    tile = board.get_tile(self.x, self.y)
    is_continuous = get_is_continuous(board, [tile])

    return (
      (
        not should_enforce_hand
        or all(map(lambda item: player.hand.get_count(item[0]) >= item[1], self.card_costs.items()))
      )
      and board.has_tile(self.x, self.y)
      and not tile.is_locked
      and is_continuous
    )
  
  def undo(self, game_state):
    player = game_state.players[self.player_id]

    for key,value in self.card_costs.items():
      player.hand.draw(key, value)

    game_state.board.set_tile(self.tile)
    resolve_ownership(game_state)
    player.turn_actions.pop()
