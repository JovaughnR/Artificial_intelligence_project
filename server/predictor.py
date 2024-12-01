import numpy as np
import torch
from transformers import BertTokenizer, BertModel
from Network import NeuralNetwork
import json
import random

# ------------------ Load Models and Vocabularies ------------------
def load_model_and_vocab(model_path, vocab_path):
    model = NeuralNetwork.load(model_path)
    vocab = np.load(vocab_path)
    return model, vocab

# Load classifier and vocab
classifier, classifier_vocab = load_model_and_vocab(
    "./files/classifier_model.pkl", "./files/classifier_embeddings.npy"
)

# Load student action model and vocab
student_action_model, student_action_vocab = load_model_and_vocab(
    "./files/student_action_model.pkl", "./files/student_action_embeddings.npy"
)

# Load student query model and vocab
student_query_model, student_query_vocab = load_model_and_vocab(
    "./files/student_query_model.pkl", "./files/student_query_embeddings.npy"
)

# Load staff action model and vocab
staff_action_model, staff_action_vocab = load_model_and_vocab(
    "./files/staff_action_model.pkl", "./files/staff_action_embeddings.npy"
)

# Load staff query model and vocab
staff_query_model, staff_query_vocab = load_model_and_vocab(
    "./files/staff_query_model.pkl", "./files/staff_query_embeddings.npy"
)
# ------------------------------------------------------------------

# ------------------ Load Data Files ------------------
def load_json(filepath):
    with open(filepath, 'r') as f:
        data = json.load(f)
    return data

classes = load_json('./files/classifier.json')
student_actions = load_json('./files/student_action.json')
student_queries = load_json('./files/student_query.json')
staff_actions = load_json('./files/staff_action.json')
staff_queries = load_json('./files/staff_query.json')
# -----------------------------------------------------

# ------------------ Load Pre-trained BERT Model ------------------
tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')
bert_model = BertModel.from_pretrained('bert-base-uncased')

def get_bert_embedding(sentence):
    inputs = tokenizer(sentence, return_tensors="pt", padding=True, truncation=True, max_length=512)
    with torch.no_grad():
        outputs = bert_model(**inputs)
    return outputs.last_hidden_state.mean(dim=1).squeeze().numpy()
# -----------------------------------------------------------------

# ------------------ Prediction Functions ------------------
def predict_class(user_input, vocab, model, intents):
    embedding = get_bert_embedding(user_input)
    normalized_embedding = (embedding - np.mean(vocab)) / np.std(vocab)
    outcomes = model.predict(normalized_embedding)
    intent = intents["intents"][np.argmax(outcomes)]
    return intent["tag"], intent["responses"]

def binary_classifier(user_input):
    return predict_class(
        user_input, classifier_vocab, classifier, classes
    )[0]


def predict(user_input, type):
    tag = binary_classifier(user_input)
    if type == "staff":
        if tag == "actions":
            return tag, predict_action_or_query(
                user_input, staff_query_vocab,
                staff_query_model, staff_queries
            )
        elif tag == "queries":
            return tag, random.choice(predict_action_or_query(
                user_input, staff_query_vocab, 
                staff_query_model, staff_queries
            ))
    elif type == "student":
        if tag == "actions":
            return tag, predict_action_or_query(
                user_input, student_action_vocab, 
                student_action_model,student_actions 
            )
        elif tag == "queries":
            return tag, random.choice(predict_action_or_query(
                user_input, student_query_vocab, 
                student_query_model, student_queries
            ))

def predict_action_or_query(user_input, vocab, model, intents):
    _, response = predict_class(user_input, vocab, model, intents)
    return response


# -------------------------------------------------------
