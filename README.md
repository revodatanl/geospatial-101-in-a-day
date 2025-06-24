# Geospatial-101-in-a-day

This repository contains training notebooks demonstrating how to perform advanced geospatial analysis on the Databricks platform. The examples use open-source tools such as:

- Apache Sedona
- PDAL
- GDAL
- GraphFrames

Each subfolder contains a self-contained notebook focused on a real-world geospatial problem.

## Notebooks Overview

### 1. Location Allocation: Ice Cream Cart Optimization
**Folder**: `notebooks/01-location-allocation/`

Find the best 1000 locations for ice cream carts near park entrances using location-allocation modeling. Uses spatial joins, clustering, and proximity analysis with Apache Sedona.

---

### 2. Change Detection: San Francisco SoMa (2022 vs. 2025)
**Folder**: `notebooks/02-change-detection/`

Perform change detection using NDVI and NDWI indices between two satellite images of San Francisco’s SoMa neighborhood (2022 and 2025). Includes interpolation and difference maps using GDAL and Apache Sedona.

---

### 3. Sky View Factor and Fisheye Plot: Washington DC
**Folder**: `notebooks/03-sky-view-factor/`

Calculate the Sky View Factor and generate fisheye plots from LiDAR point cloud data of Washington DC. Useful for urban climate and sunlight studies. Processed with PDAL and visualized using Python libraries.

---

### 4. Shortest Path Calculation: London
**Folder**: `notebooks/04-network-analysis/`

Compute the shortest path between two points in London using road network data and the GraphFrames library (Spark-based graph analysis).

---

### 5. Ocean Temperature Statistics from NetCDF
**Folder**: `notebooks/05-weather/`

Analyze ocean temperature data stored in NetCDF format to compute statistics like mean temperature and temporal variation. Uses xarray and netCDF4 in combination with Apache Spark.

---

## Technologies and Libraries

- Databricks
- Apache Sedona (spatial operations in Spark)
- PDAL (LiDAR processing)
- GDAL (raster and remote sensing)
- GraphFrames (network analysis)
- netCDF4 / xarray (climate and ocean data)
- Python packages: pandas, numpy, matplotlib

---

## Getting Started

1. Clone or import this repository into your Databricks workspace.
2. Attach the required libraries to your cluster:
   -  [Apache Sedona](https://sedona.apache.org/latest/api/sql/Visualization_SedonaPyDeck/)
   -  [GraphFrames](https://graphframes.io/docs/_site/index.html)
   - Python: `pdal`, `gdal`, `netCDF4`, `xarray`, `matplotlib`
3. Run each notebook from its folder in the order presented above.

---

Please credit this repository if you use it in your own work or research.
