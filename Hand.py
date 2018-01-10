from copy import deepcopy

class Hand:
  def __init__(self, card_counts={}):
    self.card_counts = deepcopy(card_counts)
  
  def discard(self, key, num):
    self.card_counts[key] = self.card_counts[key] - num

  def draw(self, key, num):
    self.card_counts[key] += num
  
  def get_count(self, card_name):
    return self.card_counts[card_name] if card_name in self.card_counts.keys() else 0
  
  def get_size(self):
    return sum(self.card_counts.values())
