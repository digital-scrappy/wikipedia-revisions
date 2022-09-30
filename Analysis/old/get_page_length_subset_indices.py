import json
from typing import Iterator


def get_subset_indices(json_path: str, min_lenght : int, strict : bool = True) -> Iterator[int]:
    '''Returns the indices corresponding to pages with lenght greater than min_lenght

    Args:
      json_path: The path to the json holding the page lenghts and indices
      min_lengt: The minimum page lenght for which an index will be returned
      strict: wheather to use the lenght of the strict or lenient pages for the decisions

    Returns:
      A list of indices 
    '''

    index = 1 if strict else 2
    with open(json_path, "r") as handle:
        page_list = json.load(handle)
    subset = filter(lambda x: x if (x[index] > min_lenght) else None, page_list)
    
    return map(lambda x: x[0], subset)

    
