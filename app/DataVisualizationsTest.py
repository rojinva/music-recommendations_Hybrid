import unittest

from app.DataStats import DataStats


class MyTestCase(unittest.TestCase):
  def test_users_plot(self):
    data = []
    DataStats.plot_data(data)



if __name__ == '__main__':
  unittest.main()
