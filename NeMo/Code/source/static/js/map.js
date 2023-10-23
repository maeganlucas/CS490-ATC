var map = L.map('map').fitWorld();

// Organize different elements into groups (makes it easier to clear and redraw markers on update)
var planeLayer = L.layerGroup().addTo(map).setZIndex(600);          // For plane markers
var airportLayer = L.layerGroup().addTo(map).setZIndex(600);        // For airport markers
var infoLayer = L.layerGroup().addTo(map).setZIndex(800);           // For info pane
var flightPathLayer = L.layerGroup().addTo(map).setZIndex(550);     // For flight path lines

var planeData = [];
var airportData = [];

var testInterval;


// IMPORTANT, KEEP THE TILELAYER BELOW THIS COMMENT, IS PRIMARY FOR GEOGRAPHIC MAP

L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    attribution: "&copy; <a href='https://www.openstreetmap.org/copyright'>OpenStreetMap</a> contributors"
}).addTo(map);


// THIS SORT OF WORKS NOW BUT NEEDS ADJUSTING
// format for vfrmap is https://vfrmap.com/20230810/tiles/vfrc/{z}/{x}/{y}.jpg
// FOR DIFFERENT VFRMaps
// vfrc - 
// ehc - 
// sectc -
// ifrlc -
// helic - 
/*
L.TileLayer.VFRCoords = L.TileLayer.extend({
    getTileUrl: function(tilecoords) {
        var tilecoordsNewZ = tilecoords.z;
        var tilecoordsNewX = ((2**tilecoords.z) - 1) - tilecoords.y;
        var tilecoordsNewY = tilecoords.x;
        console.log(tilecoordsNewZ,tilecoordsNewX,tilecoordsNewY);
        return 'https://vfrmap.com/20230810/tiles/ifrlc/' + tilecoordsNewZ + '/' + tilecoordsNewX + '/' + tilecoordsNewY + '.jpg';
    },
    getAttribution: function() {
        return "&copy; <a href='https://vfrmap.com/tos.html'>VFRMap</a> contributors"
    }
});

L.tileLayer.VFRCoords = function() {
    return new L.TileLayer.VFRCoords();
}

L.tileLayer.VFRCoords().addTo(map);
*/

/**
 * Decodes a transponder type to the string version (i.e. int -> string). Useful for displaying this data in the UI.
 *
 * @param {int} position_source the position source from the API endpoint
 * @returns {string} transponder source type
 */
function get_position_source_string(position_source) {
    var source = "";

    // From the API docs for OpenSky
    switch (position_source) {
        case 0:
            source = "ADS-B";
            break;
        case 1:
            source = "ASTERIX";
            break;
        case 2:
            source = "MLAT";
            break;
        case 3:
            source = "FLARM";
            break;
        default:
            source = "N/A";
    }

    return source;
}




/**
 * Clears the table in the info pane in preparation for new data.
 */
function clear_table() {
    // Remove previous data
    $("#infoPane").children().each(function (index) {
        if ($(this).attr("id") != "infoTable" && $(this).attr("id") != "closeButton")
            $(this).remove();
    });

    $("#infoTable").children().each(function (index) {
        $(this).remove();
    });
}

/**
 * Decodes a plane category from the integer representation (i.e. int -> string)
 *
 * @param {int} category plane category from API endpoint
 * @returns {string} decoded plane category
 */
/*function get_plane_category_string(category) {
    var category = "";

    // TODO: there are a lot of categories to cover here
    switch (category) {
        default:
            category = "Unknown";
    }

    return category;
}*/

function get_plane_category_string(category_plane) {
    var category = "";
    switch (category_plane) {
        case 0:
            category = "No Information";
            break;
        case 1:
            category = "No ADS-B Emitter Category Information";
            break;
        case 2:
            category = "Light";
            break;
        case 3:
            category = "Small";
            break;
        case 4:
            category = "Large";
            break;
        case 5:
            category = "High Vortex Large";
            break;
        case 6:
            category = "Heavy";
            break;
        case 7:
            category = "High Performance";
            break;
        case 8:
            category = "Rotocraft";
            break;
        case 9:
            category = "Glider/sailplane";
            break;
        case 10:
            category = "Lighter-than-air";
            break;
        case 11:
            category = "Parachutist/Skydiver";
            break;
        case 12:
            category = "Ultralight/Hang-Glider/Paraglider";
            break;
        case 13:
            category = "Reserved";
            break;
        case 14:
            category = "Unmanned Aerial Vehicle";
            break;
        case 15:
            category = "Space/Trans-Atmospheric Vehicle";
            break;
        case 16:
            category = "Surface Vehicle-Emergency Vehicle";
            break;
        case 17:
            category = "Surface Vehicle-Service Vehicle";
            break;
        case 18:
            category = "Point Obstacle";
            break;
        case 19:
            category = "Cluster Obstacle";
            break;
        case 20:
            category = "Line Obstacle";
            break;
        default:
            category = "Unknown Aircraft";
    }

    return category;
}

