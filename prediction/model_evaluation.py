from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
import numpy as np

class ModelEvaluator:
    @staticmethod
    def evaluate(model, X_test, y_test):
        """Calculates regression metrics."""
        predictions = model.predict(X_test)
        
        mae = mean_absolute_error(y_test, predictions)
        rmse = np.sqrt(mean_squared_error(y_test, predictions))
        r2 = r2_score(y_test, predictions)
        
        return {
            "MAE": mae,
            "RMSE": rmse,
            "R2": r2
        }
