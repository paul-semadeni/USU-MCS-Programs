"""
    Assignment 4
        Class: Intro to Data Analysis (CS6850)
        Instructor: Dr. Hamid Karimi
        Date: February 24, 2024
        Student: Paul Semadeni
"""
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from math import log, e
from sklearn.preprocessing import MinMaxScaler
from sklearn.decomposition import PCA

# TODO: Apply equal width discretization to produce 5 bins to the "Close" column. Display the first 5 discretized values by using the head() function.
print("\nEqual Width Discretization".upper())
with open("./files/msft.csv") as file:
    stock_prices_df = pd.read_csv(file)
bins = pd.cut(stock_prices_df["Close"], 5)
print(bins.head())
# stock_prices["range"] = pd.cut(stock_prices["Close"], 5, labels=["0-1", "1-2", "2-3", "3-4", "4-5"])

# TODO: Apply equal frequency discretization to produce 5 bins to the "Close" column.
print("\nEqual Frequency Discretization".upper())
quartiles = [0, 0.20, 0.40, 0.60, 0.80, 1]
bins = pd.qcut(stock_prices_df["Close"], quartiles)
print(bins.head())
# stock_prices["range"] = pd.qcut(stock_prices["Close"], quartiles, labels=["0-0.20", "0.20-0.40", "0.40-0.60", "0.60-0.80", "0.80-1"])

# TODO: Implement entropy-based discretization (supervised discretization) and apply it to the vehicles dataset. Implement it using recursion. Come up with a threshold to stop splitting the data. Note that you must perform the discretization separately for each feature (column). Print each feature, its discretized ranges, and the corresponding final entropy.
print("\nEntropy-based Discretization".upper())
def compute_entropy(label):
    # Reference: https://stackoverflow.com/questions/15450192/fastest-way-to-compute-entropy-in-python
    num_rows = len(label)
    values, counts = np.unique(label, return_counts=True)
    probabilities = counts/num_rows

    entropy = 0
    for prob in probabilities:
        entropy -= prob * log(prob, 2)
    return entropy

def entropy_based_discretization(column, col_name):
    inital_column_len = len(column)
    column = column.sort_values(by=[col_name]).reset_index(drop=True)
    # Compute last bin entropy
    last_bin_count = loop_through_columns(column[::-1], 0.001)
    last_bin = column[len(column["class"]) - last_bin_count:len(column["class"])]
    last_range = (column.iat[len(column["class"]) - last_bin_count, 0],column.iat[len(column["class"]) - 1, 0])
    last_bin_entropy = compute_entropy(last_bin["class"])
    # Update column values
    column = column[:len(column["class"]) - last_bin_count]
    # Compute first bin entropy
    first_bin_count = loop_through_columns(column, 0.001)
    first_bin = column[:first_bin_count]
    first_range = (column.iat[0, 0],column.iat[first_bin_count - 1, 0])
    first_bin_entropy = compute_entropy(first_bin["class"])
    # Update column values
    column = column[first_bin_count:]
    final_len_column = len(column)
    final_entropy = compute_entropy(column["class"])
    # final_range = (column.iat[0, 0],column.iat[len(column["class"]) - 1, 0])
    # Calculate ET = first_bin * E1 + column * E2 + last_bin * E3
    ET = ((first_bin_count/inital_column_len) * first_bin_entropy) + ((final_len_column/inital_column_len) * final_entropy) + ((last_bin_count/inital_column_len) * last_bin_entropy)
    print(f"{col_name}: \n\t{first_range},{(first_range[1], last_range[0])},{last_range}\n\t", ET)
    return

def loop_through_columns(columns, threshold=0.05):
    column = columns["class"]
    # This algorithm makes sure that he threshold % of the opposite value is included in the bin
    a_count = 0
    a_included = False
    b_count = 0
    b_included = False
    col_value = 0
    for c in column:
        if c == 0:
            a_count += 1
            a_included = True
        else:
            b_count += 1
            b_included = True
        a_logic = (((a_count / (a_count + b_count)) < threshold) and b_included)
        b_logic = (((b_count / (a_count + b_count)) < threshold) and a_included)
        # Check the threshold
        if a_logic != b_logic:
            continue
        else:
            # Threshold has been met but need to get rest of matching values
            col_value = columns.iat[a_count + b_count, 0]
            if a_count + b_count + 1 < len(column):
                next_col_value = columns.iat[a_count + b_count + 1, 0]
                if next_col_value != col_value:
                    break
            else:
                break
    return a_count + b_count + 1

