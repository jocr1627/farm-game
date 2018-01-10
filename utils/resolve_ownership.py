def resolve_ownership(game_state):
  board = game_state.board
  tiles = board.get_tiles()
  stack = []

  for tile in tiles:
    if tile.is_settled:
      if tile.is_fertile:
        stack.append(tile)
    else:
      tile.owner_id = None
  
  points_checked = set()

  while len(stack) > 0:
    tile = stack.pop()
    points_checked.add((tile.x, tile.y))
    owner_id = tile.owner_id

    for neighbor in board.get_neighbors(tile.x, tile.y):
      if not (neighbor.x, neighbor.y) in points_checked and neighbor.is_fertile:
        neighbor.owner_id = owner_id
        stack.append(neighbor)
  