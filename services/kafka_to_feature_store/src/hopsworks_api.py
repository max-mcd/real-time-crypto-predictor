import hopsworks
import pandas as pd

from src.config import config


def push_data_to_feature_store(
    feature_group_name: str,
    feature_group_version: int,
    data: dict,
) -> None:
    """
    Write the given "data" to the feature group specified by a name and a version.

    Args:
        feature_group_name (str): Name of the feature group to write data to
        feature_group_version (int): Version of the feature group to write data to
        data (dict): Data to write to the feature group

    Returns:
        None
    """

    # Create a connection to Hopsworks
    project = hopsworks.login(
        project=config.hopsworks_project_name,
        api_key_value=config.hopsworks_api_key,
    )

    # Get the feature store
    fs = project.get_feature_store()

    # Get or create the feature group for ohlc data
    ohlc_feature_group = fs.get_or_create_feature_group(
        name=config.feature_group_name,
        version=config.feature_group_version,
        description="OHLC data from Kraken",
        primary_key=["product_id", "timestamp"],
        event_time="timestamp",
        online_enabled=True,  # Enable online feature serving
    )

    # Transform JSON data into a DataFrame
    data = pd.DataFrame([data])

    # Insert data into feature group
    # Set start_offline_materialization to avoid starting the materialization 
    # job to write data to the offline storage
    ohlc_feature_group.insert(data, write_options={"start_offline_materialization": False})
