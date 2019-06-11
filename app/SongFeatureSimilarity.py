from datetime import datetime

import pandas

from app.DataReader import DataReader, DataSource


class SongFeatureSimilarity:
  data_reader = DataReader()
  SONG_DATA = {}
  CACHED_SIMILARITIES = {}

  def __init__(self):
    entries = self.data_reader.read_file(DataSource.SONGS)
    for index, row in entries.iterrows():
      self.SONG_DATA[row['song_id']] = row

  def compute_song_to_song_similarity(self, song_a_id, song_b_id):
    if song_a_id in self.CACHED_SIMILARITIES.keys():
      if song_b_id in self.CACHED_SIMILARITIES[song_a_id].keys():
        return self.CACHED_SIMILARITIES[song_a_id][song_b_id]
    score = self.__calculate_similarity(song_a_id, song_b_id)
    self.__cache_similarity(song_a_id, song_b_id, score)
    return score

  def __cache_similarity(self, song_a_id, song_b_id, similarity):
    if song_a_id not in self.CACHED_SIMILARITIES.keys():
      self.CACHED_SIMILARITIES[song_a_id] = {}
    self.CACHED_SIMILARITIES[song_a_id][song_b_id] = similarity
    if song_b_id not in self.CACHED_SIMILARITIES.keys():
      self.CACHED_SIMILARITIES[song_b_id] = {}
    self.CACHED_SIMILARITIES[song_b_id][song_a_id] = similarity

  def __calculate_similarity(self, song_a_id, song_b_id):
    song_a = self.SONG_DATA[song_a_id]
    song_b = self.SONG_DATA[song_b_id]
    score = self._compute_song_to_song_similarity(song_a, song_b)
    return score

  def parse_list(self, entity):
    return list(map(lambda a: a.strip(), entity.split('|')))

  def get_similarity_for_feature(self, song_a, song_b, feature):
    if pandas.isnull(song_a[feature]) or pandas.isnull(song_b[feature]):
      return 0.0
    if type(song_a[feature]) is float:
      return 1.0 if song_a[feature] == song_b[feature] else 0.0
    song_a_list = self.parse_list(song_a[feature])
    song_b_list = self.parse_list(song_b[feature])
    intersection = list(set(song_a_list) & set(song_b_list))
    return float(len(intersection)) / (len(song_a_list) + len(song_b_list))

  def _compute_song_to_song_similarity(self, song_a, song_b):
    total_similarity = 0.0
    feature_names = ['genre_ids', 'artist_name', 'composer', 'lyricist',
                     'language']
    for feature in feature_names:
      feature_similarity = self.get_similarity_for_feature(song_a, song_b,
                                                           feature)
      total_similarity += feature_similarity
    return total_similarity / len(feature_names)


class SongsFeatureSimilarityStats:
  MIN_SIMILARITY = 0.1
  SONG_TO_SONG_SIMILARITY = {}

  data_reader = DataReader()
  ifs = SongFeatureSimilarity()

  def compute_pairwise_similarities(self):
    count = 0
    start_timer = datetime.now()
    for index, entry_a in entries.iterrows():
      count += 1
      if count % 1000 == 0:
        print("Features " + str(count))
        print(datetime.now() - start_timer)
        start_timer = datetime.now()
      to_others_similarity = {}
      for index, entry_b in entries.iterrows():
        if entry_a['song_id'] is not entry_b['song_id']:
          similarity = self.ifs.compute_song_to_song_similarity(entry_a,
                                                                entry_b)
          if similarity > self.MIN_SIMILARITY:
            to_others_similarity[entry_b['song_id']] = similarity
      self.SONG_TO_SONG_SIMILARITY[entry_a['song_id']] = to_others_similarity
