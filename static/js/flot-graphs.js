/*
	flot-example.js
*/

$(document).ready(init);


function init() {

	// Pie chart
	
	var data = [
	    { label: "IE",  data: 19.5, color: "orange"},
	    { label: "Safari",  data: 4.5, color: "#9bc747"},
	    { label: "Firefox",  data: 36.6, color: "#208ed3"}
	];
	
	$.plot($(".pie"), data, {
        series: {
            pie: { 
                innerRadius: 0.5,
                show: true
            }
        }
	});

	
	// example 1 - basic line graphs
	$.plot($("#flot-example-2"),
	[
			{
				label: "Page views",
				color: "orange",
				shadowSize: 0,
				data: [ [0, 310], [1, 350], [2, 410], [3, 435], [4, 510], [5, 650], [6, 580], [7, 595], [8, 760], [9, 825], [10, 695], [11, 995] ],
				lines: {show: true},
				points: {show: true}
			},
			{
				label: "Visitors",
				color: "#9bc747",
				shadowSize: 0,
				data: [ [0, 110], [1, 250], [2, 220], [3, 290], [4, 310], [5, 420], [6, 390], [7, 415], [8, 470], [9, 525], [10, 495], [11, 595] ],
				lines: {show: true},
				points: {show: true}
			},
			{
				label: "Unique visitors",
				color: "#208ed3",
				shadowSize: 0,
				data: [ [0, 30], [1, 120], [2, 120], [3, 80], [4, 240], [5, 260], [6, 190], [7, 300], [8, 280], [9, 335], [10, 245], [11, 295] ],
				lines: {show: true},
				points: {show: true}	
			}
		],
		{
			xaxis: {
				ticks: [
					[0, "Jan"],
					[1, "Feb"],
					[2, "Mar"],
					[3, "Apr"],
					[4, "May"],
					[5, "Jun"],
					[6, "Jul"],
					[7, "Aug"],
					[8, "Sep"],
					[9, "Oct"],
					[10, "Nov"],
					[11, "Dec"]
				]
			},
			
			grid: {
				borderWidth: 0,
				color: "#aaa",
				clickable: "true"
			}
		}
	);
	
	var d1 = [[1262304000000, 0], [1264982400000, 100], [1267401600000, 140], [1270080000000, 200], [1272672000000, 350], [1275350400000, 275], [1277942400000, 200], [1280620800000, 290], [1283299200000, 440], [1285891200000, 560], [1288569600000, 680], [1291161600000, 485]];
	var d3 = [[1262304000000, 30], [1264982400000, 140], [1267401600000, 280], [1270080000000, 340], [1272672000000, 510], [1275350400000, 630], [1277942400000, 400], [1280620800000, 595], [1283299200000, 750], [1285891200000, 820], [1288569600000, 850], [1291161600000, 925]];
    var d2 = [[1262304000000, 220], [1264982400000, 290], [1267401600000, 450], [1270080000000, 435], [1272672000000, 750], [1275350400000, 860], [1277942400000, 680], [1280620800000, 835], [1283299200000, 895], [1285891200000, 980], [1288569600000, 1120], [1291161600000, 1400]];
 
    var data1 = [
        { label: "Page views", data: d1, points: { fillColor: "#9bc747", size: 5 }, color: '#9bc747', shadowSize: 0 },
        { label: "visitors", data: d2, points: { fillColor: "#208ed3", size: 5 }, color: '#208ed3', shadowSize: 0 },
		{ label: "Direct traffic", data: d3, points: { fillColor: "orange", size: 5 }, color: 'orange', shadowSize: 0 }
    ];
 
    $.plot($("#flot-example-1"), data1, {
        xaxis: {
            min: (new Date(2009, 12, 1)).getTime(),
            max: (new Date(2010, 11, 1)).getTime(),
            mode: "time",
            tickSize: [1, "month"],
            monthNames: ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"],
            tickLength: 0,
            axisLabel: 'Month',
            axisLabelUseCanvas: true
        },
        yaxis: {
            axisLabel: 'Amount',
            axisLabelUseCanvas: true
        },
        series: {
            lines: {
                show: true, fill: true
            },
            points: {
                show: true
            },
        },
        grid: {
            borderWidth: 0
        },
        legend: {
            labelBoxBorderColor: "none"
        }
    });
    
    $.plot($("#flot-example-1"),
	[
			{
				label: "Page views",
				color: "orange",
				shadowSize: 0,
				data: [ [0, 310], [1, 350], [2, 410], [3, 435], [4, 510], [5, 650], [6, 580], [7, 595], [8, 760], [9, 825], [10, 695], [11, 995] ],
				lines: {show: true},
				points: {show: true}
			},
			{
				label: "Visitors",
				color: "#9bc747",
				shadowSize: 0,
				data: [ [0, 110], [1, 250], [2, 220], [3, 290], [4, 310], [5, 420], [6, 390], [7, 415], [8, 470], [9, 525], [10, 495], [11, 595] ],
				lines: {show: true},
				points: {show: true}
			},
			{
				label: "Unique visitors",
				color: "#208ed3",
				shadowSize: 0,
				data: [ [0, 30], [1, 120], [2, 120], [3, 80], [4, 240], [5, 260], [6, 190], [7, 300], [8, 280], [9, 335], [10, 245], [11, 295] ],
				lines: {show: true},
				points: {show: true}	
			}
		],
		{
			xaxis: {
				ticks: [
					[0, "Jan"],
					[1, "Feb"],
					[2, "Mar"],
					[3, "Apr"],
					[4, "May"],
					[5, "Jun"],
					[6, "Jul"],
					[7, "Aug"],
					[8, "Sep"],
					[9, "Oct"],
					[10, "Nov"],
					[11, "Dec"]
				]
			},
			
			grid: {
				borderWidth: 0,
				color: "#aaa",
				clickable: "true"
			}
		}
	);
	
	var d1 = [[1262304000000, 0], [1264982400000, 100], [1267401600000, 140], [1270080000000, 200], [1272672000000, 350], [1275350400000, 275], [1277942400000, 200], [1280620800000, 290], [1283299200000, 440], [1285891200000, 560], [1288569600000, 680], [1291161600000, 485]];
	var d3 = [[1262304000000, 30], [1264982400000, 140], [1267401600000, 280], [1270080000000, 340], [1272672000000, 510], [1275350400000, 630], [1277942400000, 400], [1280620800000, 595], [1283299200000, 750], [1285891200000, 820], [1288569600000, 850], [1291161600000, 925]];
    var d2 = [[1262304000000, 220], [1264982400000, 290], [1267401600000, 450], [1270080000000, 435], [1272672000000, 750], [1275350400000, 860], [1277942400000, 680], [1280620800000, 835], [1283299200000, 895], [1285891200000, 980], [1288569600000, 1120], [1291161600000, 1400]];
 
    var data1 = [
        { label: "Page views", data: d1, points: { fillColor: "#9bc747", size: 5 }, color: '#9bc747', shadowSize: 0 },
        { label: "visitors", data: d2, points: { fillColor: "#208ed3", size: 5 }, color: '#208ed3', shadowSize: 0 },
		{ label: "Direct traffic", data: d3, points: { fillColor: "orange", size: 5 }, color: 'orange', shadowSize: 0 }
    ];
 
    $.plot($("#flot-example-1"), data1, {
        xaxis: {
            min: (new Date(2009, 12, 1)).getTime(),
            max: (new Date(2010, 11, 1)).getTime(),
            mode: "time",
            tickSize: [1, "month"],
            monthNames: ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"],
            tickLength: 0,
            axisLabel: 'Month',
            axisLabelUseCanvas: true
        },
        yaxis: {
            axisLabel: 'Amount',
            axisLabelUseCanvas: true
        },
        series: {
            lines: {
                show: true, fill: true
            },
            points: {
                show: true
            },
        },
        grid: {
            borderWidth: 0
        },
        legend: {
            labelBoxBorderColor: "none"
        }
    });
}