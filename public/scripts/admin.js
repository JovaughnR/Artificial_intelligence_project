const port = 3001;
const host = `http://127.0.0.1:${port}`;

// DOM Elements
const staffAccountLink = document.getElementById("staffAccount");
const addModulesLink = document.getElementById("addModules");

const moduleForm = document.getElementById("moduleForm");
const staffForm = document.getElementById("staffForm");

const logoutButton = document.getElementById("logout");
const staffSection = document.getElementById("staff");
const modulesSection = document.getElementById("registerModule");

const userName = document.getElementById("adminName");

// Helper: Display smooth notifications
function showNotification(message, type = "success") {
	const notification = document.createElement("div");
	notification.className = `notification ${type}`;
	notification.innerText = message;

	document.body.appendChild(notification);

	setTimeout(() => {
		notification.remove();
	}, 3000); // Auto-remove after 3 seconds
}

// Section Visibility Handlers
function toggleVisibility(sectionToShow, sectionToHide) {
	sectionToShow.classList.remove("hidden");
	sectionToShow.classList.add("visible");

	sectionToHide.classList.remove("visible");
	sectionToHide.classList.add("hidden");
}

function closeModulePortal() {
	modulesSection.classList.remove("visible");
	modulesSection.classList.add("hidden");
}

function closeStaffPortal() {
	staffSection.classList.remove("visible");
	staffSection.classList.add("hidden");
}

function toggleStaffSection() {
	toggleVisibility(staffSection, modulesSection);
}

function toggleModuleSection() {
	toggleVisibility(modulesSection, staffSection);
}

// Event Listeners for Navigation Links
staffAccountLink.addEventListener("click", toggleStaffSection);
addModulesLink.addEventListener("click", toggleModuleSection);

// Fetch User Details on Load
(async function fetchUserDetails() {
	try {
		const response = await fetch(`${host}/`, {
			method: "GET",
			credentials: "include",
		});
		if (response.ok) {
			const data = await response.json();
			userName.innerHTML = data.name;
		} else if (response.status === 401) {
			window.location.replace("/public/login.html");
		}
	} catch (error) {
		console.error("Error fetching user details:", error);
		showNotification("Failed to load user details.", "error");
	}
})();

// Logout Function
async function signOut() {
	try {
		const response = await fetch(`${host}/logout`, {
			method: "GET",
			credentials: "include",
		});
		if (response.ok) {
			window.location.replace("/public/login.html");
		} else {
			showNotification("Failed to log out. Please try again.", "error");
		}
	} catch (error) {
		showNotification("Logout failed due to a network error.", "error");
	}
}
logoutButton.addEventListener("click", signOut);

// Create Staff Account
async function createStaffAccount(event) {
	event.preventDefault();
	// Validate form
	const request = validateStaffForm(staffForm);
	if (!request) return;

	try {
		const response = await fetch(`${host}/register`, {
			method: "POST",
			body: JSON.stringify(request),
			headers: { "Content-Type": "application/json" },
		});

		if (response.ok) {
			showNotification("Staff account was successfully created!");
			staffForm.reset();
		} else {
			showNotification("Failed to create staff account.", "error");
		}
	} catch (error) {
		console.error("Error creating staff account:", error);
		showNotification("An error occurred. Please try again.", "error");
	}
}
staffForm.addEventListener("submit", createStaffAccount);

// Add New Module
async function addNewModule(event) {
	event.preventDefault();

	// Validate form
	const request = validateModuleForm(moduleForm);
	if (!request) return;

	try {
		const response = await fetch(`${host}/admin-add-module`, {
			method: "POST",
			body: JSON.stringify(request),
			headers: { "Content-Type": "application/json" },
		});

		if (response.ok) {
			showNotification("Module was successfully added!");
			moduleForm.reset();
		} else {
			showNotification("Failed to add module.", "error");
		}
	} catch (error) {
		console.error("Error adding new module:", error);
		showNotification("An error occurred. Please try again.", "error");
	}
}
moduleForm.addEventListener("submit", addNewModule);

function showError(input, message) {
	const formGroup = input.closest(".form-group"); // Scoped to the closest form group
	let errorElement = formGroup.querySelector(".error-message");

	if (!errorElement) {
		errorElement = document.createElement("span");
		errorElement.className = "error-message";
		formGroup.appendChild(errorElement);
	}
	errorElement.innerText = message; // Update or set the message
}

// Utility function to clear error messages
function clearError(input) {
	const formGroup = input.closest(".form-group");
	const errorElement = formGroup.querySelector(".error-message");

	if (errorElement) {
		errorElement.remove();
	}
}

// Staff Form Validation
function validateStaffForm(formElement) {
	let isValid = true;

	const firstName = formElement.querySelector("#firstName");
	const lastName = formElement.querySelector("#lastName");
	const staffId = formElement.querySelector("#newStaffId");
	const email = formElement.querySelector("#email");

	// Regex patterns
	const staffIdPattern = /^[0-9]+$/;
	const emailPattern = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;

	// Clear previous errors
	[firstName, lastName, staffId, email].forEach(clearError);

	// Validate fields
	if (firstName.value.trim() === "") {
		showError(firstName, "First Name is required.");
		isValid = false;
	}
	if (lastName.value.trim() === "") {
		showError(lastName, "Last Name is required.");
		isValid = false;
	}
	if (!staffIdPattern.test(staffId.value.trim())) {
		showError(staffId, "Staff ID must be numeric.");
		isValid = false;
	}
	if (!emailPattern.test(email.value.trim())) {
		showError(email, "Invalid email address.");
		isValid = false;
	}

	const request = {
		fname: firstName.value,
		lname: lastName.value,
		id: staffId.value,
		email: email.value,
		type: "staff",
	};

	return isValid ? request : isValid;
}

// Module Form Validation
function validateModuleForm(formElement) {
	let isValid = true;

	const moduleCode = formElement.querySelector("#moduleCode");
	const moduleName = formElement.querySelector("#moduleName");
	const credits = formElement.querySelector("#credits");

	// Regex pattern
	const creditsPattern = /^[1-4]$/;

	// Clear previous errors
	[moduleCode, moduleName, credits].forEach(clearError);

	// Validate fields
	if (moduleCode.value.trim() === "") {
		showError(moduleCode, "Module Code is required.");
		isValid = false;
	}
	if (moduleName.value.trim() === "") {
		showError(moduleName, "Module Name is required.");
		isValid = false;
	}
	if (!creditsPattern.test(credits.value.trim())) {
		showError(credits, "Credits must be a number between 1 and 4.");
		isValid = false;
	}

	const request = {
		name: moduleName.value,
		code: moduleCode.value,
		credit: credits.value,
	};

	return isValid ? request : isValid;
}
