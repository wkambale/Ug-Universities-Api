const attribution = '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
const map = L.map('map', {zoomSnap: 0})
L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', { attribution: attribution }).addTo(map);
const universities = JSON.parse(document.getElementById('universities-uganda-universities-domains').textContent);
let feature = L.geoJSON(universities);
let markers = L.markerClusterGroup();
markers.addLayer(feature).bindPopup(function (layer) { return layer.feature.properties.name; }).addTo(map);
map.addLayer(markers);
map.fitBounds(feature.getBounds(), { padding: [100, 100] });

const reload = document.querySelector('.leaflet-control-reload');

reload.addEventListener('click', (e) => {
    e.preventDefault();
    feature.clearLayers();
    markers.clearLayers();

    feature = L.geoJSON(universities);
    markers.addLayer(feature).bindPopup(function (layer) { return layer.feature.properties.name; }).addTo(map);
    map.addLayer(markers);
    map.flyToBounds(feature.getBounds(), { padding: [100, 100] });
})

const onInput = () => {
    let val = document.querySelector('#uni_name');
    let opts = document.querySelector('#uni-list').childNodes;

    opts.forEach(dist => {
        if(dist.value == val.value) {
            // send the value to backend
            fetch("/ajax/filter?" + new URLSearchParams({district: dist.value}))
            .then(response => {
                if(response.ok) {
                    return response.json()
                }
                return response;
            }).then(data => {
                // clear input
                val.value = ""

                // clear layer
                markers.clearLayers();

                const universities = data.uganda-universities-domains;
                feature = L.geoJSON(universities);
                markers.addLayer(L.geoJSON(centres)).bindPopup(function (layer) { return layer.feature.properties.name; }).addTo(map);
                map.addLayer(markers)
                map.flyToBounds(feature.getBounds(), { padding: [100, 100] });
            })
            .catch(err => console.warn('Something went wrong!', err))
        }
    });
}

document.querySelector('#uni_names').addEventListener('input', onInput);

const onClick = () => {
    const checkBox = document.querySelector('#toggle-btn');

    // TODO: show loading spinner

    if (!checkBox.checked) {
        // get test centres from backend
        fetch("/ajax/universities/test?" + new URLSearchParams({section: 'test'}))
        .then(response => {
            if(response.ok) {
                return response.json();
            }
            return response;
        }).then(data => {
            // clear current layer
            markers.clearLayers();

            const universities = data.test-universities-data;
            feature = L.geoJSON(universities).bindPopup(function (layer) { return layer.feature.properties.name; }).addTo(map);
            map.flyToBounds(feature.getBounds(), { padding: [100, 100] });

        })
        .catch(err => console.warn('Something went wrong!', err))
        console.log('Checked');
        
    } else {
        console.log('Not checked');
        feature.clearLayers();

        feature = L.geoJSON(centres);
        markers.addLayer(feature).bindPopup(function (layer) { return layer.feature.properties.name; }).addTo(map);
        map.addLayer(markers);
        map.flyToBounds(feature.getBounds(), { padding: [100, 100] });
    }
}

document.querySelector('.slider').addEventListener('click', onClick);



