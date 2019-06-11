import pandas as pd
from enum import Enum


class DataSource(Enum):
  # SONGS = 'songs',
  # TRAIN = 'train',
  # TEST = 'test',
  # SONGS = 'dev/songs_dev',
  # TRAIN = 'dev/train_dev',
  # TEST = 'dev/test_dev',
  SONGS = 'dev/final/songs_dev',
  TRAIN = 'dev/final/train_dev',
  TEST = 'dev/final/test_dev',
  NONE = 'none'


class DataReader:
  def read_file(self, dataSource):
    data = pd.read_csv('../resources/' + dataSource.value[0] + '.csv', sep=',')
    return data
