# MapDataset
All tools needed to construct a dataset based on map data.

## Guide
- Execute tiles/aerial.py to get tiles inside configurable bounding box
- Combine patches into bigger images using tiles/combiner.py
- Import vector/tile_write.py script into QGIS, and generate labels for each image. This step required QGIS and map data.
    1. Download N50 map data from [Kartverket](http://kartverket.no/Kart/Gratis-kartdata/Last-ned-norgeskartet-som-database/) in postgres format. Guide can be found [here](http://kartverket.no/Kart/Gratis-kartdata/Vegvisar-til-gratis-kartdata/Brukerveiledning-for-kartdata/)
    2. In QGIS open norway.qgs file.
    3. Open Python console by **Plugins -> Python console**.
    4. Right click in console and press **Show Editor**.
    5. Click folder icon and open vector/tile_writer.py in editor.
    6. Change **dir** and **output_dir** of vector/tile_writer.py script.
    7. Click save button and run script.

- Use dataset/formatter.py to organize images and labels into a dataset. Images tiles are given new name and randomized
- Test, validation and training folder can be created manually. 

## Dependencies
* [Numpy](http://www.numpy.org/)
* [Python 2.7](https://www.python.org/)
* [Requests](http://docs.python-requests.org/en/master/)

