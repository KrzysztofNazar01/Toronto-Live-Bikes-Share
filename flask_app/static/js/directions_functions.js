function show_directions(lat1, lon1, lat2, lon2, lat3, lon3, lat4, lon4, travel_mode){
    url= 'https://www.google.com/maps/dir/' + lat1 + ',' + lon1 + '/' + lat2 + ',' + lon2 + '/' + lat3 + ',' + lon3 + '/' + lat4 + ',' + lon4 + '/data=!3m1!4b1!4m2!4m1!3e' + travel_mode + '?entry=ttu';
    window.open(url, '_blank');
}
