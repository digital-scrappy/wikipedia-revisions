import pandas
from typing import List

path = "/home/scrappy/data/csh/bls/source/soc_structure_2018.xlsx"
def get_ocupations(path :str, group :str = "Minor Group") -> List[str]:

    with open(path, "rb") as handle:
        structure = pandas.read_excel(io=handle, skiprows=7)
    occupations = structure[~structure[group].isnull()]['Unnamed: 4'].to_list()
    return occupations
print(get_ocupations(path, group = "Detailed Occupation"))

