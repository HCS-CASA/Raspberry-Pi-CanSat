<html>
<head>
<script type='text/javascript' src='http://maps.googleapis.com/maps/api/js?key=AIzaSyD2lEMzrqe2hwWrvtnJzMZAvMHVl0nVdrI&sensor=false'></script>
<script type='text/javascript'>
var curCoords = new google.maps.LatLng(<?php
$file_handle = fopen("coords.csv", "r");

if (!feof($file_handle)) {
	$line = rtrim(fgets($file_handle));
	echo $line . ");;\n";
}

echo "var coords = [\n\tnew google.maps.LatLng($line),\n";
while (!feof($file_handle)) {
	$line = rtrim(fgets($file_handle));
	echo "\tnew google.maps.LatLng($line),\n";
}
echo "];\n";
fclose($file_handle);
?>
function initialize()
{
	var mapProp = {center:curCoords, zoom:15, mapTypeId:google.maps.MapTypeId.HYBRID, streetViewControl:false, mapTypeControl:false};
	var map = new google.maps.Map(document.getElementById("map"), mapProp);
	var location = new google.maps.Marker({position:curCoords, map:map});
	var line = new google.maps.Polyline({path:coords, map:map});
}
google.maps.event.addDomListener(window, 'load', initialize);
</script>
</head>
<body>
<div id="map" style="width:500px;height:380px;"/>
<p>
</p>
</body>
</html>