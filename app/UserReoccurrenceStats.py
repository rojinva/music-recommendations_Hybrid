class UserReoccurrenceStats:
  USER_REOCCURRENCES = {}

  def add_reoccurrence_for_user(self, user_id, song_id, reoccurrence):
    if user_id not in self.USER_REOCCURRENCES:
      entity = UserReoccurrenceEntity()
      self.USER_REOCCURRENCES[user_id] = entity
    entity = self.USER_REOCCURRENCES[user_id]
    entity.song_reoccurrences[song_id] = reoccurrence
    entity.total_count += 1
    entity.reoccurrence += reoccurrence
    self.USER_REOCCURRENCES[user_id] = entity

  def get_average_reoccurrence_for_user(self, user_id):
    return self.USER_REOCCURRENCES[user_id].reoccurrence

  '''
  Call only once
  '''
  def calculate_averages(self):
    for user_id in self.USER_REOCCURRENCES.keys():
      entity = self.USER_REOCCURRENCES[user_id]
      average_reoccurrence = float(entity.reoccurrence) / entity.total_count
      entity.reoccurrence = average_reoccurrence
      self.USER_REOCCURRENCES[user_id] = entity


class UserReoccurrenceEntity:
  def __init__(self):
    self.total_count = 0
    self.reoccurrence = 0.0
    self.song_reoccurrences = {}
