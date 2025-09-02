from fastapi import FastAPI
from pydantic import BaseModel
from nltk.tokenize import word_tokenize

app = FastAPI()

# with open('./model_knn1.pkl', 'rb') as f:
#     model = pickle.load(f)

# with open('./vectorizer.pkl', 'rb') as f:
#     vectorizer = pickle.load(f)



def predict_cluster(text):
    return text


class Item(BaseModel):
    text: str

@app.post("/predict")
def post_pred_text(item: Item):
    return {'cluster': predict_cluster(item.text)}