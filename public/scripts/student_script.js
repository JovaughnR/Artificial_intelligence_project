console.log("Script running");
console.log("Script runinigndfn");
const port = 3001;
const host = `http://127.0.0.1:${port}`;

const lookup = (id) => document.getElementById(id);
const logout = lookup("logout");
const records = lookup("records");
const queryButton = lookup("query");
const botResponse = lookup("p1");
const userInput = lookup("user-input");
const gpaTable = lookup("gpa-table");

const currentGPA = lookup("current-gpa");

const responses = lookup("responses");
const chatIcon = lookup("chat-icon");
const chatBot = lookup("chat-bot");

const showCurrentGPALink = lookup("showCurrentGPA");
const viewRecordsLink = lookup("viewRecords");
const viewAllRecordsLink = lookup("viewAllRecords");

logout.addEventListener("click", logoutUser);
// records.addEventListener("click", fetchAcademicRecords);
queryButton.addEventListener("click", chatbot);
currentGPA.addEventListener("click", showCurrentGPA);

// Get all the sections needs to be close
const recordsSection = lookup("records-section");
const resultsSection1 = lookup("resultsSection1");
const resultsSection2 = lookup("resultsSection2");
const gpaSection = lookup("gpa-section");

// get all form
const studentForm = lookup("studentForm");
const gpaForm = lookup("gpaForm");

studentForm.addEventListener("submit", (e) => {
	let status = fetchAcademicRecords(e);
	if (status) {
		recordsSection.style.display = "none";
		resultsSection2.style.display = "none";
		resultsSection1.style.display = "flex";
	}
});

gpaForm.addEventListener("submit", (e) => {
	closeSection1();
	let status = showCurrentGPA(e);
	if (status) {
		resultsSection1.style.display = "none";
		resultsSection2.style.display = "flex";
	}
});

viewRecordsLink.addEventListener("click", () => {
	recordsSection.style.display = "flex";
	resultsSection1.style.display = "none";
	resultsSection2.style.display = "none";
	gpaSection.style.display = "none";
});

showCurrentGPALink.addEventListener("click", () => {
	gpaSection.style.display = "flex";
	recordsSection.style.display = "none";
	resultsSection1.style.display = "none";
	resultsSection2.style.display = "none";
});

// This is the only link that will bring up a table
viewAllRecordsLink.addEventListener("click", (e) => {
	recordsSection.style.display = "none";
	gpaSection.style.display = "none";
	resultsSection2.style.display = "none";
	let status = fetchAllAcademicRecords(e);
	if (status) {
		resultsSection1.style.display = "flex";
	}
});

chatBot.addEventListener("click", () => {
	responses.style.display = "grid";
	chatBot.style.display = "none";
});

chatIcon.addEventListener("click", () => {
	responses.style.display = "none";
	chatBot.style.display = "block";
});

function closeSection2() {
	resultsSection2.style.display = "none";
}

function closeSection1() {
	resultsSection1.style.display = "none";
}

const functions = {
	fetchRecords: fetchAcademicRecords,
	logout: logoutUser,
	showGPA: showCurrentGPA,

	// logoutUser: logoutUser,
	// showCurrentGPA: showCurrentGPA,
	// showAcademicStatus: showAcademicStatus,
	// fetchModuleRecords: fetchModuleRecords,
	// submitUserQuery: submitUserQuery,
	// emailSupport: emailSupport,
};

// Remember to test
// function toggleChatBot() {
// 	if (chatbotlogo1.style.display == "none") {
// 		chatbotlogo1.style.display = "block";
// 		responses.style.display = "none";
// 	} else if (chatbotlogo1.style.display == "block") {
// 		chatbotlogo1.style.display = "none";
// 		responses.style.display = "block";
// 	}
// }

(async function () {
	try {
		const response = await fetch(`${host}/`, {
			method: "GET",
			credentials: "include",
		});

		if (response.ok) {
			const data = await response.json();
			let userName = lookup("studentName");
			userName.textContent = data["name"];
			return;
		}

		if (response.status === 401) {
			window.location.replace("/public/login.html");
		}
	} catch (error) {
		const errorMessage =
			error.message || "An error occurred during initialization";
		alert(errorMessage);
	}
})();

