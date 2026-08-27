import os


class LeaderboardManager:

  def __init__(self, filename="scores.txt"):
    self.filename = filename
    self.high_score = self.load_high_score()
    self.current_score = self.get_current_score()
    

  def load_high_score(self):
    # Read the high score from the text file if it exists
    if os.path.exists(self.filename):
      try:
        with open(self.filename, "r") as score:
          content = score.read().strip()
          if content.isdigit(): # score is + int always 
            return int(content)
          else:
            return 0
      except Exception:
        return 0
    return 0

  def check_and_update(self, current_score):
    # Check if the current score beats the high score
    if current_score > self.high_score:
      self.high_score = current_score
      self.save_high_score()
      return True  # Returns True if a new high score was achieved!
    return False

  def save_high_score(self):
    # Save the new high score into the text file
    try:
      with open(self.filename, "w") as score:
        score.write(str(self.high_score))
    except Exception as e:
      print(f"Error saving high score: {e}")

  def get_high_score(self):
    # Returns the high score
    return self.high_score

  def get_current_score(self):
    # Returns the current score
    return self.current_score
