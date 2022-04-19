# db_nearest_neighbor
Match samples/blocks/points by nearest distance.  
Most common use case is matching drillhole samples to other samples or to block models.  
Its very generic, so can also be used to match samples with block models, block models with survey points, and many other cases where you need to match near points.

## screenshots  
### Graphic User Interface  
![screenshot1](assets/screenshot1.png?raw=true)  
  
### Result  
![screenshot2](assets/screenshot2.png?raw=true)  
## Parameters  
 - db: structured data in one of the supported file formats: xlsx, csv, shp (ESRI Shape)
 - hid: (optional) the unique hole identifier. When used, samples with the same `hid` will not be considered neighbors.
 - lito: (optional) lithology or any other classificatory field. When used, only samples with the same `lito` will be considered neighbors.
  
## Output  
The output will be a left join of the left_db with the calculated neighbors from the right_db.  
Fields of same name will have the `_nn` sufix added to diferentiate.  
Two new fields will be created:
 - nn_i: the row index of the neightbor (right_db).
 - nn_d: the distance between the sample (left_db) and the neighbor (right_db).
