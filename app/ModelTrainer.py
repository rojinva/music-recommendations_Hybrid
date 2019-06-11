from app.DataReader import DataReader, DataSource
from app.DataStats import DataStats
from app.SongFeatureSimilarity import SongFeatureSimilarity
from app.SongReoccurenceSimilarity import SongPairsSimilarity
from app.SongReoccurrenceStats import SongReoccurrenceStats
from app.TargetPredictor import TargetPredictor
from app.UserReoccurrenceStats import UserReoccurrenceStats


class ModelTrainer:
  data_reader = DataReader()
  user_reoccurrences_stats = UserReoccurrenceStats()
  song_reoccurrences_stats = SongReoccurrenceStats()
  data_visualizations = DataStats()
  song_pairs_similarity = SongPairsSimilarity()
  song_feature_similarity = SongFeatureSimilarity()

  def read_data(self):
    train_data = self.data_reader.read_file(DataSource.TRAIN)
    print('Read data')
    return train_data

  def compute_user_and_song_reoccurrences(self, train_data):
    for index, row in train_data.iterrows():
      user_id = row['msno']
      song_id = row['song_id']
      target = row['target']
      self.user_reoccurrences_stats.add_reoccurrence_for_user(user_id, song_id,
                                                              target)
      self.song_reoccurrences_stats.put_reoccurrence_for_song(song_id, user_id,
                                                              target)
      if index % 10000 == 0:
        print("Compute reoccurrence stats " + str(index))
    print('Computed reoccurrences')
    self.user_reoccurrences_stats.calculate_averages()
    print('Calculated user averages')
    return self.user_reoccurrences_stats.USER_REOCCURRENCES, \
           self.song_reoccurrences_stats.SONG_USER_REOCCURRENCES

  def compute_song_feature_similarity_stats(self):
    self.song_feature_similarity_stats.compute_pairwise_similarities()
    return self.song_feature_similarity_stats.SONG_TO_SONG_SIMILARITY

  def train(self):
    train_data = self.read_data()
    user_reoccurrences, song_user_reoccurrences = self.compute_user_and_song_reoccurrences(
        train_data)
    print("Start song to song reoccurrence similarity")
    song_to_song_reoccurrence_similarity = self.song_pairs_similarity.calculate_pairwise_similarity(
        song_user_reoccurrences)
    # print("Start song to song feature similarity")
    # song_to_song_feature_similarity = self.compute_song_feature_similarity_stats()
    target_predictor = TargetPredictor(user_reoccurrences,
                                       song_to_song_reoccurrence_similarity,
                                       self.song_feature_similarity)
    return target_predictor
