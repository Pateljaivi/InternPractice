# -----------------------------------
# ---------Crop recommendation--------
#---Decision Tree Classifier-----

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.metrics import accuracy_score, classification_report, ConfusionMatrixDisplay
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.tree import DecisionTreeClassifier
from sklearn.tree import plot_tree
from sklearn.metrics import confusion_matrix

#Load dataset
df = pd.read_csv("Crop_recommendation.csv")
print("first 5 Rows:")
print(df.head())

print("\nShape of Dataset:",df.shape)

#Basic Information
print("\nDataset Info:")
print(df.info())

print("\nStatistical Summary:")
print(df.describe())


#Check missing values
print("\nMissing Values:")
print(df.isnull().sum())

#target class distribution
print("\nClass distribution:\n",df["label"].value_counts())


# Duplicate Check
duplicates = df.duplicated().sum()
print("\nDuplicate Rows:",duplicates)


#Outlier Detection
print("\nShowing Boxplots for Outlier Detection...")
plt.figure(figsize=(14,6))

for i,col in enumerate(df.columns[:-1],1): #exclude label column -> because it is target column
    plt.subplot(2,4,i) #2 rows,4 column's grid create,total 8 graphs
    sns.boxplot(y=df[col])
    plt.title(col)#column's name show in title
plt.tight_layout() #graphs don't overlap
plt.show()


"""linear regression,svm,knn -> use distance,so outlier may disturb the model ,necessary to remove it 

  decision tree -> it can do threshold based split -> extreme value(outlier) goes to one branch ,it not disturbing to model
"""

#outlier Handling(inter quartile range) -> P, K temperature,ph,rainfall

cols_to_clean = ["P", "K" ,"temperature","ph","rainfall"]
print("\nShape Before Outlier Handling:",df.shape)

for col in cols_to_clean:
    Q1 = df[col].quantile(0.25)#25%
    Q3 = df[col].quantile(0.75)#75%

    IQR = Q3 - Q1 #tells middle 50% data spread

    lower = Q1 - 1.5*IQR
    upper = Q3 + 1.5*IQR

    # df = df[(df[col] >= lower) & (df[col] <= upper)] ->previous to do this many rows delete accuracy 0.48

    #capping(no row deletion)
    df[col] = np.where(df[col] < lower,lower,df[col]) #agar value lower se chhoti hai to use lower bana diya
    df[col] = np.where(df[col] > upper,upper,df[col]) #agar value upper se badi hai to use badi bana diya


print("Shape After Outlier Handling:",df.shape)



#Feature and target split
X = df.drop("label",axis=1)
y = df["label"]

#Encode Target
le = LabelEncoder()
y = le.fit_transform(y)

#Train-Test Split
X_train,X_test,y_train,y_test = train_test_split(X,y,test_size=0.2,random_state=7)

#Decision Tree Model
dt = DecisionTreeClassifier(
    criterion="gini",#decision tree's impurity measure
    max_depth=8,#tree's deepness
    min_samples_split=5,#to split node minimum 5 samples // default->2
    min_samples_leaf=3,#in leaf node minimum 3 sample // default -> 1
    random_state=42
)

dt.fit(X_train,y_train)

#Prediction
y_pred = dt.predict(X_test)

#Evaluation
print("\nModel Accuracy:",accuracy_score(y_test,y_pred))
print("\nClassification Report:\n",classification_report(y_test,y_pred))

print("Train:",dt.score(X_train,y_train))
print("Test:",dt.score(X_test,y_test))

cm = confusion_matrix(y_test,y_pred)
# print("\nConfusion Matrix:\n",cm)

disp = ConfusionMatrixDisplay(confusion_matrix=cm, display_labels=dt.classes_)

plt.figure(figsize=(10,8))
disp.plot(xticks_rotation=90)
plt.title("Confusion Matrix")
plt.show()

plt.figure(figsize=(15,8))
plot_tree(
    dt,
    feature_names=X.columns,
    filled=True,
)
plt.show()
