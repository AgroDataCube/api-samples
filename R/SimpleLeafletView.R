library(rgdal)
if (!require(geojsonio)) {
  install.packages("geojsonio")
  library(geojsonio)
}
library(sp)
library(leaflet)

data_url <- "http://agrodatacube.wur.nl/api/v1/rest/fields?geometry=POLYGON%20((4.2%2052,%204.2%2053,%204.3%2053,%204.3%2052,%204.2%2052))&epsg=4326&year=2016&cropname=mais&output_epsg=4326"
data_file <- "agrodatacube.geojson"
download.file(data_url, data_file)
geojson <- geojson_read (data_file, what = "sp")
sgdf <- SpatialPolygons(geojson@polygons)
map_leaf(sgdf)
