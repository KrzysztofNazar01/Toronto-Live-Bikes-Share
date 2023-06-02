function isLatitude(value) {
    /* Check if the value is a correct latitude value.
    *
    * Args:
    *   value: value to check
    *
    * Returns:
    *   Boolean value - true if value is correct
    * */
    if (value === "") {
        alert("Error - value of Latitude is incorrect");
        return false; // Prevent form submission
    }

    return isFinite(value) && Math.abs(value) <= 90;
}

function isLongitude(value) {
    /* Check if the value is a correct longitude value.
    *
    * Args:
    *   value: value to check
    *
    * Returns:
    *   Boolean value - true if value is correct
    * */
    if (value === "") {
        alert("Error - value of Longitude is incorrect");
        return false; // Prevent form submission
    }

    return isFinite(value) && Math.abs(value) <= 180;
}

function isKValue(value) {
    /* Check if the value is a correct K value.
    *
    * Args:
    *   value: value to check
    *
    * Returns:
    *   Boolean value - true if value is correct
    * */
    if (value === "") {
        alert("Error - value of K is incorrect");
        return false; // Prevent form submission
    }

    if (isNaN(value) || value < 1 || value > 20) {
        return false;
    }
    return true;
}

function check_if_location_is_in_toronto(lat, lon) {
    /* Check if the location (latitude and longitude) is located within a given area - Toronto city.
    *
    * Args:
    *   lat: location latitude
    *   lon: location longitude
    *
    * Returns:
    *   Boolean value - true if value is correct
    * */

    // The two points - opposite corners of a rectangle covering the accepted area.
    let upper_left_lat = 43.91049
    let upper_left_lon = -79.70796
    let lower_right_lat = 43.52626
    let lower_right_lon = -78.96952

    if (upper_left_lat >= lat && lat >= lower_right_lat && upper_left_lon <= lon && lon <= lower_right_lon) {
        return true;
    } else {
        alert("Error - the desired point is not in the area of Toronto!");
        return false; // Prevent form submission
    }
}

function validateFormStations() {
    /* Validate the input in HTML form - search available bikes or docks.
    *
    * Returns:
    *   Boolean value - true if values in form are correct
    * */
    let lat = document.getElementById("lat").value;
    let lon = document.getElementById("lon").value;
    let k_value = document.getElementById("k_value").value;

    let lat_check = isLatitude(lat);
    let lon_check = isLongitude(lon);
    let k_value_check = isKValue(k_value);


    if (lat_check === true && lon_check === true && k_value_check === true) {
            return check_if_location_is_in_toronto(lat, lon);
    }
    return false;
}


function validateFormDirections() {
    /* Validate the input in HTML form - search directions between source and destination location.
    *
    * Returns:
    *   Boolean value - true if values in form are correct
    * */
    let source_lat = document.getElementById("source_lat").value;
    let source_lon = document.getElementById("source_lon").value;
    let dest_lat = document.getElementById("dest_lat").value;
    let dest_lon = document.getElementById("dest_lon").value;

    return isLatitude(source_lat) === true
        && isLongitude(source_lon) === true
        && isLatitude(dest_lat) === true
        && isLongitude(dest_lon) === true;
}
