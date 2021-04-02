import random
random.seed(42)
class Deck():
  def __init__(self):
    # We Will not differentiate between types of cards, only their values
    self.deck = []
    for i in range(2, 10):
      for j in range(4):
        self.deck += [i]
    # 10 has 16 values(10, J, Q, K)
    for i in range(16):
      self.deck += [10]
    # Add Aces(11)
    for i in range(4):
      self.deck += [11]
    self.length = len(self.deck)
    assert self.length == 52
  def shuffle(self):
    random.shuffle(self.deck)
  def get_item(self, i):
    return self.deck[i]
  def first_two_cards(self, cur_idx):
    card_one = self.deck[cur_idx]
    card_two = self.deck[cur_idx + 1]
    return card_one + card_two
class BlackJack:
  '''
  Deals with logic of the game of blackjack.
  '''
  def __init__(self, deck):
    self.deck = deck
  def turn(self, cur_idx, num_hits):
    '''
    Assuming two-player blackjack(other player must hit same amount), runs one turn of blackjack, returning earnings(-1, 0, 1) and num cards played(4 + 2h) in linear time.

    If a player busts early, just ignore this version(Illegal Game), return -inf and DP will ignore this version.

    Rules(My Adaptation):
    - You draw 2 cards, they draw 2 cards
    - You draw first, then they draw.
    - If you bust, -1
    - If they bust, 1
    - if no one busts, 0
    '''
    # Draw 2 Cards Each
    if cur_idx + 4 >= self.deck.length:
        return -1, float('-inf')
    my_score = self.deck.first_two_cards(cur_idx)
    player2_score = self.deck.first_two_cards(cur_idx + 2)
    cur_idx += 4
    count = num_hits * 2
    # Start Drawing Cards.
    while True:
      if cur_idx >= self.deck.length:
        # Deck Completed Anyways, return -inf.
        return -1, float('-inf')
      if count == 0:
        break
      my_score += self.deck.get_item(cur_idx)
      cur_idx += 1
      count -= 1
      if cur_idx >= self.deck.length:
        return -1, float('-inf')
      if my_score > 21: # Busted
        return cur_idx, -1

      player2_score += self.deck.get_item(cur_idx)
      cur_idx += 1
      count -= 1
      if cur_idx >= self.deck.length:
        return -1, float('-inf')
      if player2_score > 21:
        # They Busted
        return cur_idx, 1
    if my_score > 21:
      return cur_idx, -1
    elif player2_score > 21:
      return cur_idx, 1
    else:
      return cur_idx, 0
class DP:
  def __init__(self):
    self.deck = Deck()
    self.deck.shuffle()
    self.black_jack = BlackJack(self.deck)
    self.memoized = {}
    self.parent_pointers = {}
    self.len_deck = self.deck.length
  def reset(self):
    self.memoized = {} # reset Memoized Vals
    self.parent_pointers = {}
  def decode_pointers(self):
    '''
    Decodes a full Game of BlackJack.
    '''
    cur_idx = 0
    vals = []

    while cur_idx in self.parent_pointers:
      if self.parent_pointers[cur_idx] == None:
        # walk away from table
        return vals
      cur_score = self.memoized[cur_idx]
      idx = self.parent_pointers[cur_idx]
      score = self.memoized[idx]
      vals += [((cur_idx, cur_score), (idx, score))]
      cur_idx = idx
    return vals

  def optimize_deck(self, cur_idx):
    '''
    Recursively Optimizes the Deck using Dynamic Programming.
    '''
    # Check if Memoized already:
    if cur_idx in self.memoized:
      return self.memoized[cur_idx]
    distance = []
    best_idx = -1
    best_val = 0
    for i in range(0, self.len_deck - cur_idx):
      o = self.black_jack.turn(cur_idx, i)
      idx, score = o
      if idx == -1:
          break
      optim_score = self.optimize_deck(idx)
      best_score = optim_score + score
      distance += [best_score]
      if best_score > best_val:
        best_val = best_score
        best_idx = idx
    self.memoized[cur_idx] = best_val
    if best_idx == -1:
      # Walk Away
      self.parent_pointers[cur_idx] = None
    else:
      self.parent_pointers[cur_idx] = best_idx
    return best_val
def main():
  blackJack = DP()
  blackJack.optimize_deck(0)
  print(blackJack.decode_pointers())
if __name__ == '__main__':
  main()