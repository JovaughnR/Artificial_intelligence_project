const userLogin = document.getElementById("user-login");
userLogin.addEventListener("submit", authenticateUser);

async function authenticateUser(event) {
	event.preventDefault();
	const formData = new FormData(event.target);

	const credential = {
		userID: formData.get("userID"),
		password: formData.get("password"),
	};

	try {
		const response = await fetch("http://127.0.0.1:3001/login", {
			method: "POST",
			body: JSON.stringify(credential),
			headers: { "Content-Type": "application/json" },
			credentials: "include",
		});

		if (response.ok) {
			const data = await response.json();
			if (data["type"] === "student")
				window.location.href = "/public/student.html";
			else if (data["type"] === "staff")
				window.location.href = "/public/staff.html";
			else if (data["type"] === "admin")
				window.location.href = "/public/admin.html";
			return;
		}
		document.getElementById("error-message").style.display = "block";
	} catch (error) {
		alert("Errro while logging");
		console.error("Error during login:", error);
	}
}
