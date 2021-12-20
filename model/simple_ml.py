import numpy as np
from db import db
from sklearn.preprocessing import LabelEncoder
from sklearn.pipeline import Pipeline
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.model_selection import train_test_split
import pickle
from config import config


class DocumentClassification:
    def __init__(self, 
                 vectorizer = None, 
                 ml_model = None,
                 label_encoder = None, 
                 test_size = 0.2,
                 path = config.model_path):
        

        self.vectorizer = vectorizer if vectorizer else TfidfVectorizer(ngram_range = (1,4))
        self.ml_model = ml_model if ml_model else MultinomialNB()
        self.label_encoder = label_encoder if label_encoder else LabelEncoder()
        self.test_size = test_size
        self.path = path
        
    def train_test_split(self, data):
        return train_test_split(data['article_content'], 
                                data['topic'], 
                                test_size = self.test_size,
                                stratify = data['topic'], 
                                random_state=42)
        
    def encode_label(self, y, training = True):
        if training:
            return self.label_encoder.fit_transform(y)
        return self.label_encoder.transform(y)
       
    def create_pipeline(self):
        self.pipeline = Pipeline(steps = [('vectorize', self.vectorizer), 
                             ("model", self.ml_model)]
                    )
        
    def fit(self, data):
        print("=====Start Fitting data.=====")
        self.create_pipeline()
        X_train, X_test, y_train, y_test = self.train_test_split(data)
        self.pipeline.fit(X_train, self.encode_label(y_train))
        print("=====Fitting data. done.=====")
        train_score = self.pipeline.score(X_train, self.encode_label(y_train, training = False))
        test_score = self.pipeline.score(X_test, self.encode_label(y_test, training = False))
        print("Training score: {}".format(train_score))
        print("Testing score: {}".format(test_score))
        return self
        
    def dump_model(self):
        pickle.dump(self.label_encoder, open(f'{self.path}/encoder.pkl','wb'))
        pickle.dump(self.pipeline, open(f'{self.path}/pipeline.pkl','wb'))
        
    @classmethod
    def from_disk(cls, path = config.model_path):
        pipeline = pickle.load(open(f'{path}/pipeline.pkl','rb'))
        label_encoder = pickle.load(open(f'{path}/encoder.pkl','rb'))
        obj = cls(label_encoder = label_encoder)
        obj.pipeline = pipeline
        return obj
    
    def predict(self, X):
        idx = self.pipeline.predict(X)
        return self.label_encoder.inverse_transform(idx)