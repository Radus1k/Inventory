const mapElement = document.getElementById('map');
const greenMarker = mapElement.dataset.greenmarker;

const longitude = parseFloat(mapElement.dataset.long);
const latitude = parseFloat(mapElement.dataset.lat);

const tile = new ol.layer.Tile({
  source: new ol.source.XYZ({
    url: 'http://localhost:8080/tile/{z}/{x}/{y}.png'
  })
});

const marker = new ol.Feature({
  geometry: new ol.geom.Point(ol.proj.fromLonLat([longitude, latitude]))
});

marker.setStyle(new ol.style.Style({
  image: new ol.style.Icon({
    src: greenMarker
  })
}));

const vectorSource = new ol.source.Vector({
  features: [marker]
});

const markerVectorLayer = new ol.layer.Vector({
  source: vectorSource,
});

const map = new ol.Map({
  target: 'map',
  layers: [tile, markerVectorLayer],
  view: new ol.View({
    center: ol.proj.fromLonLat([longitude, latitude]),
    zoom: 7.4
  })
});