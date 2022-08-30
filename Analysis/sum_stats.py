import pandas as pd


def get_gender_ratio(row, col_name):

    if len(row.lenient_links) <= 2 :
        return 0
    try:
        value = float(row[col_name])
    except ValueError:
        return None
    else: 
        return value


def sum_up_attributes(old_col_name, new_col_name, df):
    df[new_col_name] = None
    subset_df = df[df.occ_group == "major"]

    for i in range(0, subset_df.shape[0]):
        occ_code = subset_df.iloc[i].occ_code


        code_slice = occ_code[:2]

        hi = df[df.apply(lambda x: x.occ_code.startswith(code_slice) and x.occ_group == "detailed", axis = 1, result_type = "reduce")]
        hi = hi.apply(get_gender_ratio, axis = 1, args= (old_col_name,))
        hi = list(filter(lambda x: x if x > 0 else None, hi))
        if hi:
            result = sum(hi) / len(hi)
        else:
            continue
        idx = df[df["occ_code"] == occ_code].index.values
        df.loc[idx,new_col_name] = result