/**
 * Draws the estimated flight path of the plane specified by the ICAO 24-bit address (from as far back as the waypoints go to
 * its current position).
 *
 * @param {string} icao24 24-bit ICAO identification number. This is a hexadecimal number represented as a string in the API.
 */
function draw_flight_path(icao24) {
    const flight_path_request = new XMLHttpRequest();

    flight_path_request.addEventListener("load", function () {
        if (flight_path_request.response == null)
            return;

        let waypoint_coords = [];
        flightPathLayer.clearLayers();

        for (const waypoint of flight_path_request.response.waypoints) {
            waypoint_coords.push([waypoint.latitude, waypoint.longitude]);

            let waypointMark = L.circleMarker(
                [waypoint.latitude, waypoint.longitude],
                {
                    radius: 10,
                    color: "black",
                    fill: true,
                    opacity: 1.0
                }
            ).addTo(flightPathLayer);

            let waypoint_time = new Date(waypoint.time);

            waypointMark.on('mouseover', function () {
                L.popup(
                    [waypoint.latitude, waypoint.longitude],
                    {
                        content: `
                        Time: ${waypoint_time.toLocaleString()}<br />
                        Location: ${waypoint.latitude}\u00b0N ${waypoint.longitude}\u00b0W`
                    }
                ).openOn(map);
            });
        }

        L.polyline(waypoint_coords, {
            color: "#000000",
            noClip: true,
            smoothFactor: 0
        }).addTo(flightPathLayer);
    });

    flight_path_request.open("GET", `/data/flight_track/${icao24}`);
    flight_path_request.responseType = "json";
    flight_path_request.send();
}

/**
 * Draws the plane markers on the Leaflet map based on the latitude, longitude, and heading information.
 * Also sets up the callback for the click event to populate the table in the information pane and draw flight path(s).
 *
 * @param {Array} plane_data An array of objects associated with a valid API response (i.e. response body isn't null).
 */
function draw_plane_markers(plane_data) {
    planeLayer.clearLayers();

    for (const plane of plane_data) {
        let marker = L.marker({
            lat: plane.latitude,
            lng: plane.longitude,
        });

        // order in which these methods are called doesn't matter
        
        marker.setIcon(L.icon({ iconUrl: plane.category_icon, iconSize: [20, 20], iconAnchor: [10, 10], className: "planeMarker" }));

        // THIS WORKS DO NOT DELETE
        //var testForSetIcon = "plane_category" + plane.category;
        //marker.setIcon(window[testForSetIcon]);

        // Rotate icon to match actual plane heading
        marker.setRotationAngle(plane.true_track);
        marker.addTo(planeLayer);

        marker.on('click', () => {
            clear_table();

            // Add plane entries entries; TODO: find a better way to do this
            $("#infoTable").append(`
                <tr>
                    <th colspan="2">Plane Properties</th>
                </tr>
            `);
            $("#infoTable").append(`
                <tr>
                    <td>ICAO 24-bit Address</td>
                    <td>${plane.icao24.toUpperCase()}</td>
                </tr>
            `);
            $("#infoTable").append(`
                <tr>
                    <td>Callsign</td>
                    <td>${plane.callsign}</td>
                </tr>
            `);
            $("#infoTable").append(`
                <tr>
                    <td>Country Origin</td>
                    <td>${plane.origin_country}</td>
                </tr>`
            );
            $("#infoTable").append(`
                <tr>
                    <td>Time of Last Position Report</td>
                    <td>${Date(plane.time_position)}</td>
                </tr>
            `);
            $("#infoTable").append(`
                <tr>
                    <td>Last Contact (time)</td>
                    <td>${Date(plane.last_contact)}</td>
                </tr>
            `);
            $("#infoTable").append(`
                <tr>
                    <td>Position</td>
                    <td>${plane.latitude}\u00b0N ${plane.longitude}\u00b0W</td>
                </tr>
            `);
            $("#infoTable").append(`
                <tr>
                    <td>Geometric Altitude</td>
                    <td>${plane.geo_altitude} meters</td>
                </tr>
            `);
            $("#infoTable").append(`
                <tr>
                    <td>On Ground?</td>
                    <td>${plane.on_ground ? "Yes" : "No"}</td>
                </tr>
            `);
            $("#infoTable").append(`
                <tr>
                    <td>Velocity</td><td>${plane.velocity} meters per second</td>
                </tr>
            `);
            $("#infoTable").append(`
                <tr>
                    <td>Heading</td>
                    <td>${plane.true_track}\u00b0</td>
                </tr>
            `);
            $("#infoTable").append(`
                <tr>
                    <td>Vertical Rate</td>
                    <td>${plane.vertical_rate} meters per second</td>
                </tr>
            `);
            $("#infoTable").append(`
                <tr>
                    <td>Squawk</td>
                    <td>${plane.squawk}</td>
                </tr>
            `);
            $("#infoTable").append(`
                <tr>
                    <td>Position Source</td>
                    <td>${get_position_source_string(plane.position_source)}</td>
                </tr>
            `);
            $("#infoTable").append(`
                <tr>
                    <td>Plane Category</td>
                    <td>${get_plane_category_string(plane.category)}</td>
                </tr>
            `);

            draw_flight_path(plane.icao24);

            // Hide zoom controls (draws over top of the table)
            $(".leaflet-control-zoom").hide();

            // Display data
            $("#infoPane").show();
        });
    }
}

