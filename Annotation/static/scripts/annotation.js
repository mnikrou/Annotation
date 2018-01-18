var canvas, ctx, drawCanvas, drawCtx, selectCanvas, selectCtx,
	selectedPoint = null,
	drawing = false,
	lastX = 0,
	lastY = 0,
	startX, startY, lineThickness = 2,
	lineColor = "yellow",
	selectStartX, selectStartY, selectMouseX, selectMouseY, rect = null,
	select = false,
	drawingMode = true,
	selectMode = false,
	edges = [],
	snappingDistance = 10,
	shiftClick, drawCanvasOffsetLeft, drawCanvasOffsetTop, selectCanvasOffsetLeft, selectCanvasOffsetTop;

function Point(x, y) {
	this.x = x;
	this.y = y;
}

function AnnotationObject(name, edges) {
	//this.name = name;
	this.edges = edges;
}

function Line(startPoint, endPoint) {
	this.start = startPoint;
	this.end = endPoint;
}

var res = window.devicePixelRatio || 1;

function initCanvas(imageUrl) {
	edges = [];
	drawCanvas = document.getElementById("drawCanvas");
	dvCanvasContainer = document.getElementById("dvCanvasContainer");
	drawCtx = drawCanvas.getContext("2d");
	drawCanvas.width = 600;
	drawCanvas.height = 400;
	drawCanvas.width *= res;
	drawCanvas.height *= res;
	dvCanvasContainer.setAttribute("style", "width:" + drawCanvas.width + "px;height:" + drawCanvas.height + "px;display: inline-block;vertical-align: top;");
	drawCanvas.style.backgroundImage = "url('" + imageUrl + "')";
	drawCanvas.style.backgroundRepeat = "no-repeat";

	// selectCanvas = document.getElementById("selectCanvas");
	// selectCtx = selectCanvas.getContext("2d");
	// selectCanvas.width = 600;
	// selectCanvas.height = 400;
	// selectCanvas.width *= res;
	// selectCanvas.height *= res;

	drawCanvas.style.marginLeft = (-1 * (drawCanvas.width / 2)) + 15 + "px";
	// selectCanvas.style.marginLeft = (-1 * (selectCanvas.width / 2)) + 15 + "px";

	drawCtx.clearRect(0, 0, drawCanvas.width, drawCanvas.height);

	reOffset();

	window.onscroll = function (e) {
		reOffset();
	}
	window.onresize = function (e) {
		reOffset();
	}

	drawCanvas.onmousedown = function (e) {
		drawCanvasHandleMouse('down', e);
	};

	drawCanvas.onmousemove = function (e) {
		drawCanvasHandleMouse('move', e);
	}

	drawCanvas.addEventListener('contextmenu', function (e) {
		e.preventDefault();
	});

	// selectCanvas.onmousedown = function (e) {
	// 	selectCanvasHandleMouse('down', e);
	// };

	// selectCanvas.onmousemove = function (e) {
	// 	selectCanvasHandleMouse('move', e);
	// }

	// selectCanvas.onmouseup = function (e) {
	// 	selectCanvasHandleMouse('up', e);
	// }

	// selectCanvas.onmouseout = function (e) {
	// 	selectCanvasHandleMouse('out', e);
	// }

	shiftClick = jQuery.Event("click");
	shiftClick.shiftKey = true;
	$("#drawCanvas").trigger(shiftClick);

	$('#fileInput1').on('change', function (e) {
		var file = e.target.files[0];
		if (!file) {
			return;
		}
		var reader = new FileReader();
		reader.onload = function (e) {
			var contents = e.target.result;
			var arr = JSON.parse(contents);
			edges = arr.edges;
			updateCanvas();
		};
		reader.readAsText(file);
	});

	$('#btnOpenFile1').on('click', function () {
		$('#fileInput1').trigger('click');
	});
}

