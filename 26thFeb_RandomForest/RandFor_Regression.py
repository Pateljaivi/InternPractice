""" House Price Prediction using Random Forest Regression """

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error,r2_score,mean_absolute_error
from sklearn.tree import plot_tree

class HousePricePrediction:
    def __init__(self,file_path,test_size=0.3,random_state=42):
        self.file_path = file_path
        self.test_size = test_size
        self.random_state = random_state

        self.data = None
        self.X_train = None
        self.y_train = None
        self.X_test = None
        self.y_test = None
        self.model = None

    #Load dataset
    def load_data(self):

        print("Loading dataset...")
        self.data = pd.read_csv(self.file_path)
        print("Dataset loaded.\n")

        print(f"Dataset Shape: {self.data.shape}\n")

        print(f"First 5 rows of dataset: {self.data.head(5)}\n")

        print(f"Statistical Summary:{self.data.describe()}\n")

        print(f"Data Information:{self.data.info()}\n")

    def clean_data(self):
        # check missing values
        print("Checking missing values...")
        print(self.data.isnull().sum(), "\n")

        # Duplicate Check
        duplicate_count = self.data.duplicated().sum()
        print(f"Duplicate Rows Found: {duplicate_count}")

        # Outlier Detection
        print("Outlier Checking...")
        numeric_cols = self.data.select_dtypes(include="number").columns


        for col in numeric_cols:
            if col != "House_Price":
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
            self.data[col] = np.where(self.data[col] < lower, lower, self.data[col])
            self.data[col] = np.where(self.data[col] > upper, upper, self.data[col])


    def feature_engineering(self):
        print("Feature Engineering...")

        current_year = 2026
        self.data["House_Age"] = current_year - self.data["Year_Built"]

        #Drop original year_built
        self.data.drop("Year_Built", axis=1, inplace=True)

        print("Feature Engineering completed.\n")

    def split_data(self):

        print("Splitting data...")

        y = self.data.pop("House_Price")
        X = self.data

        self.X_train,self.X_test,self.y_train,self.y_test = train_test_split(X,y,test_size=self.test_size,random_state=self.random_state)

        print("Train-Test split completed.\n")

    def train(self):

        print("Training model...")

        self.model = RandomForestRegressor(
            n_estimators=100,
            max_depth=5,
            min_samples_split=25,
            min_samples_leaf=15,
            max_features='sqrt',
            random_state=self.random_state)
        self.model.fit(self.X_train,self.y_train)

        print("Training completed.\n")

    def evaluate(self):

        print("Evaluating model...")

        train_pred = self.model.predict(self.X_train)
        test_pred = self.model.predict(self.X_test)

        train_r2 = r2_score(self.y_train, train_pred)
        test_r2 = r2_score(self.y_test, test_pred)
        mse = mean_squared_error(self.y_test,test_pred)
        rmse = np.sqrt(mse)
        mae = mean_absolute_error(self.y_test,test_pred)

        print("==========Model Performance==========")
        print(f"Train R2 Score: {train_r2:.4f}")
        print(f"Test R2 Score: {test_r2:.4f}")
        print(f"Mean Squared Error: {mse:.4f}")
        print(f"Root Mean Squared Error: {rmse:.4f}")
        print(f"Mean Absolute Error: {mae:.4f}")
        print("====================================\n")

    def plot_tree_structure(self,tree_index=0,max_depth=3):
        print("Plotting tree structure...")

        if self.model is None:
            print("Model not trained.\n")
            return

        tree = self.model.estimators_[tree_index]

        plt.figure(figsize=(20,10))
        plot_tree(
            tree,
            filled=True,
            max_depth=max_depth,
            feature_names=self.X_train.columns
        )

        plt.title(f"Tree structure for {tree_index}")
        plt.show()

def main():

    DATA_PATH = "house_price_regression_dataset.csv"

    model = HousePricePrediction(DATA_PATH)

    model.load_data()
    model.clean_data()
    model.feature_engineering()
    model.split_data()
    model.train()
    model.evaluate()
    model.plot_tree_structure()

if __name__ == "__main__":
    main()
