from cards import Pack
from constants import GAME_SORTINGS


class Player(object):
  def __init__(self, desk, name):
    self.name = name
    self.desk = desk
    self.in_hand_cards = []
    self.played_cards = []
  
  def is_human(self):
    return True
    return self.name not in ["amir", "sina", "mohammad"]
  
  def play_card(self, i):
    self.played_cards.append(self.in_hand_cards.pop(i))
    return self.played_cards[-1]
  
  def index_of_suit(self, suit):
    crds = self.in_hand_cards
    for i, crd in enumerate(crds):
      if crd.suit is suit:
        return i
    return -1
  
  def last_index_of_suit(self, suit):
    crds = list(reversed(self.in_hand_cards))
    
    for i, crd in enumerate(crds):
      if crd.suit is suit:
        return len(crds) - i - 1
    return -1
  
  def __repr__(self):
    return "{} on {}".format(self.name, self.desk.code)
  
  def __str__(self):
    return "{}".format(self.name)
  

class Desk(object):
  _all = {}
  def __new__(cls, code, game, players):
    obj = cls._all.get(code)
    if not obj:
      obj = object.__new__(cls)
      cls._all[code] = obj
    return obj

  def __init__(self, code, game, players):
    self.game = game
    self.code = code
    plrs = []
    for i, plr in enumerate(reversed(players)):
      plr = Player(self, plr)
      if i != 0:
        plr.next = plrs[i-1]
      plrs.append(plr)
    plrs[0].next = plrs[-1]
    self.players = tuple(reversed(plrs))


class Game(object):
  
  @classmethod
  def get_sorting_key(cls):
    return GAME_SORTINGS[cls.__name__]
  
  def __init__(self, code, players):
    self.desk = Desk(code, self, players)
    self.pack = Pack(code)
  