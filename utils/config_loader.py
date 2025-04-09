import configparser
from dataclasses import dataclass

@dataclass
class Config:
    datetime: str
    students_csv: str
    schools_csv: str
    output_path: str
    api_key: str

def load_config_ini(path: str) -> Config:
    parser = configparser.ConfigParser()
    parser.read(path)

    return Config(
        datetime=parser['GENERAL']['datetime'],
        students_csv=parser['FILES']['students_csv'],
        schools_csv=parser['FILES']['schools_csv'],
        output_path=parser['FILES']['output_folder'],
        api_key=parser['API']['api_key']
    )