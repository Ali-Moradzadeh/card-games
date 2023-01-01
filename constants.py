from enum import Enum


SPADE = "\u2660"
HEART = "\u2661"
DIAMOND = "\u2662"
CLUB = "\u2663"

HOKM_VALIDATOR = "Hokm"
HOKM_TAKNARAS = "taknaras"
HOKM_NARAS = "naras"
HOKM_SARAS = "saras"
HOKM_MID_TEAMMATE = "mid teammate"

class Ranks(Enum):
  ACE = "A"
  KING = "K"
  QUEEN = "Q"
  JACK = "J"
  TEN = "10"
  NINE = "9"
  EIGHT = "8"
  SEVEN = "7"
  SIX = "6"
  FIVE = "5"
  FOUR = "4"
  THREE = "3"
  TWO = "2"


class Suits(Enum):
  SPADE = SPADE
  HEART = HEART
  CLUB = CLUB
  DIAMOND = DIAMOND


class HokmType(Enum):
  SPADE = SPADE
  HEART = HEART
  CLUB = CLUB
  DIAMOND = DIAMOND
  TAKNARAS = HOKM_TAKNARAS
  NARAS = HOKM_NARAS
  SARAS = HOKM_SARAS
  MID_TEAMMATE = HOKM_MID_TEAMMATE

SORTED_RANKS = tuple([r for r in Ranks])
SORTED_SUITS = tuple([s for s in Suits])
SORTED_HOKMTYPE = tuple([h for h in HokmType])

HOKM_SORTING_CARDS = lambda crd : 13 * SORTED_SUITS.index(crd.suit) + SORTED_RANKS.index(crd.rank) + 1

HOKM_ORDINARY_KEY = lambda crd, desk_suit, hokm_suit: 13 * (2 if crd.suit.value == hokm_suit.value else (1 if crd.suit is desk_suit else 0)) + list(reversed(SORTED_RANKS)).index(crd.rank) + 1

_srtd_rnks = SORTED_RANKS[1:] + SORTED_RANKS[0:1]
HOKM_TAKNARAS_KEY = lambda crd, desk_suit, _: 13 * (1 if crd.suit is desk_suit else 0) + _srtd_rnks.index(crd.rank) + 1

HOKM_NARAS_KEY = lambda crd, desk_suit, _ : 13 * (1 if crd.suit is desk_suit else 0) + SORTED_RANKS.index(crd.rank) + 1

HOKM_SARAS_KEY = lambda crd, desk_suit, _ : 13 * (1 if crd.suit is desk_suit else 0) + list(reversed(SORTED_RANKS)).index(crd.rank) + 1

HOKM_HOKM_TYPES_SORTING_KEYS = {
  SPADE : HOKM_ORDINARY_KEY,
  HEART : HOKM_ORDINARY_KEY,
  CLUB : HOKM_ORDINARY_KEY,
  DIAMOND : HOKM_ORDINARY_KEY,
  HOKM_MID_TEAMMATE : HOKM_ORDINARY_KEY,
  HOKM_TAKNARAS : HOKM_TAKNARAS_KEY,
  HOKM_NARAS : HOKM_NARAS_KEY,
  HOKM_SARAS : HOKM_SARAS_KEY,
}

GAME_SORTINGS = {
  HOKM_VALIDATOR : HOKM_SORTING_CARDS,
}
