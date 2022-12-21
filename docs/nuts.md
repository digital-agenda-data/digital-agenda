## Updating NUTS topology

The TopoJSON used for the maps must be downloaded from https://gisco-services.ec.europa.eu/distribution/v2/countries/
For example the full list of files for 2020 can be found https://gisco-services.ec.europa.eu/distribution/v2/countries/countries-2020-files.json

Example downloading for 2020 using [EPSG:3857](https://epsg.io/3857)

```shell
wget https://gisco-services.ec.europa.eu/distribution/v2/countries/topojson/CNTR_RG_10M_2020_3857.json -O frontend/src/assets/topology.json
```

**IMPORTANT** If you are changing the projection, the default center and zoom of the MapChart 
may require changing. See [MapCompareCountries.chartOptions.mapView](../frontend/src/components/charts/map/MapCompareCountries.vue). 
And Highcharts docs [here](https://api.highcharts.com/highmaps/mapView).

---

_**Optionally**_ remove any unnecessary geometries from the TopoJSON. As the map view is fixed, and we don't allow panning,
any geometries that are off-screen can be removed and therefore making the download size much smaller and optimizing 
the CPU/memory used by the browser to render the chart.

For example [Mapshaper](https://mapshaper.org/) is a simple online tool than can be used for this purpose:

- upload the file 
- use the "shift-drag box tool" to select what to keep
- clip the selection 
- export it back to TopoJSON and copy it back to the assets folder