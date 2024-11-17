const userLogin = document.getElementById("user-login");

userLogin.addEventListener("submit", authenticateUser);

async function authenticateUser(event) {
	event.preventDefault();
	const formData = new FormData(event.target);

	const credentials = {
		userID: formData.get("userID"),
		password: formData.get("password"),
	};

	try {
		let data = {
			method: "POST",
			body: JSON.stringify(credentials),
			headers: { "Content-Type": "application/json" },
		};
		let response = await fetch("http://127.0.0.1:3001/login", data);

		if (response.status == 401) {
			const errorMsgHolder = document.getElementById("error-message");
			errorMsgHolder.style.display = "block";
			return;
		}

		if (response.ok) {
			let info = await response.json();
			data = { method: "GET", body: info["key"] };
			response = await fetch("http://127.0.0.1:3001/", data);
			if (response.ok) {
				window.location.href = "/public/index.html";
			}
		}
	} catch (error) {
		console.log("Error from login script:", error);
	}
}
