const host = `http://192.168.100.219:8000`;

// Utility for element lookup
const lookup = (id) => document.getElementById(id);

// DOM Elements
const logoutButton = lookup("logout");
const userName = lookup("staffName");
const recordTable = lookup("record-table");
const chatBot = lookup("chat-bot");
const chatIcon = lookup("chat-icon");
const responseArea = lookup("responses");
const botResponse = lookup("p1");
const gpaDefault = lookup("defaulted_gpa");
const userInput = lookup("user-input");

const links = {
	records: lookup("retrieveRecordsLink"),
	registerStudent: lookup("registerStudentLink"),
	addModule: lookup("addModuleDetailLink"),
	gpaThreshold: lookup("gpaThresholdLink"),
	semesterEnd: lookup("semesterEnd"),
};

const sections = {
	admin: lookup("admin"),
	registerStudent: lookup("registerStudent"),
	addModuleDetails: lookup("addModuleDetails"),
	results: lookup("results"),
	gpaThreshold: lookup("gpaThreshold"),
	endSemester: lookup("endSemester"),
};

const forms = {
	admin: lookup("adminForm"),
	module: lookup("moduleForm"),
	register: lookup("registerForm"),
	endSemester: lookup("semEndForm"),
};

function closePortal(section) {
	sections[section].classList.add("hidden");
	sections[section].classList.remove("visible");
}

// Event Listeners
logoutButton.addEventListener("click", signOut);
forms.admin.addEventListener("submit", retrieveStudentRecords);
forms.register.addEventListener("submit", registerNewStudent);
forms.module.addEventListener("submit", addNewModuleDetails);
forms.endSemester.addEventListener("submit", sendAlerts);
// forms.gpaThreshold.addEventListener("submit", updateGPAthreshold);

links.records.addEventListener("click", () => toggleSection("admin"));
links.registerStudent.addEventListener("click", () =>
	toggleSection("registerStudent")
);
links.addModule.addEventListener("click", () =>
	toggleSection("addModuleDetails")
);
links.gpaThreshold.addEventListener("click", () =>
	toggleSection("gpaThreshold")
);

links.semesterEnd.addEventListener("click", () => toggleSection("endSemester"));

chatBot.addEventListener("click", () => toggleChat(true));
chatIcon.addEventListener("click", () => toggleChat(false));
userInput.addEventListener("keypress", (e) => {
	if (e.key === "Enter") responseBot();
});

// Functions

// Toggle sections visibility
function toggleSection(sectionKey) {
	console.log(`Switching to section: ${sectionKey}`);
	Object.keys(sections).forEach((key) => {
		// console.log(sections[key]);
		// console.log(sections[key].classList);
		if (sectionKey == key) {
			sections[key].classList.remove("hidden");
			sections[key].classList.add("visible");
		} else {
			sections[key].classList.add("hidden");
			sections[key].classList.remove("visible");
		}
	});
}

// Toggle chat visibility
function toggleChat(showChat) {
	responseArea.style.display = showChat ? "grid" : "none";
	chatBot.style.display = showChat ? "none" : "block";
}

// IIFE: Auto-fetch logged-in user details
(async function fetchUserDetails() {
	try {
		const response = await fetch(`${host}/`, {
			method: "GET",
			credentials: "include",
		});

		if (response.ok) {
			const data = await response.json();
			userName.innerHTML = data["name"];
		} else if (response.status === 401) {
			window.location.replace("/login.html");
		}
	} catch (error) {
		console.error("Error fetching user details:", error);
	}
})();

// IIFE: Fetch default GPA threshold
(async function fetchDefaultGPA() {
	try {
		const response = await fetch(`${host}/gpa-threshold`, {
			method: "GET",
		});

		if (response.ok) {
			const data = await response.json();
			const gpaText = `<span style="color:green;">${data["GPA"]}</span>`;
			gpaDefault.innerHTML = `Default GPA: [ ${gpaText} ]`;
		}
	} catch (error) {
		systemError("Error fetching default GPA threshold.");
		console.error(error);
	}
})();

// Fetch and display student records
async function retrieveStudentRecords(event) {
	event.preventDefault();

	const formData = new FormData(event.target);
	const requestData = {
		studID: formData.get("studentId"),
		year: formData.get("academicYear"),
		targetGPA: formData.get("desiredGPA"),
	};

	if (!(requestData.studID || requestData.targetGPA)) {
		return systemError("Either Student ID or Target GPA is required.");
	}

	const requestConfig = {
		method: "POST",
		body: JSON.stringify(requestData),
		headers: { "Content-Type": "application/json" },
	};

	try {
		if (requestData.studID) {
			await displayRecords(requestConfig);
		} else {
			await displayTargetRecords(requestConfig);
		}
	} catch (error) {
		systemError("Failed to retrieve records.");
		console.error(error);
	}
}

// Display all student records
async function displayRecords(requestConfig) {
	const endpoint = `${host}/staff/stud-record`;
	try {
		const response = await fetch(endpoint, requestConfig);

		if (response.status === 204) {
			return systemError("No records found for the given year.");
		}

		if (response.ok) {
			const data = await response.json();
			while (recordTable.rows.length > 1) {
				recordTable.deleteRow(1);
			}
			const row = document.createElement("tr");
			for (let res of data["student"]) {
				const cell = document.createElement("td");
				cell.textContent = res;
				row.appendChild(cell);
			}
			recordTable.appendChild(row);

			console.log("student:", data["student"]);
			toggleSection("results");
		}
	} catch (error) {
		systemError("Error fetching student records.");
		console.error(error);
	}
}

