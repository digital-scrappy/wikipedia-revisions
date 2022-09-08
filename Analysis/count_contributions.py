import json

def contributions_by_user(rev_list):
    contribution_list = list(map(lambda x: x["user"], rev_list))
    unique_contributors = set(contribution_list)
    count_by_user = [(user, contribution_list.count(user)) for user in unique_contributors]
    count_by_user.sort(key=lambda x: x[1], reverse= True)

    return unique_contributors # instead of count_by_user (originally)


def amount_detailed(df_all, df_major):
    amount_of_detailed = []
    for code in df_major["occ_code"].tolist():
        sub_df = df_all[df_all['occ_code'].str.contains(str(code)[0:2] + "-")]
        df_sub_detailed = sub_df.loc[(sub_df["occ_group"] == "detailed")]
        amount_of_detailed.append(len(df_sub_detailed))
    
    articles_per_detailed = []
    for idx, lst in enumerate(df_major["lenient_links"].tolist()):
        articles_per_detailed.append((len(json.loads(lst))/amount_of_detailed[idx]))
    return articles_per_detailed

def avg_unique_auth_page_lengths(df_major):
    avg_unique_auths = []
    avg_page_lengths = []
    number_articles = []
    
    for idx, links_list in enumerate(df_major["lenient_links"].tolist()):
        links_list = json.loads(links_list)
        
        number_articles.append(len(links_list))
        
        revisions_dict = json.loads(df_major.iloc[idx]["lenient_revs"])
        page_length_dict = json.loads(df_major.iloc[idx]["lenient_lengths"])
        
        unique_total, pages_total = 0, 0
        for link in links_list:
            link_name = link[0]
            unique_total += len(contributions_by_user(revisions_dict[link_name]))
            pages_total += page_length_dict[link_name]
            
        avg_unique_auths.append(unique_total/len(links_list))
        avg_page_lengths.append(pages_total/len(links_list))        

    return avg_unique_auths, avg_page_lengths, number_articles
    

    
    
