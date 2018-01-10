class GameState:
  def __init__(self, options):
    self.board = options["board"] if "board" in options else Board()
    self._get_is_over = options["get_is_over"]
    self._get_possible_actions = options["get_possible_actions"]
    self._get_scores = options["get_scores"]
    self.players = options["players"]
    self.turn_number = 0
  
  def get_is_over(self):
    return self._get_is_over(self)

  def get_possible_actions(self, player_id, should_enforce_hand):
    return self._get_possible_actions(player_id, self, should_enforce_hand)

  def get_scores(self):
    return self._get_scores(self)
