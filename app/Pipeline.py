from datetime import datetime

from app.ModelTrainer import ModelTrainer


class Pipeline:
  model_trainer = ModelTrainer()

  def execute(self):
    target_predictor = self.model_trainer.train()
    print("Start predicting values:")
    print(datetime.now())
    target_predictor.calculate_prediction_accuracies()


def main():
  print("######## ####### ABSOLUTE START TIME ##########")
  print(datetime.now())
  pipeline = Pipeline()
  pipeline.execute()
  print("######## ####### ABSOLUTE END TIME ##########")
  print(datetime.now())


if __name__ == "__main__": main()
