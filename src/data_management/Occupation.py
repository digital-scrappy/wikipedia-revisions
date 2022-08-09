import json
from typing import List, Tuple

class Occupation:

        
    def __init__(self,
                 expected_lenght,
                 occ_code: str,
                 occ_group: str,
                 occ_title: str,
                 links: List[ Tuple[str,str] ],
                 rev_dirs: List[str],
                 tot_emp: List[float],
                 h_mean: List[float],
                 a_mean: List[float],
                 h_pct10: List[float],
                 h_pct25: List[float],
                 h_median: List[float],
                 h_pct75: List[float],
                 h_pct90: List[float],
                 a_pct10: List[float],
                 a_pct25: List[float],
                 a_median: List[float],
                 a_pct75: List[float],
                 a_pct90: List[float],
                 ):


        list_that_should_be_of_length = [ "tot_emp", "h_mean", "a_mean", "h_pct10", "h_pct25", "h_median", "h_pct75", "h_pct90", "a_pct10", "a_pct25", "a_median", "a_pct75", "a_pct90"]
        self.occ_code = occ_code
        self.occ_group = occ_group
        self.occ_title = occ_title
        self.links = links
        self.rev_dirs = rev_dirs
        self.tot_emp = tot_emp
        self.h_mean = h_mean
        self.a_mean = a_mean
        self.h_pct10 = h_pct10
        self.h_pct25 = h_pct25
        self.h_median = h_median
        self.h_pct75 = h_pct75
        self.h_pct90 = h_pct90
        self.a_pct10 = a_pct10
        self.a_pct25 = a_pct25
        self.a_median = a_median
        self.a_pct75 = a_pct75
        self.a_pct90 = a_pct90
        self.noNaNs = True


        for attr in list_that_should_be_of_length:
            lenght = len(getattr(self, attr))

            if lenght != expected_lenght:
                self.noNaNs = False




    

    def to_db(self):


        return (self.occ_code,                               
                self.occ_group,
                self.occ_title,
                json.dumps(self.links),
                json.dumps(self.rev_dirs),
                json.dumps(self.tot_emp),
                json.dumps(self.h_mean),
                json.dumps(self.a_mean),
                json.dumps(self.h_pct10),
                json.dumps(self.h_pct25),
                json.dumps(self.h_median),
                json.dumps(self.h_pct75),
                json.dumps(self.h_pct90),
                json.dumps(self.a_pct10),
                json.dumps(self.a_pct25),
                json.dumps(self.a_median),
                json.dumps(self.a_pct75),
                json.dumps(self.a_pct90),
                self.noNaNs)
