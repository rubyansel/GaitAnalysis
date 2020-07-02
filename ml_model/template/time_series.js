/*window.addEventListener("load", function() {
	showplot();
})
function showplot() {
	var ExpP = document.getElementById("epf");
	var data = [
		{
			x: ['2013-10-04 22:23:00', '2013-11-04 22:23:00', '2013-12-04 22:23:00'],
			y: [1, 3, 6],
			type: 'scatter'
		}
	];
	Plotly.plot( ExpP,data);
}
*/

var file1 = "module_data_foot_06";
var file2 = "module_data_shank_06";
var PAST = 0;
var CNT = 100;
Plotly.d3.csv(file1, function(err, rows){
	function unpack(rows, key) {
		var col = [];
		for (var i=rows.length-PAST-CNT; i < rows.length-PAST; i++) {
			var row = rows[i];
			col.push(row[key]);
		}
		return col;
	}
	function calltime(rows) {
		var col = [];
		var past = 0;
		var times = 0;
		for (var i = rows.length-PAST-CNT; i < rows.length-PAST; i++) {
			if (i < 0) {
				continue;
			}
			var row = rows[i];
			if (past == row['time']) {
				times++;
			} else {
				for (var j = 0; j < times; j++) {
					var num = 100/times*j;
					var cat = ":".concat(num.toString());
					var time = rows[i-times+j]['time'].slice(11);
					col.push(time.concat(cat));
				}
				times = 1;
				past = row['time'];
			}
		}
		for (var j = 0; j < times; j++) {
			var num = 100/times*j;
			var cat = ":".concat(num.toString());
			var time = rows[rows.length-PAST-times+j]['time'].slice(11);
			col.push(time.concat(cat));
		}
		col.push('steps');
		return col;
	}

	function callcal(rows) {
		var cal = 0
		for (var i = rows.length-1; i >= 0; i--) {
			var row = rows[i];
			var ax = Number(row['ax']);
			var ay = Number(row['ay']);
			var az = Number(row['az']);
			var gx = Number(row['gx']);
			var gy = Number(row['gy']);
			var gz = Number(row['gz']);
			if (row['name'] == 'walking') {
				cal = i;
				break;
			}
		}

		var calcol = []
		var cnt = 0;
		if (cal == 0) {
			calcol.push(0);
			calcol.push(0);
			calcol.push(0);
			calcol.push(0);
			calcol.push(0);
			calcol.push(0);
		}
		for (var i = cal-1; i >= 0 && i >= cal-10; i--) {
			var row = rows[i];
			if (i == cal-1) {
				calcol.push(Number(row['ax']));
				calcol.push(Number(row['ay']));
				calcol.push(Number(row['az']));
				calcol.push(Number(row['gx']));
				calcol.push(Number(row['gy']));
				calcol.push(Number(row['gz']));
			} else {
				calcol[0] += Number(row['ax']);
				calcol[1] += Number(row['ay']);
				calcol[2] += Number(row['az']);
				calcol[3] += Number(row['gx']);
				calcol[4] += Number(row['gy']);
				calcol[5] += Number(row['gz']);
			}
			cnt++;
		}

		var call = []
		for (var i = 0; i < 6; i++) {
			if (cnt == 0)
				call.push(0);
			else
				call.push(calcol[i]/cnt);
		}

		return call;
	}

	function callacc(rows, cals) {
		var col = []
		for (var i = rows.length-PAST-CNT; i < rows.length; i++) {
			if (i < 0) {
				continue;
			}
			var row = rows[i];
			var ax = (Number(row['ax'])-cals[0]);
			var ay = (Number(row['ay'])-cals[1]);
			var az = (Number(row['az'])-cals[2]);
			var num = Math.sqrt(ax*ax+ay*ay+az*az);
//			if (row['ax'] == '0' && row['ay'] == '0' && row['az'] == '0')
//				num = 0;
//			var num = i-rows.length;
			col.push(num);
		}
		var step = 0;
		for (var i = 1; i < col.length-1; i++) {
			if (col[i] > col[i-1] && col[i] > col[i+1])
				step++;
		}
		col.push(step);
		return col;
	}

	function callgeo(rows, cals) {
		var col = []
		for (var i = rows.length-PAST-CNT; i < rows.length; i++) {
			if (i < 0) {
				continue;
			}
			var row = rows[i];
			var gx = Number(row['gx']);
			var gy = Number(row['gy']);
			var gz = Number(row['gz']);
			var num = Math.sqrt(gx*gx+gy*gy+gz*gz);
//			if (row['ax'] == '0' && row['ay'] == '0' && row['az'] == '0')
//				num = 0;
//			var num = i-rows.length;
			col.push(num);
		}
		var step = 0;
		for (var i = 1; i < col.length-1; i++) {
			if (col[i] > col[i-1] && col[i] > col[i+1])
				step++;
		}
		col.push(step);
		return col;
	}

	var cals = callcal(rows);

	var trace1 = {
		type: "scatter",
		mode: "lines",
		name: 'geometrics',
		x: calltime(rows, 'time'),
		y: callgeo(rows, cals),
		line: {color: '#17BECF'}
	}

	var trace2 = {
		type: "scatter",
		mode: "lines",
		name: 'accelerator',
		x: calltime(rows, 'time'),
		y: callacc(rows, cals),
		line: {color: '#7F7F7F'}
	}

	var data = [trace1, trace2];

	var layout = {
		title: file1,
		yaxis: {
			//range:[0, 19000]
		}
	};

	Plotly.newPlot('left', data, layout);
})

