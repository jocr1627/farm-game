class Tile:
  def __init__(self, x, y):
    self.is_fertile = False
    self.is_locked = False
    self.is_settled = False
    self.owner_id = None
    self.x = x
    self.y = y
