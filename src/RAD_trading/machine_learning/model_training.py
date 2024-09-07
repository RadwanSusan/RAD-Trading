# src\RAD_trading\machine_learning\model_training.py
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier
def train_model(features, target, test_size=0.2, random_state=42):
    """
    Train a machine learning model.
    :param features: DataFrame of features
    :param target: Series of target values
    :param test_size: Proportion of data to use for testing
    :param random_state: Random state for reproducibility
    :return: Trained model and scaler
    """
    X_train, X_test, y_train, y_test = train_test_split(features, target, test_size=test_size, random_state=random_state)
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)
    model = RandomForestClassifier(n_estimators=100, random_state=random_state)
    model.fit(X_train_scaled, y_train)
    return model, scaler, X_test_scaled, y_test
