from constants import Suits, Ranks
from random import shuffle


class Card(object):
  _all = {}
  
  def __new__(cls, pack, suit, rank):
    cards = cls._all.get(pack, {})
    if not cards:
      obj = object.__new__(cls)
      cards[(suit, rank)] = obj
      cls._all[pack] = cards
      return obj
    
    obj = cls._all[pack].get((suit, rank))
    if not obj:
      obj = object.__new__(cls)
      cls._all[pack][(suit, rank)] = obj
    return obj

  def __init__(self, pack, suit, rank):
    self.pack = pack
    self.suit = suit
    self.rank = rank

  def __str__(self):
    return self.__repr__()

  def __repr__(self):
    return "{}{}".format(self.rank.value, self.suit.value)


class Pack(object):
  _all = {}
  
  def __new__(cls, code):
    obj = cls._all.get(code)
    if not obj:
      obj = object.__new__(cls)
      cls._all[code] = obj
    return obj
  
  def __init__(self, code):
    self.code = code 
    self.sort()
  
  def sort(self):
    if hasattr(self, "not_dealed_cards"):
      delattr(self, "not_dealed_cards")
    self.cards = [Card(self, s, r) for s in Suits for r in Ranks]
    self.dealed_cards = []
  
  def add_to_dealed(self, *args):
    for dealed in args:
      self.not_dealed_cards.remove(dealed)
      self.dealed_cards.append(dealed)
  
  def shuffle(self):
    shuffle(self.cards)
    self.not_dealed_cards = self.cards[::]
