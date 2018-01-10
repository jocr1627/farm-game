from Tile import Tile

class Place:
  card_costs = { "earth": 1 }
  name = "Place"

  def __init__(self, player_id, x, y):
    self.player_id = player_id
    self.x = x
    self.y = y

  def execute(self, game_state):
    player = game_state.players[self.player_id]

    for key,value in self.card_costs.items():
      player.hand.discard(key, value)
  
    tile = Tile(self.x, self.y)
    game_state.board.set_tile(tile)
    player.turn_actions.append(self)

  def is_possible(self, game_state, should_enforce_hand):
    board = game_state.board
    player = game_state.players[self.player_id]
    neighbors = board.get_neighbors(self.x, self.y)

    return (
      (
        not should_enforce_hand
        or all(map(lambda item: player.hand.get_count(item[0]) >= item[1], self.card_costs.items()))
      )
      and not board.has_tile(self.x, self.y)
      and len(neighbors) > 0
    )
  
  def undo(self, game_state):
    player = game_state.players[self.player_id]

    for key,value in self.card_costs.items():
      player.hand.draw(key, value)

    game_state.board.remove_tile(self.x, self.y)
    player.turn_actions.pop()
