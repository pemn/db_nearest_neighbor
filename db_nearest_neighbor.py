#!python
# find nearest neighbor sample between two sets
# left_hid: (optional) the unique hole identifier
# left_lito: (optional) lithology or any other classificatory field
# right_hid: (optional) only search for samples which do not match the left hid
# right_lito: (optional) only search for samples which match the left lito
# v2.0 2023/10 paulo.ernesto
# v1.1 2022/04 paulo.ernesto
# v1.0 2020/12 paulo.ernesto
'''
Copyright 2020 - 2022 Vale

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

https://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.

*** You can contribute to the main repository at: ***

https://github.com/pemn/db_nearest_neighbor
---------------------------------

usage: $0 left_db*csv,xlsx,isis,dm,bmf left_condition left_hid:left_db left_lito:left_db left_xyz#:left_db right_db*csv,xlsx,bmf right_condition right_hid:right_db right_lito:right_db right_xyz#:right_db output*csv,xlsx
'''

import sys, os.path
import numpy as np
import pandas as pd

# import modules from a pyz (zip) file with same name as scripts
sys.path.insert(0, os.path.splitext(sys.argv[0])[0] + '.pyz')

from _gui import usage_gui, pd_load_dataframe, pd_save_dataframe, commalist

from sklearn.metrics import pairwise_distances_argmin_min

def np_dropna(s):
  s = np.asfarray(s)
  return np.compress(np.min(np.isfinite(s), 1), s, 0)

def pd_nearest_neighbor(df0, hid0, lito0, xyz0, df1, hid1, lito1, xyz1):
  li = [None]
  if lito0 and lito1:
    if lito0 in df0 and lito1 in df1:
      li[:] = set(df0[lito0].str.lower().unique()).intersection(df1[lito1].str.lower().unique())

  lh = [None]
  if hid0 and hid1:
    if hid0 in df0 and hid1 in df1:
      lh[:] = set(df0[hid0].unique()).intersection(df1[hid1].unique())

  nni = np.full(df0.shape[0], np.nan)
  nnd = np.full(df0.shape[0], np.nan)

  bi0 = np.empty(df0.shape[0], dtype='bool')
  bi1 = np.empty(df1.shape[0], dtype='bool')
  ri0 = np.arange(df0.shape[0])
  ri1 = np.arange(df1.shape[0])
  for l in li:
    for h in lh:
      if l is None:
        bi0.fill(True)
        bi1.fill(True)
      else:
        bi0 = df0[lito0].str.lower() == l
        bi1 = df1[lito1].str.lower() == l

      if h is not None:
        bi0 = np.bitwise_and(bi0, df0[hid0] == h)
        bi1 = np.bitwise_and(bi1, df1[hid1] != h)

      if np.any(bi0) and np.any(bi1):
        i1,d1 = pairwise_distances_argmin_min(df0.loc[bi0, xyz0], df1.loc[bi1, xyz1])
      
        nnd[bi0] = d1
        nni[bi0] = ri1[bi1][i1]

  df0['nn_d'] = nnd
  df0['nn_i'] = nni
  return df0.join(pd.DataFrame.from_records([pd.Series() if np.isnan(_) else df1.loc[_] for _ in nni]), rsuffix='_nn')

def db_nearest_neighbor(db0, condition0, hid0, lito0, xyz0, db1, condition1, hid1, lito1, xyz1, output):
  print("# db_nearest_neighbor started")

  odf = pd_nearest_neighbor(pd_load_dataframe(db0, condition0), hid0, lito0, commalist(xyz0).split(), pd_load_dataframe(db1, condition1), hid1, lito1, commalist(xyz1).split())
  if output:
    pd_save_dataframe(odf, output)
  else:
    print(odf.to_string())

  print("finished")

main = db_nearest_neighbor

if __name__=="__main__":
  usage_gui(__doc__)
