from dataclasses import dataclass
import json
from bin_revision_history import month_bin_revisions


@dataclass
class Occupation:

    id: int
    occ_code: str
    occ_title: str
    lenient_links: str
    strict_links: str
    TOT_EMP: str
    H_MEAN: str
    A_MEAN: str
    H_PCT10: str
    H_PCT25: str
    H_MEDIAN: str
    H_PCT75: str
    H_PCT90: str
    A_PCT10: str
    A_PCT25: str
    A_MEDIAN: str
    A_PCT75: str
    A_PCT90: str
    strict_revisions: str
    lenient_revisions: str


    def __post_init__(self):
        """take all the columns that are stored in json and turn them into python data structures"""
        json_attrs = ['lenient_links', 'strict_links', 'TOT_EMP', 'H_MEAN', 'A_MEAN', 'H_PCT10', 'H_PCT25', 'H_MEDIAN',
                      'H_PCT75', 'H_PCT90', 'A_PCT10', 'A_PCT25', 'A_MEDIAN', 'A_PCT75', 'A_PCT90', 'strict_revisions', 'lenient_revisions']

        for attr in json_attrs:
            setattr(self, attr,
                    json.loads(getattr(self, attr)))

        self.strict_binned_edits, self.strict_binned_diffs = self.get_revision_stats(self.strict_revisions)
        self.lenient_binned_edits, self.lenient_binned_diffs = self.get_revision_stats(self.lenient_revisions)

    @staticmethod
    def get_stats_for_page(binned_revs):
        temp_edits = {}
        temp_diffs = {}
        for key, value in binned_revs.items():
        
            num_edits = len(value)
            num_changes= sum([revision["size"] for revision in value])

            temp_edits[key] = num_edits
            temp_diffs[key] = num_changes

        return temp_edits, temp_diffs

    def get_revision_stats(self, revisions):
        binned_revs_dict = month_bin_revisions(revisions)
        edits = {}
        diffs = {}
        for page_name, binned_revs in binned_revs_dict.items():
            edits[page_name], diffs[page_name]= self.get_stats_for_page(binned_revs)
        return edits, diffs