async function showCurrentGPA(event) {
	event.preventDefault();
	const formData = new FormData(event.target);
	const year = formData.get("gpaAcademicYear");

	try {
		const res = await fetch(`${host}/student/gpa`, {
			method: "POST",
			headers: { "Content-Type": "application/json" },
			body: JSON.stringify({ year: year }),
			credentials: "include",
		});

		if (res.ok) {
			console.log("Number of children in table:", gpaTable.children.length);
			if (gpaTable.children.length > 2) {
				gpaTable.removeChild(gpaTable.lastChild);
			}

			const data = await res.json();
			const tr = document.createElement("tr");
			for (let gpa of data["GPAs"]) {
				const td = document.createElement("td");
				td.innerHTML = gpa;
				tr.appendChild(td);
			}
			gpaTable.append(tr);
			return true;
		}
	} catch (error) {
		systemError("GPA data did not found");
		return false;
	}
}

// queryButton.addEventListener("click", async (event) => {
// 	console.log("Query Button pressed")
// 		console.log("userInput:", userInput.value)
// 		const request = {
// 			method: "POST",
// 			headers: {"Content-Type": "application/json"},
// 			body: JSON.stringify({"query": userInput.value}),
// 			credentials: "include"
// 		};

// 		const response = await fetch(`${host}/student/bot`, request);
// 		console.log(response)
// });

async function chatbot() {
	let input = userInput.value;
	if (input == "") return;
	userInput.value = "";

	try {
		const req = {
			method: "POST",
			headers: { "Content-Type": "application/json" },
			body: JSON.stringify({ query: input }),
		};

		const res = await fetch(`${host}/student/bot`, req);
		console.log(res);

		if (res.ok) {
			const data = await res.json();
			const type = data["query"];
			const result = data["res"];

			if (type == "queries") {
				generateResponse(botResponse, result);
			} else if (type == "actions") {
				functions[result]();
			}
		}
	} catch (error) {
		systemError("Issue with server");
	}
}

async function logoutUser() {
	try {
		const response = await fetch(`${host}/logout`, {
			method: "GET",
			credentials: "include",
		});

		if (response.ok) {
			window.location.replace("/public/login.html");
			return;
		}
		console.error("Failed to logout:", response.statusText);
		systemError("Logout failed. Try again");

		// display error message
	} catch (error) {
		console.error("Network error during logout:", error);
		systemError("Logout failed due to a network error.");
	}
}

function generateResponse(element, description) {
	return new Promise((resolve, reject) => {
		if (!element) return reject("Element not found");

		let index = 0;
		element.innerHTML = "";

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

async function fetchAcademicRecords(event) {
	event.preventDefault();
	const formData = new FormData(event.target);
	const request = { year: formData.get("academicYear") };

	console.log("Fetching records");
	try {
		const res = await fetch(`${host}/student/records`, {
			method: "POST",
			headers: { "Content-Type": "application/json" },
			body: JSON.stringify(request),
			credentials: "include",
		});

		if (res.ok) {
			const data = await res.json();
			console.log(data);
			const studentRecords = data["records"];
			const tableResult = lookup("tableResult");
			console.log("Table:", tableResult);

			if (!studentRecords.length) {
				systemError("No records found");
				// Implement AI logic here
			}
			console.log("Number of records:", studentRecords.length);
			console.log("student records:", studentRecords);
			if (tableResult.children.length > 2) {
				tableResult.removeChild(tableResult.lastChild);
			}
			for (let record of studentRecords) {
				const tr = document.createElement("tr");
				console.log("loopoing");
				for (let item of record) {
					const td = document.createElement("td");
					td.innerHTML = item;
					tr.appendChild(td);
				}
				tableResult.appendChild(tr);
			}
			return true;
		}
		if (res.status == 401) {
			systemError("Failed to fetch records");
			return false;
		}
	} catch (error) {
		systemError(error);
		return false;
	}
}

async function fetchAllAcademicRecords() {
	console.log("Fetching records");
	try {
		const res = await fetch(`${host}/student/records`, {
			method: "GET",
			credentials: "include",
		});

		if (res.ok) {
			const data = await res.json();
			const studentRecords = data["records"];
			const tableResult = lookup("tableResult");

			if (!studentRecords.length) {
				systemError("No records found");
				// Implement AI logic here
			}

			if (tableResult.children.length > 2) {
				tableResult.removeChild(tableResult.lastChild);
			}
			for (let record of studentRecords) {
				let row = document.createElement("tr");
				for (let item of record) {
					let col = document.createElement("td");
					col.innerHTML = item;
					row.appendChild(col);
				}
				tableResult.appendChild(row);
			}
			return true;
		}
		if (res.status == 401) {
			systemError("Failed to fetch records");
			return false;
		}
	} catch (error) {
		systemError(error);
		return false;
	}
}

function systemError(error) {
	console.error("System Error: ", error);
}