Plotly.d3.csv(file2, function(err, rows){
	function unpack(rows, key) {
		var col = [];
		for (var i=rows.length-PAST-CNT; i < rows.length-PAST; i++) {
			var row = rows[i];
			col.push(row[key]);
		}
		return col;
	}
	function calltime(rows) {
		var col = [];
		var past = 0;
		var times = 0;
		for (var i = rows.length-PAST-CNT; i < rows.length-PAST; i++) {
			if (i < 0) {
				continue;
			}
			var row = rows[i];
			if (past == row['time']) {
				times++;
			} else {
				for (var j = 0; j < times; j++) {
					var num = 100/times*j;
					var cat = ":".concat(num.toString());
					var time = rows[i-times+j]['time'].slice(11);
					col.push(time.concat(cat));
				}
				times = 1;
				past = row['time'];
			}
		}
		for (var j = 0; j < times; j++) {
			var num = 100/times*j;
			var cat = ":".concat(num.toString());
			var time = rows[rows.length-PAST-times+j]['time'].slice(11);
			col.push(time.concat(cat));
		}
		col.push('steps');
		return col;
	}

	function callcal(rows) {
		var cal = 0
		for (var i = rows.length-1; i >= 0; i--) {
			var row = rows[i];
			var ax = Number(row['ax']);
			var ay = Number(row['ay']);
			var az = Number(row['az']);
			var gx = Number(row['gx']);
			var gy = Number(row['gy']);
			var gz = Number(row['gz']);
			if (row['name'] == 'walking') {
				cal = i;
				break;
			}
		}

		var calcol = []
		var cnt = 0;
		if (cal == 0) {
			calcol.push(0);
			calcol.push(0);
			calcol.push(0);
			calcol.push(0);
			calcol.push(0);
			calcol.push(0);
		}
		for (var i = cal-1; i >= 0 && i >= cal-10; i--) {
			var row = rows[i];
			if (i == cal-1) {
				calcol.push(Number(row['ax']));
				calcol.push(Number(row['ay']));
				calcol.push(Number(row['az']));
				calcol.push(Number(row['gx']));
				calcol.push(Number(row['gy']));
				calcol.push(Number(row['gz']));
			} else {
				calcol[0] += Number(row['ax']);
				calcol[1] += Number(row['ay']);
				calcol[2] += Number(row['az']);
				calcol[3] += Number(row['gx']);
				calcol[4] += Number(row['gy']);
				calcol[5] += Number(row['gz']);
			}
			cnt++;
		}

		var call = []
		for (var i = 0; i < 6; i++) {
			if (cnt == 0)
				call.push(0);
			else
				call.push(calcol[i]/cnt);
		}

		return call;
	}

	function callacc(rows, cals) {
		var col = []
		for (var i = rows.length-PAST-CNT; i < rows.length; i++) {
			if (i < 0) {
				continue;
			}
			var row = rows[i];
			var ax = (Number(row['ax'])-cals[0]);
			var ay = (Number(row['ay'])-cals[1]);
			var az = (Number(row['az'])-cals[2]);
			var num = Math.sqrt(ax*ax+ay*ay+az*az);
//			if (row['ax'] == '0' && row['ay'] == '0' && row['az'] == '0')
//				num = 0;
//			var num = i-rows.length;
			col.push(num);
		}
		var step = 0;
		for (var i = 1; i < col.length-1; i++) {
			if (col[i] > col[i-1] && col[i] > col[i+1])
				step++;
		}
		col.push(step);
		return col;
	}

	function callgeo(rows, cals) {
		var col = []
		for (var i = rows.length-PAST-CNT; i < rows.length; i++) {
			if (i < 0) {
				continue;
			}
			var row = rows[i];
			var gx = Number(row['gx']);
			var gy = Number(row['gy']);
			var gz = Number(row['gz']);
			var num = Math.sqrt(gx*gx+gy*gy+gz*gz);
//			if (row['name'] == 'walking')
//				num = 0;
//			var num = i-rows.length;
			col.push(num);
		}
		var step = 0;
		for (var i = 1; i < col.length-1; i++) {
			if (col[i] > col[i-1] && col[i] > col[i+1])
				step++;
		}
		col.push(step);
		return col;
	}

	var cals = callcal(rows);

	var trace1 = {
		type: "scatter",
		mode: "lines",
		name: 'geometrics',
		x: calltime(rows, 'time'),
		y: callgeo(rows, cals),
		line: {color: '#17BECF'}
	}

	var trace2 = {
		type: "scatter",
		mode: "lines",
		name: 'accelerator',
		x: calltime(rows, 'time'),
		y: callacc(rows, cals),
		line: {color: '#7F7F7F'}
	}

	var data = [trace1, trace2];

	var layout = {
		title: file2,
	};

	Plotly.newPlot('right', data, layout);
})
