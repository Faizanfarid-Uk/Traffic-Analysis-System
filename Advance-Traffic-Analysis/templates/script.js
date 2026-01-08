let map, heatmap;


function initMap() {
map = new google.maps.Map(document.getElementById('map'), {
center: { lat: 31.5204, lng: 74.3587 },
zoom: 13,
});


const trafficLayer = new google.maps.TrafficLayer();
trafficLayer.setMap(map);


heatmap = new google.maps.visualization.HeatmapLayer({
data: [],
map: map
});
}


window.onload = function() {
document.getElementById('start-btn').onclick = function() {
document.getElementById('welcome-overlay').style.display = 'none';
if (typeof google === 'object' && typeof google.maps === 'object') {
initMap();
loadIncidents();
} else {
alert('Google Maps failed to load. Check your API key and internet.');
}
}


document.getElementById('refresh').onclick = loadIncidents;
}


async function loadIncidents() {
try {
const resp = await fetch('http://127.0.0.1:5000/api/incidents');
if (!resp.ok) throw new Error('Network response not ok');
const data = await resp.json();
const points = data.map(i => new google.maps.LatLng(i.lat, i.lng));
heatmap.setData(points);
} catch (err) {
console.error(err);
alert('Failed to load incidents. Is the backend running?');
}
}