function drawCanvasHandleMouse(act, e) {
	e.preventDefault();
	e.stopPropagation();

	switch (act) {
		case 'down':
			switch (e.button) {
				case 0: // left click
					if (!selectMode) {
						if (startX && startY) {
							sPoint = new Point(startX, startY);
							ePoint = new Point(lastX, lastY);
							line = new Line(sPoint, ePoint);
							edges.push(line);
							startX = lastX;
							startY = lastY;
						} else {
							startX = e.clientX - drawCanvasOffsetLeft;
							startY = e.clientY - drawCanvasOffsetTop;
							var p = new Point(startX, startY);
							var res = JSON.parse(validateNewPoint(p));
							if (!res.result) {
								resetPoints();
								alert('The new line should be connected to graph!');
							} else {
								if (res.point) {
									startX = res.point.x;
									startY = res.point.y;
								}
								drawing = true;
							}
						}
					}
					else {
						selectStartX = e.clientX - drawCanvasOffsetLeft;
						selectStartY = e.clientY - drawCanvasOffsetTop;
						var p = new Point(selectStartX, selectStartY);
						selectPoint(p);
					}
					break;
				case 2: // middle click
					if (!selectMode) {
						drawing = false;
						/*
						 * sPoint = new Point(startX, startY); ePoint = new Point(lastX,
						 * lastY); line = new Line(sPoint, ePoint); if (ePoint !=
						 * sPoint) shape.push(line);
						 */
						resetPoints();
					}
					break;
				case 3: // right
					if (!selectMode) {
						drawing = false;
						/*
						 * sPoint = new Point(startX, startY); ePoint = new Point(lastX,
						 * lastY); line = new Line(sPoint, ePoint); if (ePoint !=
						 * sPoint) shape.push(line);
						 */
						resetPoints();
					}
					break;
			}
			break;
		case 'move':
			if (!selectMode) {
				if (drawing) {
					lastX = e.clientX - drawCanvasOffsetLeft;;
					lastY = e.clientY - drawCanvasOffsetTop;
					updateCanvas()
					sp = new Point(startX, startY);
					ep = new Point(lastX, lastY)
					draw(sp, ep);
				} else {
					if (e.shiftKey) {
						updateCanvas();
						pX = e.clientX - drawCanvasOffsetLeft;
						pY = e.clientY - drawCanvasOffsetTop;
						var p = new Point(pX, pY);
						var res = JSON.parse(validateNewPoint(p));
						if (!res.result) { }
					} else {
						updateCanvas();
					}
				}
			}
			break;
		default:
			break;
	}
}

// function selectCanvasHandleMouse(act, e) {
// 	e.preventDefault();
// 	e.stopPropagation();
// 	switch (act) {
// 		case 'down':
// 			selectStartX = parseInt(e.clientX - selectCanvasOffsetLeft);
// 			selectStartY = parseInt(e.clientY - selectCanvasOffsetTop);
// 			validateNewPoint(new Point(selectStartX, selectStartY))
// 			//selectPoint();
// 			//select = true;
// 			break;
// 		case 'up':
// 			// selectMouseX = parseInt(e.clientX - selectCanvasOffsetLeft);
// 			// selectMouseY = parseInt(e.clientY - selectCanvasOffsetTop);
// 			// select = false;
// 			// selectCtx.clearRect(0, 0, selectCanvas.width, selectCanvas.height);
// 			// endSelect();
// 			break;
// 		case 'out':
// 			// selectMouseX = parseInt(e.clientX - selectCanvasOffsetLeft);
// 			// selectMouseY = parseInt(e.clientY - selectCanvasOffsetTop);
// 			// select = false;
// 			break;
// 		case 'move':
// 			// if (select) {
// 			// 	selectMouseX = parseInt(e.clientX - selectCanvasOffsetLeft);
// 			// 	selectMouseY = parseInt(e.clientY - selectCanvasOffsetTop);
// 			// 	var width = selectMouseX - selectStartX;
// 			// 	var height = selectMouseY - selectStartY;
// 			// 	rect = {
// 			// 		p1: new Point(selectStartX, selectStartY),
// 			// 		p2: new Point(selectStartX + width, selectStartY),
// 			// 		p3: new Point(selectStartX, selectStartY + height),
// 			// 		p4: new Point(selectStartX + width, selectStartY + height)
// 			// 	}

// 			// 	selectCtx.clearRect(0, 0, selectCanvas.width, selectCanvas.height);
// 			// 	selectCtx.strokeStyle = "lightgray";
// 			// 	selectCtx.lineWidth = 3;
// 			// 	selectCtx.strokeRect(selectStartX, selectStartY, width, height);
// 			// }
// 			break;
// 		default:
// 			break;
// 	}
// }

