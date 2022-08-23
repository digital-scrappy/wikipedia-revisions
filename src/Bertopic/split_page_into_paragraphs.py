from typing import List

def split_page_into_paragraphs(page :str, min_lenght :int = 10) -> List[str]:
    ''' splits the page into paragraphs using the seperator "\n\n"'''

    paragraph_list = filter(lambda x: len(x) > min_lenght, page.split("\n\n"))

    return list(paragraph_list)



    
