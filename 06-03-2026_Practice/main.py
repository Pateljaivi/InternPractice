import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.pipeline import make_pipeline
from sklearn.tree import DecisionTreeRegressor
from sqlalchemy import create_engine
from sklearn.model_selection import train_test_split
from sklearn.compose import make_column_selector,make_column_transformer
from sklearn.preprocessing import OneHotEncoder,StandardScaler
from sklearn.tree import DecisionTreeRegressor


class SocialNetwork:

    def __init__(self,server,database,table_name,target_column,test_size=0.2,random_state=42):
        self.server = server
        self.database = database
        self.table_name = table_name
        self.test_size = test_size
        self.random_state = random_state
        self.pipeline = None
        self.engine = None
        self.df = None

        self.X = None
        self.y = None

        self.X_train = None
        self.y_train = None
        self.X_test = None
        self.y_test = None
        self.target_column = target_column


    def connect_database(self):

        self.engine = create_engine(
            f"mssql+pyodbc://@localhost/{self.database}"
            "?driver=ODBC+Driver+17+for+SQL+Server"
            "&trusted_connection=yes"
        )
        print("Databse connection successful")


    def load_data(self):
        query = f"select * from {self.table_name}"
        self.df = pd.read_sql(query,self.engine)

        print("data loaded succefully")

        print("first five rows:",self.df.head(5))


    def prepare_data(self):

        print("cleaning data....")

        print("Missing value:",self.df.isnull().sum())
        print("Duplicate value:",self.df.duplicated().sum())

        print("Outlier Checking...")

        numeric_cols = self.df.select_dtypes(include=np.number).columns

        for col in numeric_cols:
            plt.figure(figsize=(6,4))
            plt.boxplot(self.df[col])
            plt.title(f"Box plot of {col}")
            plt.xlabel(col)
            plt.ylabel(col)
            plt.grid(True)
            plt.show()


        print("Outlier Handling...")

        for col in numeric_cols:
            Q1 = self.df[col].quantile(0.25)
            Q2 = self.df[col].quantile(0.75)

            IQR =  Q2 - Q1

            lower = Q1 - 1.5 * IQR
            upper = Q2 + 1.5 * IQR

            self.df[col] = np.where(self.df[col]<lower,lower,self.df[col])
            self.df[col] = np.where(self.df[col]>upper,upper,self.df[col])


    def train_test_split(self):

        self.X = self.df.drop(self.target_column,axis=1)
        self.y = self.df[self.target_column]

        self.X_train,self.X_test,self.y_train,self.y_test = train_test_split(
            self.X,self.y,test_size=self.test_size,random_state=self.random_state
        )

        print("train test split successful")

    def build_pipeline(self):

        print("building pipeline....")

        cat_cols = make_column_selector(dtype_include=object)

        numeric_cols = make_column_selector(dtype_include=np.number)

        transformer = make_column_transformer(
            (OneHotEncoder(handle_unknown="ignore"),cat_cols),
            (StandardScaler(),numeric_cols),
            remainder="passthrough"
        )

        rand_for = DecisionTreeRegressor()
        self.pipeline = make_pipeline(rand_for, transformer)

        print("Pipeline build successful")


    def train_model(self):

        self.pipeline.fit(self.X_train,self.y_train)