// Display target student records
async function displayTargetRecords(requestConfig) {
	try {
		const response = await fetch(
			`${host}/staff/target-students`,
			requestConfig
		);

		if (response.status === 204) {
			return systemError("No target records found.");
		}

		if (response.ok) {
			const data = await response.json();
			while (recordTable.rows.length > 1) {
				recordTable.deleteRow(1);
			}

			for (let records of data["student"]) {
				const row = document.createElement("tr");
				for (let record of records) {
					const cell = document.createElement("td");
					cell.textContent = record;
					row.appendChild(cell);
				}
				recordTable.appendChild(row);
			}
			toggleSection("results");
		}
	} catch (error) {
		systemError("Error fetching target records.");
		console.error(error);
	}
}

// Register a new student
async function registerNewStudent(event) {
	event.preventDefault();
	const form = event.target;
	const formData = new FormData(form);
	const requestData = {
		fName: formData.get("firstName"),
		lName: formData.get("lastName"),
		id: formData.get("newStudentId"),
		email: formData.get("email"),
		programme: formData.get("programme"),
		type: "student",
	};

	try {
		const response = await fetch(`${host}/register`, {
			method: "POST",
			body: JSON.stringify(requestData),
			headers: { "Content-Type": "application/json" },
		});

		if (response.status === 409) {
			return systemError("Student already exists in the system.");
		}

		if (response.ok) {
			systemOk("New student registered successfully.");
			form.reset();
		}
	} catch (error) {
		systemError("Error registering new student.");
		console.error(error);
	}
}

// Add new module details
async function addNewModuleDetails(event) {
	event.preventDefault();
	const form = event.target;
	const formData = new FormData(form);
	const requestData = {
		stdID: formData.get("moduleStudentId"),
		moduleCode: formData.get("moduleCode").toUpperCase(),
		moduleName: formData.get("moduleName"),
		gradepoint: formData.get("gradePoints"),
		year: formData.get("moduleYear"),
		semester: formData.get("semester"),
	};

	try {
		const response = await fetch(`${host}/add-module-details`, {
			method: "POST",
			body: JSON.stringify(requestData),
			headers: { "Content-Type": "application/json" },
		});

		if (response.ok) {
			systemOk("Module details added successfully.");
			form.reset();
		} else {
			systemError("Failed to add module details.");
		}
	} catch (error) {
		systemError("Error adding module details.");
		console.error(error);
	}
}

async function updateGPAthreshold() {
	const gpa = lookup("newDefaultGPA").value;
	if (gpa < 1 || gpa > 4.3) {
		botResponse("GPA value is out of range");
		return;
	}
	try {
		const response = await fetch(`${host}/update-gpa-threshold`, {
			method: "POST",
			body: JSON.stringify({ gpa }),
			headers: { "Content-Type": "application/json" },
		});

		if (response.ok) {
			gpaDefault.innerHTML = `Default GPA: [ <span style="color:green;">${gpa}</span> ]`;
			systemOk("GPA threshold updated successfully.");
			lookup("newDefaultGPA").value = ""; // Clear input field
		} else {
			systemError("Failed to update GPA threshold.");
		}
	} catch (error) {
		systemError("Error updating GPA threshold.");
		console.error(error);
	}
}

// Logout
async function signOut() {
	try {
		const response = await fetch(`${host}/logout`, {
			method: "GET",
			credentials: "include",
		});

		if (response.ok) {
			window.location.replace("/login.html");
		} else {
			systemError("Logout failed.");
		}
	} catch (error) {
		alert("Network error while logging out.");
		console.error(error);
	}
}

// Utility functions
function systemError(message) {
	generateResponse(botResponse, message);
	console.error("System Error:", message);
}

function systemOk(message) {
	generateResponse(botResponse, message);
	console.log("Success:", message);
}

function generateResponse(element, description) {
	return new Promise((resolve) => {
		element.innerHTML = "";

		let index = 0;
		const id = setInterval(() => {
			if (index < description.length) {
				element.innerHTML += description[index++];
			} else {
				clearInterval(id);
				resolve();
			}
		}, 15);
	});
}

async function responseBot() {
	const input = userInput.value.trim();
	if (!input) return;

	userInput.value = "";

	try {
		const response = await fetch(`${host}/bot`, {
			method: "POST",
			headers: { "Content-Type": "application/json" },
			body: JSON.stringify({ query: input }),
			credentials: "include",
		});
		if (response.ok) {
			const { query, res } = await response.json();
			if (query === "queries") {
				generateResponse(botResponse, res);
			} else if (query === "actions") {
				generateResponse(botResponse, "Feature to be updated soon");
			}
		}
	} catch (error) {
		systemError("Issue with server");
	}
}

async function sendAlerts(event) {
	const form = event.target;
	event.preventDefault();
	const formData = new FormData(form);
	const request = {
		pass: formData.get("pass"),
		year: formData.get("schoolYear"),
	};

	try {
		const response = await fetch(`${host}/alerts`, {
			method: "POST",
			headers: { "Content-Type": "application/json" },
			body: JSON.stringify(request),
			credentials: "include",
		});

		if (response.ok) {
			generateResponse(botResponse, "GPA alerts sent to respective students.");
			form.reset();
			return;
		}

		if (response.status == 401) {
			generateResponse(
				botResponse,
				"Invalid request. Cannot generate alerts.",
				"error"
			);
			return;
		} else {
			throw new Error("Unexpected server error");
		}
	} catch (error) {
		generateResponse(botResponse, "Sorry can't send alerts at this time");
	}
}
