library(sf)
library(terra)
library(ggplot2)

setwd('C:/Users/carroll/Documents/col/data')

# generate all domain bbox
crbu <- vect('C:/Users/carroll/Documents/col/data/2025/CRBU_AOP_Bounding_Polygon_5_16_2025.geojson')
almo <- vect('C:/Users/carroll/Documents/col/data/2025/ALMO_AOP_Bounding_Polygon_5_16_2025.geojson')
upta <- vect('C:/Users/carroll/Documents/col/data/2025/UPTA_AOP_Bounding_Polygon_5_16_2025.geojson')
all <- rbind(crbu, almo, upta) %>%
  project('epsg:32613')
bbox <- ext(all) %>%
  as.polygons() %>%
  buffer(20000)

plot(bbox)
plot(all, add=T)

tiles = list()
srtm_fps = list.files(pattern='\\v3.bil$', recursive=T, full.names=T) # downloaded srtm tiles that intersect bbbox from EarthExplorer

for (fp in srtm_fps){
  tile = rast(fp) %>%
    project('epsg:32613') %>%
    crop(bbox)
  tiles <- c(tiles, tile)
}

mosaic = do.call(merge, tiles) %>%
  crop(bbox)

plot(mosaic)
plot(bbox, add=T)
plot(all, add=T)

# export
writeRaster(mosaic, 'skyview/bbox_srtm_mosaic', filetype='ENVI', overwrite=T)