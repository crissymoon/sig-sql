import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, mean_squared_error

# Linear Regression
def linear_regression_example():
    X = np.random.randn(100, 1)
    y = 2 * X.flatten() + 1 + np.random.randn(100) * 0.1
    model = LinearRegression()
    model.fit(X, y)
    return model

# Logistic Regression
def sigmoid(z):
    return 1 / (1 + np.exp(-z))

def logistic_regression(X, y, learning_rate=0.01, epochs=1000):
    m, n = X.shape
    weights = np.zeros(n)
    bias = 0
    
    for i in range(epochs):
        z = X.dot(weights) + bias
        predictions = sigmoid(z)
        
        cost = -(1/m) * np.sum(y * np.log(predictions) + (1-y) * np.log(1-predictions))
        
        dw = (1/m) * X.T.dot(predictions - y)
        db = (1/m) * np.sum(predictions - y)
        
        weights -= learning_rate * dw
        bias -= learning_rate * db
        
    return weights, bias

# K-Means Clustering
def kmeans(X, k, max_iters=100):
    centroids = X[np.random.choice(X.shape[0], k, replace=False)]
    
    for _ in range(max_iters):
        distances = np.sqrt(((X - centroids[:, np.newaxis])**2).sum(axis=2))
        labels = np.argmin(distances, axis=0)
        
        new_centroids = np.array([X[labels == i].mean(axis=0) for i in range(k)])
        
        if np.allclose(centroids, new_centroids):
            break
        centroids = new_centroids
    
    return centroids, labels

# Neural Network (Simple)
class NeuralNetwork:
    def __init__(self, input_size, hidden_size, output_size):
        self.W1 = np.random.randn(input_size, hidden_size) * 0.01
        self.b1 = np.zeros((1, hidden_size))
        self.W2 = np.random.randn(hidden_size, output_size) * 0.01
        self.b2 = np.zeros((1, output_size))
    
    def forward(self, X):
        self.z1 = X.dot(self.W1) + self.b1
        self.a1 = np.tanh(self.z1)
        self.z2 = self.a1.dot(self.W2) + self.b2
        self.a2 = sigmoid(self.z2)
        return self.a2
    
    def backward(self, X, y, output):
        m = X.shape[0]
        
        dz2 = output - y
        dW2 = (1/m) * self.a1.T.dot(dz2)
        db2 = (1/m) * np.sum(dz2, axis=0, keepdims=True)
        
        da1 = dz2.dot(self.W2.T)
        dz1 = da1 * (1 - np.power(self.a1, 2))
        dW1 = (1/m) * X.T.dot(dz1)
        db1 = (1/m) * np.sum(dz1, axis=0, keepdims=True)
        
        return dW1, db1, dW2, db2

# Gradient Descent
def gradient_descent(X, y, theta, alpha, iterations):
    m = len(y)
    cost_history = []
    
    for i in range(iterations):
        h = X.dot(theta)
        cost = (1/(2*m)) * np.sum((h - y)**2)
        cost_history.append(cost)
        
        gradient = (1/m) * X.T.dot(h - y)
        theta = theta - alpha * gradient
    
    return theta, cost_history

# Decision Tree (Simple Implementation)
class DecisionNode:
    def __init__(self, feature=None, threshold=None, left=None, right=None, value=None):
        self.feature = feature
        self.threshold = threshold
        self.left = left
        self.right = right
        self.value = value

def gini_impurity(y):
    classes = np.unique(y)
    impurity = 1.0
    for cls in classes:
        prob = len(y[y == cls]) / len(y)
        impurity -= prob ** 2
    return impurity

# Support Vector Machine (Linear)
def svm_cost_function(X, y, w, b, C):
    n_samples = X.shape[0]
    distances = 1 - y * (X.dot(w) + b)
    distances[distances < 0] = 0
    hinge_loss = C * np.sum(distances) / n_samples
    regularization = 0.5 * np.dot(w, w)
    return hinge_loss + regularization

# Principal Component Analysis
def pca(X, n_components):
    X_centered = X - np.mean(X, axis=0)
    cov_matrix = np.cov(X_centered.T)
    eigenvalues, eigenvectors = np.linalg.eigh(cov_matrix)
    idx = np.argsort(eigenvalues)[::-1]
    components = eigenvectors[:, idx[:n_components]]
    return X_centered.dot(components)

# Cross Validation
def k_fold_cross_validation(X, y, model, k=5):
    fold_size = len(X) // k
    scores = []
    
    for i in range(k):
        start_idx = i * fold_size
        end_idx = (i + 1) * fold_size
        
        X_val = X[start_idx:end_idx]
        y_val = y[start_idx:end_idx]
        X_train = np.concatenate([X[:start_idx], X[end_idx:]])
        y_train = np.concatenate([y[:start_idx], y[end_idx:]])
        
        model.fit(X_train, y_train)
        predictions = model.predict(X_val)
        score = accuracy_score(y_val, predictions)
        scores.append(score)
    
    return np.mean(scores)
