from sklearn.metrics import roc_auc_score
from app.DataReader import DataReader, DataSource


class TargetPredictor:
  REOCCURRENCE_SIMILARITY_WEIGHT = 0.4
  THRESHOLD = 0.5
  data_reader = DataReader()

  def __init__(self, user_reoccurrences, song_to_song_reoccurrence_similarity,
      song_feature_similarity):
    self.user_reoccurrences = user_reoccurrences
    self.song_to_song_reoccurrence_similarity = song_to_song_reoccurrence_similarity
    self.song_feature_similarity = song_feature_similarity

  def calculate_reoccurrence_score_for_user(self, user_reoccurrence,
      song_similarity):
    score_upper_sum = 0.0
    score_lower_sum = 0.0
    user_song_reoccurrence = user_reoccurrence.song_reoccurrences
    for song_id in user_song_reoccurrence:
      if song_id in song_similarity.keys():
        score_upper_sum += song_similarity[song_id] * user_song_reoccurrence[
          song_id]
        score_lower_sum += song_similarity[song_id]
    reoccurrence_score = score_upper_sum / score_lower_sum
    return reoccurrence_score

  def calculate_feature_score_for_user(self, user_reoccurrence, song_id_target):
    score_upper_sum = 0.0
    score_lower_sum = 0.0
    user_song_reoccurrence = user_reoccurrence.song_reoccurrences
    for song_id in user_song_reoccurrence.keys():
      song_similarity = self.song_feature_similarity.compute_song_to_song_similarity(
          song_id, song_id_target)
      score_upper_sum += song_similarity * user_song_reoccurrence[song_id]
      score_lower_sum += song_similarity
    reoccurrence_score = score_upper_sum / score_lower_sum
    return reoccurrence_score

  def predict_for_user_song_pair(self, user_id, song_id):
    user_reoccurrence = self.user_reoccurrences[user_id]
    reoccurrence_score = 0.5
    if song_id in self.song_to_song_reoccurrence_similarity.keys():
      song_reoccurrence_sim = self.song_to_song_reoccurrence_similarity[song_id]
      reoccurrence_score = self.calculate_reoccurrence_score_for_user(
          user_reoccurrence,
          song_reoccurrence_sim)
    feature_score = self.calculate_feature_score_for_user(user_reoccurrence,
                                                          song_id)

    return reoccurrence_score, feature_score

  def compute_predicted_label(self, scores):
    final_score = scores[0]
    if len(scores) == 2:
      final_score *= self.REOCCURRENCE_SIMILARITY_WEIGHT
      final_score += ((1 - self.REOCCURRENCE_SIMILARITY_WEIGHT) * scores[1])
    return 1 if final_score > self.THRESHOLD else 0

  def calculate_auc_roc(self, expected, actual, label):
    result = roc_auc_score(expected, actual)
    print("Final AUC under ROC Curve for:  #" + label + "  " + str(result))

  def calculate_prediction_accuracies(self):
    test_data = self.data_reader.read_file(DataSource.TEST)

    expected_labels = test_data['target'].tolist()
    scores_from_reoccurrence = []
    scores_from_features = []
    combined_scores = []

    for index, row in test_data.iterrows():
      user_id = row['msno']
      song_id = row['song_id']
      reoccurrence_score, feature_score = self.predict_for_user_song_pair(
          user_id, song_id)
      label_from_reoccurrence = self.compute_predicted_label(
          [reoccurrence_score])
      scores_from_reoccurrence.append(label_from_reoccurrence)
      label_from_features = self.compute_predicted_label([feature_score])
      scores_from_features.append(label_from_features)
      combined_label = self.compute_predicted_label(
          [reoccurrence_score, feature_score])
      combined_scores.append(combined_label)

    self.calculate_auc_roc(expected_labels, scores_from_reoccurrence,
                           "Reoccurrence")
    self.calculate_auc_roc(expected_labels, scores_from_features, "Features")
    self.calculate_auc_roc(expected_labels, combined_scores, "Combined")
