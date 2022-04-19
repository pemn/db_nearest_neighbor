#!python
# find nearest neighbor sample between two sets
# left_hid: (optional) the unique hole identifier
# left_lito: (optional) lithology or any other classificatory field
# right_hid: (optional) only search for samples which match the left hid
# right_lito: (optional) only search for samples which do not match the left lito
# v1.1 04/2022 paulo.ernesto
# v1.0 12/2020 paulo.ernesto
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

usage: $0 left_db*csv,xlsx,isis,dm,bmf left_hid:left_db left_lito:left_db left_x:left_db left_y:left_db left_z:left_db right_db*csv,xlsx,bmf right_hid:right_db right_lito:right_db right_x:right_db right_y:right_db right_z:right_db output*csv,xlsx
'''

import sys, os.path
import numpy as np
import pandas as pd

# import modules from a pyz (zip) file with same name as scripts
sys.path.insert(0, os.path.splitext(sys.argv[0])[0] + '.pyz')

from _gui import usage_gui, pd_load_dataframe, pd_save_dataframe

from sklearn.metrics import pairwise_distances_argmin_min

def pd_nearest_neighbor(dfs, hid0, lito0, x0, y0, z0, hid1, lito1, x1, y1, z1):
  v_lut = [{},{}]
  v_lut[0]['hid'] = hid0
  v_lut[0]['lito'] = lito0
  v_lut[0]['midx'] = x0
  v_lut[0]['midy'] = y0
  v_lut[0]['midz'] = z0
  v_lut[1]['hid'] = hid1
  v_lut[1]['lito'] = lito1
  v_lut[1]['midx'] = x1
  v_lut[1]['midy'] = y1
  v_lut[1]['midz'] = z1
  odf = pd.DataFrame()
  df1 = dfs[1]

  for i0,row0 in dfs[0].iterrows():
    row1 = pd.Series(dtype=np.object_)
    row1.rename(i0, inplace=True)
    query = ''
    if v_lut[0]['hid'] and v_lut[1]['hid']:
      hid = row0[v_lut[0]['hid']]
      query = "%s != '%s'" % (v_lut[1]['hid'], hid)
    if v_lut[0]['lito'] and v_lut[1]['lito']:
      if query:
        query += ' and '
      query += "%s == '%s'" % (v_lut[1]['lito'], row0[v_lut[0]['lito']])

    if query:
      df1 = dfs[1].query(query)

    if not (df1 is None or df1.empty):
      xyz0 = row0[[v_lut[0]['midx'],v_lut[0]['midy'],v_lut[0]['midz']]]
      xyz0 = np.reshape(xyz0.values, (1, len(xyz0)))
      xyz1 = df1[[v_lut[1]['midx'],v_lut[1]['midy'],v_lut[1]['midz']]]
      if xyz1.ndim == 1:
        xyz1 = np.reshape(xyz1.values, (1, len(xyz1)))
      else:
        xyz1 = xyz1.values
      #print(xyz0)
      #print(xyz1)
      i1,d1 = pairwise_distances_argmin_min(xyz0, xyz1)
      # print(np.ndim(xyz0),np.ndim(xyz1),np.ndim(i1),np.ndim(d1))
      row1 = df1.iloc[i1].copy()
      row1['nn_i'] = i1[0]
      row1['nn_d'] = d1[0]

    odf = odf.append(row1)

  odf.set_index(pd.RangeIndex(0, len(odf)), False, False, True)

  odf = dfs[0].join(odf, rsuffix='_nn')

  return odf

def db_nearest_neighbor(db0, hid0, lito0, x0, y0, z0, db1, hid1, lito1, x1, y1, z1, output):
  print("# db_nearest_neighbor started")
  dfs = []
  dfs.append(pd_load_dataframe(db0))
  dfs.append(pd_load_dataframe(db1))

  odf = pd_nearest_neighbor(dfs, hid0, lito0, x0, y0, z0, hid1, lito1, x1, y1, z1)
  if output:
    pd_save_dataframe(odf, output)
  else:
    print(odf.to_string())

  print("finished")

main = db_nearest_neighbor

if __name__=="__main__":
  usage_gui(__doc__)
