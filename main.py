import sys, logging
from networksecurity.components.data_ingestion import DataIngestion
from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.logging import logger
from networksecurity.entity.config_entity import TrainingPipelineConfig, DataIngestionConfig, DataValidationConfig
from networksecurity.components.data_validation import DataValidation

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
    except Exception as e:
        raise NetworkSecurityException(e, sys)