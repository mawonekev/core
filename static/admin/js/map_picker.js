/**
 * Leaflet GPS map picker for Django admin.
 * Injects a live map below the latitude/longitude fields.
 * Clicking the map or dragging the marker updates the inputs.
 */
(function () {
  'use strict';

  const LEAFLET_CSS = 'https://unpkg.com/leaflet@1.9.4/dist/leaflet.css';
  const LEAFLET_JS  = 'https://unpkg.com/leaflet@1.9.4/dist/leaflet.js';

  // Tanzania geographic centre as fallback
  const DEFAULT_LAT = -6.369028;
  const DEFAULT_LNG = 34.888822;
  const DEFAULT_ZOOM = 6;

  function loadLeaflet(cb) {
    if (window.L) { cb(); return; }

    const link = document.createElement('link');
    link.rel = 'stylesheet';
    link.href = LEAFLET_CSS;
    document.head.appendChild(link);

    const script = document.createElement('script');
    script.src = LEAFLET_JS;
    script.onload = cb;
    document.head.appendChild(script);
  }

  function initMap() {
    const latInput = document.getElementById('id_latitude');
    const lngInput = document.getElementById('id_longitude');
    if (!latInput || !lngInput) return;

    // ── Container ───────────────────────────────────────────────────────────
    const wrapper = document.createElement('div');
    wrapper.style.cssText = 'margin: 8px 0 16px 170px;'; // aligns under the label column

    const toolbar = document.createElement('div');
    toolbar.style.cssText = 'display:flex; gap:8px; margin-bottom:6px; align-items:center;';

    const locBtn = document.createElement('button');
    locBtn.type = 'button';
    locBtn.textContent = '📍 Use my location';
    locBtn.style.cssText = 'padding:4px 10px; font-size:12px; cursor:pointer; border:1px solid #ccc; border-radius:4px; background:#fff;';

    const hint = document.createElement('span');
    hint.textContent = 'Click map or drag marker to set coordinates';
    hint.style.cssText = 'font-size:12px; color:#666;';

    toolbar.appendChild(locBtn);
    toolbar.appendChild(hint);

    const mapDiv = document.createElement('div');
    mapDiv.id = 'xeno-map-picker';
    mapDiv.style.cssText = 'height:340px; width:100%; border:1px solid #ccc; border-radius:6px;';

    wrapper.appendChild(toolbar);
    wrapper.appendChild(mapDiv);

    // Insert after the longitude row
    const lngRow = lngInput.closest('.form-row') || lngInput.parentElement;
    lngRow.insertAdjacentElement('afterend', wrapper);

    // ── Map init ────────────────────────────────────────────────────────────
    const initLat = parseFloat(latInput.value) || DEFAULT_LAT;
    const initLng = parseFloat(lngInput.value) || DEFAULT_LNG;
    const zoom    = (latInput.value && lngInput.value) ? 10 : DEFAULT_ZOOM;

    const map = window.L.map('xeno-map-picker').setView([initLat, initLng], zoom);

    window.L.tileLayer('https://{s}.basemaps.cartocdn.com/rastertiles/voyager/{z}/{x}/{y}{r}.png', {
      attribution: '© <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors © <a href="https://carto.com/attributions">CARTO</a>',
      maxZoom: 19,
    }).addTo(map);

    const marker = window.L.marker([initLat, initLng], { draggable: true }).addTo(map);

    function updateInputs(lat, lng) {
      latInput.value = lat.toFixed(6);
      lngInput.value = lng.toFixed(6);
    }

    marker.on('dragend', function (e) {
      const pos = e.target.getLatLng();
      updateInputs(pos.lat, pos.lng);
    });

    map.on('click', function (e) {
      marker.setLatLng(e.latlng);
      updateInputs(e.latlng.lat, e.latlng.lng);
    });

    // Sync map if inputs are changed manually
    function syncMapFromInputs() {
      const lat = parseFloat(latInput.value);
      const lng = parseFloat(lngInput.value);
      if (!isNaN(lat) && !isNaN(lng)) {
        marker.setLatLng([lat, lng]);
        map.setView([lat, lng], map.getZoom());
      }
    }
    latInput.addEventListener('change', syncMapFromInputs);
    lngInput.addEventListener('change', syncMapFromInputs);

    locBtn.addEventListener('click', function () {
      if (!navigator.geolocation) {
        alert('Geolocation not supported by this browser.');
        return;
      }
      locBtn.textContent = 'Locating…';
      navigator.geolocation.getCurrentPosition(
        function (pos) {
          const lat = pos.coords.latitude;
          const lng = pos.coords.longitude;
          marker.setLatLng([lat, lng]);
          map.setView([lat, lng], 13);
          updateInputs(lat, lng);
          locBtn.textContent = '📍 Use my location';
        },
        function () {
          alert('Unable to retrieve location.');
          locBtn.textContent = '📍 Use my location';
        }
      );
    });
  }

  document.addEventListener('DOMContentLoaded', function () {
    loadLeaflet(initMap);
  });
})();
