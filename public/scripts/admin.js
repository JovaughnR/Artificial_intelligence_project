const port = 3001;
const host = `http://127.0.0.1:${port}`;

const staffAccountLink = document.getElementById("staffAccount");
const addModulesLink = document.getElementById("addModules");

// Froms
const moduleForm = document.getElementById("moduleForm");
const staffForm = document.getElementById("staffForm");

const logoutButton = document.getElementById("logout");
const staffSection = document.getElementById("staff");
const modulesSection = document.getElementById("registerModule");

moduleForm.addEventListener("submit", addNewModule);
staffForm.addEventListener("submit", createStaffAccount);

logoutButton.addEventListener("click", signOut);

staffAccountLink.addEventListener("click", () => {
	staffSection.style.display = "flex";
	modulesSection.style.display = "none";
});

addModulesLink.addEventListener("click", () => {
	modulesSection.style.display = "flex";
	staffSection.style.display = "none";
});

(async function () {
	try {
		const response = await fetch(`${host}/`, {
			method: "GET",
			credentials: "include",
		});
		if (response.ok) {
			const data = await response.json();
			userName.innerHTML = data["name"];
		}
		if (response.status === 401) {
			window.location.replace("/public/login.html");
			return;
		}
	} catch (error) {
		console.error(error);
	}
})();

async function signOut() {
	try {
		const response = await fetch(`${host}/logout`, {
			method: "GET",
			credentials: "include",
		});

		if (response.ok) {
			window.location.replace("/public/login.html");
			return;
		}
		// display error message
	} catch (error) {
		alert("Logout failed due to a network error.");
	}
}

async function createStaffAccount(event) {
	event.preventDefault();
	const formData = new FormData(event.target);

	const request = {
		fName: formData.get("firstName"),
		lName: formData.get("lastName"),
		id: formData.get("userID"),
		email: formData.get("email"),
		type: "staff",
	};

	try {
		const res = await fetch(`${host}/register`, {
			method: "POST",
			body: JSON.stringify(request),
			headers: { "Content-Type": "application/json" },
		});

		if (res.ok) {
			alert("Staff account was created!");
			return;
		}
	} catch (error) {
		console.log(error);
	}
}

async function addNewModule(event) {
	event.preventDefault();
	const formData = new FormData(event.target);

	const request = {
		code: formData.get("moduleCode"),
		name: formData.get("moduleName"),
		credit: formData.get("credits"),
	};

	try {
		const res = await fetch(`${host}/admin-add-module`, {
			method: "POST",
			body: JSON.stringify(request),
			headers: { "Content-Type": "application/json" },
		});

		if (res.ok) {
			alert("Module Was added!");
			return;
		}
	} catch (error) {
		console.log(error);
	}
}
