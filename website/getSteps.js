var threshold = 1000;

function createRequest(rawFile) {
	try {
		rawFile = new XMLHttpRequest();
	} catch (trymicrosoft) {
		try {
			rawFile = new ActiveXObject("Msxml2.XMLHTTP");
		} catch (othermicrosoft) {
			try {
				rawFile = new ActiveXObject("Microsoft.XMLHTTP");
			} catch (failed) {
				rawFile = null;
			}
		}
	}
	if (rawFile == null)
		alert("Error creating rawFile object")
	return rawFile;
}

function getSteps() {
	var file1 = "module_data_foot";
	var file2 = "module_data_shank";
	var foot_res = readTextFile(file1);
	var shank_res = readTextFile(file2);
}

function readTextFile(file)
{
	var rawFile = null;
	function updateText() {
		var allText = rawFile.responseText;
		var rows = Papa.parse(allText).data;

		function callcal(rows) {
			var call = []
			for (var i = 0; i < 6; i++) {
				call.push(0);
			}
			return call;
		}

		function callacc(rows, cals) {
			var col = []
			for (var i = 1; i < rows.length; i++) {
				var row = rows[i];
				var ax = (Number(row[2])-cals[0]);
				var ay = (Number(row[3])-cals[1]);
				var az = (Number(row[4])-cals[2]);
				var num = Math.sqrt(ax*ax+ay*ay+az*az);
				col.push(num);
			}
			var step = 0;
			for (var i = 0; i < col.length-1; i++) {
				if (col[i] > col[i-1]+threshold && col[i] > col[i+1]+threshold)
					step++;
			}
			return step;
		}

		function callgeo(rows, cals) {
			var col = []
			for (var i = 1; i < rows.length; i++) {
				var row = rows[i];
				var gx = Number(row[5]);
				var gy = Number(row[6]);
				var gz = Number(row[7]);
				var num = Math.sqrt(gx*gx+gy*gy+gz*gz);
				col.push(num);
			}
			var step = 0;
			for (var i = 0; i < col.length-1; i++) {
				if (col[i] > col[i-1]+threshold && col[i] > col[i+1]+threshold)
					step++;
			}
			return step;
		}

		var cals = callcal(rows);
		var step_g = callgeo(rows, cals);
		var step_a = callacc(rows, cals);


		res_g = String(step_g);
		res_a = String(step_a);
		var ele_geo = document.getElementById(file.split('_')[2]+'_geo');
		var ele_acc = document.getElementById(file.split('_')[2]+'_acc');
		replaceText(ele_geo, res_g);
		replaceText(ele_acc, res_a);
	}
	var url = "getSteps.php?file='" + escape(file) + "'&date="+new Date().getTime();
	rawFile = createRequest(rawFile)
	rawFile.open("GET", url, true);
	rawFile.onreadystatechange = updateText;
	rawFile.send(null);
}


function replaceText(el, text) {
	if (el != null) {
		clearText(el);
		var newNode = document.createTextNode(text);
		el.appendChild(newNode);
	}
}

function clearText(el) {
	if (el != null) {
		if (el.childNodes) {
			for (var i = 0; i < el.childNodes.length; i++) {
				var childNode = el.childNodes[i];
				el.removeChild(childNode);
			}
		}
	}
}

function getText(el) {
	var text = "";
	if (el != null) {
		if (el.childNodes) {
			for (var i = 0; i < el.childNodes.length; i++) {
				var childNode = el.childNodes[i];
				if (childNode.nodeValue != null) {
					text = text + childNode.nodeValue;
				}
			}
		}
	}
	return text;
}

