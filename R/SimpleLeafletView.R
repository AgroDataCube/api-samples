# For more ideas:
#  https://cran.r-project.org/web/packages/httr/vignettes/quickstart.html 
#  https://www.r-bloggers.com/processing-of-geojson-data-in-r/
#  https://ropensci.org/tutorials/geojsonio_tutorial/
#  https://rstudio.github.io/leaflet/

if (!require(httr)) {
  install.packages("httr")
  library(httr)
}
library(leaflet)

data_url <- "http://agrodatacube.wur.nl/api/v1/rest/fields?geometry=POLYGON%20((4.2%2052,%204.2%2053,%204.3%2053,%204.3%2052,%204.2%2052))&epsg=4326&year=2016&cropname=mais&output_epsg=4326"
response <- GET(data_url, add_headers(token = "<your access token>"))
if (response$status_code == 200) {
  map_leaf(content(response, "text"))  
} else {
  print(content(response, "text"))
  stop_for_status(response)
}