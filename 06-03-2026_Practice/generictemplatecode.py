import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, confusion_matrix
from sklearn.pipeline import make_pipeline
from sklearn.compose import make_column_selector, make_column_transformer
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OneHotEncoder, StandardScaler


class GeneticCode:
    def __init__(self,file_path,target_column,test_size=0.3,random_state=42):
        self.file_path = file_path
        self.target_column = target_column
        self.test_size = test_size
        self.random_state = random_state
        self.df = None

        self.X = None
        self.y = None

        self.X_train = None
        self.y_train = None
        self.X_test = None
        self.y_test = None

        self.pipeline = None


    def load_data(self):

      """loading the data,shape od dataset,statistical summary,information of dataset """

      try:
            print("Loading data...")
            self.df = pd.read_csv(self.file_path)
            print("Dataset loaded...")

      except FileNotFoundError:
            print(f"{self.file_path} Dataset not found...")

      except Exception as e:
            print(f"Error:{e}")

      print("\n shape:",self.df.shape)
      print("\nStatistical Summary:",self.df.describe())
      print("Dataset Information:\n",self.df.info())

    def clean_data(self):

        """ basic cleaning and outlier handling """

        self.load_data()

        try:
            print("Cleaning data...")

            print("Missing values:",self.df.isnull().sum())

            print("Duplicate values:",self.df.duplicated().sum())

            print("Outlier Handling...")

            numeric_col = self.df.select_dtypes(include="number")

            for col in numeric_col:
                plt.figure(figsize=(6,4))
                plt.boxplot(self.df[col])
                plt.title(f"Boxplot of {col}")
                plt.xlabel(col)
                plt.grid(True)
                plt.show()

            print("Outlier Handling...")

            for col in numeric_col:
                Q1 = self.df[col].quantile(0.25)
                Q2 = self.df[col].quantile(0.75)

                IQR = Q2 - Q1

                lower = Q1 - 1.5*IQR
                upper = Q1 + 1.5*IQR

                self.df[col] = np.where(self.df[col] < lower, lower, self.df[col])
                self.df[col] = np.where(self.df[col] > upper, upper, self.df[col])
        except Exception as e:
            print(f"Error during cleaning data:{e}")

    def train_test_split(self):

        """train test split of dataset"""

        self.clean_data()

        try:
            self.X = self.df.drop(self.target_column, axis=1)
            self.y = self.df[self.target_column]


            self.X_train,self.X_test,self.y_train,self.y_test = train_test_split(
                self.X,self.y,test_size=self.test_size,random_state=self.random_state
            )

            print("Train test split Successfully...")
        except Exception as e:
            print(f"Error during splitting:{e}")

    def build_pipeline(self):

        """Pipeline building - Onehotencoder ,standard scaling"""

        self.train_test_split()

        try:
            print("Building pipeline...")

            cat_cols = make_column_selector(dtype_include=object)

            numeric_cols = make_column_selector(dtype_include=np.number)

            transformer = make_column_transformer(
                (OneHotEncoder(handle_unknown='ignore'), cat_cols),
                (StandardScaler(), numeric_cols),
                remainder="passthrough"
            )

            rand_for = LogisticRegression()
            self.pipeline = make_pipeline(transformer, rand_for)

            print("Pipeline built successfully...")
        except Exception as e:
            print(f"Error during building pipeline:{e}")

    def train_model(self):

        """Training model using pipeline"""

        self.build_pipeline()

        try:
            print("Training model...")
            self.pipeline.fit(self.X_train,self.y_train)
            print("Model Training Completed...")
        except Exception as e:
            print(f"Error during training:{e}")

    def evaluate_model(self):

        """Evaluate model performance"""

        self.train_model()

        try:
            print("Evaluating model...")

            train_pred =   self.pipeline.predict(self.X_train)
            y_pred = self.pipeline.predict(self.X_test)

            train_acc = accuracy_score(self.y_train,train_pred)
            acc = accuracy_score(self.y_test, y_pred)

            print("Test Accuracy:",acc)

            print("Training Accuracy:",train_acc)

            cm = confusion_matrix(self.y_test, y_pred)

            print("Confusion Matrix:\n",cm)

            plt.figure(figsize=(6,4))
            sns.heatmap(cm,annot=True,fmt="g",cmap="YlOrRd")
            plt.title("Confusion Matrix")
            plt.show()
        except Exception as e:
            print(f"Error during evaluation:{e}")


def main():

    DATA_PATH = "Social_Network_Ads.csv"

    try:
        model = GeneticCode(DATA_PATH,"Purchased")
        model.evaluate_model()
    except Exception as e:
        print(f"Fatal Error in main: {e}")


if __name__ == "__main__":
    main()
