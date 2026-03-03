import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler,LabelEncoder
from sklearn.svm import SVC
from sklearn.inspection import DecisionBoundaryDisplay
from sklearn.metrics import accuracy_score,confusion_matrix,classification_report


class SVMSocialAds:
    def __init__(self,file_path):
        self.file_path = file_path
        self.model = None
        self.scaler = StandardScaler()

    def load_data(self):
        self.df = pd.read_csv(self.file_path)
        print("Data Loaded Successfully\n")
        print(self.df.head())

    def splitdata(self):
        X = self.df.drop("Purchased",axis=1)
        y = self.df["Purchased"]

        self.X_train,self.X_test,self.y_train,self.y_test = train_test_split(X,y,test_size=0.2,random_state=42)

        self.X_train = self.scaler.fit_transform(self.X_train)
        self.X_test = self.scaler.transform(self.X_test)


    def train_model(self,kernel='rbf',C=1.0,gamma='scale'):
        self.model = SVC(kernel=kernel,C=C,gamma=gamma)
        self.model.fit(self.X_train,self.y_train)
        print("Trained Model Successfully\n")

    def evaluate(self):
        y_pred = self.model.predict(self.X_test)

        print("\nAccuracy:",accuracy_score(self.y_test,y_pred)*100)
        print("Confusion Matrix:\n",confusion_matrix(self.y_test,y_pred))
        print("Classification Report:",classification_report(self.y_test,y_pred))

    def plot_boundary(self):

        DecisionBoundaryDisplay.from_estimator(
            self.model,
            self.X_train,
            response_method="predict",
            alpha=0.3
        )


        plt.scatter(self.X_train[:, 0], self.X_train[:, 1], c=self.y_train, edgecolors="k")

        plt.xlabel("Age(Scaled)")
        plt.ylabel("Estimated Salary(Scaled)")
        plt.title("SVM Decision Boundary")
        plt.show()


def main():
    file_path = "Social_Network_Ads.csv"

    model = SVMSocialAds(file_path)
    model.load_data()
    model.splitdata()
    model.train_model(kernel='rbf',C=1.0,gamma='scale')
    model.evaluate()
    model.plot_boundary()




if __name__ == "__main__":
    main()