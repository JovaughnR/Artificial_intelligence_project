const host = "http://192.168.100.219:8000";

const lookup = (id) => document.getElementById(id);

const uploadForm = lookup("uploadForm");
const verifcationForm = lookup("verifactionForm");

uploadForm.addEventListener("submit", saveUser);

let user_id = null;
verifcationForm.addEventListener("submit", verifyUserId);

async function verifyUserId(event) {
	event.preventDefault();
	const formData = new FormData(event.target);

	const userID = formData.get("verificationID");
	console.log("User ID:", userID);
	try {
		const response = await fetch(`${host}/verify-id`, {
			method: "POST",
			body: JSON.stringify({ id: userID }),
			headers: { "Content-Type": "application/json" },
		});
		if (response.status == 200) {
			user_id = userID;
			showOk("Identification number verified");
			uploadForm.style.display = "block";
			verifcationForm.style.display = "none";
		}
		if (response.status == 204) {
			showError("Verification failed");
		}
	} catch (error) {
		console.log(error);
	}
}

async function saveUser(event) {
	event.preventDefault();

	const formData = new FormData(event.target);
	const passwd = formData.get("password");
	const confirmPasswd = formData.get("confirm_password");

	if (passwd !== confirmPasswd) {
		showError("Passwords don't match!");
		return;
	}
	try {
		const res = await fetch(`${host}/authenticate`, {
			method: "POST",
			body: JSON.stringify({ passwd: passwd, id: user_id }),
			headers: { "Content-Type": "application/json" },
		});

		if (res.ok) {
			showOk("Your account was created successfully");
			window.location.href = "/login.html";
		} else {
			const error = await res.json();
			showError("Failed to create account. Try again.");
			console.error("Error:", error.message || "Failed to create account");
		}
	} catch (error) {
		console.error("Network Error:", error);
		alert("Failed to connect to the server.");
	}
}

function showError(message) {
	const errorElement = document.getElementById("error");
	errorElement.classList.remove("hidden");
	errorElement.classList.add("visible");
	errorElement.innerHTML = message;
	setTimeout(() => {
		errorElement.classList.remove("visible");
		errorElement.classList.add("hidden");
	}, 3000);
}

function showOk(message) {
	const okElement = document.getElementById("ok");
	okElement.classList.remove("hidden");
	okElement.classList.add("visible");
	okElement.innerHTML = message;
	setTimeout(() => {
		okElement.classList.remove("visible");
		okElement.classList.add("hidden");
	}, 2500);
}
