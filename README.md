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
