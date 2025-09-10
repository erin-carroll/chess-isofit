library(sf)
library(terra)
library(ggplot2)

setwd('C:/Users/carroll/Documents/col/data/skyview')

# generate the srtm mosaic
bbox = vect('BoundingBox.geojson') %>%
  project('epsg:32613')
bbox_buf = bbox %>%
  buffer(1250)
plot(bbox_buf)

tiles = list()
srtm_fps = list.files(pattern='\\.bil', recursive=T, full.names=T)

for (fp in srtm_fps){
  tile = rast(fp) %>%
    project('epsg:32613') %>%
    crop(bbox_buf)
  tiles <- c(tiles, tile)
}

mosaic = do.call(merge, tiles)
plot(mosaic)

# merge srtm mosaic and local dsm at dsm resolution
dsm_1m = rast('dsm_mosaic_min_phase_me.tif')
tmplt <- extend(dsm1m, ext(mosaic))
srtm_1m <- resample(mosaic, tmplt, method = "bilinear")
dsm_1m  <- resample(dsm_1m,  tmplt, method = "near")

mosaic <- cover(dsm_1m, srtm_1m)
plot(mosaic)
writeRaster(mosaic, 'dsm_1m_mosaic_bbox_buf1250m.bil', filetype='ENVI', overwrite=T)

# upsample to 10m? To speed it up... Should be mostly good
mosaic_10m = aggregate(mosaic, fact=10, fun=mean, na.rm=T)
plot(mosaic_10m)
writeRaster(mosaic_10m, 'dsm_10m_mosaic_bbox_buf1250m.bil', filetype='ENVI', overwrite=T)

