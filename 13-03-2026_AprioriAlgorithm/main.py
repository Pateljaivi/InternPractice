"""
   Implement Apriori Algorithm

   Dataset : basket_analysis.csv
"""

import pandas as pd
import matplotlib.pyplot as plt
from mlxtend.frequent_patterns import apriori,association_rules




class AprioriAlgorithm:

    """
        A class to perform Market Basket Analysis using the Apriori Algorithm
    """

    def __init__(self,file_path,min_support=0.05,min_threshold=1):
        self.file_path = file_path
        self.min_support = min_support
        self.min_threshold = min_threshold

        self.frequent_itemsets = None


        self.df = None
        self.rules = None


    def load_data(self):

        """
           Reads the dataset from the CSV file into a pandas DataFrame
        """
        try:
            print("Loading data...")
            self.df = pd.read_csv(self.file_path)
            print("Dataset Loaded successfully...")
            print("Shape of the dataset:", self.df.shape)
        except Exception as e:
            print(f"Error while loading the dataset:{e}")


    def preprocess_data(self):

        """
             Cleans the dataset by removing unnecessary columns and checking for
             missing values or duplicates.
        """

        self.load_data()

        try:
            print("Preprocessing data...")

            print("Removing unnecessary column...")
            #remove unnecessary column->unnamed
            if "Unnamed: 0" in self.df.columns:
                self.df.drop(columns=["Unnamed: 0"],inplace=True)


            print("Shape of the dataset:", self.df.shape)
            print("First 5 rows of the dataset:\n", self.df.head(5))
            print("Check Missing value:\n",self.df.isnull().sum())
            print("Duplicate value:",self.df.duplicated().sum())

        except Exception as e:
            print(f"Error while preprocessing data:{e}")


    def apply_apriori(self):

        """
                Runs the Apriori algorithm to identify sets of items that appear
                frequently together based on the min_support threshold.
        """

        self.preprocess_data()

        try:
            print("Applying apriori algorithm...")

            self.frequent_itemsets = apriori(
                self.df,
                min_support=self.min_support,
                use_colnames=True
            )

            print("Frequent Itemsets:\n")
            print(self.frequent_itemsets.head())

        except Exception as e:
            print(f"Error while applying apriori algorithm:{e}")


    def plot_all_items(self):

        """
              Filters the frequent itemsets for individual items and creates a
              bar chart to visualize their frequency (support)
        """


        self.apply_apriori()

        try:
            print("Visualizing all item freqencies...")

            single_items = self.frequent_itemsets[
                self.frequent_itemsets["itemsets"].apply(lambda x: len(x) == 1)
            ]

            single_items["items"] = single_items["itemsets"].apply(lambda x: list(x)[0])

            plt.figure()

            plt.bar(single_items["items"], single_items["support"])

            plt.xticks(rotation=45)

            plt.xlabel("Items")
            plt.ylabel("Support(Frequency)")

            plt.title("Frequency of all items")

            plt.tight_layout()
            plt.show()

        except Exception as e:
            print(f"Error while plotting all items:{e}")



    def generate_rules(self):

        """
               Generates association rules (If-Then relationships) from the frequent
               itemsets using 'lift' as the primary quality metric
        """

        self.plot_all_items()

        try:
            print("Generating Association rules...")

            self.rules = association_rules(
                self.frequent_itemsets,
                metric = "lift",# This tells the code how to judge if a rule is "good"
                #Lift is a measure of how much more likely the items are to be bought together than they would be
                # by pure random chance
                # Lift = 1 means the items are completely independent (no relationship)
                # Lift > 1 means the items have a positive relationship (they "belong" together)
                min_threshold =  self.min_threshold #qaulity filter -> sets the minimum score required to keep a rule
            )

            print(self.rules)

        except Exception as e:
            print(f"Error while generating association rules:{e}")


    def find_best_rule(self):

        """
            Identifies and prints the single strongest rule by sorting the
            generated rules by highest Lift and Confidence
        """

        self.generate_rules()

        try:
            print("Finding best association rule...")

            #highest lift rule

            best_rule = self.rules.sort_values(["lift","confidence"], ascending = False).iloc[0]

            antecedent = list(best_rule["antecedents"])
            consequent = list(best_rule["consequents"])

            print("Best Rule Found:\n")

            print(f"If a customer buys {antecedent}")
            print(f"Then they are most likely to buy {consequent}")

            print("\nRule Metrics:")

            print("Support:",round(best_rule["support"],3))

            print("Confidence:",round(best_rule["confidence"],3))

            print("Lift:",round(best_rule["lift"],3))

        except Exception as e:
            print(f"Error while finding best rule:{e}")


def main():

    """
       Entry point of the script. Sets the data path and runs the algorithm.
    """

    DATA_PATH = "basket_analysis.csv"

    model = AprioriAlgorithm(DATA_PATH)

    model.find_best_rule()

if __name__ == "__main__":
    main()