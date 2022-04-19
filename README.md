# db_nearest_neighbor
match samples of different drillholes and of same lithology
## screenshots
### Graphic User Interface
![screenshot1](assets/screenshot1.png?raw=true)
### Result
![screenshot5](assets/screenshot2.png?raw=true)
## Parameters
 - db: structured data in one of the supported file formats: xlsx, csv, shp (ESRI Shape)
 - hid: (optional) the unique hole identifier. When used, samples with the same `hid` will not be considered neighbors.
 - lito: (optional) lithology or any other classificatory field. When used, only samples with the same `lito` will be considered neighbors.
## Output
The output will be a join of the two input tables. Fields of same name will have to `_nn` sufix added to diferentiate. Two new fields will be created:
 - nn_i: the row index of the neightbor (right_db).
 - nn_d: the distance between the sample (left_db) and the neighbor (right_db).
