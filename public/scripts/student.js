const host = `http://192.168.100.219:8000`;

// Utility function to get an element by ID
const lookup = (id) => document.getElementById(id);

// DOM Elements
const elements = {
	logout: lookup("logout"),
	queryButton: lookup("query"),
	botResponse: lookup("p1"),
	userInput: lookup("user-input"),
	gpaTable: lookup("gpa-table"),
	tableResult: lookup("tableResult"),
};

const links = {
	showCurrentGPALink: lookup("showCurrentGPA"),
	viewRecordsLink: lookup("viewRecords"),
	viewAllRecordsLink: lookup("viewAllRecords"),
};

const sections = {
	recordsSection: lookup("recordsSection"),
	resultsSection1: lookup("resultsSection1"),
	resultsSection2: lookup("resultsSection2"),
	gpaSection: lookup("gpaSection"),
};

const forms = {
	studentForm: lookup("studentForm"),
	gpaForm: lookup("gpaForm"),
};

const bot = {
	chatIcon: lookup("chat-icon"),
	chatBot: lookup("chatBot"),
	responses: lookup("responses"),
};

const methods = {
	logout: logoutUser,
	fetchRecords: fetchAllAcademicRecords,
};

// Event Listeners
bot.chatIcon.addEventListener("click", () =>
	toggleChat("responses", "chatBot")
);

bot.chatBot.addEventListener("click", () => {
	toggleChat("chatBot", "responses");
});

elements.logout.addEventListener("click", logoutUser);
elements.queryButton.addEventListener("click", chatbot);
elements.userInput.addEventListener("keypress", (event) => {
	if (event.key === "Enter") chatbot();
});

forms.studentForm.addEventListener("submit", fetchAcademicRecords);
forms.gpaForm.addEventListener("submit", showCurrentGPA);

links.viewRecordsLink.addEventListener("click", () =>
	toggleSection("recordsSection")
);
links.showCurrentGPALink.addEventListener("click", () =>
	toggleSection("gpaSection")
);
links.viewAllRecordsLink.addEventListener("click", fetchAllAcademicRecords);

// Section Visibility Management
function toggleSection(sectionKey) {
	Object.keys(sections).forEach((key) => {
		if (sectionKey === key) {
			sections[key].classList.remove("hidden");
			sections[key].classList.add("visible");
		} else {
			sections[key].classList.remove("visible");
			sections[key].classList.add("hidden");
		}
	});
}

function toggleChat(toHide, toShow) {
	bot[toHide].classList.remove("unhidden");
	bot[toHide].classList.add("hidden");
	bot[toShow].classList.remove("hidden");
	bot[toShow].classList.add("unhidden");
}

function closePortal(portal) {
	sections[portal].classList.remove("visible");
	sections[portal].classList.add("hidden");
}

// Fetch Functions
async function fetchAcademicRecords(event) {
	event.preventDefault();
	const form = event.target;
	const formData = new FormData(form);
	const request = { year: formData.get("academicYear") };

	try {
		const res = await fetch(`${host}/student/records`, {
			method: "POST",
			headers: { "Content-Type": "application/json" },
			body: JSON.stringify(request),
			credentials: "include",
		});

		console.log("REsponse: ", res.ok);

		if (res.ok) {
			const { records } = await res.json();
			renderTable(elements.tableResult, records);
			toggleSection("resultsSection1");
			form.reset();
			return true;
		}

		throw new Error("Failed to fetch records");
	} catch (error) {
		systemError(error.message);
		return false;
	}
}

async function fetchAllAcademicRecords(event) {
	event.preventDefault();
	try {
		const res = await fetch(`${host}/student/records`, {
			method: "GET",
			credentials: "include",
		});

		if (res.ok) {
			const { records } = await res.json();
			renderTable(elements.tableResult, records);
			toggleSection("resultsSection1");
			return true;
		}

		throw new Error("Failed to fetch records");
	} catch (error) {
		systemError(error.message);
		return false;
	}
}

async function showCurrentGPA(event) {
	event.preventDefault();
	const formData = new FormData(event.target);
	const year = formData.get("gpaAcademicYear");

	try {
		const res = await fetch(`${host}/student/gpa`, {
			method: "POST",
			headers: { "Content-Type": "application/json" },
			body: JSON.stringify({ year }),
			credentials: "include",
		});

		if (res.ok) {
			const { GPAs } = await res.json();
			while (elements.gpaTable.rows.length > 1) {
				elements.gpaTable.deleteRow(1);
			}
			const row = document.createElement("tr");
			GPAs.forEach((gpa) => {
				const cell = document.createElement("td");
				cell.innerText = gpa;
				row.appendChild(cell);
			});
			elements.gpaTable.appendChild(row);
			toggleSection("resultsSection2");
			return true;
		}
		throw new Error("GPA data not found");
	} catch (error) {
		systemError(error.message);
		return false;
	}
}

// Logout Function
async function logoutUser() {
	try {
		const res = await fetch(`${host}/logout`, {
			method: "GET",
			credentials: "include",
		});

		if (res.ok) {
			window.location.replace("/login.html");
		} else {
			throw new Error("Logout failed");
		}
	} catch (error) {
		systemError(error.message);
	}
}

// Chatbot Functionality
async function chatbot() {
	const input = elements.userInput.value.trim();
	if (!input) return;

	elements.userInput.value = "";

	try {
		const response = await fetch(`${host}/bot`, {
			method: "POST",
			headers: { "Content-Type": "application/json" },
			body: JSON.stringify({ query: input }),
			credentials: "include",
		});

		if (response.ok) {
			const { query, res } = await response.json();
			console.log("Query:", query);
			console.log("Res:", res);

			if (query === "queries") {
				generateResponse(elements.botResponse, res);
			} else if (query === "actions") {
				if (res in methods) {
					methods[res]();
				} else
					generateResponse(elements.botResponse, "Feature not yet available.");
			}
		}
	} catch (error) {
		systemError("Issue with server");
	}
}

// Utility Functions
function renderTable(tableElement, records) {
	// Clear previous table content
	while (tableElement.rows.length > 1) {
		tableElement.deleteRow(1);
	}
	if (!records.length) {
		systemError("No records found");
		return;
	}

	for (const record of records) {
		const row = document.createElement("tr");
		record.forEach((item) => {
			const col = document.createElement("td");
			col.textContent = item;
			row.appendChild(col);
		});
		tableElement.appendChild(row);
	}
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

function systemError(message) {
	generateResponse(message);
	console.error("System Error: ", message);
}

// Auto-Initialization
(async function init() {
	try {
		const response = await fetch(`${host}/`, {
			method: "GET",
			credentials: "include",
		});

		if (response.ok) {
			const { name } = await response.json();
			lookup("studentName").textContent = name;
		} else if (response.status === 401) {
			window.location.replace("/login.html");
		}
	} catch (error) {
		systemError(error.message || "Initialization failed");
	}
})();
