document.addEventListener("DOMContentLoaded", () => {
	const videoAuth = document.getElementById("video-auth");
	const canvasAuth = document.getElementById("canvas-auth");
	const overlayAuth = document.getElementById("overlay-auth");
	const overlayCtx = overlayAuth.getContext("2d");
	const authButton = document.getElementById("auth-button");
	const authMessage = document.getElementById("auth-message");

	let authAnalysisInterval = null;

	const startAuthAnalysis = () => {
		if (authAnalysisInterval) return;
		authButton.textContent = "Parar Análise";
		authMessage.textContent = "Analisando...";
		authMessage.className = "message";

		authAnalysisInterval = setInterval(async () => {
			const imageData = takePicture(videoAuth, canvasAuth);
			try {
				const response = await fetch("/analyze_frame", {
					method: "POST",
					headers: { "Content-Type": "application/json" },
					body: JSON.stringify({ image: imageData }),
				});
				const result = await response.json();
				let color = "#dc3545"; // Vermelho por padrão

				if (result.status === "GOOD_POSITION") {
					color = "#28a745"; // Verde
					showMessage(authMessage, "Posição ideal! Autenticando...", true);
					stopAuthAnalysis();
					authenticateFace(imageData);
				} else {
					showMessage(authMessage, result.message, false);
				}

				drawStaticOverlay(overlayCtx, overlayAuth, color);
			} catch (error) {
				showMessage(authMessage, "Erro de conexão.", false);
				stopAuthAnalysis();
			}
		}, 1000);
	};

	const stopAuthAnalysis = () => {
		if (authAnalysisInterval) {
			clearInterval(authAnalysisInterval);
			authAnalysisInterval = null;
			authButton.textContent = "Autenticar";
		}
	};

	const authenticateFace = async (imageData) => {
		try {
			const response = await fetch("/authenticate", {
				method: "POST",
				headers: { "Content-Type": "application/json" },
				body: JSON.stringify({ image: imageData }),
			});
			const result = await response.json();
			const isSuccess = result.status === "authenticated";
			const color = isSuccess ? "#28a745" : "#dc3545";
			const nameText = isSuccess ? result.name : "Desconhecido";

			drawStaticOverlay(overlayCtx, overlayAuth, color);
			showMessage(authMessage, `Status: ${nameText}`, isSuccess);
		} catch (error) {
			showMessage(authMessage, "Erro ao autenticar.", false);
		}
	};

	authButton.addEventListener("click", async () => {
		if (authAnalysisInterval) {
			stopAuthAnalysis();
		} else {
			startAuthAnalysis();
		}
	});

	setupCamera(videoAuth, canvasAuth, overlayAuth);
});
