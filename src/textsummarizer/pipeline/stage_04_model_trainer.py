from textsummarizer.config.configuration import ConfigurationManager
from textsummarizer.components.mode_trainer import ModelTrainer
from textsummarizer.logging import logger

class ModelTrainerTrainingPipeline:
    def __init__(self):
        pass

    def main(self):
          config = ConfigurationManager()
          model_trainer_config= config.get_data_transformation_config()
          model_trainer_config =ModelTrainer(config=model_trainer_config)
          model_trainer_config.convert()