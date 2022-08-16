from test_data import doc_1, doc_2
from bertopic import BERTopic
from path_util import revisions_path
from split_page_into_paragraphs import split_page_into_paragraphs
import numpy as np
import os
import json
from datetime import datetime


docs = {}

rev_dirs = ["15-1211", "15-1221", "15-1231", "15-1242", "15-1244", "15-1251", "15-1252", "15-1253", "15-1254"]

rev_dirs = ["15-1211", "15-1221", "15-1231", "15-1242", "15-1244", "15-1251", "15-1252", "15-1253", "15-1254"]

for rev_dir in rev_dirs:
    rev_dir_path = revisions_path / rev_dir
    page_dirs = os.listdir(rev_dir_path)

    for page_name in page_dirs:
        docs[page_name] = {}
        page_dir_path = rev_dir_path / page_name
        rev_file_list = os.listdir(page_dir_path)

        for file_name in rev_file_list[::5]:
            file_path = page_dir_path / file_name
            with open(file_path, "r") as rev_file:
                rev = json.load(rev_file)
                docs["page_name"].append(rev)

                


topic_model = BERTopic(language="english",calculate_probabilities=True, verbose=True)

topics,  probs= topic_model.fit_transform(docs)


topics_1 = topic_model.transform(doc_1)
topics_2 = topic_model.transform(doc_2)
topic_probs_1 = np.argsort(topics_1[1])[::-1]
topic_probs_2 = np.argsort(topics_2[1])[::-1]
topic_set_1 = set(list(topic_probs_1[0][:20]))
topic_set_2 = set(list(topic_probs_2[0][:20]))

topic_diff = topic_set_2 - topic_set_1
freq = topic_model.get_topic_info()
print(freq[freq.Topic.isin(list(topic_diff))])


