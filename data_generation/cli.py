import typer
import os

from main import GenerateData

def main(dstype: str):
    """
    Perform actions based on the specified data source type.

    Allowed types are: mssql, postgres, mongodb, redis, all

    Args:
        dstype: The type of the data source.
    """

    if dstype == "mssql":
        print(GenerateData.load_data(ds_type="mssql"))
    elif dstype == "postgres":
        print(GenerateData.load_data(ds_type="postgres"))
    elif dstype == "mongodb":
        print(GenerateData.load_data(ds_type="mongodb"))
    elif dstype == "redis":
        GenerateData.load_data(ds_type="redis")
    elif dstype == "all":
        GenerateData.load_data(ds_type="mssql")
        GenerateData.load_data(ds_type="postgres")
        GenerateData.load_data(ds_type="mongodb")
        GenerateData.load_data(ds_type="redis")

if __name__ == "__main__":
    main("all")
    # main("mssql")