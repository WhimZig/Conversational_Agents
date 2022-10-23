# This is a dumb class made so that I can test stuff and write without worrying about dirtying the main class
#   There should be nothing of value here, at least long term
import numpy as np
import pandas as pd
import json

# First thing, this is just a way of creating a dummy json file for testing later on
test_graph = {'The Starry Night': ['Vincent Van Gogh', 'Oil', 'Dutch', 'Village', 'Nature'],
              'The Siesta': ['Vincent Van Gogh', 'Oil', 'Dutch', 'People', 'Day'],
              'The Great Wave off Kanagawa': ['Katsushika Hokusai', 'Woodblock print', 'Japanese', 'Sea', 'Day'],
              'Fine Wind, Clear Morning': ['Katsushika Hokusai', 'Woodblock print', 'Japanese', 'Mountain', 'Nature'],
              # The things before are paintings, everything after are the topics. Separation done for ease
              'Vincent Van Gogh': ['The Starry Night', 'The Siesta', 'Dutch'],
              'Oil': ['The Starry Night', 'The Siesta', 'Medium'],
              'Dutch': ['Vincent Van Gogh', 'The Starry Night', 'The Siesta'],
              'Village': ['The Starry Night'],
              'Nature': ['The Starry Night', 'Fine Wind, Clear Morning'],
              'People': ['The Siesta'],
              'Day': ['The Siesta', 'The Great Wave off Kanagawa'],
              'Katsushika Hokusai': ['The Great Wave off Kanagawa', 'Fine Wind, Clear Morning', 'Japanese'],
              'Woodblock print': ['Medium', 'The Great Wave off Kanagawa', 'Fine Wind, Clear Morning'],
              'Japanese': ['The Great Wave off Kanagawa', 'Fine Wind, Clear Morning', 'Katsushika Hokusai'],
              'Sea': ['The Great Wave off Kanagawa'],
              'Mountain': ['Fine Wind, Clear Morning']}

paintings = ['The Starry Night', 'The Siesta', 'The Great Wave off Kanagawa', 'Fine Wind, Clear Morning']

# For now, I'll just store these two files, one as a json, and the other as a text file for reading.
with open("paintings.txt", 'w') as f:
    f.write("\n".join(map(str, paintings)))

with open('test_default.json', 'w', encoding='utf-8') as f:
    json.dump(test_graph, f, ensure_ascii=False, indent=4)


# This is a test node weights, done because I will probably use this later on!
vert_weights = pd.Series(0, index=test_graph.keys())

vert_weights.to_csv('UserVertexWeights/test_user.csv')
