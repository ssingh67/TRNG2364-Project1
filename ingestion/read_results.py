# Testing to see if we can read the data
import pandas as pd


try:
    results_df = pd.read_csv("./datasets/results.csv")

    print(f"\nResults DataFrame:\n{results_df.info()}")

except FileNotFoundError:
    print("File Not Found.")