/**
 * Draws the airport markers that are fetched from the data API when the app starts.
 * Sets up the callback functions for clicking the icons and populating the info table
 * with whatever data is available.
 *
 * @param {Array} airport_data An array of objects associated with a valid API response
 * from the /data/airports/<state> API endpoint.
 */
function draw_airport_markers(airport_data) {
    // TODO: combine airport and plane marker draw functions into one function
    airportLayer.clearLayers();

    for (const airport of airport_data) {
        let marker = L.marker([airport.latitude, airport.longitude]);
        marker.setIcon(airportIcon);
        marker.addTo(airportLayer);

        marker.on('click', (event) => {
            clear_table();

            // Add airport properties
            $("#infoTable").append(`
                <tr>
                    <th colspan="2">Airport Properties</th>
                </tr>
            `);
            $("#infoTable").append(`
                <tr>
                    <td>Identifier</td>
                    <td>${airport.ident}</td>
                </tr>
            `);
            $("#infoTable").append(`
                <tr>
                    <td>Name</td>
                    <td>${airport.name}</td>
                </tr>
            `);
            $("#infoTable").append(`
                <tr>
                    <td>Position</td>
                    <td>${airport.latitude}\u00b0N  ${airport.longitude}\u00b0W</td>
                </tr>
            `);
            $("#infoTable").append(`
                <tr>
                    <td>Elevation</td>
                    <td>${airport.elevation} feet</td>
                </tr>
            `);
            $("#infoTable").append(`
                <tr>
                    <td>Region Name</td>
                    <td>${airport.region_name}</td>
                </tr>
            `);
            $("#infoTable").append(`
                <tr>
                    <td>Municipality</td>
                    <td>${airport.municipality}</td>
                </tr>
            `);
            $("#infoTable").append(`
                <tr>
                    <td>GPS Code</td>
                    <td>${airport.gps_code}</td>
                </tr>
            `);
            $("#infoTable").append(`
                <tr>
                    <td>IATA Code</td>
                    <td>${airport.iata_code}</td>
                </tr>
            `);
            $("#infoTable").append(`
                <tr>
                    <td>Local Code</td>
                    <td>${airport.local_code}</td>
                </tr>
            `);
            $("#infoTable").append(`
                <tr>
                    <td>Website</td>
                    <td>${airport.home_link}</td>
                </tr>
            `);

            // If there are airport frequencies available, add them to the info pane
            if (airport.tower_frequencies) {
                // collapsible button to show/hide media players
                const $tower_freq = $(`
                    <button type='button' class='collapsible'>Tower Frequencies</button>
                `);
                // container for the media players and labels
                let $content_div = $("<div class='content'></div>");

                // click event handler for the tower frequency dropdown
                $tower_freq.on("click", () => {
                    // toggle visibility
                    $content_div.toggle();
                    // toggle active class (mostly for visual feedback)
                    $tower_freq.toggleClass("active");
                });

                // place collapsible menu after the airport properties
                $("#infoTable").after($tower_freq);
                // 'content' div for the media players after the frequency menus
                $tower_freq.after($content_div);

                for (const frequency of airport.tower_frequencies) {
                    let $audio_figure = $(`
                        <figure>
                            <figcaption>${frequency}</figcaption>
                        </figure>
                    `);

                    $content_div.append($audio_figure);
                    $audio_figure.append(`
                        <audio
                            controls
                            src="https://livetraffic2.near.aero/stream/${airport.ident}_${frequency.replace(".", "")}.mp3"
                        >
                        </audio>
                        <button id="transcribe-${airport.ident}_${frequency.replace(".", "")}">Transcribe</button>
                    `);

                    $(`#transcribe-${airport.ident}_${frequency.replace(".", "")}`).on("click", (event) => {
                        $.ajax({
                            url: "/models/transcribe",
                            method: "POST",
                            contentType: "text/plain",
                            data: `https://livetraffic2.near.aero/stream/${airport.ident}_${frequency.replace(".", "")}.mp3`,
                        }).done(() => {
                            console.log("Done");
                        })
                    });
                }
            }

            // Hide zoom controls (draws over top of the table)
            $(".leaflet-control-zoom").hide();

            // Display data
            $("#infoPane").show();
        });
    }
}

