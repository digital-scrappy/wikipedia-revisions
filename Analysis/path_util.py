from socket import gethostname
from pathlib import Path
import os

hostname = gethostname()

if hostname == "yocto":
    base_path = Path("/home/scrappy/Projects/csh")

# insert your hostname here and the path to the repository   
elif hostname == "Maria":
    #just an example below
    base_path = Path("/home/Maria/Projects/csh")
elif hostname == "LAPTOP-SCIFPBE4":
    #just an example below
    base_path = Path("C:\\Users\\leond\\Documents\\Github\\csh")
else:
    base_path = Path(os.getcwd())
    parents = 0
    while not str(base_path.parents[parents]).endswith("csh"):
        parents += 1
    base_path = base_path.parents[parents]

data_path = base_path / "data"
secrets_path = base_path / "secrets"
revisions_path = data_path / "revisions"
old_database_path = data_path / "data_bases" / "aggregated_edits.db"

print(old_database_path)