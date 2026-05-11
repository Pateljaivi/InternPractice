"""Insurance Charges Prediction Using Linear Regression"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder, StandardScaler
#OneHotEncoder -> Categorical data ko numbers me convert karta hai
#standardscaler -> data ko scale karta hai
from sklearn.model_selection import train_test_split #dataset ko train test me split karta hai
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score, mean_squared_error, mean_absolute_error


class InsuranceChargesPrediction:
    def __init__(self, file_path, test_size=0.3, random_state=42):
        self.file_path = file_path
        self.test_size = test_size
        self.random_state = random_state

        self.data = None
        self.X = None
        self.y = None

        self.X_train = None
        self.y_train = None
        self.X_test = None
        self.y_test = None

        self.scaler = None
        self.model = None
        self.preprocessor = None

    def load_data(self):
        print("Loading dataset...")
        self.data = pd.read_csv(self.file_path)
        print("Dataset loaded.\n")

        print(f"Dataset Shape: {self.data.shape}\n")

        print(f"First 5 rows of dataset: {self.data.head(5)}")

        print(f"Statistical Summary:{self.data.describe()}")

        print(f"Data Information:{self.data.info()}")


    def clean_data(self):
        # check missing values
        print("Checking missing values...")
        print(self.data.isnull().sum(), "\n")

        # Duplicate Check
        duplicate_count = self.data.duplicated().sum()
        print(f"Duplicate Rows Found: {duplicate_count}")

        if duplicate_count > 0:
            self.data.drop_duplicates(inplace=True)

        print("Duplicate Rows Removed:", self.data.duplicated().sum())

        # Outlier Detection
        print("Outlier Checking...")
        numeric_cols = self.data.select_dtypes(include="number").columns


        for col in numeric_cols:
            if col != "charges":
               plt.figure(figsize=(6, 4))
               plt.boxplot(self.data[col])
               plt.title(f"Boxplot for {col}")
               plt.xlabel(col)
               plt.grid(True)
               plt.show()

        print("Outlier Handling...")
        for col in numeric_cols:
            Q1 = self.data[col].quantile(0.25)  # 25%
            Q3 = self.data[col].quantile(0.75)  # 75%

            IQR = Q3 - Q1  # tells middle 50% data spread

            lower = Q1 - 1.5 * IQR
            upper = Q3 + 1.5 * IQR

            # capping(no row deletion)
            self.data[col] = np.where(self.data[col] < lower, lower,self.data[col])
            self.data[col] = np.where(self.data[col] > upper, upper,self.data[col])


    def encode_data(self):
        print("Encoding and Scaling data...")

        # Define columns
        categorical_cols = ['sex', 'smoker', 'region']
        numeric_cols = ['age', 'bmi', 'children']

        # This handles BOTH scaling and encoding
        self.preprocessor = ColumnTransformer(
            transformers=[
                ('num', StandardScaler(), numeric_cols),
                ('cat', OneHotEncoder(drop='first', handle_unknown='ignore'), categorical_cols)
            ])

        # Fit on training data, transform both
        self.X_train = self.preprocessor.fit_transform(self.X_train)
        self.X_test = self.preprocessor.transform(self.X_test)

        print("Preprocessing (Encoding + Scaling) completed.\n")

    def split_data(self):

        print("Splitting data...")

        y = self.data["charges"]
        X = self.data.drop("charges", axis=1)

        self.X_train, self.X_test, self.y_train, self.y_test = train_test_split(X, y, test_size=self.test_size,random_state=self.random_state)


        print("Train-Test split completed.\n")



    def train(self):
        print("Training model...")
        self.model = LinearRegression()
        self.model.fit(self.X_train, self.y_train)
        print("Training completed.\n")

    def evaluate(self):
        print("Evaluating model...")

        train_pred = self.model.predict(self.X_train)
        test_pred = self.model.predict(self.X_test)

        train_r2 = r2_score(self.y_train, train_pred)
        test_r2 = r2_score(self.y_test, test_pred)
        mse = mean_squared_error(self.y_test, test_pred)
        rmse = np.sqrt(mse)
        mae = mean_absolute_error(self.y_test, test_pred)

        print("==========Model Performance==========")
        print(f"Train R2 Score: {train_r2:.4f}")
        print(f"Test R2 Score: {test_r2:.4f}")
        print(f"Mean Squared Error: {mse:.4f}")
        print(f"Root Mean Squared Error: {rmse:.4f}")
        print(f"Mean Absolute Error: {mae:.4f}")
        print("====================================\n")

def main():
    DATA_PATH = "insurance.csv"

    model = InsuranceChargesPrediction(DATA_PATH)
    model.load_data()
    model.clean_data()

    model.split_data()
    model.encode_data()

    model.train()
    model.evaluate()

if __name__ == "__main__":
    main()