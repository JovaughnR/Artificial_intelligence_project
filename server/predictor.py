import numpy as np
import torch
from transformers import BertTokenizer, BertModel
from Network import NeuralNetwork
import json
import random


# Load knowledge base model
# model_1 = NeuralNetwork.load("prolog_knowledge_model.pkl")

# ------------- Load all models their paramters -----------
# Load classifier model parameters
classifier = NeuralNetwork.load("files/action_queries_model.pkl")
# Load the classfier model embedded arguments
classifier_args = np.load('./files/classifier_embeddings.npy')

# Load action model parameters
student_action_model = NeuralNetwork.load('./files/student_action_model.pkl')
# Load action model embedded arguments
student_action_args = np.load('./files/action_args_embeddings.npy')

# Load student querries model parameters
student_query_model = NeuralNetwork.load("./files/student_query_model.pkl")
# Load student queries model embedded arguments
student_query_args = np.load('./files/student_query_embeddings.npy')

# --------------------------------------------------------

def load(filepath):
    all_patterns = []

    with open(filepath, 'r') as f:
        data = json.load(f)
        for intent in data['intents']:
            for pattern in intent["patterns"]:
                all_patterns.append(pattern)

    return data, all_patterns

# ------------------ Load all data files -----------------
# Load the `classifier.json` file
classes, patterns = load('./files/classifier.json')

# Load the `actions`.json file
student_actions, patterns = load('./files/actions.json')

# Load the `student_queries.json` file
student_queries, patterns = load('./files/student_data.json')
# -------------------------------------------------------


# Load pre-trained BERT model and tokenizer
tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')
model = BertModel.from_pretrained('bert-base-uncased')

# Function to get BERT embedding for a sentence
def get_bert_embedding(sentence):
    inputs = tokenizer(
        sentence, return_tensors="pt", 
        padding=True, truncation=True, 
        max_length=512
    )
    with torch.no_grad():
        outputs = model(**inputs)
    return outputs.last_hidden_state.mean(dim=1).squeeze().numpy()


def predict_class(user_input, args, model, object):
    X = args
    embedding = get_bert_embedding(user_input)
    normalized_embedding = (embedding-np.mean(X))/np.std(X)
    outcomes = model.predict(normalized_embedding)
    intent = object["intents"][np.argmax(outcomes)]
    return intent["tag"], intent["responses"]


def binary_classfier(user_input):
    return predict_class(
        user_input, classifier_args, classifier, classes
    )[0]



def predict(user_input):
    print("Predicting")
    tag = binary_classfier(user_input)
    if tag == "actions":
        tag, response = predict_class(
            user_input, student_action_args, 
            student_action_model, student_actions
        )
        return "actions", response
    
    elif tag == "queries":
        tag, response = predict_class(
            user_input, student_query_args,
            student_query_model, student_queries
        )
        rand = random.randint(0, len(response)-1)
        return "queries", response[rand]


# print(binary_classifier_params)



# data_object_1, patterns = load('./files/student_data.json')
# pattern_embeddings_1 = np.array(
#         [get_bert_embedding(pattern) for pattern in patterns]
#     )

# np.save("./files/student_query_embeddings.npy", pattern_embeddings_1)

# print(pattern_embeddings_1.shape)

# data_object_2, patterns = read_file('./files/actions.json')
# pattern_embeddings_2 = np.array(
#     [get_bert_embedding(pattern) for pattern in patterns]
# )

# np.save("files/actions_embeddings.npy", pattern_embeddings_2)
# classes = []
# # Combine all patterns
# all_patterns = []




# Read data from JSON and create labels
# with open('data.json', 'r') as f:
#     data = json.load(f)

#     for intent in data['intents']:
#         classes.append(intent["tag"])
#         for pattern in intent["patterns"]:
#             all_patterns.append(pattern)





# def predict_class(user_input, object, model: NeuralNetwork):
#     X = pattern_embeddings
#     embedding = get_bert_embedding(user_input)
#     normalized_embedding = (embedding - np.mean(X)) / np.std(X)
#     probabilities = model.predict(normalized_embedding)
#     return object["intents"][np.argmax(probabilities)]["tag"]




