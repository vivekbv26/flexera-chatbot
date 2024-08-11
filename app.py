from flask import Flask, request, jsonify, render_template
import json
from transformers import RobertaTokenizer, RobertaForSequenceClassification, pipeline
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
knowledge_base = load_knowledge_base('C:/Users/Vivek/chatbot/flexera-chatbot/kn.json')
vectorizer, clf = train_intent_classifier(knowledge_base)

# Load pre-trained RoBERTa model for abusive word detection
model_name = "cardiffnlp/twitter-roberta-base-offensive"
tokenizer = RobertaTokenizer.from_pretrained(model_name)
model = RobertaForSequenceClassification.from_pretrained(model_name)
abusive_classifier = pipeline('sentiment-analysis', model=model, tokenizer=tokenizer)

# Function to check for abusive language
def is_abusive(text):
    result = abusive_classifier(text)[0]
    label = result['label']
    # Adjust label comparison based on model's output
    return label == 'LABEL_1'

# Home route to serve the frontend
@app.route('/')
def home():
    return render_template('index.html')

# API route for chatbot response
@app.route('/get-response', methods=['POST'])
def get_response():
    user_input = request.json.get('message')
    
    # Check if the input contains abusive content
    if is_abusive(user_input):
        return jsonify({'response': "Your message contains inappropriate content and cannot be processed."})
    
    # Intent classification
    X_user = vectorizer.transform([user_input])
    predicted_answer = clf.predict(X_user)[0]
    return jsonify({'response': predicted_answer})

# Run the Flask app
if __name__ == '__main__':
    app.run(debug=True)
