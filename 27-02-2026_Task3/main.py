"""Insurance Charges Prediction using Random Forest Regression"""
"""Dataset load from SSMS"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sqlalchemy import create_engine
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import r2_score,mean_squared_error,mean_absolute_error
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder
from sklearn.tree import plot_tree

class InsuranceCharges:

    def __init__(self,server,database,table):
        self.server = server
        self.database = database
        self.table = table
        self.engine = None
        self.df = None
        self.pipeline = None


    #connect database
    def connect_database(self):
        self.engine = create_engine(
            f"mssql+pyodbc://@localhost/{self.database}"
            "?driver=ODBC+Driver+17+for+SQL+Server"
            "&trusted_connection=yes"
        )

        print("Database Connection Established...")

    #Load Data
    def load_data(self):
        query = f"select * from {self.table}"
        self.df = pd.read_sql(query,self.engine)
        print("Data Loaded successfully")
        print(self.df.head())


    #Handling Missing and Duplicates
    def basic_cleaning(self):

        print("Missing values:\n",self.df.isnull().sum())
        # self.df.dropna(inplace=True)

        print("Duplicate  Rows:",self.df.duplicated().sum())
        self.df.drop_duplicates(inplace = True)
        print("After Removing duplicate rows:",self.df.duplicated().sum())

        # Outlier Detection
        print("Outlier Checking...")
        numeric_cols = self.df.select_dtypes(include="number").columns

        for col in numeric_cols:
            if col != "charges":
                plt.figure(figsize=(6, 4))
                plt.boxplot(self.df[col])
                plt.title(f"Boxplot for {col}")
                plt.xlabel(col)
                plt.grid(True)
                plt.show()

        print("Outlier Handling...")
        for col in numeric_cols:
            Q1 = self.df[col].quantile(0.25)  # 25%
            Q3 = self.df[col].quantile(0.75)  # 75%

            IQR = Q3 - Q1  # tells middle 50% data spread

            lower = Q1 - 1.5 * IQR
            upper = Q3 + 1.5 * IQR

            # capping(no row deletion)
            self.df[col] = np.where(self.df[col] < lower, lower, self.df[col])
            self.df[col] = np.where(self.df[col] > upper, upper, self.df[col])

    def build_pipeline(self):
        X = self.df.drop(columns="charges")
        y = self.df["charges"]

        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.2, random_state = 42)

        # Define columns
        categorical_cols = ['sex', 'smoker', 'region']
        numeric_cols = ['age', 'bmi', 'children']

        #preprocessing
        preprocessor = ColumnTransformer(
            transformers=[
                ("cat",OneHotEncoder(drop="first"),categorical_cols)],remainder="passthrough"
        )

        #Full pipeline
        self.pipeline = Pipeline(steps = [
            ("preprocessing", preprocessor),
        ("model", RandomForestRegressor(n_estimators=200,max_depth=8,min_samples_split=15,min_samples_leaf=5,random_state=42)),
        ])

        #Train
        self.pipeline.fit(X_train,y_train)
        print("Pipeline Completed Successfully")

        #Predict
        train_pred = self.pipeline.predict(X_train)
        test_pred = self.pipeline.predict(X_test)


        #comparison DataFrame
        comparison_df = pd.DataFrame({
            "Actual":y_test.values,
            "Predicted":test_pred,
            "Error":y_test.values - test_pred
        })

        train_r2 = r2_score(y_train,train_pred)
        r2 = r2_score(y_test, test_pred)

        mse = mean_squared_error(y_test,test_pred)

        rmse = np.sqrt(mse)

        mae = mean_absolute_error(y_test,test_pred)
        print("==========Model Performance==========")
        print(f"Train R2 Score: {train_r2}")
        print(f"Test R2 Score: {r2}")
        print(f"Mean Squared Error: {mse} ")
        print(f"Root Mean Squared Error: {rmse}")
        print(f"Mean Absolute Error: {mae}")
        print("====================================\n")

        print("\nSample Actual vs predicted..")
        print(comparison_df.head(20))



    def predicted_charges(self):

        X_full = self.df.drop("charges",axis=1) #remove target from features

        self.df["predicted_charges"] = self.pipeline.predict(X_full)#trained random forest model predict on full dataset

        print("Prediction Column Added...")


    def store_prediction(self):
        #updated dataframe
        self.df.to_sql(
            self.table,
            self.engine,
            if_exists="replace",
            index=False,

        )
        print("Prediction stored successfully")

    def plot_tree_structure(self, tree_index=0, max_depth=3):
        print("Plotting tree structure...")

        if self.pipeline is None:
            print("Model not trained.\n")
            return

        # Access the 'model' step from the pipeline
        model = self.pipeline.named_steps['model']

        #Access the specific tree from the RandomForest model
        tree = model.estimators_[tree_index]

        plt.figure(figsize=(20, 10))
        plot_tree(
            tree,
            filled=True,
            feature_names=None, 
            max_depth=max_depth
        )

        plt.title(f"Tree structure for estimator index: {tree_index}")
        plt.show()


def main():

    model = InsuranceCharges(
        server = "localhost",
        database = "InsuranceDB",
        table = "insurance_data",
    )

    model.connect_database()
    model.load_data()
    model.basic_cleaning()
    model.build_pipeline()
    model.predicted_charges()
    model.store_prediction()
    model.plot_tree_structure()


if __name__ == "__main__":
    main()