function updateCanvas() {
	drawCtx.clearRect(0, 0, drawCanvas.width, drawCanvas.height);
	edges.forEach(function (line) {
		draw(line.start, line.end);
	});
}

function draw(sPoint, ePoint) {
	drawCtx.beginPath();
	drawCtx.moveTo(sPoint.x, sPoint.y);
	drawCtx.lineTo(ePoint.x, ePoint.y);
	drawCtx.strokeStyle = lineColor;
	drawCtx.lineWidth = lineThickness;
	drawCtx.closePath();
	drawCtx.stroke();
	drawCtx.beginPath();
	drawCtx.arc(sPoint.x, sPoint.y, 3, 0, 2 * Math.PI, false);
	drawCtx.arc(ePoint.x, ePoint.y, 3, 0, 2 * Math.PI, false);
	drawCtx.fillStyle = lineColor;
	drawCtx.fill();
}

function clearCanvas() {
	edges = [];
	drawCtx.clearRect(0, 0, drawCanvas.width, drawCanvas.height);
}

function resetPoints() {
	startX = null;
	startY = null;
	lastX = null;
	lastY = null;
}

function calculateDistance(point1, point2) {
	var a = point1.x - point2.x;
	var b = point1.y - point2.y;
	return Math.sqrt(a * a + b * b);
}

function validateNewPoint(point) {
	var result = '{"result":false,"point":""}';
	var sPoint = null;
	if (edges && edges.length > 0) {
		edges.forEach(function (line) {
			disS = calculateDistance(line.start, point);
			disE = calculateDistance(line.end, point);
			if (disS <= snappingDistance) {
				result = '{"result":true,"point":' +
					JSON.stringify(line.start) + '}';
				sPoint = line.start;
				return true;
			} else if (disE <= snappingDistance) {
				result = '{"result":true,"point":' +
					JSON.stringify(line.end) + '}';
				sPoint = line.end;
				return true;
			}
		});
		highLightPoint(sPoint, '#99d9ea')
		return result;
	}
	return '{"result":true,"point":""}';
}

function highLightPoint(point, color) {
	if (point) {
		drawCtx.beginPath();
		drawCtx.arc(point.x, point.y, 7, 0, 2 * Math.PI, false);
		drawCtx.fillStyle = color;
		drawCtx.fill();
	}
}

function saveFile() {
	var ann = new AnnotationObject("test", edges);
	var data = JSON.stringify(ann);

	var csvContent = "data:text/csv;charset=utf-8,";
	csvContent += data;
	var encodedUri = encodeURI(csvContent);
	var link = document.createElement("a");
	link.setAttribute("href", encodedUri);
	link.setAttribute("download", "cdata.csv");
	document.body.appendChild(link);
	link.click();
}

function beginSelectDraw() {
	if (drawingMode) {
		selectMode = true;
		drawingMode = false;
		$("#btnDelete").css("visibility", "visible");
		$("#btnSelectDraw").val('Draw');
	} else {
		selectMode = false;
		drawingMode = true;
		$("#btnSelectDraw").val('Select');
		$("#btnDelete").css("visibility", "hidden");
	}
}

function selectPoint(point) {
	updateCanvas();
	var sPoint = null;
	var edgeCount = 0;
	if (edges && edges.length > 0) {
		edges.forEach(function (line) {
			disS = calculateDistance(line.start, point);
			disE = calculateDistance(line.end, point);
			if (disS <= snappingDistance) {
				sPoint = line.start;
				edgeCount++;
			} else if (disE <= snappingDistance) {
				sPoint = line.end;
				edgeCount++;
			}
		});
		if (sPoint && (edgeCount == 1)) {
			highLightPoint(sPoint, '#ff0000');
			selectedPoint = sPoint;
		}

	}
}

function reOffset() {
	var bb = drawCanvas.getBoundingClientRect();
	drawCanvasOffsetLeft = bb.left;
	drawCanvasOffsetTop = bb.top;
	// var bbs = selectCanvas.getBoundingClientRect();
	// selectCanvasOffsetLeft = bbs.left;
	// selectCanvasOffsetTop = bbs.top;
}

function deletePoint(point) {
	if (edges && edges.length > 0) {
		for (i = 0; i < edges.length; i++) {
			if (edges[i].start == point || edges[i].end == point)
				edges.splice(i, 1);
		}
		updateCanvas();
	}
}