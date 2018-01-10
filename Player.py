import random
from actions.Burn import Burn
from actions.Cultivate import Cultivate
from actions.Destroy import Destroy
from actions.Fertilize import Fertilize
from actions.Lock import Lock
from actions.Move import Move
from actions.Place import Place
from actions.Settle import Settle
from actions.Shift import Shift
from Hand import Hand

def default_get_action_priority_list():
  action_priority_lists = [
    [Cultivate, Fertilize, Settle, Place, Move, Shift, Destroy, Burn, Lock]
    # [Cultivate, Fertilize, Lock, Settle, Burn, Move, Shift, Place, Destroy],
    # [Settle, Place, Burn, Destroy, Cultivate, Fertilize, Lock, Move, Shift],
    # [Settle, Place, Burn, Destroy, Cultivate, Fertilize, Lock, Move, Shift],
    # [Settle, Place, Burn, Destroy, Cultivate, Fertilize, Lock, Move, Shift],
    # [Settle, Place, Cultivate, Fertilize, Move, Shift, Lock, Burn, Destroy]
  ]

  return action_priority_lists[0]

def get_place(player_id, game_state):
  scores = game_state.get_scores()
  current_score = scores[player_id]
  
  return sorted(scores.values(), reverse=True).index(current_score)

def default_action_strategy(player_id, game_state, should_enforce_hand, depth):
  if depth <= 0:
    return []

  scores = game_state.get_scores()
  current_score = scores[player_id]
  current_place = get_place(player_id, game_state)
  player = game_state.players[player_id]
  action_priority_list = player.get_action_priority_list()
  possible_actions = game_state.get_possible_actions(player_id, should_enforce_hand)
  possible_actions = sorted(possible_actions, key=lambda action: action_priority_list.index(action.__class__))
  outcomes = []

  for action in possible_actions:
    action.execute(game_state)

    next_actions = default_action_strategy(player_id, game_state, should_enforce_hand, depth - 1)
    
    for next_action in next_actions:
      next_action.execute(game_state)

    action_stack = [action] + next_actions
    place = get_place(player_id, game_state)
    score = game_state.get_scores()[player_id]

    if place <= current_place or score >= current_score:
      outcomes.append({ "actions": action_stack, "place": place, "score": score })
  
    for action_in_stack in reversed(action_stack):
      action_in_stack.undo(game_state)

    if place < current_place and score > current_score:
      break
  
  best_outcomes = sorted(outcomes, key=lambda outcome: outcome["place"])
  best_outcomes = [outcome for outcome in best_outcomes if outcome["place"] == best_outcomes[0]["place"]]
  best_outcomes = sorted(best_outcomes, key=lambda outcome: outcome["score"], reverse=True)
  best_outcome = best_outcomes[0] if len(best_outcomes) > 0 else None

  return best_outcome["actions"] if best_outcome is not None else []

def default_draw_strategy(player_id, game_state, should_print):
  player = game_state.players[player_id]
  turn_actions = player.turn_actions
  player.turn_actions = []
  actions = player.action_strategy(player_id, game_state, False, player.max_depth)
  player.turn_actions = turn_actions
  card_costs = []

  if len(actions) > 0:
    card_costs = sorted(actions[0].card_costs.items(), key=lambda item: item[1], reverse=True)
    
  while player.hand.get_size() < 4:
    card_to_draw = None
  
    for key,num in card_costs:
      if player.hand.get_count(key) < num:
        card_to_draw = key
        break

    if card_to_draw is None:
      card_to_draw = sorted(player.hand.card_counts.items(), key=lambda item: item[1])[0][0]
    
    if player.hand.get_count("fire") < 1:
      card_to_draw = "fire"

    player.hand.draw(card_to_draw, 1)
    
    if should_print:
      print(player_id, "draw", card_to_draw)

class Player:
  next_player_id = 0

  def __init__(
    self,
    card_counts={},
    get_action_priority_list=default_get_action_priority_list,
    max_depth=1,
    action_strategy=default_action_strategy,
    draw_strategy=default_draw_strategy
  ):
    self.action_strategy = action_strategy
    self.draw_strategy = draw_strategy
    self.id = Player.next_player_id
    self.get_action_priority_list = get_action_priority_list
    self.hand = Hand(card_counts)
    self.max_depth = max_depth
    self.turn_actions = []

    Player.next_player_id += 1

  def take_turn(self, game_state, should_print=False):
    self.turn_actions = []
    is_done = False

    while not is_done:
      actions = self.action_strategy(self.id, game_state, True, self.max_depth)
      
      if len(actions) == 0:
        is_done = True
      else:
        action = actions[0]

        if should_print:
          print(self.id, action.name)

        action.execute(game_state)

    self.draw_strategy(self.id, game_state, should_print)
