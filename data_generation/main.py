import os
import json
import random
import pandas as pd

from datetime import datetime
from objects import mssql_users, mongodb_users, rides, vehicle

import numpy as np
from pycpfcnpj import gen

mssql_users = mssql_users.Users()
mongodb_users = mongodb_users.Users()
rides = rides.Rides()
vehicle = vehicle.Vehicle()

class Features(object):
    """
    A class that provides methods for generating user IDs and timestamps.
    """

    @staticmethod
    def gen_user_id():
        """
        Generate a random user ID.

        Returns:
            numpy.ndarray: An array of random user IDs.
        """

        return np.random.randint(1, 10000, size=100)

    @staticmethod
    def gen_cpf():
        """
        Generate a cpf number.

        Returns:
            str: A formatted cpf string.
        """

        return gen.cpf_with_punctuation()

    @staticmethod
    def gen_timestamp():
        """
        Generate a formatted timestamp.

        Returns:
            str: A formatted timestamp string.
        """

        current_datetime = datetime.now()
        return current_datetime.strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]

class GenerateData(object):
    """
    This class is used to write data into the landing zone
    """

    def __init__(self):
        self.add = ""

    @staticmethod
    def create_dataframe(dt, file_name, ds_type, is_cpf=False):
        """
        Create a dataframe based on the provided data and data source type.

        Args:
            dt: The data to create the dataframe from.
            ds_type: The type of the data source.
            is_cpf: Whether generates a cpf.

        Returns:
            tuple: A tuple containing the JSON-encoded dataframe and the data source type.
        """

        if ds_type == "redis":
            pd_df = pd.DataFrame(dt)
        else:
            pd_df = pd.DataFrame(dt)
            pd_df['user_id'] = Features.gen_user_id()
            pd_df['dt_current_timestamp'] = Features.gen_timestamp()

            if is_cpf:
                pd_df['cpf'] = is_cpf

        json_data = pd_df.to_json(orient="records")

        with open(file_name, 'w', encoding='utf-8') as f:
            f.write(json_data)

        return json_data.encode('utf-8'), ds_type

    @staticmethod
    def write_file(dir_path, data_content, ds_type):
        """
        Write files based on the specified data source type.

        Args:
            dir_path: Path where the file will be saved
            data_content: Has the dataframe content based on a specif feature
            ds_type: The type of the data source.
        """

        year, month, day, hour, minute, second = (
            datetime.now().strftime("%Y %m %d %H %M %S").split()
        )

        os.makedirs(dir_path, exist_ok=True)
        timestamp = f'{year}_{month}_{day}_{hour}_{minute}_{second}.json'
        user_file_name = os.path.join(dir_path, timestamp)

        gen_cpf = Features.gen_cpf()
        GenerateData.create_dataframe(data_content, user_file_name, ds_type, is_cpf=gen_cpf)
        
        return print(f"File saved on {user_file_name.replace("\\", "/")}")

    @staticmethod
    def load_data(ds_type: str):
        """
        Load data based on the specified feature.

        Args:
            ds_type: The type of the data source.
        """
    
        if ds_type == "mssql":
            dt_mssql_users = mssql_users.get_multiple_rows(gen_dt_rows=10**2)

            dir_path = f"./files/{ds_type}/users"
            GenerateData.write_file(dir_path= dir_path, data_content= dt_mssql_users, ds_type= ds_type)            
        
        elif ds_type== "postgres":
            dt_vehicle = vehicle.get_multiple_rows(gen_dt_rows=10**2)

            dir_path = f"./files/{ds_type}/vehicle"
            GenerateData.write_file(dir_path= dir_path, data_content= dt_vehicle, ds_type= ds_type)
        
        elif ds_type == "mongodb":

            dt_rides = rides.get_multiple_rows(gen_dt_rows=10**2)

            dir_path = f"./files/{ds_type}/rides"
            GenerateData.write_file(dir_path= dir_path, data_content= dt_rides, ds_type= ds_type)

            dt_mongodb_users = mongodb_users.get_multiple_rows(gen_dt_rows=10**2)
            dir_path = f"./files/{ds_type}/users"
            GenerateData.write_file(dir_path= dir_path, data_content= dt_mongodb_users, ds_type= ds_type)

        return None