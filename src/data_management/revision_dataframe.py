from path_util import revisions_path
import os
import json
from datetime import datetime
import pandas as pd

def main():
    rev_dict = {}
    #new key and old key in tuples
    #this is used so I can loop over a try except statement
    #this is turns gurantees that if only on element is missing still the others are added to the dataframe
    key_pairs = [("user_id", "userid"),("user_name","user"),("tags","tags")]

    for occ_name in os.listdir(revisions_path):
        occ_path = (revisions_path / occ_name)

        for page_name in os.listdir(occ_path):
            page_path = (occ_path / page_name)

            for revision_name in os.listdir(page_path):
                revision_path = (page_path / revision_name)
                with open(revision_path) as infile:
                    try:
                        revision = json.load(infile)
                    except json.JSONDecodeError:
                        continue
                revision_number = revision["revid"]
                rev_dict[revision_number] = {}
                rev_dict[revision_number]["occ_number"] = occ_name
                rev_dict[revision_number]["page_name"] = page_name
                rev_dict[revision_number]["datetime"] = datetime.fromisoformat(revision["timestamp"])
                rev_dict[revision_number]["complete"] = True
                for new_key, old_key in key_pairs:
                    try:
                        rev_dict[revision_number][new_key] = revision[old_key]
                    except KeyError:
                        rev_dict[revision_number]["complete"] = False
                        continue
    df = pd.DataFrame.from_dict(rev_dict,orient= "index")
    return df

if __name__ == "__main__":
    main()



            
            
            





            



            
            
            
    
