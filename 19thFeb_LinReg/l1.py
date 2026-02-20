#This can be done through log transformation

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.compose import ColumnTransformer
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score, mean_squared_error, mean_absolute_error


df = pd.read_csv("insurance.csv")
df.head()

df.info()

df.describe()

df.isnull().sum()

print("Duplicate rows:",df.duplicated().sum())

df = df.drop_duplicates()

print("Duplicate rows:",df.duplicated().sum())

print(df.shape)

plt.figure()
sns.histplot(df["charges"], kde=True)
plt.title("Distribution of Charges")
plt.show()

plt.figure()
sns.heatmap(df.corr(numeric_only=True), annot=True,cmap="coolwarm")
plt.show()

plt.figure()
sns.boxplot(x="smoker", y="charges", data=df)
plt.show()

plt.figure(figsize=(8,5))
sns.boxplot(x=df["charges"])
plt.title("Boxplot of Charges")
plt.show()

print(df.shape)

df["charges"] = np.log(df["charges"])

sns.histplot(df["charges"], kde=True)
plt.title("Log Transformed Charges")
plt.show()

df = pd.get_dummies(df,drop_first=True)

print(df.columns)

print(df.shape)

df["bmi_smoker"] = df["bmi"] * df["smoker_yes"]
#smoker + high BMI ->extremely high charges
#Non - smoker + High BMI -> moderate increase
#this not linear relation

X = df.drop("charges", axis=1)
y = df["charges"]

scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

X_train, X_test, y_train, y_test = train_test_split(
    X_scaled, y, test_size=0.2, random_state=42
)

model = LinearRegression()
model.fit(X_train, y_train)

y_pred = model.predict(X_test)

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



