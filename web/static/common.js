function takePicture(videoElement, canvasElement) {
	const context = canvasElement.getContext("2d");
	canvasElement.width = videoElement.videoWidth;
	canvasElement.height = videoElement.videoHeight;
	context.drawImage(
		videoElement,
		0,
		0,
		videoElement.videoWidth,
		videoElement.videoHeight
	);
	return canvasElement.toDataURL("image/jpeg");
}

function showMessage(element, text, isSuccess) {
	element.textContent = text;
	element.className = "message";
	if (isSuccess === true) element.classList.add("success");
	else if (isSuccess === false) element.classList.add("error");
}

function createOvalPath(ctx, canvas) {
	const ovalWidth = canvas.width * 0.4;
	const ovalHeight = canvas.height * 0.8;
	const center_x = canvas.width / 2;
	const center_y = canvas.height / 2;
	const axis_x = ovalWidth / 2;
	const axis_y = ovalHeight / 2;
	ctx.beginPath();
	ctx.ellipse(center_x, center_y, axis_x, axis_y, 0, 0, 2 * Math.PI);
	return { center_x, center_y, axis_x, axis_y };
}

function drawStaticOverlay(ctx, canvas, borderColor = "#aaa") {
	ctx.clearRect(0, 0, canvas.width, canvas.height);
	ctx.save();
	ctx.fillStyle = "rgba(0, 0, 0, 0.6)";
	ctx.fillRect(0, 0, canvas.width, canvas.height);
	ctx.globalCompositeOperation = "destination-out";
	createOvalPath(ctx, canvas);
	ctx.fill();
	ctx.restore();
	ctx.strokeStyle = borderColor;
	ctx.lineWidth = 5;
	createOvalPath(ctx, canvas);
	ctx.stroke();
}

async function setupCamera(videoElement, canvasElement, overlayCanvas) {
	try {
		const stream = await navigator.mediaDevices.getUserMedia({ video: true });
		videoElement.srcObject = stream;
		videoElement.onloadedmetadata = () => {
			if (overlayCanvas) {
				const resizeOverlay = () => {
					overlayCanvas.width = videoElement.clientWidth;
					overlayCanvas.height = videoElement.clientHeight;
					drawStaticOverlay(overlayCanvas.getContext("2d"), overlayCanvas);
				};
				resizeOverlay();
				window.addEventListener("resize", resizeOverlay);
			}
		};
	} catch (err) {
		console.error("Erro ao acessar a câmera: ", err);
		alert(
			"Não foi possível acessar a câmera. Por favor, verifique as permissões."
		);
	}
}
