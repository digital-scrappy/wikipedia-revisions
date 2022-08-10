from bin_revision_history import all_revs
from count_contributions import contributions_by_user

print(type(all_revs))

for occ_dict in all_revs:
    for occ_name, revisions_dict in occ_dict.items():
        for date, list_revisions_date in revisions_dict.items():
            user_contrib_monthly = contributions_by_user(list_revisions_date)
            print(occ_name, date, x)
            break

    break


