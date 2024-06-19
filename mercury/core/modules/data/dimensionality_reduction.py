import pandas as pd
from sklearn.preprocessing import StandardScaler
from umap import UMAP


def standardize_data(data: pd.DataFrame) -> pd.DataFrame:
    """
    Standardizes the numerical data using StandardScaler.

    Parameters:
    - data (pd.DataFrame): The data to be standardized.

    Returns:
    - pd.DataFrame: The standardized data.
    """
    scaler = StandardScaler()
    return scaler.fit_transform(data)


def perform_umap(data: pd.DataFrame, n_neighbors: int) -> pd.DataFrame:
    """
    Performs UMAP dimensionality reduction on the given data.

    Parameters:
    - data (pd.DataFrame): The data to perform UMAP on.
    - n_neighbors (int): The number of neighbors to consider for each point in UMAP.

    Returns:
    - pd.DataFrame: The 2D embedding of the data after UMAP reduction.
    """
    umap_model = UMAP(n_components=2, n_neighbors=n_neighbors)
    umap_result = umap_model.fit_transform(data)
    return pd.DataFrame(umap_result, columns=["UMAP_1", "UMAP_2"])
