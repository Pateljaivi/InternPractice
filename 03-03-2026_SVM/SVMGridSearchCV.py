import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.compose import ColumnTransformer
from sklearn.model_selection import GridSearchCV, train_test_split
from sklearn.inspection import DecisionBoundaryDisplay
from sklearn.decomposition import PCA
#GridSearchCV -> Find best hyperparameter
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.svm import SVC
from sklearn.metrics import confusion_matrix, accuracy_score,classification_report
import warnings


class SVMtrainClassifier:
    def __init__(self,file_path):
        self.file_path = file_path
        self.df = None
        self.X_train = None
        self.y_train = None
        self.X_test = None
        self.y_test = None
        self.scaler = StandardScaler()
        self.best_model = None #after gridsearch best model will store here
        warnings.filterwarnings("ignore")

    def load_and_clean_data(self):
        try:
            self.df = pd.read_csv(self.file_path)
            print(f"Data Loaded Successfully.Shape:{self.df.shape}")
        except FileNotFoundError:
            print("File Not Found!")
            exit()

        print("Missing values:\n", self.df.isnull().sum())


        print("Duplicate  Rows:", self.df.duplicated().sum())
        self.df.drop_duplicates(inplace=True)
        print("After Removing duplicate rows:", self.df.duplicated().sum())

        #Drop passengerId(useless column)
        if "PassengerId" in self.df.columns:
            self.df.drop("PassengerId", axis=1, inplace=True)

        # Outlier Detection
        print("Outlier Checking...")
        numeric_cols = self.df.select_dtypes(include="number").columns

        for col in numeric_cols:
           if col != "Survived":
            plt.figure(figsize=(6, 4))
            plt.boxplot(self.df[col])
            plt.title(f"Boxplot for {col}")
            plt.xlabel(col)
            plt.grid(True)
            plt.show()


    def prepare_data(self):

        X = self.df.drop("Survived", axis=1)
        y = self.df["Survived"]

        self.X_train,self.X_test,self.y_train,self.y_test = train_test_split(X,y,test_size=0.2,random_state=1)


    def run_pipeline_gridsearch(self):

        numerical_cols = ["Pclass","Age","SibSp","Parch","Fare"]
        categorical_cols = ["Sex","Embarked"]

        #Column Transformer
        preprocessor = ColumnTransformer([
            ('num', StandardScaler(), numerical_cols),
            ('cat', OneHotEncoder(drop='first'), categorical_cols),
        ])

        #Full Pipeline
        pipe = Pipeline([
            ('preprocessor', preprocessor),
            ('svm',SVC())
        ])

        param_grid = {
            'svm__C':[0.1,1,10],
            'svm__kernel':['linear', 'rbf'],
            'svm__gamma':['scale',0.1],
        }

        grid = GridSearchCV(pipe,param_grid = param_grid,scoring = 'accuracy',cv=5)
        #cv=5-->fold cross validation,try all combination,choose that give best accuracy
        #pipe->full pipline,param_grid->parametres combinations,scoring=accuracy -> best accuracy chhose,cv=5->fold cross validation
        grid.fit(self.X_train,self.y_train)

        self.best_model=grid.best_estimator_#store best trained pipeline
        print("Best Parameters:",grid.best_params_)#give best parameters


    def evaluate_model(self):

        y_pred = self.best_model.predict(self.X_test)

        acc = accuracy_score(self.y_test, y_pred)
        print("\nAccuracy:",acc)
        print("Classification Report:\n",classification_report(self.y_test, y_pred))

        cm = confusion_matrix(self.y_test, y_pred)
        plt.figure(figsize=(6, 4))
        sns.heatmap(cm,annot=True,fmt="d",cmap="YlGnBu")
        plt.title("Confusion Matrix")
        plt.show()

    def visualize_comparison(self):
        # Get predictions from your model
        y_pred = self.best_model.predict(self.X_test)

        # Create a temporary plot area with 2 side-by-side graphs
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 6))

        # Colors dots by what actually happened (Survived or Not)
        sns.scatterplot(x=self.X_test['Age'], y=self.X_test['Fare'],
                        hue=self.y_test, palette='coolwarm', ax=ax1)
        ax1.set_title("REALITY: Who actually survived?")
        ax1.set_xlabel("Age")
        ax1.set_ylabel("Ticket Fare")

        # --- SVM PREDICTION ---
        # Colors dots by what the SVM predicted
        sns.scatterplot(x=self.X_test['Age'], y=self.X_test['Fare'],
                        hue=y_pred, palette='coolwarm', ax=ax2)
        ax2.set_title("PREDICTION: Who did the SVM think survived?")
        ax2.set_xlabel("Age")
        ax2.set_ylabel("Ticket Fare")

        plt.tight_layout()
        plt.show()

    def plot_boundary_pca(self):
        # Process data for PCA
        X_processed = self.best_model.named_steps['preprocessor'].transform(self.X_train)

        # Compress 7 features into 2 Components
        pca = PCA(n_components=2)
        X_pca = pca.fit_transform(X_processed)


        vis_model = SVC(kernel='rbf', C=1.0)
        vis_model.fit(X_pca, self.y_train)

        # Create the Plot
        plt.figure(figsize=(10, 7))

        # Draw the straight background boundary
        DecisionBoundaryDisplay.from_estimator(
            vis_model,
            X_pca,
            response_method="predict",
            grid_resolution=500,  # Higher resolution for a crisp straight line
            alpha=0.4,
            cmap='RdBu',
            ax=plt.gca()
        )

        # Scatter the actual data
        plt.scatter(X_pca[:, 0], X_pca[:, 1],
                    c=self.y_train,
                    edgecolors="k",
                    cmap='RdBu',
                    s=35)

        plt.title("Titanic SVM: Linear Decision Boundary\n(Perfectly straight line separating Died vs Survived)")
        plt.xlabel("Principal Component 1")
        plt.ylabel("Principal Component 2")
        plt.grid(True, linestyle='--', alpha=0.3)
        plt.show()

def main():

    DATA_PATH = "SVMtrain.csv"
    model = SVMtrainClassifier(DATA_PATH)
    model.load_and_clean_data()
    model.prepare_data()
    model.run_pipeline_gridsearch()
    model.evaluate_model()
    model.visualize_comparison()
    model.plot_boundary_pca()

if __name__ == "__main__":
    main()