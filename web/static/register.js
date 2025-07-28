document.addEventListener("DOMContentLoaded", () => {
	const videoRegister = document.getElementById("video-register");
	const canvasRegister = document.getElementById("canvas-register");
	const overlayRegister = document.getElementById("overlay-register");
	const overlayRegisterCtx = overlayRegister.getContext("2d");
	const registerButton = document.getElementById("register-button");
	const nameInput = document.getElementById("name");
	const registerMessage = document.getElementById("register-message");

	let registerAnalysisInterval = null;

	const startRegisterAnalysis = () => {
		if (registerAnalysisInterval) return;
		registerAnalysisInterval = setInterval(async () => {
			const imageData = takePicture(videoRegister, canvasRegister);
			try {
				const response = await fetch("/analyze_frame", {
					method: "POST",
					headers: { "Content-Type": "application/json" },
					body: JSON.stringify({ image: imageData }),
				});
				const result = await response.json();
				let color = "#dc3545";
				let isGoodPosition = false;

				if (result.status === "GOOD_POSITION") {
					color = "#28a745"; // Verde
					isGoodPosition = true;
				}

				drawStaticOverlay(overlayRegisterCtx, overlayRegister, color);
				showMessage(registerMessage, result.message, isGoodPosition);
				registerButton.disabled = !isGoodPosition || !nameInput.value.trim();
			} catch (error) {
				showMessage(registerMessage, "Erro de conexão.", false);
			}
		}, 1000);
	};

	registerButton.addEventListener("click", async () => {
		const name = nameInput.value.trim();
		if (!name) {
			showMessage(registerMessage, "Por favor, digite um nome.", false);
			return;
		}
		const imageData = takePicture(videoRegister, canvasRegister);
		try {
			const response = await fetch("/register", {
				method: "POST",
				headers: { "Content-Type": "application/json" },
				body: JSON.stringify({ name, image: imageData }),
			});
			const result = await response.json();
			showMessage(
				registerMessage,
				result.message,
				response.ok && result.status === "success"
			);
			if (response.ok) {
				clearInterval(registerAnalysisInterval);
				registerButton.disabled = true;
			}
		} catch (error) {
			showMessage(registerMessage, "Erro ao conectar com o servidor.", false);
		}
	});

	nameInput.addEventListener("input", () => {
		const isNameFilled = nameInput.value.trim() !== "";
		const isPositionGood =
			!registerButton.disabled ||
			(registerMessage.classList.contains("success") &&
				registerMessage.textContent === "Posição ideal!");
		registerButton.disabled = !(isNameFilled && isPositionGood);
	});

	setupCamera(videoRegister, canvasRegister, overlayRegister).then(
		startRegisterAnalysis
	);
});
