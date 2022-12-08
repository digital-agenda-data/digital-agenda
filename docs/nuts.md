## Updating NUTS topology

The TopoJSON used for the maps must be downloaded from https://gisco-services.ec.europa.eu/distribution/v2/countries/
For example the full list of files for 2020 can be found https://gisco-services.ec.europa.eu/distribution/v2/countries/countries-2020-files.json

Example downloading for 2020 using [EPSG:3857](https://epsg.io/3857)

```shell
wget https://gisco-services.ec.europa.eu/distribution/v2/countries/topojson/CNTR_RG_10M_2020_3857.json -O frontend/src/assets/topology.json
```

If you are changing the projection, the default center and zoom of the MapChart 
may require changing. See [MapCompareCountries.chartOptions.mapView](../frontend/src/components/charts/map/MapCompareCountries.vue). 
And Highcharts docs [here](https://api.highcharts.com/highmaps/mapView).