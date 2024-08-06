from flask import Flask, request, jsonify, render_template
import json
from difflib import get_close_matches
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB

app = Flask(__name__)

# Load the knowledge base
def load_knowledge_base(file_path: str):
    with open(file_path, 'r') as file:
        data = json.load(file)
    return data

# Train the intent classifier
def train_intent_classifier(knowledge_base):
    questions = [q["question"] for q in knowledge_base["questions"]]
    answers = [q["answer"] for q in knowledge_base["questions"]]
    vectorizer = CountVectorizer()
    X = vectorizer.fit_transform(questions)
    clf = MultinomialNB()
    clf.fit(X, answers)
    return vectorizer, clf

# Load and train
knowledge_base = load_knowledge_base('C:/Users/Vivek/flexera/kn.json')
vectorizer, clf = train_intent_classifier(knowledge_base)

# Home route to serve the frontend
@app.route('/')
def home():
    return render_template('index.html')

# API route for chatbot response
@app.route('/get-response', methods=['POST'])
def get_response():
    user_input = request.json.get('message')
    X_user = vectorizer.transform([user_input])
    predicted_answer = clf.predict(X_user)[0]
    return jsonify({'response': predicted_answer})

# Run the Flask app
if __name__ == '__main__':
    app.run(debug=True)
