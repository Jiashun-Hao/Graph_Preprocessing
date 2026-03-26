import json
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, f1_score, precision_score, recall_score
from sklearn.svm import SVC  
def Model(File_Jsonl,File_Title):
    def load_data(file_path):
        X, y = [], []
        with open(file_path, 'r') as file:
            for line in file:
                data = json.loads(line.strip())
                X.append(data['func'])
                y.append(data['target'])
        return np.array(X), np.array(y)

    def split_data(X, y, test_size=0.2):
        return train_test_split(X, y, test_size=test_size, random_state=42)

    # Train
    def train_model(model, X_train, y_train):
        model.fit(X_train, y_train)

    # Evaluate
    def evaluate_model(model, X_test, y_test):
        y_pred = model.predict(X_test)
        acc = accuracy_score(y_test, y_pred)
        f1 = f1_score(y_test, y_pred)
        precision = precision_score(y_test, y_pred)
        recall = recall_score(y_test, y_pred)
        print('SVM:'+File_Jsonl+''f'Accuracy: {acc:.4f}, F1 Score: {f1:.4f}, Precision: {precision:.4f}, Recall: {recall:.4f}')


    X, y = load_data(File_Jsonl)
    X_train, X_test, y_train, y_test = split_data(X, y)

    model = SVC()  
    train_model(model, X_train, y_train)

    evaluate_model(model, X_test, y_test)

Model('AST_Emberding_code.jsonl','AST')
Model('CFG_Emberding_code.jsonl','CFG')
Model('CPG_Emberding_code.jsonl','CPG')
Model('PDG_Emberding_code.jsonl','PDG')
