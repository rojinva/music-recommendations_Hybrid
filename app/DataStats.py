import matplotlib.pyplot as plt


class DataStats:
  @staticmethod
  def plot_data(data):
    plt.boxplot(data, showmeans=True, whis=99)
    plt.show()

  def plot_users_listening_count(self, data):
    res =list( map(lambda entity: entity.total_count, data.values()))
    self.plot_data(res)