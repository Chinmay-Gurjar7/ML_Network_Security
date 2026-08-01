from platform import processor
import sys, os
import logging
import numpy as np
import pandas as pd
from sklearn.impute import KNNImputer
from sklearn.pipeline import Pipeline

from networksecurity.constant.training_pipeline import TARGET_COLUMN
from networksecurity.constant.training_pipeline import DATA_TRANSFORMED_IMPUTER_PARAMS
from networksecurity.entity.artifact_entity import DataTransformationArtifact, DataValidationArtifact
from networksecurity.logging import logger
from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.utils.main_utils.utils import save_object, save_numpy_array_data
from networksecurity.entity.config_entity import DataTransformationConfig

class DataTransformation:
    def __init__(
        self,
        data_transformation_config: DataTransformationConfig,
        data_validation_artifact: DataValidationArtifact
    ):
        try:
            self.data_transformation_config = data_transformation_config
            self.data_validation_artifact = data_validation_artifact
        except Exception as e:
            raise NetworkSecurityException(e, sys) from e
        
    @staticmethod
    def read_data(file_path) -> pd.DataFrame:
        try:
            return pd.read_csv(file_path)
        except Exception as e:
            raise NetworkSecurityException(e, sys)
        
    def get_data_transformer_object(self):
        logging.info('Entered get_data_transformer_object method of Data_Transformation class')
        try:
            imputer = KNNImputer(
                **DATA_TRANSFORMED_IMPUTER_PARAMS
            )
            logging.info('Exited get_data_transformer_object method of Data_Transformation class')
            processor:Pipeline = Pipeline([('imputer', imputer)])
            return processor
            
        except Exception as e:  
            raise NetworkSecurityException(e, sys) from e
        
    def initiate_data_transformation(self)->DataTransformationArtifact:
        try:
            logging.info("Starting data transformation process")
            train_df = DataTransformation.read_data(self.data_validation_artifact.valid_train_file_path)
            test_df = DataTransformation.read_data(self.data_validation_artifact.valid_test_file_path)
           
            # training dataframe
            input_feature_train_df = train_df.drop(columns=[TARGET_COLUMN])
            target_feature_train_df = train_df[TARGET_COLUMN]
            target_feature_train_df = target_feature_train_df.replace(-1, 0)
            
            # testing dataframe
            input_feature_test_df = test_df.drop(columns=[TARGET_COLUMN])
            target_feature_test_df = test_df[TARGET_COLUMN]
            target_feature_test_df = target_feature_test_df.replace(-1, 0)
            
            preprocessor = self.get_data_transformer_object()
            
            preprocessor_object = preprocessor.fit(input_feature_train_df)
            transform_input_feature_train_arr = preprocessor_object.transform(input_feature_train_df)
            transform_input_feature_test_arr = preprocessor_object.transform(input_feature_test_df)
            
            train_arr = np.c_[transform_input_feature_train_arr, np.array(target_feature_train_df)]
            test_arr = np.c_[transform_input_feature_test_arr, np.array(target_feature_test_df)]
            
            # Save numpy array data
            save_numpy_array_data(
                file_path=self.data_transformation_config.transformed_train_file_path,
                array=train_arr
            )

            save_numpy_array_data(
                file_path=self.data_transformation_config.transformed_test_file_path,
                array=test_arr
            )

            save_object(
                file_path=self.data_transformation_config.transformed_object_file_path,
                obj=preprocessor_object
            )
            
            save_object("final_model/preprocessor.pkl", preprocessor_object)
            
            # Preparing artifact
            data_transformation_artifact = DataTransformationArtifact(
            transformed_train_file_path=self.data_transformation_config.transformed_train_file_path,
            transformed_test_file_path=self.data_transformation_config.transformed_test_file_path,
            transformed_object_file_path=self.data_transformation_config.transformed_object_file_path
            )
            return data_transformation_artifact
            
        except Exception as e:
            raise NetworkSecurityException(e, sys)