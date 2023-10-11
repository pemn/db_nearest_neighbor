## 📌 Description
Match samples/blocks/points by nearest distance.  
## Purpose
Most common use case is matching drillhole samples to other samples or to block models.  
It requires XYZ, so in cases of ASSAY samples you must first desurvey using pemn/db_desurvey_straight or other method.
Its very generic, so can also be used to match samples with block models, block models with survey points, and many other cases where you need to match near points.
## 📸 Screenshot
### Graphic User Interface  
![screenshot1](https://github.com/pemn/assets/blob/main/db_nearest_neighbor1.png?raw=true)
  
### Result  
![screenshot2](https://github.com/pemn/assets/blob/main/db_nearest_neighbor2.png?raw=true)
## 📝 Parameters
name|optional|description
---|---|------
|db|❎|structured data in one of the supported file formats: xlsx, csv, shp (ESRI Shape)|
|condition|❎|python expression to select rows that evaluate as True|
|hid|☑️|the unique hole identifier. When used, samples with the same `hid` will not be considered neighbors.|
|lito|☑️|lithology or any other classificatory field. When used, only samples with the same `lito` will be considered neighbors.|
|xyz|❎|fields that will be used as coordinates. can be any numeric, but are usualy the sample xyz|
|output|☑️|path to save the merged tables|
## Output  
The output will be a left join of the left_db with the calculated neighbors from the right_db.  
Fields of same name will have the `_nn` sufix added to diferentiate.  
Two new fields will be created:
 - nn_i: the row index of the neightbor (right_db).
 - nn_d: the distance between the sample (left_db) and the neighbor (right_db).
## Repository
https://github.com/pemn/db_nearest_neighbor
## 🧩 Compatibility
distribution|status
---|---
![winpython_icon](https://github.com/pemn/assets/blob/main/winpython_icon.png?raw=true)|✔
![vulcan_icon](https://github.com/pemn/assets/blob/main/vulcan_icon.png?raw=true)|❓
![anaconda_icon](https://github.com/pemn/assets/blob/main/anaconda_icon.png?raw=true)|❌
## 🙋 Support
Any question or problem contact:
 - paulo.ernesto
## 💎 License
Apache 2.0
Copyright ![vale_logo_only](https://github.com/pemn/assets/blob/main/vale_logo_only_r.svg) Vale 2023
