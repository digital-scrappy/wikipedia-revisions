import os
from path_util import data_path, revisions_path
import json

for occ_dir in os.listdir(revisions_path):
    occ_path = revisions_path / occ_dir
    for page_dir in os.listdir(occ_path):
        page_path = occ_path / page_dir
        for revision_name in os.listdir(page_path):
            old_revision_path = page_path / revision_name
            with open(old_revision_path) as handle:
                revision = json.load(handle)
            new_revison_path = revisions_path / occ_dir / page_dir / f"{revision['revid']}.json"
            with open(new_revison_path, "w") as handle:
                json.dump(revision, handle)
            os.remove(old_revision_path)

                
        

        
