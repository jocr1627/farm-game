from utils.resolve_ownership import resolve_ownership

class Burn:
  card_costs = { "fire": 1 }
  name = "Burn"

  def __init__(self, player_id, x, y):
    self.player_id = player_id
    self.x = x
    self.y = y

  def execute(self, game_state):
    player = game_state.players[self.player_id]
    tile = game_state.board.get_tile(self.x, self.y)

    for key,value in self.card_costs.items():
      player.hand.discard(key, value)
  
    tile.is_fertile = False
    resolve_ownership(game_state)
    player.turn_actions.append(self)

  def is_possible(self, game_state, should_enforce_hand):
    board = game_state.board
    player = game_state.players[self.player_id]
    tile = board.get_tile(self.x, self.y)

    return (
      (
        not should_enforce_hand
        or all(map(lambda item: player.hand.get_count(item[0]) >= item[1], self.card_costs.items()))
      )
      and board.has_tile(self.x, self.y)
      and not tile.is_locked
      and tile.is_fertile
    )
  
  def undo(self, game_state):
    player = game_state.players[self.player_id]
    tile = game_state.board.get_tile(self.x, self.y)

    for key,value in self.card_costs.items():
      player.hand.draw(key, value)

    tile.is_fertile = True
    resolve_ownership(game_state)
    player.turn_actions.pop()