with open("./files/vehicles.csv") as file:
    vehicles_df = pd.read_csv(file)
vehicles_df = vehicles_df[((vehicles_df["class"] == "van") | (vehicles_df["class"] == "bus"))]
vehicles_df["class"] = vehicles_df["class"].replace(["van"],0)
vehicles_df["class"] = vehicles_df["class"].replace(["bus"],1)

for col in vehicles_df:
    col_name = str(col)
    if col_name != "class":
        entropy_based_discretization(vehicles_df[[col_name, "class"]], col_name)

# TODO: Compute the Mean Absolute Deviation of features (columns) as well correlation matrix of vehicles dataset. Based on the mean absolute deviation, what are the best features? Also, according to the correlation matrix, choose a few features that can/should be removed.
print("\nMean Absolute Deviation".upper())
with open("./files/vehicles.csv") as file:
    vehicles_df = pd.read_csv(file)
for col in vehicles_df:
    col_name = str(col)
    if col_name != "class":
        abs_val_sum = 0
        num_elements = len(vehicles_df[col_name])
        mean = vehicles_df[col_name].mean()
        for row in vehicles_df[col_name]:
            abs_val_sum += abs(row - mean)
        mad = round(abs_val_sum/num_elements, 1)
        print(f"{col_name} mean absolute deviation: ", mad)
print("\nCorrelation Matrix".upper())
print(vehicles_df.drop(columns=["class"]).corr())

# TODO: Apply PCA to vehicles dataset. You can use PCA from sklearn or calculate PCs from eigenvectors of the covariance matrix as described in the lecture.
def generate_pc(columns):
    scaler = MinMaxScaler()
    data_rescaled = scaler.fit_transform(columns.to_numpy())

    pca = PCA().fit(data_rescaled)
    plt.rcParams["figure.figsize"] = (12,6)

    fig, ax = plt.subplots()
    xi = np.arange(1, 19, step=1)
    y = np.cumsum(pca.explained_variance_ratio_)

    plt.ylim(0.0,1.1)
    plt.plot(xi, y, marker="o", linestyle="--", color="b")

    plt.xlabel("Number of Components")
    plt.xticks(np.arange(0, 19, step=1))
    plt.ylabel("Cumulative variance (%)")
    plt.title("The number of components needed to explain variance")

    plt.axhline(y=0.99, color="r", linestyle="-")
    plt.text(0.5, 0.85, "99% cut-off threshold", color="red", fontsize=16)

    ax.grid(axis="x")
    plt.show()
    return

def generate_pc_2(columns):
    num_components = 2
    cov = columns.cov().to_numpy()
    A = columns.to_numpy()
    [eigvals, pcs] = np.linalg.eig(cov)
    sorted_index = np.argsort(eigvals)[::-1]
    eigvals = eigvals[sorted_index]
    pcs = pcs[:,sorted_index]
    M = (A-np.mean(A.T, axis = 1)).T
    projected = np.dot(pcs.T, M).T
    projected = pd.DataFrame(projected[:,:num_components], columns=["pc1", "pc2"])
    projected.plot(kind="scatter", x="pc1", y="pc2")
    plt.show()

    # fig, axes = plt.subplots(2, 1, sharex=True)
    # attribute = list(columns)
    # pcdata = pd.Series(pcs[:,1], index=attribute)
    # pcdata.plot(kind="barh", ax=axes[1], color="k", alpha=0.7)
    # axes[0].set_title(r"1st PC", size="x-large")
    # pcdata = pd.Series(pcs[:,1], index=attribute)
    # pcdata.plot(kind="barh", ax=axes[1], color="k", alpha=0.7)
    # axes[0].set_title(r"2nd PC", size="x-large")
    return

print("\nPrincipal Component Analysis (PCA)".upper())
generate_pc(vehicles_df.drop(columns=["class"]))
generate_pc_2(vehicles_df.drop(columns=["class"]))