from model.simple_ml import DocumentClassification
from db import db
import os
from config import config
import logging
logging.basicConfig(level = logging.INFO)
logger = logging.getLogger()

def train():
    if not os.path.exists(config.model_path):
        os.makedirs(config.model_path)
    logger.info("Training ml document classification model")
    data = db.read()
    classifier = DocumentClassification()
    classifier.fit(data)
    classifier.dump_model()
    logger.info("Training finished.")
    
if __name__ == "__main__":
    train()