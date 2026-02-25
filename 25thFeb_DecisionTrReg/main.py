import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.compose import make_column_selector, ColumnTransformer
from sklearn.model_selection import train_test_split
from sklearn.pipeline import make_pipeline
from sklearn.compose import make_column_transformer,make_column_selector
from sklearn.tree import DecisionTreeRegressor
from sklearn.preprocessing import LabelEncoder, OneHotEncoder
from sklearn.metrics import r2_score,mean_squared_error

class CarPricePrediction:
    def __init__(self,file_path,test_size=0.2,random_state=42):

        #Basic Configuration
        self.file_path = file_path
        self.test_size = test_size
        self.random_state = random_state

        #Data Containers
        self.data = None
        self.X = None
        self.y = None

        #Train Test data
        self.X_train = None
        self.y_train = None
        self.X_test = None
        self.y_test = None

        #pipeline
        self.pipeline = None

    def load_data(self):

        print("Loading dataset...")

        self.data = pd.read_csv(self.file_path)

        print(f"Dataset loaded: {self.data.shape}")

        print(f"First 5 rows of dataset: {self.data.head(5)}")

        print(f"Statistical Summary:{self.data.describe()}")

        print(f"Data Information:{self.data.info()}")

    def preprocess_data(self):
        print("Preprocessing dataset...")

        #remove Car_ID
        if "Car_ID" in self.data.columns:
            self.data.drop("Car_ID",axis=1,inplace=True)


        #Duplicate Check
        duplicate_count = self.data.duplicated().sum()
        print(f"Duplicate Rows Found: {duplicate_count}")

        #Missing value check
        missing_values = self.data.isnull().sum()
        total_missing = missing_values.sum()

        print("Missing values per column:\n",missing_values)

       #Outlier Detection
        print("Outlier Checking...")
        numeric_cols = self.data.select_dtypes(include="number").columns

        for col in numeric_cols:
            if col != "Price":
                plt.figure(figsize=(6,4))
                plt.boxplot(self.data[col])
                plt.title(f"Boxplot for {col}")
                plt.xlabel(col)
                plt.grid(True)
                plt.show()


        #separate target variable
        self.y = self.data.pop("Price")

        #Remainig columns are features
        self.X = self.data

        #train test split
        self.X_train, self.X_test, self.y_train, self.y_test = train_test_split(
            self.X, self.y, test_size=self.test_size, random_state=self.random_state
        )
        print("Train Test Split Completed.\n")

   


    def build_pipeline(self):
        print("Building pipeline...")

        categorical_Selector = make_column_selector(dtype_include=object)

        #APPLY onehotencoding to categorical columns
        transformer = make_column_transformer(
            (OneHotEncoder(handle_unknown="ignore"),categorical_Selector),
            remainder="passthrough"
        )

        #initialize decision tree regressor
        model = DecisionTreeRegressor(
            max_depth=None,
            min_samples_split=5,
            min_samples_leaf=3,
            random_state=self.random_state
        )

        #Create pipeline
        self.pipeline = make_pipeline(transformer, model)
        print("Pipeline built.\n")

    def train(self):
       print("Training Model....")
       self.pipeline.fit(self.X_train,self.y_train)
       print("Model Training Completed.\n")

    def evaluate(self):
        print("Evaluating Model....")

        train_pred = self.pipeline.predict(self.X_train)
        test_pred = self.pipeline.predict(self.X_test)

        train_r2 = r2_score(self.y_train,train_pred)
        test_r2 = r2_score(self.y_test,test_pred)
        mse = mean_squared_error(self.y_test,test_pred)


        print("------MOdel Performance-----")
        print(f"Train R2 Score: {train_r2:.4f}\n")
        print(f"Test R2 Score: {test_r2:.4f}\n")
        print(f"Mean Squared Error: {mse:.4f}\n")
        print("----------------------------\n")

def main():

    DATA_PATH = "car_price_prediction_.csv"

    model = CarPricePrediction(DATA_PATH)

    model.load_data()
    model.preprocess_data()
    model.build_pipeline()
    model.train()
    model.evaluate()

if __name__ == "__main__":
    main()