var file1 = "../ml_model/module_data_foot";
var file2 = "../ml_model/module_data_shank";

function draw(err, rows){
	function calltime(rows) {
		var col = [];
		var past = 0;
		var times = 0;
		for (var i = 0; i < rows.length; i++) {
			var row = rows[i];
			if (past == row['time']) {
				times++;
			} else {
				for (var j = 0; j < times; j++) {
					var num = 100/times*j;
					var cat = ".".concat(num.toString());
					var time = rows[i-times+j]['time'];
					col.push(time.concat(cat));
				}
				times = 1;
				past = row['time'];
			}
		}
		for (var j = 0; j < times; j++) {
			var num = 100/times*j;
			var cat = ".".concat(num.toString());
			var time = rows[rows.length-times+j]['time'];
			col.push(time.concat(cat));
		}
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
		for (var i = 0; i < rows.length; i++) {
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
		for (var i = 0; i < rows.length; i++) {
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

	function getTimeStart(times) {
		if (times.length < 100)
			return times[0];
		else
			return times[times.length-100];
	}

	var cals = callcal(rows);
	var times = calltime(rows, 'time');

	var trace1 = {
		type: "scatter",
		mode: "lines",
		name: 'geometrics',
		x: times,
		y: callgeo(rows, cals),
		line: {color: '#17BECF'}
	}

	var trace2 = {
		type: "scatter",
		mode: "lines",
		name: 'accelerator',
		x: times,
		y: callacc(rows, cals),
		line: {color: '#7F7F7F'}
	}

	var data = [trace1, trace2];
	var time_start = getTimeStart(times);

	var layout = {
		title: file1,
		xaxis: {
			range: [time_start, times[times.length-1]],
			rangeselector: {buttons: [
				{
					count: 30,
					label: '30s',
					step: 'second',
					stepmode: 'backward'
				},
				{
					count: 1,
					label: '1m',
					step: 'minute',
					stepmode: 'backward'
				},
				{step: 'all'}
			]},
			rangeslider: {range: [times[0], times[times.length-1]]},
			type: 'date'
		},
		yaxis: {
			//range:[0, 19000]
		},
		margin: {
			l: 40,
			r: 20,
			t: 20,
			b: 20,
			pad: 15
		},
		paper_bgcolor: "#fffcec",
		plot_bgcolor: "#fffcec",
	};

	return [data, layout];
}

function getPictures() {
	Plotly.d3.csv(file1, function(err, rows){
		res = draw(err, rows);
		res[1].title = file1;
		Plotly.newPlot('left', res[0], res[1]);
	})

	Plotly.d3.csv(file2, function(err, rows){
		res = draw(err, rows);
		res[1].title = file2;
		Plotly.newPlot('right', res[0], res[1]);
	})
}
