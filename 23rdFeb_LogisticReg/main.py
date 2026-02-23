import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score,confusion_matrix, classification_report
from sklearn.preprocessing import StandardScaler, OneHotEncoder, LabelEncoder
from scipy import stats


#Load dataset
df = pd.read_csv("train.csv")
print(df.head())
#
print(df.shape)
#
# #basic info
print(df.info())
print(df.describe())
print(df.isnull().sum()) # education -> 2409 and previous_year_rating ->  4124 missing values

#andling missing values

df["education"] = df["education"].fillna(df["education"].mode()[0])
#mode->jo value sabse zyada bar ati hai
#inplace=true -> means operation direct original dataframe par apply karo,not return new dataframe

df["previous_year_rating"] = df["previous_year_rating"].fillna(df["previous_year_rating"].median)
#previous_year_rating ka median nikalke missing value me de denge

print(df.isnull().sum()) #rechech for missing values
print(df.columns)
print(df.columns.tolist())


#Drop Unnecessary Column
df = df.drop("employee_id",axis=1)
print(df.columns.tolist())


#Taget variable check
sns.countplot(x="is_promoted",data=df)
plt.show()

print(df["is_promoted"].value_counts())#for printing exact count
#50140-> 0(not promoted) and  4668 -> 1(promoted)

print(df["is_promoted"].value_counts(normalize=True))#for showing percentage


#Checking outlier in numeric columns
num_cols = ["age","length_of_service","avg_training_score"]

for col in num_cols:
    plt.figure()
    sns.boxplot(x=df[col])
    plt.title(col)
    plt.show()


#Log transformation on length_of_service beacuse it has outlier
df["length_of_service"] = np.log1p(df["length_of_service"])


plt.figure()
sns.boxplot(x=df["length_of_service"])
plt.title("Log transform of length_of_service")
plt.show()


#Separate Features and Target
X = df.drop("is_promoted",axis=1)
y = df["is_promoted"]

#label encoding for education(ordinal column)
# LabelEncoder cannot handle NaNs. Fill them first!
X["education"] = X["education"].fillna("Unknown").astype(str)
le = LabelEncoder()
X["education"] = le.fit_transform(X["education"])


#OneHotEncoding for remaining categorical columns->department,region,gender,recruitment_channel
cat_cols = X.select_dtypes(include=["object", "string"]).columns


# Fill NaNs and force to string to prevent 'float' vs 'method' errors
X[cat_cols] = X[cat_cols].fillna("Missing").astype(str)

encoder = OneHotEncoder(drop="first", sparse_output=False, handle_unknown="ignore")
encoded = encoder.fit_transform(X[cat_cols])


# Using get_feature_names_out makes the columns readable (e.g., 'gender_Male')
encoded_df = pd.DataFrame(encoded, columns=encoder.get_feature_names_out(cat_cols))


X = X.drop(cat_cols, axis=1)
X = pd.concat([X.reset_index(drop=True), encoded_df.reset_index(drop=True)], axis=1)

# print("Encoding successful! New shape:", X.shape)


#Train-Test Split
X_train, X_test, y_train, y_test = train_test_split(X,y,test_size=0.2,random_state=42)


scaler = StandardScaler()
X_train = scaler.fit_transform(X_train)
X_test = scaler.transform(X_test)

#Logistic regression model
model = LogisticRegression(max_iter=1000,class_weight="balanced")
model.fit(X_train,y_train)

#Prediction
y_pred = model.predict(X_test)


#Accuracy and Evaluation

print("Accuracy:",accuracy_score(y_test,y_pred))

print("\nConfusion Matrix:\n",confusion_matrix(y_test,y_pred))

print("\nClassification Report:\n",classification_report(y_test,y_pred))
