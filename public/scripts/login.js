let userID = null;
const host = "http://192.168.100.219:8000";

// Form references
const forms = {
	userlogin: document.getElementById("userlogin"),
	verificationForm: document.getElementById("verificationForm"),
	resetPass: document.getElementById("resetPass"),
};

// Elements for messages
const errorElement = document.getElementById("error");
const okElement = document.getElementById("ok");

// Event listeners
document.getElementById("forgetPass").addEventListener("click", () => {
	toggleForm("userlogin", "verificationForm");
});

forms.userlogin.addEventListener("submit", authenticateUser);
forms.verificationForm.addEventListener("submit", forgetPassword);
forms.resetPass.addEventListener("submit", updatePassword);

// Function to toggle forms
function toggleForm(formToHide, formToShow) {
	forms[formToHide].classList.add("hidden");
	forms[formToHide].classList.remove("visible");
	forms[formToShow].classList.add("visible");
	forms[formToShow].classList.remove("hidden");
}

// Function to display messages
function showMessage(element, message, duration = 3000) {
	element.classList.remove("hidden");
	element.classList.add("visible");
	element.innerHTML = message;
	setTimeout(() => {
		element.classList.remove("visible");
		element.classList.add("hidden");
	}, duration);
}

function showError(message) {
	showMessage(errorElement, message, 3000);
}

function showOk(message) {
	showMessage(okElement, message, 2500);
}

// Function to authenticate the user
async function authenticateUser(event) {
	event.preventDefault();
	const formData = new FormData(event.target);

	const credentials = {
		userID: formData.get("userID"),
		password: formData.get("password"),
	};

	try {
		const response = await fetch(`${host}/login`, {
			method: "POST",
			body: JSON.stringify(credentials),
			headers: { "Content-Type": "application/json" },
			credentials: "include",
		});

		if (response.ok) {
			const data = await response.json();
			const redirectMap = {
				student: "/student.html",
				staff: "/staff.html",
				admin: "/admin.html",
			};
			window.location.href = redirectMap[data["type"]] || "/login.html";
		} else {
			showError("Incorrect user ID or password");
		}
	} catch (error) {
		showError("Error during login");
		console.error("Login error:", error);
	}
}

// Function to handle forget password
async function forgetPassword(event) {
	event.preventDefault();
	const formData = new FormData(event.target);

	const request = {
		email: formData.get("email"),
		id: formData.get("verificationID"),
	};

	try {
		const response = await fetch(`${host}/forget-password`, {
			method: "POST",
			body: JSON.stringify(request),
			headers: { "Content-Type": "application/json" },
		});

		if (response.ok) {
			userID = request["id"];
			showOk("Verification successful!");
			toggleForm("verificationForm", "resetPass");
		} else if (response.status === 401) {
			showError("Verification failed!");
		}
	} catch (error) {
		showError("Something went wrong");
		console.error("Verification error:", error);
	}
}

// Function to handle password update
async function updatePassword(event) {
	event.preventDefault();
	const formData = new FormData(event.target);

	const passwd = formData.get("pass1");
	const confirmPasswd = formData.get("confirmPass1");

	if (passwd !== confirmPasswd) {
		showError("Passwords do not match");
		return;
	}

	try {
		const response = await fetch(`${host}/authenticate`, {
			method: "POST",
			body: JSON.stringify({ passwd: passwd, id: userID }),
			headers: { "Content-Type": "application/json" },
		});

		if (response.ok) {
			showOk("Password reset successful!");
			toggleForm("resetPass", "userlogin");
		} else {
			showError("Password reset failed!");
		}
	} catch (error) {
		showError("Something went wrong");
		console.error("Password update error:", error);
	}
}
