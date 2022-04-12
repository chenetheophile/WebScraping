<!DOCTYPE html>
<html lang="en">

<head>
	<meta charset="UTF-8">
	<meta http-equiv="X-UA-Compatible" content="IE=edge">
	<meta name="viewport" content="width=device-width, initial-scale=1.0">
	<title>Document</title>
	<link rel="stylesheet" href="https://unpkg.com/leaflet@1.7.1/dist/leaflet.css" />
	<script src="https://unpkg.com/leaflet@1.7.1/dist/leaflet.js"></script>
	<style>
		#map {
			position: absolute;
			z-index: -1;
			top: 0;
			bottom: 0;
			left: 0;
			right: 0;
		}

		#recherche {
			position: absolute;
			bottom: 10px;
			left: 0;
			right: 0;
		}
		#recherche table{
			margin-left: auto;
			margin-right: auto;
		}
		.tg {
			border-collapse: collapse;
			border-color: #93a1a1;
			border-spacing: 0;
		}

		.tg td {
			background-color: #fdf6e3;
			border-color: #93a1a1;
			border-style: solid;
			border-width: 1px;
			color: #002b36;
			font-family: Arial, sans-serif;
			font-size: 14px;
			overflow: hidden;
			padding: 10px 5px;
			word-break: normal;
		}

		.tg th {
			background-color: #657b83;
			border-color: #93a1a1;
			border-style: solid;
			border-width: 1px;
			color: #fdf6e3;
			font-family: Arial, sans-serif;
			font-size: 14px;
			font-weight: normal;
			overflow: hidden;
			padding: 10px 5px;
			word-break: normal;
		}

		.tg .tg-2bhk {
			background-color: #eee8d5;
			border-color: inherit;
			text-align: left;
			vertical-align: top
		}
		p{
			font-family: Verdana, Geneva, Tahoma, sans-serif;
			color: black;
			font-size: large;
			position: relative;
			width: fit-content;
		}
		
		.bouton {
			align-items: center;
			appearance: none;
			background-image: radial-gradient(100% 100% at 100% 0, #5adaff 0, #5468ff 100%);
			border: 0;
			border-radius: 6px;
			box-shadow: rgba(45, 35, 66, .4) 0 2px 4px,rgba(45, 35, 66, .3) 0 7px 13px -3px,rgba(58, 65, 111, .5) 0 -3px 0 inset;
			box-sizing: border-box;
			color: #fff;
			cursor: pointer;
			display: inline-flex;
			font-family: "JetBrains Mono",monospace;
			height: 40px;
			justify-content: center;
			line-height: 1;
			list-style: none;
			overflow: hidden;
			padding-left: 16px;
			padding-right: 16px;
			position: relative;
			text-align: left;
			text-decoration: none;
			transition: box-shadow .15s,transform .15s;
			user-select: none;
			-webkit-user-select: none;
			touch-action: manipulation;
			white-space: nowrap;
			will-change: box-shadow,transform;
			font-size: 18px;
		}

		.bouton:focus {
		box-shadow: #3c4fe0 0 0 0 1.5px inset, rgba(45, 35, 66, .4) 0 2px 4px, rgba(45, 35, 66, .3) 0 7px 13px -3px, #3c4fe0 0 -3px 0 inset;
		}

		.bouton:hover {
		box-shadow: rgba(45, 35, 66, .4) 0 4px 8px, rgba(45, 35, 66, .3) 0 7px 13px -3px, #3c4fe0 0 -3px 0 inset;
		transform: translateY(-2px);
		}

		.bouton:active {
		box-shadow: #3c4fe0 0 3px 7px inset;
		transform: translateY(2px);
		}
	</style>

	</style>
</head>

<body>

	<?php if ($_GET['annee'] < 2014) {
		$annee = 2021;
	} elseif ($_GET['annee'] > 2021) {
		$annee = 2014;
	} else {
		$annee = $_GET['annee'];
	}
	?>
	<div id="recherche">
	<table>
<thead>
  <tr>
    <td><button class="bouton" onclick="location.href='<?php echo ('../Code/pagephp.php?annee=' . $annee - 1); ?>'">Précédent</button></td>
    <td></td>
	<td><p>Année: <?php echo $annee; ?></p></td>
    <td></td>
	<td><button class="bouton" onclick="location.href='<?php echo ('../Code/pagephp.php?annee=' . $annee + 1); ?>'">Suivant</button></td>
  </tr>
</thead>
</table>	
	</div>

	<div id="map">
		<script>
			<?php
			 $filename = "../Map/regionsjson".$annee.".geojson";
			 $file = fopen( $filename, "r" );
			 
			 if( $file == false ) {
				echo ( "Error in opening file" );
				exit();
			 }
			 
			 $filesize = filesize( $filename );
			 $filetext = fread( $file, $filesize );
			 fclose( $file );
			?>
			var Geo=<?php echo $filetext;?>;
			console.log(Geo);
			var map = L.map('map').setView([45, 5], 6);
			L.tileLayer('https://api.maptiler.com/maps/basic/{z}/{x}/{y}.png?key=yogklvzwv3dBSOZ03oIc', {
				attribution: '<a href="https://www.maptiler.com/copyright/" target="_blank">&copy; MapTiler</a> <a href="https://www.openstreetmap.org/copyright" target="_blank">&copy; OpenStreetMap contributors</a>'
			}).addTo(map)

			function showInfo(layer) {
				var properties = layer.feature.properties;
				return properties;
			}

			function showMessage(layer) {
				console.log(layer.feature.properties);
				var lol = "<table class='tg'><thead>"+ layer.feature.properties.nom+"</thead><tbody><tr><td class='tg-0pky'>Population</td><td class='tg-2bhk'>" + layer.feature.properties.population + "</td><td class='tg-0pky'>Moyenne Qualité de l'air</td><td class='tg-2bhk'>" + layer.feature.properties.moyenneRegion + "</td></tr><tr><td></td><td></td><td></td><td></td></tr><tr><td class='tg-0pky'>Nucleaire</td><td class='tg-2bhk'>" + layer.feature.properties.nucleaire + "</td><td class='tg-0pky'>Hydrolique</td><td class='tg-2bhk'>" + layer.feature.properties.hydrolique + "</td></tr><tr><td class='tg-0pky'>Thermique</td><td class='tg-2bhk'>" + layer.feature.properties.thermique + "</td><td class='tg-0pky'>Eolien</td><td class='tg-2bhk'>" + layer.feature.properties.eolien + "</td></tr><tr><td class='tg-0pky'>Solaire</td><td class='tg-2bhk'>" + layer.feature.properties.solaire + "</td><td class='tg-0pky'>BioEnergie</td><td class='tg-2bhk'>" + layer.feature.properties.bioenergie + "</td></tr><tr><td></td><td></td><td></td><td></td></tr><tr><td class='tg-0pky'>Essence</td><td class='tg-2bhk'>" + layer.feature.properties.essence + "</td><td class='tg-0pky'>GPL</td><td class='tg-2bhk'>" + layer.feature.properties.gpl + "</td></tr><tr><td class='tg-0pky'>Diesel</td><td class='tg-2bhk'>" + layer.feature.properties.diesel + "</td><td class='tg-0pky'>Electrique</td><td class='tg-2bhk'>" + layer.feature.properties.electrique + "</td></tr><tr><td class='tg-0pky'>Hybride</td><td class='tg-2bhk'>" + layer.feature.properties.hybride + "</td><td class='tg-0pky'>Autre</td><td class='tg-2bhk'>" + layer.feature.properties.autre + "</td></tr><tr><td></td><td></td><td></td><td></td></tr></tbody></table>";
				return String(lol);
			}
			var options={
    'maxWidth': '400',
    'width': '200',
    'className' : 'popupCustom'
    };
			map = L.geoJSON(Geo)
				.bindPopup((e) => showMessage(e),options).addTo(map);
		</script>
	</div>

</body>

</html>

