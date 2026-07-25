from networksecurity.entity.artifact_entity import DataIngestionArtifact
from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.logging import logger

## Configuration for data ingestion config
from networksecurity.entity.config_entity import DataIngestionConfig

import os, sys
import pymongo
import logging
import pandas as pd
import numpy as np
from typing import List
from sklearn.model_selection import train_test_split

# 1. Read from MongoDB and save it to feature store

from dotenv import load_dotenv
load_dotenv()

MONGO_DB_URL = os.getenv("MONGO_DB_URL")

class DataIngestion:
    def __init__(self, data_ingestion_config: DataIngestionConfig):
        try:
            self.data_ingestion_config = data_ingestion_config
        
        except Exception as e:  
            raise NetworkSecurityException(e, sys) 
        
    def export_collection_as_dataframe(self):
        try:
            database_name = self.data_ingestion_config.data_ingestion_database_name
            collection_name = self.data_ingestion_config.data_ingestion_collection_name

            # Connect to MongoDB
            self.mongo_client = pymongo.MongoClient(MONGO_DB_URL)
            collection = self.mongo_client[database_name][collection_name] 

            # Export collection as DataFrame
            dataframe = pd.DataFrame(list(collection.find()))
            if "_id" in dataframe.columns:
                dataframe = dataframe.drop("_id", axis=1)

            dataframe.replace({"na":np.nan}, inplace=True)  # Replace "na" with NaN
            return dataframe

        except Exception as e:
            raise NetworkSecurityException(e, sys)

    def export_data_to_feature_store(self, dataframe: pd.DataFrame):
        try:
            feature_store_dir = self.data_ingestion_config.feature_store_dir
            os.makedirs(feature_store_dir, exist_ok=True)
            feature_store_file_path = os.path.join(feature_store_dir, "feature_store.csv")
            dataframe.to_csv(feature_store_file_path, index=False)
            logging.info(f"Feature store file saved at: {feature_store_file_path}")
            return dataframe
        
        except Exception as e:
            raise NetworkSecurityException(e, sys)
        
    def split_data_as_train_test(self, dataframe: pd.DataFrame):
            try:
                train_set, test_set = train_test_split(
                    dataframe, test_size=self.data_ingestion_config.train_test_split_ratio, random_state=42)
                logging.info("Perform train test split on the data frame")
                logging.info("Exited from split_data_as_train_test method of Data Ingestion class")
                
                dir_path = os.path.dirname(self.data_ingestion_config.train_file_path)
                os.makedirs(dir_path, exist_ok=True)
                logging.info(f"Exporting training dataset to file: [{self.data_ingestion_config.train_file_path}]")
                
                train_set.to_csv(
                    self.data_ingestion_config.train_file_path, index=False, header= True)
                logging.info(f"Exporting test dataset to file: [{self.data_ingestion_config.test_file_path}]")
                
                test_set.to_csv(
                    self.data_ingestion_config.test_file_path, index=False, header= True)
                logging.info(f"Exported train and test file path")
                
            except Exception as e:
                raise NetworkSecurityException(e, sys) 
        
    def initiate_data_ingestion(self):
            try:
                dataframe = self.export_collection_as_dataframe()
                dataframe = self.export_data_to_feature_store(dataframe)
                self.split_data_as_train_test(dataframe)
                dataingestionartifact = DataIngestionArtifact(
                    train_file_path=self.data_ingestion_config.train_file_path,
                    test_file_path=self.data_ingestion_config.test_file_path
                )
                
                return dataingestionartifact

            except Exception as e:
                raise NetworkSecurityException(e, sys)
            
    