from flask import Flask, request, jsonify
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.svm import SVC
from sklearn.model_selection import train_test_split
from sklearn.decomposition import TruncatedSVD
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from sklearn.multiclass import OneVsOneClassifier
from matplotlib.colors import ListedColormap

app = Flask(__name__)

df = pd.read_csv("just-test.csv", header=None, names=["text", "label"])
df.dropna(inplace=True)
df = df.reset_index(drop=True)

label_mapping = {label: idx for idx, label in enumerate(set(df['label']))}
df['label'] = df['label'].map(label_mapping)

train_texts, test_texts, train_labels, test_labels = train_test_split(
    df['text'].tolist(), df['label'].tolist(), test_size=0.1, random_state=42
)

vectorizer = TfidfVectorizer()
X_train_tfidf = vectorizer.fit_transform(train_texts)


ovo_classifier = OneVsOneClassifier(SVC(kernel="linear", probability=True))
ovo_classifier.fit(X_train_tfidf, train_labels)

def plot_ovo_svm(X_train, y_train, classifier, labels):

    svd = TruncatedSVD(n_components=2, random_state=42)
    X_2d = svd.fit_transform(X_train.toarray())  

    if X_2d.shape[1] < 2:
        raise ValueError("The dimensionality after SVD is less than 2. Unable to plot decision boundaries.")

    plt.figure(figsize=(12, 8))
    cmap = ListedColormap(plt.cm.get_cmap("tab10").colors[:len(labels)])

    scatter = plt.scatter(
        X_2d[:, 0],
        X_2d[:, 1],
        c=y_train,
        cmap=cmap,
        s=50,
        edgecolors="k",
    )
    plt.colorbar(scatter, ticks=range(len(labels)))

    unique_classes = classifier.classes_

    class_pairs = [(unique_classes[i], unique_classes[j]) for i in range(len(unique_classes)) for j in range(i + 1, len(unique_classes))]

    for i, estimator in enumerate(classifier.estimators_):
        w = estimator.coef_[0] 

        if hasattr(w, "getnnz"): 
            w = w.toarray().flatten() 
        if len(w) < 2:
            print(f"Warning: Estimator {i} has only {len(w)} coefficient(s). Skipping decision boundary plot.")
            continue

        b = estimator.intercept_[0]

        if w[1] == 0:
            print(f"Skipping decision boundary plot for estimator {i} (w[1] is zero).")
            continue

        slope = -w[0] / w[1]
        intercept = -b / w[1]

        if not np.isfinite(slope) or not np.isfinite(intercept):
            print(f"Skipping invalid decision boundary plot for estimator {i}.")
            continue

        x_vals = np.linspace(X_2d[:, 0].min(), X_2d[:, 0].max(), 100)
        decision_boundary = slope * x_vals + intercept

        class1, class2 = class_pairs[i]
        plt.plot(x_vals, decision_boundary, label=f"Class {class1} vs {class2}")

    plt.title("One-vs-One SVM Decision Boundaries")
    plt.xlabel("Feature 1")
    plt.ylabel("Feature 2")
    plt.legend()
    plt.grid(True)
    plt.show()


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

    svm_pred = ovo_classifier.predict(x_tfidf)
    reverse_label_mapping = {v: k for k, v in label_mapping.items()}
    result = []
    for i, article in enumerate(articles):
        result.append({
            "title": article.get("title", ""),
            "description": article.get("description", ""),
            "content": article.get("content", ""),
            "svm_category": reverse_label_mapping[int(svm_pred[i])],
            "url": article.get("url", ""),
        })
    return jsonify({"articles": result})

if __name__ == '__main__':
    sample_size = min(100, len(train_labels))
    plot_ovo_svm(X_train_tfidf[:sample_size], train_labels[:sample_size], ovo_classifier, label_mapping)
    app.run(host='0.0.0.0', port=5000)
