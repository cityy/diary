//https://github.com/ariutta/svg-pan-zoom
var svgElement = document.getElementById('circosSVG');

var panZoomTiger = svgPanZoom(svgElement, {
  viewportSelector: '.svg-pan-zoom_viewport', 
  panEnabled: true, 
  controlIconsEnabled: false, 
  zoomEnabled: true, 
  dblClickZoomEnabled: false, 
  mouseWheelZoomEnabled: true, 
  preventMouseEventsDefault: true, 
  zoomScaleSensitivity: 0.2, 
  minZoom: 0.8, 
  maxZoom: 2, 
  fit: true, 
  contain: false, 
  center: true, 
  refreshRate: 'auto', 
  beforeZoom: function(){}, 
  onZoom: function(){}, 
  beforePan: function(){}, 
  onPan: function(){}, 
  onUpdatedCTM: function(){}, 
  eventsListenerElement: null
});