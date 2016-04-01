# MapDataset
All tools needed to construct a dataset based on map data.

## Guide
- Execute tiles/aerial.py to get tiles inside configurable bounding box
- Combine patches into bigger images using tiles/combiner.py
- Import vector/tile_write.py script into QGIS, and generate labels for each image. This step required QGIS and map data.
- Use dataset/formatter.py to organize images and labels into a dataset, with test, validation and training set.

## Dependencies
* [Numpy](http://www.numpy.org/)
* [Python 2.7](https://www.python.org/)
* [Requests](http://docs.python-requests.org/en/master/)

