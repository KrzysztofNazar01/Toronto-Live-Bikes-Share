function isLatitude(lat) {
    if (lat === "") {
        alert("Error - value of Latitude is incorrect");
        return false; // Prevent form submission
    }

    return isFinite(lat) && Math.abs(lat) <= 90;
}

function isLongitude(lon) {

    if (lon === "") {
        alert("Error - value of Longitude is incorrect");
        return false; // Prevent form submission
    }

    return isFinite(lon) && Math.abs(lon) <= 180;
}

function isKValue(k_value) {

    if (k_value === "") {
        alert("Error - value of K is incorrect");
        return false; // Prevent form submission
    }

    if (isNaN(k_value) || k_value < 1) {
        return false;
    }
    return true;
}

function check_if_location_within_border_points(lat, lon) {
    upper_left_lat = 43.91049
    upper_left_lon = -79.70796
    lower_right_lat = 43.52626
    lower_right_lon = -78.96952

    if (upper_left_lat >= lat && lat >= lower_right_lat && upper_left_lon <= lon && lon <= lower_right_lon) {
        return true;
    } else {
        alert("Error - the desired point is not in the area of Toronto!");
        return false;
    }
}

function validateFormStations() {
    // Get the value of the input field with id="numb"
    let lat = document.getElementById("lat").value;
    let lon = document.getElementById("lon").value;
    let k_value = document.getElementById("k_value").value;

    let lat_check = isLatitude(lat);
    let lon_check = isLongitude(lon);
    let k_value_check = isKValue(k_value);


    if (lat_check === true && lon_check === true && k_value_check === true) {
        //console.log("values correct");
        location_in_toronto = check_if_location_within_border_points(lat, lon);
        if (location_in_toronto === true){
            return true;
        }
    }
    return false;
}



function validateFormDirections() {
    let source_lat = document.getElementById("source_lat").value;
    let source_lon = document.getElementById("source_lon").value;
    let dest_lat = document.getElementById("dest_lat").value;
    let dest_lon = document.getElementById("dest_lon").value;

    return isLatitude(source_lat) === true
        && isLongitude(source_lon) === true
        && isLatitude(dest_lat) === true
        && isLongitude(dest_lon) === true;

}
