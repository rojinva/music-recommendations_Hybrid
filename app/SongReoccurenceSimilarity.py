import math
from datetime import datetime

from app.UserReoccurrenceStats import UserReoccurrenceStats


class SongReoccurrenceSimilarity:
  urs = UserReoccurrenceStats()

  def average_user_reoccurrence(self, user_id):
    return self.urs.get_average_reoccurrence_for_user(user_id)

  def song_to_song_similarity(self, song_a_reoccurrence, song_b_reoccurrence):
    intersected_users = song_a_reoccurrence.compute_intersection(
        song_b_reoccurrence)
    if len(intersected_users) == 0:
      return 0.0
    song_a_values = song_a_reoccurrence.song_user_reoccurrences
    song_b_values = song_b_reoccurrence.song_user_reoccurrences
    upper_sum = lower_sum_a = lower_sum_b = 0.0
    for user_id in intersected_users:
      r_u_a = float(song_a_values[user_id])
      r_u_b = float(song_b_values[user_id])
      r_u = self.average_user_reoccurrence(user_id)
      upper_sum += (r_u_a - r_u) * (r_u_b - r_u)
      lower_sum_a += (r_u_a - r_u) * (r_u_a - r_u)
      lower_sum_b += (r_u_b - r_u) * (r_u_b - r_u)
    if lower_sum_a < 1e-6 or lower_sum_b < 1e-6:
      return 0.0
    similarity_a_b = upper_sum / (
        math.sqrt(lower_sum_a) * math.sqrt(lower_sum_b))
    return similarity_a_b


class SongPairsSimilarity:
  song_sim = SongReoccurrenceSimilarity()
  MIN_SIMILARITY = 1e-2
  SONG_TO_SONG_SIMILARITY = {}

  def calculate_pairwise_similarity(self, song_user_reoccurrences):
    count = 0
    start_timer = datetime.now()
    songs_ids = song_user_reoccurrences.keys()
    for song_a_id in songs_ids:
      count += 1
      if count % 1000 == 0:
        print("Reoccurrence " + str(count))
        print(datetime.now()-start_timer)
        start_timer = datetime.now()
      to_others_similarity = {}
      for song_b_id in songs_ids:
        if song_a_id is not song_b_id:
          similarity = self.song_sim.song_to_song_similarity(
              song_user_reoccurrences[song_a_id],
              song_user_reoccurrences[song_b_id])
          if similarity > self.MIN_SIMILARITY:
            to_others_similarity[song_b_id] = similarity
      self.SONG_TO_SONG_SIMILARITY[song_a_id] = to_others_similarity
    return self.SONG_TO_SONG_SIMILARITY