/**
 * One-time event listener setup.
 */
function setup_event_listeners() {
    // Event listener for clicking on the close button
    $("#closeButton").on('click', (event) => {
        // Hide table
        $("#infoPane").hide();
        // Redraw zoom controls
        $(".leaflet-control-zoom").show();
    });

    // Prevent mouse events from interacting with the map below the info panel
    $("#infoPane").on('click', (event) => {
        event.stopImmediatePropagation();
    });

    $("#infoPane").on('dblclick', (event) => {
        event.stopImmediatePropagation();
    });

    // Clears and redraws icons when a map zoom event fires.
    // This is to address an issue where the placement of the icons becomes less accurate the further in the map zooms.
    map.on('zoom', function (event) {
        planeLayer.clearLayers();
        flightPathLayer.clearLayers();

        draw_plane_markers(planeData);
    });
}

/**
 * Main function that gets called on map startup.
 */
function main() {
    // create http request object
    const plane_data_request = new XMLHttpRequest();

    // add event listener for when a plane data response is received
    plane_data_request.addEventListener("load", () => {
        // ignore cases where response body is null
        if (plane_data_request.response == null)
            return;

        planeData = plane_data_request.response.plane_data;
        draw_plane_markers(plane_data_request.response.plane_data);
    });

    // Create a GET request to send to the plane_states endpoint
    plane_data_request.open("GET", "/data/plane_states");
    // Specify a JSON return type
    plane_data_request.responseType = "json";
    // Send request
    plane_data_request.send();
}


map.on("zoomend", onMapZoomEnd);
map.on("moveend", onMapMoveEnd);

function getMapLatLonBounds() { // this function order got fucked up, need to fix mm
    var minLonEast = map.getBounds().getEast();
    var maxLonWest = map.getBounds().getWest();
    var minLatSouth = map.getBounds().getSouth();
    var maxLatNorth = map.getBounds().getNorth();

    //var latLonBounds = [minLonEast, maxLonWest, minLatSouth, maxLatNorth]
    var latLonBounds = [minLatSouth, maxLatNorth, maxLonWest, minLonEast]
    
    //console.log(JSON.stringify({latLonBounds : latLonBounds})); // for debugging purposes
    $.ajax({
        url: '/data/getMapLatLonBounds',
        type: 'POST',
        contentType: 'application/json',
        data: JSON.stringify({latLonBounds: latLonBounds}),
//        success: function(response) { console.log(response); },
        error: function(error) {
            console.log(error);
        }
    })
}

function onMapZoomEnd() {
    getMapLatLonBounds();
    checkMapZoomLevel();
}

function onMapMoveEnd() {
    getMapLatLonBounds();
}

function checkMapZoomLevel() {
    // Enable the overlay, we are zoomed too far out
    if (map.getZoom() < 8) {
        document.getElementsByClassName('leaflet-map-pane')[0].style.filter = 'blur(10px)';
        document.getElementById('zoomedTooFarOut').style.display = 'flex';

        clearInterval(testInterval); // clear the current interval we have to stop calling planes
        testInterval = null;
    }
    // Disable the overlay, we are zoomed in enough to load planes
    else {
        document.getElementsByClassName('leaflet-map-pane')[0].style.filter = 'blur(0px)';
        document.getElementById('zoomedTooFarOut').style.display = 'none';

        if (map.getZoom() == 8 && testInterval == null) {
            testInterval = setInterval(main, 30000);
        }
    }
}