import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.metrics import accuracy_score, classification_report, mean_squared_error
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.tree import DecisionTreeClassifier, DecisionTreeRegressor
from sklearn.tree import plot_tree
from sklearn.metrics import r2_score, mean_squared_error

#Load dataset
df = pd.read_csv("Salary_Data.csv")
print("first 5 Rows:")
# print(df.head())

print("\nShape of Dataset:",df.shape)

#Basic Information
print("\nDataset Info:")
print(df.info())

print("\nStatistical Summary:")
print(df.describe())


#Check missing values
print("\nMissing Values:")
print(df.isnull().sum())


# Duplicate Check
duplicates = df.duplicated().sum()
print("\nDuplicate Rows:",duplicates)


#Remove duplicates
df = df.drop_duplicates()
print("Shape after removing duplicates:",df.shape)


#Remove completely Empty rows
empty_rows = df.isnull().all(axis=1).sum()
print(f"\nNumber of empty rows:{empty_rows}")
df = df.dropna(how="all")
print("Shape after dropping completely empty rows:",df.shape)


#check missing value after remove empty rows
print("\nMissing Values:")
print(df.isnull().sum())

#Outlier Detection

""" Decision Tree Regression me target continuous numeric value hota hai,aur label encoding sirt categorical labels ko numbers me covert karne ke liye use hoti hai -> traget"""

#outlier detection
numeric_cols = df.select_dtypes(include="number").columns.drop("Salary")

for col in numeric_cols:
    plt.figure(figsize=(6,4))
    plt.boxplot(df[col],vert=False)
    plt.title(f"Boxplot for {col}")
    plt.show()


#no outlier in age &  years_of_experience


#Separate Features & Target
X = df.drop("Salary",axis=1)
y = df["Salary"]

#Identify categorical and numerical columns
categorical_cols = X.select_dtypes(include=["object","string"]).columns.tolist()
print(f"\ncategorical columns:{categorical_cols}")
numerical_cols = X.select_dtypes(include="number").columns.tolist()
print(f"\nnumerical columns:{numerical_cols}")

label_encoder = {}
for col in categorical_cols:
    le = LabelEncoder()
    X[col] = le.fit_transform(X[col])
    label_encoder[col] = le


#Train Test Split
X_train,X_test,y_train,y_test = train_test_split(X,y,test_size=0.2,random_state=7)


#Decison Tree Regression
dt = DecisionTreeRegressor(
    criterion="squared_error",
    max_depth=6,
    min_samples_split=5,
    min_samples_leaf=3,
    random_state=42
)
dt.fit(X_train,y_train)

#Prediction And Evaluation
y_pred = dt.predict(X_test)

print("\nR2 score:",r2_score(y_test,y_pred))
print("Mean Squared Error:",mean_squared_error(y_test,y_pred))

plt.figure(figsize=(20,10))
plot_tree(
    dt,
    feature_names = X.columns,
    filled=True,
    fontsize=10
)
plt.show()