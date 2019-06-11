class SongReoccurrenceStats:
  SONG_USER_REOCCURRENCES = {}

  def put_reoccurrence_for_song(self, song_id, user_id, reoccurence_value):
    if song_id not in self.SONG_USER_REOCCURRENCES.keys():
      reoccurrence = SongReoccurrence()
      self.SONG_USER_REOCCURRENCES[song_id] = reoccurrence
    reoccurrence = self.SONG_USER_REOCCURRENCES[song_id]
    reoccurrence.put_reoccurence(user_id, reoccurence_value)
    self.SONG_USER_REOCCURRENCES[song_id] = reoccurrence


class SongReoccurrence:
  def __init__(self):
    self.song_user_reoccurrences = {}

  def put_reoccurence(self, user_id, reoccurrence):
    self.song_user_reoccurrences[user_id] = reoccurrence

  def compute_intersection(self, other_song_reoccurrence):
    this_song_stats = self.song_user_reoccurrences.keys()
    other_song_stats = other_song_reoccurrence.song_user_reoccurrences.keys()
    user_ids_intersection = list(set(this_song_stats) & set(other_song_stats))
    return user_ids_intersection
