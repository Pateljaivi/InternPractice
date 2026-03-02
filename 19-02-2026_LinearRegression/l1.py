#This can be done through log transformation

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.preprocessing import OneHotEncoder, StandardScaler
#OneHotEncoder -> Categorical data ko numbers me convert karta hai
#standardscaler -> data ko scale karta hai
from sklearn.model_selection import train_test_split #dataset ko train test me split karta hai
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score, mean_squared_error, mean_absolute_error


df = pd.read_csv("insurance.csv")
df.head() #first 5 rows

df.info() #check columns's datatype and null values

df.describe() #give statistical summary of numerical columns(mean,std,min,max)

df.isnull().sum() #check missing values in each column

print("Duplicate rows:",df.duplicated().sum()) #print how many duplicate row exist

df = df.drop_duplicates() #remove duplicate row

print("Duplicate rows:",df.duplicated().sum())

print(df.shape) #give count of rows and columns

#Data visualization

#distribution of charges->histogram,kde(kernel density estimation)->smooth curve jo overall patten show karta hai
plt.figure()
sns.histplot(df["charges"], kde=True)
plt.title("Distribution of Charges")
plt.show()

plt.figure()
sns.heatmap(df.corr(numeric_only=True), annot=True,cmap="coolwarm")
#df.corr() -> dataframe ke columns ke beech correlation calculate karta hai,numeric_only=True-> apply correlation on only numeric columns
#annot = True -> show correlation value inside all boxes
plt.show()

#boxplot of smoker vs charges
plt.figure()
sns.boxplot(x="smoker", y="charges", data=df)
plt.show()

# plt.figure(figsize=(8,5))
# sns.boxplot(x=df["charges"])
# plt.title("Boxplot of Charges")
# plt.show()

print(df.shape)


#Log Transformation


df["charges"] = np.log(df["charges"])

sns.histplot(df["charges"], kde=True)
plt.title("Log Transformed Charges")
plt.show()

#convert categorical to numerical
df = pd.get_dummies(df,drop_first=True)
#suppose we have 2 columns in category so dorp_first -> remove one

print(df.columns)

print(df.shape)


#create new feature
df["bmi_smoker"] = df["bmi"] * df["smoker_yes"]
#smoker + high BMI ->extremely high charges
#Non - smoker + High BMI -> moderate increase
#this not linear relation

#Define X and Y
X = df.drop("charges", axis=1)
y = df["charges"]


#Feature Scaling -> all value lie between -1 to +1
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)


#train test split
X_train, X_test, y_train, y_test = train_test_split(
    X_scaled, y, test_size=0.2, random_state=42
)
#random_state = 42 same result when run


#Model training
model = LinearRegression()
model.fit(X_train, y_train)

#predict on test data
y_pred = model.predict(X_test)

#r2 score-> tell how nicely fit model in range from 0 to 1
r2 = r2_score(y_test, y_pred)
mse = mean_squared_error(y_test, y_pred)
rmse = np.sqrt(mse)
mae = mean_absolute_error(y_test, y_pred)

print("R2 Score:", r2)
print("MSE:", mse)
print("RMSE:", rmse)
print("MAE:", mae)


print(df.shape)

plt.figure()
plt.scatter(y_test,y_pred)
plt.plot([y_test.min(),y_test.max()],[y_test.min(),y_test.max()],color="red")
plt.xlabel("Actual Charges")
plt.ylabel("Predicted Charges")
plt.show()


results = pd.DataFrame({
    "Actual Charges": y_test.values,
    "Predicted Charges": y_pred,
})
results.head(10)



