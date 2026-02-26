"""Heart Failure Prediction using Random Forest Classifier"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.preprocessing import OneHotEncoder
from sklearn.compose import make_column_selector,make_column_transformer
from sklearn.pipeline import make_pipeline
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import  accuracy_score, roc_auc_score ,roc_curve


class HeartFailurePrediction:
    def __init__(self,file_path,test_size=0.2,random_state=42):
        self.file_path = file_path
        self.test_size = test_size
        self.random_state = random_state

        self.data =  None
        self.X = None
        self.y = None

        self.X_train = None
        self.y_train = None
        self.X_test = None
        self.y_test = None

        self.pipeline = None


    #Load Dataset
    def load_data(self):
        print("Loading dataset...")
        self.data = pd.read_csv(self.file_path)
        print("Dataset loaded.\n")

        print(f"Dataset Shape: {self.data.shape}\n")

        print(f"First 5 rows of dataset: {self.data.head(5)}")

        print(f"Statistical Summary:{self.data.describe()}")

        print(f"Data Information:{self.data.info()}")

    def clean_data(self):

        #check missing values
        print("Checking missing values...")
        print(self.data.isnull().sum(),"\n")

        # Duplicate Check
        duplicate_count = self.data.duplicated().sum()
        print(f"Duplicate Rows Found: {duplicate_count}")

        # Outlier Detection
        print("Outlier Checking...")
        # numeric_cols = self.data.select_dtypes(include="number").columns
        numeric_cols = ["Age", "RestingBP","Cholesterol","MaxHR","Oldpeak"]

        for col in numeric_cols:
            # if col != "HeartDisease":
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
            self.data[col] = np.where(self.data[col] < lower, lower, self.data[col])  # agar value lower se chhoti hai to use lower bana diya
            self.data[col] = np.where(self.data[col] > upper, upper, self.data[col])  # agar value upper se badi hai to use badi bana diya


    def prepare_data(self):

        #split target and feature
        y =  self.data.pop("HeartDisease")
        X = self.data

        self.X_train,self.X_test,self.y_train,self.y_test = train_test_split(X,y,test_size=self.test_size,random_state=self.random_state)

        print("Train-Test Split completed.\n")

    def build_pipeline(self):

        print("Building pipeline...")

        #automatically detect categorical column
        categorical_Selector = make_column_selector(dtype_include=object)

        # APPLY one hot encoding to categorical columns
        transformer = make_column_transformer(
            (OneHotEncoder(handle_unknown="ignore"), categorical_Selector),
            remainder="passthrough" #if this miss non-categorical column means numeric column might be removed
        )

        # initialize decision tree regressor
        model = RandomForestClassifier(
            n_estimators=200, #300 decison tree
            max_depth=7, #tree's growth
            random_state=self.random_state
        )

        # Create pipeline
        self.pipeline = make_pipeline(transformer, model)
        print("Pipeline built.\n")

    #training model
    def train(self):
            print("Training Model....")
            self.pipeline.fit(self.X_train, self.y_train)
            print("Model Training Completed.\n")

    #evalute model
    def evaluate(self):
        print("Evaluating Model....")

        # train_pred = self.pipeline.predict(self.X_train)
        # test_pred = self.pipeline.predict(self.X_test)
        #
        # print("Train Accuracy:",accuracy_score(self.y_train,train_pred)*100)
        # print("Test Accuracy:",accuracy_score(self.y_test,test_pred)*100)

        y_pred = self.pipeline.predict(self.X_test)
        train_probs = self.pipeline.predict_proba(self.X_train)[:,1]
        test_probs = self.pipeline.predict_proba(self.X_test)[:,1]

        accuracy = accuracy_score(self.y_test,y_pred)

        train_auc = roc_auc_score(self.y_train, train_probs)
        test_auc = roc_auc_score(self.y_test, test_probs)

        print("\n=========Model Performance=========\n")
        print(f"Accuracy: {accuracy:.4f}")
        print(f"Train AUC: {train_auc:.4f}")
        print(f"Test AUC: {test_auc:.4f}")
        print("====================================\n")

        return test_probs

    #Plot ROC CURVE
    def plot_roc_curve(self,test_probs):

        print("Plotting ROC Curve...")

        baseline_probs = [1 for _ in range(len(self.y_test))]  #for all test sample Probability = 1 aasign

        base_fpr,base_tpr, _ = roc_curve(self.y_test,baseline_probs) #calculate base model ROC
        model_fpr , model_tpr , _ = roc_curve(self.y_test,test_probs) #Actual model's ROC curve

        plt.figure(figsize=(8,6))

        plt.plot(base_fpr,base_tpr,linestyle='--',label="Baseline")#baseline
        plt.plot(model_fpr,model_tpr,marker='.',label="Random Forest")#actual model's ROC curve

        plt.xlabel("False Positive Rate")
        plt.ylabel("True Positive Rate")
        plt.title("ROC Curve - Heart Failure Prediction")

        plt.legend()
        plt.grid(True)
        plt.show()

def main():

    DATA_PATH = "heart.csv"

    model = HeartFailurePrediction(DATA_PATH)

    model.load_data()
    model.clean_data()
    model.prepare_data()
    model.build_pipeline()
    model.train()

    test_probs = model.evaluate()
    model.plot_roc_curve(test_probs)


if __name__ == "__main__":
    main()