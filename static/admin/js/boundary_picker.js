/**
 * Boundary picker — Leaflet + Leaflet.Draw widget for the boundary_geojson admin field.
 * Loads dynamically so it doesn't affect other admin pages.
 */
(function () {
  function loadScript(src, onload) {
    var s = document.createElement('script');
    s.src = src; s.onload = onload; document.head.appendChild(s);
  }
  function loadStyle(href) {
    var l = document.createElement('link');
    l.rel = 'stylesheet'; l.href = href; document.head.appendChild(l);
  }

  document.addEventListener('DOMContentLoaded', function () {
    var textarea = document.getElementById('id_boundary_geojson');
    var mapEl = document.getElementById('boundary-map-widget');
    if (!textarea || !mapEl) return;

    loadStyle('https://unpkg.com/leaflet@1.9/dist/leaflet.css');
    loadStyle('https://cdnjs.cloudflare.com/ajax/libs/leaflet.draw/1.0.4/leaflet.draw.css');

    loadScript('https://unpkg.com/leaflet@1.9/dist/leaflet.js', function () {
      loadScript('https://cdnjs.cloudflare.com/ajax/libs/leaflet.draw/1.0.4/leaflet.draw.js', function () {
        initMap(textarea, mapEl);
      });
    });
  });

  function initMap(textarea, mapEl) {
    var map = L.map(mapEl, { scrollWheelZoom: false }).setView([-6.3, 34.8], 6);

    L.tileLayer('https://{s}.basemaps.cartocdn.com/rastertiles/voyager/{z}/{x}/{y}{r}.png', {
      attribution: '&copy; OpenStreetMap &copy; CARTO', maxZoom: 18,
    }).addTo(map);

    var drawnItems = new L.FeatureGroup().addTo(map);

    // Load existing boundary
    var raw = textarea.value.trim();
    if (raw) {
      try {
        var geo = JSON.parse(raw);
        var geoInput = (geo.type === 'Feature' || geo.type === 'FeatureCollection')
          ? geo : { type: 'Feature', geometry: geo };
        var layer = L.geoJSON(geoInput, {
          style: { color: '#C8903A', weight: 2, fillOpacity: 0.15 },
          onEachFeature: function (f, l) { drawnItems.addLayer(l); }
        });
        if (layer.getBounds().isValid()) map.fitBounds(layer.getBounds(), { padding: [20, 20] });
      } catch (e) {}
    }

    map.addControl(new L.Control.Draw({
      edit: { featureGroup: drawnItems },
      draw: {
        polygon: { shapeOptions: { color: '#C8903A', fillOpacity: 0.15 } },
        rectangle: { shapeOptions: { color: '#C8903A', fillOpacity: 0.15 } },
        polyline: false, circle: false, marker: false, circlemarker: false,
      },
    }));

    function sync() {
      var layers = drawnItems.getLayers();
      if (!layers.length) { textarea.value = ''; return; }
      textarea.value = layers.length === 1
        ? JSON.stringify(layers[0].toGeoJSON().geometry)
        : JSON.stringify({ type: 'FeatureCollection', features: layers.map(function (l) { return l.toGeoJSON(); }) });
    }

    map.on(L.Draw.Event.CREATED, function (e) { drawnItems.addLayer(e.layer); sync(); });
    map.on(L.Draw.Event.EDITED, sync);
    map.on(L.Draw.Event.DELETED, sync);

    // Helper: import pasted GeoJSON
    var btn = document.getElementById('boundary-import-btn');
    var hint = document.getElementById('boundary-hint');
    if (btn) {
      btn.addEventListener('click', function () {
        drawnItems.clearLayers();
        var raw2 = textarea.value.trim();
        if (!raw2) { if (hint) hint.textContent = 'Textarea is empty.'; return; }
        try {
          var geo2 = JSON.parse(raw2);
          var geoInput2 = (geo2.type === 'Feature' || geo2.type === 'FeatureCollection')
            ? geo2 : { type: 'Feature', geometry: geo2 };
          L.geoJSON(geoInput2, {
            style: { color: '#C8903A', weight: 2, fillOpacity: 0.15 },
            onEachFeature: function (f, l) { drawnItems.addLayer(l); },
          }).addTo(map);
          var b = drawnItems.getBounds();
          if (b.isValid()) map.fitBounds(b, { padding: [20, 20] });
          if (hint) hint.textContent = 'Loaded ✓';
        } catch (e) { if (hint) hint.textContent = 'Invalid GeoJSON: ' + e.message; }
      });
    }
  }
})();
