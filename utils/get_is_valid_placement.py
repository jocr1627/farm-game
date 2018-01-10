def get_is_valid_neighbor(neighbor, owner_id):
  return not neighbor.is_fertile or neighbor.owner_id is None or neighbor.owner_id == owner_id

def get_is_valid_placement(tile, board, **changes):
  is_fertile = changes["is_fertile"] if "is_fertile" in changes else tile.is_fertile
  is_settled = changes["is_settled"] if "is_settled" in changes else tile.is_settled
  owner_id = changes["owner_id"] if "owner_id" in changes else tile.owner_id
  x = changes["x"] if "x" in changes else tile.x
  y = changes["y"] if "y" in changes else tile.y

  if not is_fertile:
    return True

  neighbors = board.get_neighbors(x, y)
  is_valid_placement = True

  if owner_id is None:
    owner_ids = [neighbor.owner_id for neighbor in neighbors if neighbor.owner_id is not None]
    owner_id = owner_ids[0] if len(owner_ids) > 0 else None

  for neighbor in neighbors:
    if not get_is_valid_neighbor(neighbor, owner_id):
      is_valid_placement = False
      break

  return is_valid_placement
