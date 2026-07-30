from networksecurity.constant.training_pipeline import SAVED_MODEL_DIR, MODEL_FILE_NAME
import os, sys
from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.logging import logger

class NetworkModel:
    def __init__(self, preprocessor, model):
        try:
            self.prerocessor = preprocessor
            self.model = model
        except Exception as e:
            raise NetworkSecurityException(e, sys)
        
    def predict(self, x):
        try:
            x_transformed = self.prerocessor.transform(x)
            y_hat = self.model.predict(x_transformed)
            return y_hat
        except Exception as e:
            raise NetworkSecurityException(e, sys)