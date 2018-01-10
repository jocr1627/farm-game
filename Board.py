import math
from functools import reduce
from PIL import Image, ImageDraw, ImageFont
from Tile import Tile

class Board:
  def __init__(self, tiles={}):
    self.tiles = tiles
  
  def draw(self, size=1000):
    min_q = min(self.tiles.keys())
    max_q = max(self.tiles.keys())
    q_range = max_q - min_q + 1
    r_values = reduce(lambda acc, value: acc + list(value.keys()), self.tiles.values(), [])
    min_r = min(r_values)
    max_r = max(r_values)
    r_range = max_r - min_r + 1
    max_cartesian_range = max(0.5 * (3 ** 0.5) * (q_range + 0.5), 0.75 * (r_range - 1) + 1)
    side_length = size / (2 * max_cartesian_range)

    image = Image.new("RGB", (size, size), color="white")
    font = ImageFont.truetype("Arial.ttf", int(side_length))
    drawer = ImageDraw.Draw(image)

    for tile in self.get_tiles():
      q = tile.x - min_q
      r = tile.y - min_r
      center_x = (3 ** 0.5) * side_length * (q + 0.5 * r + 0.5)
      center_y = side_length * (1.5 * r + 1)
      points = []
      
      for angle in [30, 90, 150, 210, 270, 330]:
        x = center_x + side_length * math.cos(2 * math.pi * angle / 360)
        y = center_y + side_length * math.sin(2 * math.pi * angle / 360)
        points.append((x, y))

      color = "green" if tile.is_fertile else "brown"
      drawer.polygon(points, color, "black")

      if tile.is_locked:
        shift = 0.1 * side_length
        vertical_shift = 0.7 * side_length
        points = [
          (center_x + shift, center_y + shift - vertical_shift),
          (center_x - shift, center_y - shift - vertical_shift)
        ]
        drawer.rectangle(points, "white")

      if tile.is_settled:
        shift = 0.5 * side_length
        points = [
          (center_x + shift, center_y + shift),
          (center_x - shift, center_y - shift)
        ]
        drawer.rectangle(points, "black")
        drawer.text((center_x - 0.275 * side_length, center_y - 0.55 * side_length), str(tile.owner_id), fill="white", font=font)

    del drawer
    image.show()

  def get_neighbors(self, x, y):
    neighbors = []

    for i in range(-1, 2):
      for j in range(-1, 2):
        if i == j:
          continue
        
        neighbor = self.get_tile(x + i, y + j)
        
        if neighbor is not None:
          neighbors.append(neighbor)
    
    return neighbors

  def get_tile(self, x, y):
    if x not in self.tiles:
      return None
    
    return self.tiles[x][y] if y in self.tiles[x] else None
  
  def get_tiles(self):
    tiles = []

    for x in self.tiles:
      for y in self.tiles[x]:
        tiles.append(self.tiles[x][y])
    
    return tiles
  
  def has_tile(self, x, y):
    return self.get_tile(x, y) is not None
  
  def move_tile(self, x, y, targetX, targetY):
    if self.has_tile(x, y) and not self.has_tile(targetX, targetY):
      tile = self.get_tile(x, y)
      tile.x = targetX
      tile.y = targetY
      self.remove_tile(x, y)
      self.set_tile(tile)
  
  def remove_tile(self, x, y):
    if self.has_tile(x, y):
      del self.tiles[x][y]

      if len(self.tiles[x]) == 0:
        del self.tiles[x]
  
  def set_tile(self, tile):
    if tile.x not in self.tiles:
      self.tiles[tile.x] = {}
    
    self.tiles[tile.x][tile.y] = tile

  def swap_tiles(self, x0, y0, x1, y1):
    tile0 = self.get_tile(x0, y0)
    tile1 = self.get_tile(x1, y1)

    if tile0 is not None:
      tile0.x = x1
      tile0.y = y1
      self.set_tile(tile0)
    else:
      self.remove_tile(x1, y1)

    if tile1 is not None: 
      tile1.x = x0
      tile1.y = y0
      self.set_tile(tile1)
    else:
      self.remove_tile(x0, y0)
