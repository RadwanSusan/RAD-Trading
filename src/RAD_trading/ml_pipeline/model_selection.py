# src\RAD_trading\ml_pipeline\model_selection.py
from sklearn.model_selection import cross_val_score
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import SVC
from xgboost import XGBClassifier
class ModelSelector:
    def __init__(self, X, y, cv=5, scoring='accuracy'):
        self.X = X
        self.y = y
        self.cv = cv
        self.scoring = scoring
        self.models = {
            'logistic_regression': LogisticRegression(),
            'decision_tree': DecisionTreeClassifier(),
            'random_forest': RandomForestClassifier(),
            'svm': SVC(),
            'xgboost': XGBClassifier()
        }
    def evaluate_models(self):
        results = {}
        for name, model in self.models.items():
            scores = cross_val_score(model, self.X, self.y, cv=self.cv, scoring=self.scoring)
            results[name] = {
                'mean_score': scores.mean(),
                'std_score': scores.std()
            }
        return results
    def select_best_model(self):
        results = self.evaluate_models()
        best_model = max(results, key=lambda x: results[x]['mean_score'])
        return best_model, self.models[best_model]
