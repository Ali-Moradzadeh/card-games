import os
from desk import Game
import constants
from random import choice
from enum import Enum


class Hokm(Game):
  
  def __init__(self, code, players, colapse_over_win=False):
    
    if len(players) != 4:
      raise ValueError("hokm must has exactly 4 players")
    super().__init__(code, players)
    self.sets_tricks = tuple([[[] for _ in range(13)] for _ in range(7)])
    
    self.colapse_over_win = colapse_over_win
    self.leader = None
    self.lead = None
    self.hand_scores = [0, 0]
    self.trick_scores = [0, 0]
  
  @property
  def played_hands(self):
    return sum(self.hand_scores)
  
  @property
  def played_tricks(self):
    return sum(self.trick_scores)
    
  def get_lead_sorting_key(self):
    return constants.HOKM_HOKM_TYPES_SORTING_KEYS[self.lead.value]
  
  def start(self):
    self.pack.shuffle()
    self.set_leader()
    self.start_hand()
  
  def start_hand(self):
    self.trick_scores = [0, 0]
    self.print_specials()
    self.pack.sort()
    self.pack.shuffle()
    self.deal_first_trick()
    self.set_lead()
    self.deal_other_tricks()
    self.sort_players_cards()
    self.start_trick()
  
  def sort_players_cards(self):
    key = self.get_sorting_key()
    for plr in self.desk.players:
      plr.in_hand_cards = sorted(plr.in_hand_cards, key=key)
  
  def set_lead(self):
    s = constants.SORTED_HOKMTYPE
    if self.leader.is_human():
      suits = list(enumerate(s, start=1))
      pr = lambda s : f"{s[0]} for {s[1].value}"
      print(self.leader , self.leader.in_hand_cards)
      p = ("\nselect lead suit\ninsert " + (len(s)*"{}, ")[:-2] + " : ").format(*list(map(pr, suits)))
      
      while not (inp:=input(p)).isnumeric() or not 0 <= (i:=int(inp)-1) < len(s):
        print("valids are 1, 2, 3, 4")
      else:
        if s[i].value == constants.HOKM_MID_TEAMMATE:
          self.lead = self.leader.next.next.in_hand_cards[2].suit
        else:
          self.lead = s[i]
    else :
      self.lead = choice(s)

  def deal_other_tricks(self):
    current_plr = self.leader
    for i in range(8):
      to_deal = self.pack.not_dealed_cards[:4]
      self.pack.add_to_dealed(*to_deal)
      current_plr.in_hand_cards.extend(to_deal)
      current_plr = current_plr.next
  
  def set_leader(self):
    for i, card in enumerate(self.pack.cards):
      if card.rank == constants.Ranks.ACE:
        self.leader = self.desk.players[i%4]
        self.trick_starting_player = self.leader
        return
  
  def deal_first_trick(self):
    if not self.pack.dealed_cards:
      self.pack.add_to_dealed(*self.pack.not_dealed_cards[:20])
      plrs = self.desk.players
      
      curr = self.leader
      for i in range(4):
        curr.in_hand_cards = self.pack.dealed_cards[i*5:i*5+5]
        curr = curr.next
  
  def _valid_range(self, plr, suit=None):
    crds = plr.in_hand_cards
    if not suit:
      return (1, len(crds))
    
    index = plr.index_of_suit(suit)
    if index == -1:
      return (1, len(crds))
    
    last_index = plr.last_index_of_suit(suit)
    return (index+1, last_index+1)
  
  def start_trick(self):
    self.print_specials()
    self.play_trick()
    self.set_trick_winner()
    self.next_step()
  
  def play_trick(self):
    self.trick_suit = None
    current_plr = self.trick_starting_player
    
    while len(self.current_trick_list) != 4:
      crds = current_plr.in_hand_cards
      mn, mx = self._valid_range(current_plr, self.trick_suit)
      
      print("", f"desk cards : {self.current_trick_list}", sep="\n")
      print(f"\n{current_plr} cards :", crds, sep="\n")
      
      msg = "type your chosen card number ({} to {}) : ".format(mn, mx)
      
      while not (inp:=input(msg)).isnumeric() or not mn-1 <= (i:=int(inp)-1) < mx:
        print("try again")
      else:
        crd = current_plr.play_card(i)
        self.current_trick_list.append(crd)
        if not self.trick_suit:
          self.trick_suit = crd.suit
      current_plr = current_plr.next
  
  def set_trick_winner(self):
    print(self.trick_suit)
    key = lambda crd : self.get_lead_sorting_key()(crd, self.trick_suit, self.lead)
    winner_crd = lambda crd : key(crd)
    crd = sorted(self.current_trick_list, key=winner_crd)[-1]
    
    winner = list(filter(lambda plr : crd in plr.played_cards, self.desk.players))[0]
    self.trick_starting_player = winner
  
  def next_step(self):
    plrs = self.desk.players
    index = plrs.index(self.trick_starting_player)%2
    self.trick_scores[index] += 1
    
    #hand not finished yet
    if by7:=self.trick_scores[index]%7:
      self.start_trick()
    #hand finished
    else:
      changing_leader = self.trick_starting_player not in (self.leader, self.leader.next.next)
      #finished with koat
      if not self.trick_scores[1 - index]:
        self.hand_scores[index] += (2 + changing_leader)
      else :
        self.hand_scores[index] += 1
      
      if (self.hand_scores[index] >= 7 and not self.colapse_over_win) or self.hand_scores[index] == 7:
        plr = self.trick_starting_player
        os.system("clear")
        print(plr, plr.next.next, "won")
        return
      
      if self.colapse_over_win:
        self.hand_scores[index] %= 7
      
      if changing_leader:
        self.leader = self.leader.next
      self.trick_starting_player = self.leader
      
      self.start_hand()
    #hand finished normally
 
  @property
  def current_trick_list(self):
    return self.sets_tricks[self.played_hands][self.played_tricks]
  
  def print_specials(self):
    os.system("clear")
    print("leader : ", self.leader)
    print("lead : ", self.lead.value if self.lead else self.lead)
    print()
    print("hand scores : ", self.hand_scores)
    print("trick scores : ", self.trick_scores)
    print()
