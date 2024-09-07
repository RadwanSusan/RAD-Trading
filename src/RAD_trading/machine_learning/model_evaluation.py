# src\RAD_trading\machine_learning\model_evaluation.py
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
def evaluate_model(model, X_test, y_test):
    """
    Evaluate a trained machine learning model.
    :param model: Trained model
    :param X_test: Test features
    :param y_test: True labels for test data
    :return: Dictionary of evaluation metrics
    """
    y_pred = model.predict(X_test)
    return {
        'accuracy': accuracy_score(y_test, y_pred),
        'precision': precision_score(y_test, y_pred, average='weighted'),
        'recall': recall_score(y_test, y_pred, average='weighted'),
        'f1_score': f1_score(y_test, y_pred, average='weighted')
    }
