import time
import pandas as pd
import numpy as np

max_num = 4000000

d = {
  'A': np.random.rand(max_num),
  'B': np.random.rand(max_num),
  'C': np.random.rand(max_num),
  'D': np.random.rand(max_num),
  'D1': np.random.rand(max_num),
  'D2': np.random.rand(max_num),
  'D3': np.random.rand(max_num),
  'D4': np.random.rand(max_num),
  'D5': np.random.rand(max_num),
  'D6': np.random.rand(max_num),
  'S': [[1,2]] * max_num,
  'S1': ['tempstr1'] * max_num,
  'X': ['tempstr2'] * max_num,
  'Y': ['tempstr3'] * max_num,
}

t = time.time()
df1 = pd.DataFrame(d)
# df1 = pd.DataFrame.from_dict(d)
print('dict to DataFrame cost:{}'.format(time.time() - t))

t = time.time()
df2 = pd.DataFrame(index = range(max_num))
for k, v in d.items():
  df2[k] = v
print('dict loop to DataFrame cost:{}'.format(time.time() - t))
