var $root = $('html, body');

$(document).on('shown.bs.collapse', function(event){
    console.log()
    $root.animate({
        scrollTop: $("#" + event.currentTarget.activeElement.id.substring(0,3)).offset().top - 55
    }, 500);
});

// DFE Scripts
$("#region").change(function() {
    $("#Lat").val('');
    $("#Lon").val('');
    getRegionData();
});

$("#station_dd").change(function() {
    getStationData();
    getCatchData();
});

$("#dfe_method").change(function() {
    clear_map();
    $("#Lat").val('');
    $("#Lon").val('');
    $("#station_dd").val('');
    $('.dws').hide();
    $('.latlon').hide();
    $('.' + $(this).val()).show();
    getCatchData();
});

$("#dfe_get_loc").click(function (){
    clear_map();
    navigator.geolocation.getCurrentPosition(function(location) {
        var latlng = new L.LatLng(location.coords.latitude, location.coords.longitude);
        var marker = L.marker(latlng).addTo(mapsPlaceholder[0]);
            markersHolder.push(marker);
            $("#Lat").val(Math.round((latlng['lat'] + 0.000001) * 10000) / 10000);
            $("#Lon").val(Math.round((latlng['lng'] + 0.000001) * 10000) / 10000);
        mapsPlaceholder[0].setView(latlng, 12);
    });
});

function clear_map () {
    if (markersHolder.length == 1) {
        var m = markersHolder.pop();
        m.remove();
    }
    if (polyHolder.length == 1) {
        var p = polyHolder.pop();
        p.remove();
    }
}

function dfe_map_init_basic (map, options) {
    map.resetviewControl.remove();
    map.setMinZoom(5);
    map.setZoom(5);
    mapsPlaceholder.push(map);
    $("#dfe_latlon_but").hide()
    if (sname.length == 6) {
        $("#region").val(sname[0]);
    }
    getRegionData();
    if (document.getElementById('station_dd').length > 1) {
        document.getElementById('station_dd').value = "{{ name }}";
    }
    map.on('click', function(e){
        if ($("#dfe_method").val() == "latlon") {
            clear_map();
            var marker = L.marker(e.latlng).addTo(map);
            markersHolder.push(marker);
            $("#Lat").val(Math.round((e.latlng['lat'] + 0.000001) * 10000) / 10000);
            $("#Lon").val(Math.round((e.latlng['lng'] + 0.000001) * 10000) / 10000);
            map.setView(e.latlng);
        }

    });

}

function getStationData() {
    mapsPlaceholder[0].spin(true);
    $.ajax({
       headers: {"X-CSRFToken": getCookie('csrftoken')},
       method: "POST",
       url: gdataurl,
       data: { 'station': $("#station_dd").val()},
       success: function(data) {
            $("#Lat").val(data.lat);
            $("#Lon").val(data.lon);
            clear_map();
            if (data.lat != 0) {
                var marker = L.marker([data.lat, data.lon]).addTo(mapsPlaceholder[0]);
                markersHolder.push(marker);
                mapsPlaceholder[0].setView([data.lat, data.lon], 8);
            }
            if (data.poly[0][0] != 0) {
                var poly = L.polygon(data.poly, {color: 'green'}).addTo(mapsPlaceholder[0]);
                polyHolder.push(poly);
                mapsPlaceholder[0].fitBounds(poly.getBounds());
            }
    }
    }).done(function() {
        mapsPlaceholder[0].spin(false);
    });
}

function getCatchData() {
    mapsPlaceholder[0].spin(true);
    $.ajax({
       headers: {"X-CSRFToken": getCookie('csrftoken')},
       method: "POST",
       url: cdataurl,
       data: { 'station': $("#station_dd").val()},
       success: function(data) {
            $("#catch_param").html(data);
        }
    }).done(function() {
        mapsPlaceholder[0].spin(false);
    });
}

function getRegionData() {
    $.ajax({
        headers: {"X-CSRFToken": getCookie('csrftoken')},
        method: "POST",
        url:rdataurl,
        data: { 'region': $("#region").val()},
        success: function(data) {
            $("#station_dd").html(data);
            clear_map();
        }
    }).done(function() {
        if (sname.length == 6) {
            $("#station_dd").val(sname);
            getStationData();
            getCatchData();
        }
    });
}

// Gauges scripts
function gauges_map_init_basic (map, options) {
    mapsPlaceholder.push(map);

    var markers = L.markerClusterGroup();


    var gauges = $.ajax({
        headers: {"X-CSRFToken": getCookie('csrftoken')},
        url:'/api/gauges/',
        dataType:'json',
    });

    $.when(gauges).done(function() {
        var geoJsonLayer = L.geoJson(gauges.responseJSON, {
            onEachFeature: function (feature, layer) {
                layer.bindPopup('<h6>' + feature.properties.dws_id +
                    '</h6>' +
                    '<div class="d-flex justify-content-between align-items-center">' +
                    '<form action="/K52748/dfe/" method="post">' +
                    '<input type="hidden" name="csrfmiddlewaretoken" value="' + getCookie('csrftoken') + '">' +
                    '<h6><button class="badge badge-secondary" type="submit" name="station" value="' +
                    feature.properties.dws_id + '">DFE</button></h6></form>' +
                    '<h6><button class="badge badge-secondary" onclick="window.location.href = ' +
                    '\'https://www.dwa.gov.za/Hydrology/Verified/HyDataSets.aspx?Station=' +
                    feature.properties.dws_id + '&SiteDesc=RIV\'">DWS Site</button></div></h6>' +
                    '<table class="table table-sm"><tr><td>Start Date:</td><td>' + feature.properties.obsStart +
                    '</td></tr><tr><td>End Date:</td><td>' + feature.properties.obsEnd +
                    '</td></tr><tr><td colspan="2"><a href="https://www.dwa.gov.za/Hydrology/Verified/CGI-BIN/HIS/Photos/' +
                    feature.properties.dws_id + '.JPG" target="_blank"><img src="https://www.dwa.gov.za/Hydrology/Verified/CGI-BIN/HIS/Photos/' +
                    feature.properties.dws_id + '.JPG" alt="Image loading or no image available" width="200"/></a></tr></table>');
                layer.bindTooltip(feature.properties.dws_id);
                layer.on('popupopen', function(e) {
                    var px = map.project(e.popup._latlng); // find the pixel location on the map where the popup anchor is
                    px.y -= e.popup._container.clientHeight/2 + 80; // find the height of the popup container, divide by 2, subtract from the Y axis of marker location
                    map.panTo(map.unproject(px),{animate: true}); // pan to new center
                });
            }
        });
        markers.addLayer(geoJsonLayer);

    });

    map.addLayer(markers);
    // mapsPlaceholder[0].getContainer().className += ' sidebar-map'
}

// General
function getCookie(name) {
    var cookieValue = null;

    if (document.cookie && document.cookie != '') {
        var cookies = document.cookie.split(';');

        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);

            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) == (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }

    return cookieValue;
}