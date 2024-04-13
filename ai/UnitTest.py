import unittest
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from utility import (
    find_non_numeric_columns,
    category_to_numerical,
    handle_missing_values,
)


class TestPreprocessingFunctions(unittest.TestCase):
    def setUp(self):
        # Mock data for testing preprocessing functions
        self.mock_data = pd.DataFrame({
            'col1': ['a', 'b', 'c', 'd'],
            'col2': [1, np.nan, 3, 4],
            'col3': [5, 6, 7, np.nan],
            'col4': ['x', 'y', np.nan, 'z']
        })

    def test_find_non_numeric_columns(self):
        # Test find_non_numeric_columns function
        non_numeric_cols = find_non_numeric_columns(self.mock_data)
        self.assertEqual(non_numeric_cols, ['col1', 'col4'])

    def test_category_to_numerical(self):
        # Test category_to_numerical function
        columns = ['col1', 'col4']
        transformed_data = category_to_numerical(self.mock_data, columns)
        self.assertTrue(all(transformed_data[col].dtype == 'int' for col in columns))

    def test_handle_missing_values(self):
        # Test handle_missing_values function
        columns = ['col1', 'col2', 'col3', 'col4']
        transformed_data = category_to_numerical(self.mock_data, columns)
        cleaned_data = handle_missing_values(transformed_data)
        self.assertTrue(cleaned_data.isna().sum().sum() == 0)


class TestRandomForestModel(unittest.TestCase):
    def setUp(self):
        # Mock data for testing Random Forest model
        self.mock_data = pd.DataFrame({
            'feature1': np.random.rand(100),
            'feature2': np.random.rand(100),
            'feature3': np.random.rand(100),
            'price': np.random.rand(100)
        })

    def test_model_training_and_prediction(self):
        # Test model training and prediction
        X = self.mock_data[['feature1', 'feature2', 'feature3']]
        y = self.mock_data['price']
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
        scaler = StandardScaler()
        X_train_scaled = scaler.fit_transform(X_train)
        X_test_scaled = scaler.transform(X_test)

        model_rf = RandomForestRegressor(n_estimators=50, max_features=4,max_depth=None,min_samples_split=3,
                                        random_state=42, bootstrap=False)
        model_rf.fit(X_train_scaled, y_train)
        predictions = model_rf.predict(X_test_scaled)

        # Check if predictions are within a reasonable range
        self.assertTrue(all(predictions >= 0))


if __name__ == '__main__':
    unittest.main()
