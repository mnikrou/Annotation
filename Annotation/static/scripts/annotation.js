var canvas, ctx, drawCanvas, drawCtx, selectCanvas, selectCtx, imageId, isExpertUser, backgroundImg, training_nodes_count,
	selectedPoint = null,
	drawing = false, saved = false,
	lastX = 0, lastY = 0,
	startX, startY, lineThickness = 2,
	lineColor = "yellow",
	selectStartX, selectStartY, selectMouseX, selectMouseY, rect = null,
	select = false,
	drawingMode = true,
	selectMode = false,
	edges = [],
	snappingDistance = 5,
	shiftClick, drawCanvasOffsetLeft, drawCanvasOffsetTop, selectCanvasOffsetLeft, selectCanvasOffsetTop;

function Point(x, y) {
	this.x = x;
	this.y = y;
}

function pointsAreEqual(p1, p2) {
	if (p1 && p2) {
		if (p1.x == p2.x && p1.y == p2.y)
			return true;
		else
			return false;
	}
	else
		return false;
}

function AnnotationObject(edges) {
	this.edges = edges;
}

function Line(startPoint, endPoint) {
	this.start = startPoint;
	this.end = endPoint;
}

function initCanvas(data) {
	resetPoints();
	drawing = false;
	jsonResponse = JSON.parse(data);
	console.log(jsonResponse);

	imageId = jsonResponse.imageId;
	isExpertUser = jsonResponse.isExpertUser;
	edges = [];
	drawCanvas = document.getElementById("drawCanvas");
	drawCtx = drawCanvas.getContext("2d");
	var res = window.devicePixelRatio || 1;
	drawCanvas.width = jsonResponse.imgWidth;
	drawCanvas.height = jsonResponse.imgHeight;
	saved = false;
	$("#pointsUsed").text("Number of points used so far : 0");
	//drawCanvas.width *= res;
	//drawCanvas.height *= res;
	//drawCanvas.style.backgroundImage = "url('" + imageUrl + "')";
	//drawCanvas.style.backgroundRepeat = "no-repeat";
	//drawCanvas.style.backgroundSize = "cover";
	drawCtx.clearRect(0, 0, drawCanvas.width, drawCanvas.height);

	backgroundImg = new Image();
	backgroundImg.onload = function () {
		if (jsonResponse.annotation) {
			var arr = JSON.parse(jsonResponse.annotation);
			edges = arr.edges;
			if (edges && edges.length != 0)
				saved = true;
			updateCanvas();
		}
		else {
			drawCtx.drawImage(backgroundImg, 0, 0, drawCanvas.width, drawCanvas.height);
		}
	};
	backgroundImg.src = jsonResponse.imageUrl;

	training_nodes_count = jsonResponse.nodesCount
	$("#pointsCount").text("Number of points : " + training_nodes_count);

	reOffset();

	if (isExpertUser)
		lineColor = "#ff6600";
	else
		lineColor = "yellow";

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

	shiftClick = jQuery.Event("click");
	shiftClick.shiftKey = true;
	$("#drawCanvas").trigger(shiftClick);
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
							var sPoint = new Point(startX, startY);
							var ePoint = new Point(lastX, lastY);
							var endPointExists = pointExists(ePoint);
							if (endPointExists) {
								alert('Cycles are not allowed!');
							}
							else {
								line = new Line(sPoint, ePoint);
								edges.push(line);
								startX = lastX;
								startY = lastY;
							}
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

						resetPoints();
					}
					break;
				case 3: // right
					if (!selectMode) {
						drawing = false;

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
					var sp = new Point(startX, startY);
					var ep = new Point(lastX, lastY)
					draw(sp, ep);
				} else {
					if (e.shiftKey) {
						updateCanvas();
						var pX = e.clientX - drawCanvasOffsetLeft;
						var pY = e.clientY - drawCanvasOffsetTop;
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

function updateCanvas() {
	drawCtx.clearRect(0, 0, drawCanvas.width, drawCanvas.height);
	drawCtx.drawImage(backgroundImg, 0, 0, drawCanvas.width, drawCanvas.height);
	edges.forEach(function (line) {
		draw(line.start, line.end);
	});
	var pointUsed = 0;
	if (edges.length > 0)
		pointUsed = edges.length + 1;
	$("#pointsUsed").text("Number of points used so far : " + pointUsed);
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
	drawCtx.drawImage(backgroundImg, 0, 0, drawCanvas.width, drawCanvas.height);
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

function save() {
	updateCanvas();
	var ann = new AnnotationObject(edges);
	var data = JSON.stringify(ann);

	var csvContent = "data:text/csv;charset=utf-8,";
	csvContent += data;

	var imageUrl = "";
	imageUrl = drawCanvas.toDataURL();

	$.ajax({
		type: 'POST',
		url: $('meta[name="ajaxUrl"]').attr('content') + '/save_annotation/',
		data: {
			'image_id': imageId,
			'annotation_json': data,
			'image_url': imageUrl,
			'training_nodes_count': training_nodes_count,
			csrfmiddlewaretoken: $('meta[name="csrf-token"]').attr('content'),
		},
		success: function (data) {
			if (data == "") {
				alert('Successfully Saved!');
				saved = true;
			}
			else {
				alert(data);
				saved = false;
			}
		},
		error: function (xhr, textStatus, errorThrown) {
			alert("error: " + xhr + "-" + textStatus + "-" + errorThrown);
		}
	});
}

function beginSelectDraw() {
	if (drawingMode) {
		selectMode = true;
		drawingMode = false;
		$("#btnDelete").css("display", "unset");
		$("#btnSelectDraw").val('Draw');
	} else {
		selectMode = false;
		drawingMode = true;
		$("#btnSelectDraw").val('Select');
		$("#btnDelete").css("display", "none");
	}
}

function selectPoint(point) {
	updateCanvas();
	selectedPoint = null;
	var sPoint = null;
	var connectedEdgeCount = 0;
	var disS = 0;
	var disE = 0;
	if (edges && edges.length > 0) {
		edges.forEach(function (line) {
			disS = calculateDistance(line.start, point);
			disE = calculateDistance(line.end, point);
			if (disS <= snappingDistance) {
				if (connectedEdgeCount > 0) {
					if (pointsAreEqual(sPoint, line.start))
						connectedEdgeCount++;
				}
				else
					connectedEdgeCount++;
				sPoint = line.start;
			} else if (disE <= snappingDistance) {
				if (connectedEdgeCount > 0) {
					if (pointsAreEqual(sPoint, line.end))
						connectedEdgeCount++;
				}
				else
					connectedEdgeCount++;
				sPoint = line.end;
			}
		});
		if (sPoint && (connectedEdgeCount == 1)) {
			highLightPoint(sPoint, '#ff0000');
			selectedPoint = sPoint;
		}

	}
}

function reOffset() {
	var bb = drawCanvas.getBoundingClientRect();
	drawCanvasOffsetLeft = bb.left;
	drawCanvasOffsetTop = bb.top;
}

function deletePoint() {
	if (edges && edges.length > 0) {
		for (i = 0; i < edges.length; i++) {
			if (edges[i].start == selectedPoint || edges[i].end == selectedPoint)
				edges.splice(i, 1);
		}
		updateCanvas();
	}
}

function pointExists(point) {
	res = false;
	if (edges && edges.length > 0) {
		edges.forEach(function (line) {
			if ((line.start.x == point.x && line.start.y == point.y) || (line.end.x == point.x && line.end.y == point.y)) {
				res = true;
			}
		});
	}
	return res;
}