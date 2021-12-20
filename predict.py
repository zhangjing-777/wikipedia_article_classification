from model.simple_ml import DocumentClassification
from typing import List

clf = DocumentClassification.from_disk()

def predict_sentence(X:List[str]):
    return clf.predict(X)



if __name__ == "__main__":
    result = predict_sentence([
        "computer science is a technology.",
        "This music sounds good",
        "math is difficult to learn"]
        )
    print(result)