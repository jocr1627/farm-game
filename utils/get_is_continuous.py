def get_is_continuous(board, removed_tiles=[]):
  tiles = [tile for tile in board.get_tiles() if tile not in removed_tiles]

  if len(tiles) == 0:
    return False

  stack = [tiles[0]]
  traversed_points = set()

  while len(stack) > 0:
    tile = stack.pop()
    traversed_points.add((tile.x, tile.y))
    
    for neighbor in board.get_neighbors(tile.x, tile.y):
      if (neighbor.x, neighbor.y) not in traversed_points and neighbor not in removed_tiles:
        stack.append(neighbor)
  
  return len(tiles) == len(traversed_points)
