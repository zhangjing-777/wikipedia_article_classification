from fastapi import APIRouter
from model.simple_ml import MlPredictor
from pydantic import BaseModel
from typing import List

model = MlPredictor()

router = APIRouter(
    prefix="/text",
    tags=['text'],
    responses={404: {'description': "Not found"}}
)


class TextClassificationRequest(BaseModel):
    texts: List[str]


class TextClassificationResponse(BaseModel):
    results: List[str]


@router.post("/nb", response_model=TextClassificationResponse)
async def predict(req: TextClassificationRequest):
    results = model.predict_sentence(req.texts)
    return TextClassificationResponse(results=list(results))
