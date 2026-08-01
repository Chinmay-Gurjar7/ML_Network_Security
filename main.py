import sys, logging, os
from networksecurity.components.data_ingestion import DataIngestion
from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.logging import logger
from networksecurity.entity.config_entity import ModelTrainerConfig, TrainingPipelineConfig, DataIngestionConfig, DataValidationConfig, DataTransformationConfig
from networksecurity.components.data_transformation import DataTransformation
from networksecurity.components.data_validation import DataValidation
from networksecurity.components.model_trainer import ModelTrainer

if __name__ == "__main__":
    try:
        trainingpipelineconfig = TrainingPipelineConfig()
        dataingestionconfig = DataIngestionConfig(trainingpipelineconfig)
        dataingestion = DataIngestion(dataingestionconfig)
        logging.info("Starting data ingestion process...")
        dataingestionartifact = dataingestion.initiate_data_ingestion()
        print(dataingestionartifact)

        # Initialize data validation
        datavalidationconfig = DataValidationConfig(trainingpipelineconfig)
        datavalidation = DataValidation(dataingestionartifact, datavalidationconfig)
        logging.info("Starting data validation process...")
        datavalidationartifact = datavalidation.initiate_data_validation()
        print(datavalidationartifact)

        # Initialize data transformation
        datatransformationconfig = DataTransformationConfig(trainingpipelineconfig)
        datatransformation = DataTransformation(datavalidationartifact, datatransformationconfig)
        logging.info("Starting data transformation process...")
        datatransformationartifact = datatransformation.initiate_data_transformation()
        print(datatransformationartifact)
        
        # Initialize model trainer
        logging.info("Model Training sstared")
        model_trainer_config=ModelTrainerConfig(trainingpipelineconfig)
        model_trainer=ModelTrainer(model_trainer_config=model_trainer_config,data_transformation_artifact=datatransformationartifact)
        model_trainer_artifact=model_trainer.initiate_model_trainer()

        logging.info("Model Training artifact created")
        
    except Exception as e:
        raise NetworkSecurityException(e, sys)