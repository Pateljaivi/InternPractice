"""Implement K-Means Clustering on penguins dataset"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans

from sklearn.compose import make_column_selector,make_column_transformer
from sklearn.decomposition import PCA
from sklearn.metrics import silhouette_score
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler,OneHotEncoder



class PenguinsClustering:
    def __init__(self,file_path):
        self.file_path = file_path
        self.df = None
        self.pipeline = None

    def load_data(self):

        """Loading dataset"""

        try:
            print("Loading data...")

            self.df = pd.read_csv(self.file_path)

            print("Dataset loaded successfully")

            print(self.df.head())

        except Exception as e:

            print(f"Error loading data: {e}")


    def preprocess_data(self):

            """Preprocessing dataset: Cleaning, Missing Values, and Outlier Removal"""


            self.load_data()

            print("\nStarting Preprocessing...")
            try:

                print("Before Handling Missing Values:\n", self.df.isnull().sum())


                numeric_cols = self.df.select_dtypes(include=np.number).columns
                cat_cols = self.df.select_dtypes(include=["object", "string"]).columns

                # NaN -> Meadian
                for col in numeric_cols:
                    self.df[col] = self.df[col].fillna(self.df[col].median())

                # Categorical -> the most frequent value
                for col in cat_cols:
                    if not self.df[col].mode().empty:
                        self.df[col] = self.df[col].fillna(self.df[col].mode()[0])

                print("Outlier Detection...")
                for col in numeric_cols:
                     plt.figure(figsize=(6,4))
                     plt.boxplot(self.df[col])
                     plt.title(f"Box Plot of {col}")
                     plt.xlabel(col)
                     plt.grid(True)
                     plt.show()


                print("Removing extreme outliers (negative value and Outlier 5000mm)...")
                initial_shape = self.df.shape[0]

                # Keep only realistic flipper lengths
                self.df = self.df[(self.df['flipper_length_mm'] > 150) & (self.df['flipper_length_mm'] < 300)]

                rows_removed = initial_shape - self.df.shape[0]
                print(f"Outliers removed: {rows_removed} rows deleted.")


                print("Checking for duplicates...")
                print("Duplicate Values:", self.df.duplicated().sum())
                self.df = self.df.drop_duplicates()

                print("After Removing Duplicate Values:", self.df.duplicated().sum())



                print("\nFinal Missing Value Check:\n", self.df.isnull().sum())
                print(f"Final Dataset Shape: {self.df.shape}")

                print("Generating Box Plots for confirmation...")
                for col in numeric_cols:
                    plt.figure(figsize=(6, 4))
                    plt.boxplot(self.df[col])
                    plt.title(f"Box Plot of {col}")
                    plt.xlabel(col)
                    plt.grid(True)
                    plt.show()

            except Exception as e:
                print(f"Error during preprocessing data: {e}")

    def basic_info(self):

        self.preprocess_data()

        try:
            print("Shape of the dataset:",self.df.shape)

            print("Statistical Summary of the dataset:\n",self.df.describe())

            print("Information of the dataset:\n")

            self.df.info()
        except Exception as e:
            print(f"Error during basic info: {e}")

    def build_pipeline(self):

        self.basic_info()

        try:
            print("Building pipeline...")

            cat_cols = make_column_selector(dtype_include=object)
            num_cols = make_column_selector(dtype_include=np.number)

            transformer = make_column_transformer(
                (OneHotEncoder(handle_unknown='ignore'), cat_cols),
                (StandardScaler(), num_cols),
                remainder="passthrough"
            )

            kmeans = KMeans(n_clusters=3,random_state=42)

            self.pipeline = make_pipeline(transformer, kmeans)

            print("Pipeline built successfully")

        except Exception as e:
            print(f"Error during building pipeline: {e}")

    def train_model(self):

        self.build_pipeline()

        try:
            print("Training model...")
            self.pipeline.fit(self.df)

            print("Train model successfully")
        except Exception as e:
            print(f"Error during training model: {e}")

    def evaluate_model(self):

        self.train_model()

        try:
            print("Evaluating model...")

            X_transformed = self.pipeline[:-1].transform(self.df)

            clusters = self.pipeline[-1].predict(X_transformed)

            score = silhouette_score(X_transformed,clusters)

            print(f"Silhouette score is: {score:.4f}")
        except Exception as e:
            print(f"Error during evaluating model: {e}")

    def elbow_method(self):

        self.evaluate_model()

        try:
            print("Running Elbow Method...")

            cat_cols = make_column_selector(dtype_include=["object", "string"])
            num_cols = make_column_selector(dtype_include=np.number)

            transformer = make_column_transformer(
                (OneHotEncoder(handle_unknown='ignore'), cat_cols),
                (StandardScaler(), num_cols),
                remainder="passthrough"
            )

            X_transformed = transformer.fit_transform(self.df)

            wcss = [] #Within-Cluster Sum of Squares (Inertia)
            k_range = range(1,11)

            for i in k_range:
                kmeans = KMeans(n_clusters=i,init='k-means++',random_state=42)
                kmeans.fit(X_transformed)
                wcss.append(kmeans.inertia_)

            plt.figure(figsize=(8, 5))
            plt.plot(k_range, wcss, marker='o', linestyle='--')
            plt.xlabel("Number of clusters (k)")
            plt.ylabel("WCSS (Inertia)")
            plt.title("Elbow Method for Optimal k")
            plt.grid(True)
            plt.show()

        except Exception as e:
            print(f"Error during elbow method: {e}")

    def visualize_clustering(self):



        self.elbow_method()

        try:
            print("Visualizing clusters...")
            df_for_transform = self.df.drop(columns=['Cluster_Label'], errors='ignore')

            X_transformed = self.pipeline[:-1].transform(df_for_transform)
            clusters = self.pipeline[-1].predict(X_transformed)

            self.df['Cluster_Label'] = clusters

            pca = PCA(n_components=2)
            x_pca = pca.fit_transform(X_transformed)

            plt.figure(figsize=(8,6))

            scatter = plt.scatter(x_pca[:,0],x_pca[:,1],c=clusters, cmap='viridis', s=60, edgecolors='white', alpha=0.8)

            plt.legend(*scatter.legend_elements(),title="Penguin Clusters",loc='upper right')
            plt.title("K-Means Cluster Visualization")
            plt.xlabel("PCA Components 1(General Size/Weight)")
            plt.ylabel("PCA Components 2(Bill Dimensions)")
            plt.grid(True,linestyle='--',alpha=0.5)
            plt.show()

            print("\n Statistical Profile of Each Cluster...")

            print(self.df.groupby('Cluster_Label').mean(numeric_only=True))


        except Exception as e:
            print(f"Error during visualizing clusters: {e}")



def main():

    DATA_PATH = "penguins.csv"

    model = PenguinsClustering(DATA_PATH)

    model.visualize_clustering()

if __name__ == "__main__":
    main()

