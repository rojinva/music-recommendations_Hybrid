from datetime import datetime

from app.DataReader import DataReader, DataSource
import pandas as pd
from sklearn.model_selection import train_test_split

PATH_TO_DEV_DATA = "../resources/dev/"


class DatasetSubsampling:
  REQUIRED_USERS_COUNT = 5
  SONGS_CUTOFF_RATIO = 0.1
  TEST_TRAIN_SPLIT_RATIO = 0.3
  data_reader = DataReader()

  def generate_data_stats(self, dataset, dataset_name):
    print("=========================================")
    print("Dataset " + dataset_name)
    print("Mean users per song " + str(
        dataset.groupby('song_id')['msno'].nunique().mean()))
    print("Mean songs per user " + str(
        dataset.groupby('msno')['song_id'].nunique().mean()))

    print("Total number of songs " + str(dataset['song_id'].nunique()))
    print("Total number of users " + str(dataset['msno'].nunique()))

  def measure_time(self, descr):
    print("==== Start: " + descr + "====")
    print(datetime.now())

  def read_train_data(self):
    train_data = self.data_reader.read_file(DataSource.TRAIN)
    return train_data.drop(
        columns=['source_system_tab', 'source_screen_name', 'source_type'])

  def extract_most_active_users_subset(self, train_data):
    most_active_users_df = \
      train_data.groupby('msno')['song_id'].count().reset_index(
          name='count').sort_values(['count'], ascending=False).head(
          self.REQUIRED_USERS_COUNT)[['msno']]
    most_active_users_set = set(list(most_active_users_df['msno'].tolist()))
    most_active_users_train_subset = train_data[
      train_data['msno'].isin(most_active_users_set)]
    return most_active_users_train_subset

  def extract_most_popular_songs_in_dataset(self, dataset):
    required_songs_count = int(dataset[
                                 'song_id'].nunique() * self.SONGS_CUTOFF_RATIO)

    most_popular_songs_in_subset_df = \
      dataset.groupby('song_id')[
        'msno'].count().reset_index(
          name='count').sort_values(['count'], ascending=False).head(
          required_songs_count)[['song_id']]
    most_popular_songs_in_subset = set(
        most_popular_songs_in_subset_df['song_id'].tolist())
    return most_popular_songs_in_subset

  def extract_required_songs_details(self, song_ids):
    songs_df = self.data_reader.read_file(DataSource.SONGS)
    target_songs_df = songs_df[
      songs_df['song_id'].isin(song_ids)]
    return target_songs_df

  def extract_target_subset(self, most_active_users_train_subset,
      most_popular_songs_in_subset):
    target_subset = most_active_users_train_subset[
      most_active_users_train_subset['song_id'].isin(
          most_popular_songs_in_subset)]
    return target_subset

  def split_dataframe(self, target_dataset):
    grouped = target_dataset.groupby('msno')
    train = pd.DataFrame(columns=target_dataset.keys())
    test = pd.DataFrame(columns=target_dataset.keys())

    for name, group in grouped:
      train_group, test_group = train_test_split(group,
                                                 test_size=self.TEST_TRAIN_SPLIT_RATIO)
      train = train.append(train_group)
      test = test.append(test_group)

    songs_in_train = set(train['song_id'].unique())
    songs_in_test = set(test['song_id'].unique())
    percentage_songs_not_in_train = len(songs_in_test - songs_in_train) / len(
        songs_in_test)
    print("Percentage songs in test that are not in train " + str(
        percentage_songs_not_in_train))
    return train, test

  def subsample_dataset(self, train_data):
    self.measure_time("most_active_users_train_subset")
    most_active_users_train_subset = self.extract_most_active_users_subset(
        train_data)
    self.generate_data_stats(most_active_users_train_subset,
                             "Most active users subset")
    self.measure_time("most_popular_songs")
    most_popular_songs = self.extract_most_popular_songs_in_dataset(
        most_active_users_train_subset)
    self.measure_time("required_songs_with_features")
    required_songs_with_features = self.extract_required_songs_details(
        most_popular_songs)
    self.measure_time("target_subset")
    target_subset = self.extract_target_subset(most_active_users_train_subset,
                                               most_popular_songs)
    self.generate_data_stats(target_subset, "Target subset")
    self.measure_time("train_test_split")
    train, test = self.split_dataframe(target_subset)
    self.generate_data_stats(train,
                             "Train dataset")
    self.generate_data_stats(test,
                             "Test dataset")
    self.measure_time("Print to file")
    train.to_csv(PATH_TO_DEV_DATA + "train_dev.csv", index=False)
    test.to_csv(PATH_TO_DEV_DATA + "test_dev.csv", index=False)
    required_songs_with_features.to_csv(PATH_TO_DEV_DATA + "songs_dev.csv",
                                        index=False)

  def execute(self):
    train_data = self.read_train_data()
    self.generate_data_stats(train_data, "Complete dataset")
    self.subsample_dataset(train_data)


def main():
  print("######## ####### ABSOLUTE START TIME ##########")
  print(datetime.now())
  ds = DatasetSubsampling()
  ds.execute()
  print("######## ####### ABSOLUTE END TIME ##########")
  print(datetime.now())


if __name__ == "__main__": main()
