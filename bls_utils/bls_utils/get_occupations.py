import pandas
from typing import List

def get_occupations(path :str, group :str = "Detailed Occupation") -> List[str]:
    '''extracts the occupations from the structure of the bls soc classification

    Args:
        path (str): The path to the soc structure file
        group (str): The the level at which to extract occupations can be one of either ["Minor Group", "Broad Group", "Detailed Occupation"]

    Returns:
        A list of occupation names
    '''
    

    with open(path, "rb") as handle:
        structure = pandas.read_excel(io=handle, skiprows=7)
    occupations = structure[~structure[group].isnull()]['Unnamed: 4'].to_list()
    return occupations

