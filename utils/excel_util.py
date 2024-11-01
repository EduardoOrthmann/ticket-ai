import pandas as pd
from pandas import DataFrame


class ExcelUtil:
    def __init__(self, file_path: str) -> None:
        self.__data = self.limit_data(self._load_file(file_path))

    def _load_file(self, file_path: str) -> DataFrame:
        return pd.read_excel(file_path)

    def get_data(self) -> DataFrame:
        return self.__data

    def limit_data(self, data: DataFrame) -> DataFrame:
        return data[30:]

    def get_clean_data(self, data: DataFrame) -> DataFrame:
        return data.drop(columns=[
            'Priority',
            'Brief Description',
            'Assignment',
            'Description',
            'Dicas',
            'Unnamed: 0',
            'Unnamed: 1',
            'Unnamed: 2',
            'Unnamed: 3',
            'Unnamed: 4',
            'Category 1',
            'Category 2',
            'Category 3',
            'Category 4'
        ])

    def get_static_data(self) -> dict:
        static_data = {}

        for index, row in self.__data.iterrows():
            static_data[row['Cause Code Alteração']] = {
                'Priority': str(row['Priority']),
                'Brief Description': row['Brief Description'],
                'Assignment': row['Assignment']
            }

        return static_data

    def get_data_by_cause_code(self, cause_code: str) -> dict:
        return self.get_static_data().get(cause_code)
