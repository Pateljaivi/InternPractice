import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import pickle
from sklearn.metrics import confusion_matrix, accuracy_score,classification_report
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.neighbors import KNeighborsClassifier
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import LabelEncoder, StandardScaler


class HeartRisk:
    def __init__(self,file_path,target_column,test_size=0.2,random_state=42,neighbors=5):
        self.file_path = file_path
        self.test_size = test_size
        self.random_state = random_state
        self.neighbors = neighbors
        self.df = None
        self.target_column = target_column
        self.X = None
        self.y = None
        self.X_train = None
        self.X_test = None
        self.y_train = None
        self.y_test = None
        self.pipeline = None
        self.best_model = None


        #ML components
        self.label_encoder = LabelEncoder()
        self.model = KNeighborsClassifier(n_neighbors=self.neighbors)


    def load_data(self):

        print("Loading data...")
        self.df = pd.read_csv(self.file_path)

        print("Data loaded.\n")

        print(f"\nShape of dataset: {self.df.shape}")

        print(f"\nfirst 5 rows of dataset: {self.df.head(5)}")

        print(f"\nDataset's Statical summary: {self.df.describe()}")

        print(f"Dataset Information: {self.df.info()}")

        print("Target column:", self.target_column)


    def clean_data(self):

        print("Cleaning data...")

        print(f"Missing values:\n",self.df.isnull().sum())

        print("Duplicate values:\n",self.df.duplicated().sum())

        print("Outlier Checking...")

        numeric_cols = self.df.select_dtypes(include=np.number).columns

        for col in numeric_cols:
            if col != self.target_column:
                plt.figure(figsize = (6,4))
                plt.boxplot(self.df[col])
                plt.title(f"Boxplot for {col}")
                plt.xlabel(col)
                plt.grid(True)
                plt.show()

        print("Outlier handling...")

        for col in numeric_cols:
            Q1 = self.df[col].quantile(0.25)

            Q3 = self.df[col].quantile(0.75)

            IQR = Q3 - Q1

            lower = Q1 - 1.5*IQR
            upper = Q3 + 1.5*IQR

            self.df[col] = np.where(self.df[col] < lower,lower,self.df[col])
            self.df[col] = np.where(self.df[col] > upper,upper,self.df[col])


        print("After outlier handling...")
        for col in numeric_cols:
            if col != self.target_column:
                plt.figure(figsize=(6, 4))
                plt.boxplot(self.df[col])
                plt.title(f"Boxplot for {col}")
                plt.xlabel(col)
                plt.grid(True)
                plt.show()

    def prepare_data(self):

        self.X = self.df.drop(self.target_column,axis=1)
        self.y = self.df[self.target_column]

        self.X_train,self.X_test,self.y_train,self.y_test = train_test_split(
            self.X , self.y ,test_size=self.test_size,random_state=self.random_state
        )
        print("Train test split successfully...")

    def build_pipeline(self):

        self.pipeline = Pipeline(
            steps= [
                ("scaler", StandardScaler()),
                ("knn", KNeighborsClassifier())
        ])

        self.pipeline.fit(self.X_train,self.y_train)

        print("pipeline created...")

    def run_gridsearch(self):

        param_grid = {
            "knn__n_neighbors":[3,5,7,9,11],
            "knn__weights":["uniform","distance"],
            "knn__metric":["euclidean","manhattan"]
        }

        grid = GridSearchCV(self.pipeline,param_grid=param_grid,cv=5,scoring="accuracy",n_jobs=-1)
        grid.fit(self.X_train,self.y_train)

        self.best_model = grid.best_estimator_
        print("Best Parameters:",grid.best_params_)

    def evaluate_model(self):

        train_pred = self.pipeline.predict(self.X_train)
        y_pred = self.pipeline.predict(self.X_test)

        cm = confusion_matrix(self.y_test, y_pred)
        train_acc = accuracy_score(self.y_train,train_pred)
        test_acc = accuracy_score(self.y_test, y_pred)
        cr = classification_report(self.y_test, y_pred)

        print("Train Accuracy:",train_acc)
        print("Test Accuracy:",test_acc)
        print("Confusion Matrix:\n",cm)
        print("Classification Report:\n",cr)

        plt.figure(figsize=(6, 4))
        sns.heatmap(cm, annot=True, fmt="d", cmap="YlGnBu")
        plt.title("Confusion Matrix")
        plt.show()

    def save_model(self,file_name="knn_model.pkl"):

        package = {
            "model":self.model,
            "pipeline":self.pipeline,
            "encoder":self.label_encoder
        }

        with open(file_name,"wb") as file:
            pickle.dump(package,file)

        print(f"Model saved successfully to {file_name}")

def main():

    DATA_PATH = "health_risk_classification.csv"

    model = HeartRisk(DATA_PATH,"high_risk_flag")
    model.load_data()
    model.clean_data()
    model.prepare_data()
    model.build_pipeline()
    model.run_gridsearch()
    model.evaluate_model()
    model.save_model()

if __name__ == "__main__":
    main()
