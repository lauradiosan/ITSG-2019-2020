from sklearn.datasets import fetch_lfw_people
lfw_people = fetch_lfw_people(data_home="dataset",min_faces_per_person=10, resize=0.4)
lfw_people.
for name in lfw_people.target_names:
    print(name)

import os
for root, dirs, files in os.walk("dataset"):
    path = root.split(os.sep)
    print((len(path) - 1) * '---', os.path.basename(root))
    for file in files:
        print(len(path) * '---', file)
