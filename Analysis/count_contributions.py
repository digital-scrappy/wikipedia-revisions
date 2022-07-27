

def contributions_by_user(rev_list):
    contribution_list = list(map(lambda x: x["user"], rev_list))
    unique_contributors = set(contribution_list)
    count_by_user = [ (user, contribution_list.count(user)) for user in unique_contributors]
    count_by_user.sort(key=lambda x: x[1], reverse= True)

    return count_by_user


    
    
