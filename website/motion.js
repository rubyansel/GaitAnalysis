function createRequest(request) {
	try {
		request = new XMLHttpRequest();
	} catch (trymicrosoft) {
		try {
			request = new ActiveXObject("Msxml2.XMLHTTP");
		} catch (othermicrosoft) {
			try {
				request = new ActiveXObject("Microsoft.XMLHTTP");
			} catch (failed) {
				request = null;
			}
		}
	}
	if (request == null)
		alert("Error creating request object")
	return request;
}

function getMotion() {
	var request = null;
	function updatePage() {
		var newMotion = request.responseText;
		console.log(newMotion);
		var data = Papa.parse(newMotion).data;
		var length = data.length;
		if (length == 0)
			return;
		var time1El = document.getElementById("time1");
		var motion1_1El = document.getElementById("motion1_1");
		var motion2_1El = document.getElementById("motion2_1");
		replaceText(time1El, data[3][0]);
		replaceText(motion1_1El, data[3][1]);
		replaceText(motion2_1El, data[3][2]);
		var time2El = document.getElementById("time2");
		var time3El = document.getElementById("time3");
		var time4El = document.getElementById("time4");
		var motion1_2El = document.getElementById("motion1_2");
		var motion1_3El = document.getElementById("motion1_3");
		var motion1_4El = document.getElementById("motion1_4");
		var motion2_2El = document.getElementById("motion2_2");
		var motion2_3El = document.getElementById("motion2_3");
		var motion2_4El = document.getElementById("motion2_4");
		replaceText(time2El, data[2][0]);
		replaceText(time3El, data[1][0]);
		replaceText(time4El, data[0][0]);
		replaceText(motion1_2El, data[2][1]);
		replaceText(motion1_3El, data[1][1]);
		replaceText(motion1_4El, data[0][1]);
		replaceText(motion2_2El, data[2][2]);
		replaceText(motion2_3El, data[1][2]);
		replaceText(motion2_4El, data[0][2]);
	}
	request = createRequest(request);
	var url = "motion.php?date="+new Date().getTime();
	request.open("GET", url, true);
	request.onreadystatechange = updatePage;
	request.send(null);
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

