from flask import Flask, request, jsonify
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.svm import SVC
from sklearn.model_selection import train_test_split
from transformers import pipeline, AutoTokenizer, AutoModelForSequenceClassification
import torch
import pandas as pd

app = Flask(__name__)

df = pd.read_csv("just-test.csv", header=None,names=["text", "label"])
df.dropna(inplace=True)
df = df.reset_index(drop=True)

label_mapping = {label: idx for idx, label in enumerate(set(df['label']))}

train_texts, test_texts, train_labesl, text_labels = train_test_split(
    df['text'].tolist(), df['label'].tolist(),test_size=0.1, random_state=42
)

X_train = [text for text in train_texts if isinstance(text, str) and text.strip() != ""]


svm_model = SVC(kernel="linear", probability=True)
vectorizer = TfidfVectorizer()


X_train_tfidf = vectorizer.fit_transform(X_train)
svm_model.fit(X_train_tfidf, train_labesl)

@app.route('/process', methods=['POST'])
def process_news():
    data = request.json
    articles = data.get("articles", [])
    
    if not articles or not isinstance(articles, list):
        return jsonify({"error": "No valid articles provided"}), 400
    texts = [
        (article.get("title", "") or "") + " " +(article.get("description", "") or "") + " " + (article.get("content", "") or "") 
        for article in articles
    ]
    x_tfidf = vectorizer.transform(texts)

    svm_pred = svm_model.predict(x_tfidf)

    result = []
    for i, article in enumerate(articles):
        result.append({
            "title": article.get("title", ""),
            "description": article.get("description", ""),
            "content": article.get("content", ""),
            "svm_category": svm_pred[i],
            "url": article.get("url", ""),
        })

    return jsonify({"articles": result})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
