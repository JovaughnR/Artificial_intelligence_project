const lookup = (id) => document.getElementById(id);

const logoutButton = lookup("logout");
const userName = lookup("staffName");
const recordTable = lookup("record-table");
const chatBot = lookup("chat-bot");
const chatIcon = lookup("chat-icon");
const responseArea = lookup("responses");

const recordsLink = lookup("retrieveRecordsLink");
const registerStudentLink = lookup("registerStudentLink");
const addModuleDetailLink = lookup("addModuleDetailLink");
const gpaThresholdLink = lookup("gpaThresholdLink");

const resultSection = lookup("resultsSection");
const adminSection = lookup("admin");
const registeStudentSection = lookup("registerStudent");
const addModuleDetailSection = lookup("addModuleDetails");
const gpaThresholdSection = lookup("gpaThreshold");

const adminForm = lookup("adminForm");
const moduleForm = lookup("moduleForm");
const registerForm = lookup("registerForm");
// const thresholdForm = lookup('thresholdForm');

const gpaDefault = lookup("defaulted_gpa");

// console.log(thresholdForm); // Ensure this logs the form element

const port = 3001;
const host = `http://127.0.0.1:${port}`;
console.log("Staff Script running");

logoutButton.addEventListener("click", signOut);
adminForm.addEventListener("submit", retrieveStudentRecords);
registerForm.addEventListener("submit", registerNewStudent);
moduleForm.addEventListener("submit", addNewModuleDetails);
// document.getElementById('thresholdForm').addEventListener('submit', updateGPAthreshold);

recordsLink.addEventListener("click", () => {
	adminSection.style.display = "flex";
	gpaThresholdSection.style.display = "none";
	addModuleDetailSection.style.display = "none";
	registeStudentSection.style.display = "none";
});

registerStudentLink.addEventListener("click", () => {
	registeStudentSection.style.display = "flex";
	adminSection.style.display = "none";
	gpaThresholdSection.style.display = "none";
	addModuleDetailSection.style.display = "none";
});

addModuleDetailLink.addEventListener("click", () => {
	addModuleDetailSection.style.display = "flex";
	registeStudentSection.style.display = "none";
	adminSection.style.display = "none";
	gpaThresholdSection.style.display = "none";
});

gpaThresholdLink.addEventListener("click", () => {
	console.log("Threshold link button pressed");
	gpaThresholdSection.style.display = "flex";
	addModuleDetailSection.style.display = "none";
	registeStudentSection.style.display = "none";
	adminSection.style.display = "none";
});

chatBot.addEventListener("click", () => {
	responseArea.style.display = "grid";
	chatBot.style.display = "none";
});

chatIcon.addEventListener("click", () => {
	responseArea.style.display = "none";
	chatBot.style.display = "block";
});

function closeSection() {
	resultSection.style.display = "none";
}

function closeAdmin() {
	lookup("admin").style.display = "none";
}

function closeRegisterPortal() {
	lookup("registerStudent").style.display = "none";
}

function closeModulePortal() {
	lookup("addModuleDetails").style.display = "none";
}

function closeThresholdPortal() {
	lookup("gpaThreshold").style.display = "none";
}

async function displayrecords(request) {
	const endpoint = `${host}/staff/stud-record`;
	const response = await fetch(endpoint, request);

	if (response.status == 204) {
		systemError(`no data related to your request year (${year}).`);
		return;
	}

	if (response.ok) {
		const data = await response.json();
		const row = document.createElement("tr");

		for (let info of data["student"]) {
			let td = document.createElement("td");
			td.innerHTML = info;
			row.appendChild(td);
		}
		recordTable.appendChild(row);
	}
	closeAdmin();
	resultSection.style.display = "block";
	return;
}

async function displayTargetRecords(request) {
	const endpoint = `${host}/staff/target-students`;
	const response = await fetch(endpoint, request);

	if (response.status == 204) {
		systemError(`no data related to your request year (${year}).`);
		return;
	}

	if (response.ok) {
		const data = await response.json();
		const row = document.createElement("tr");

		for (let student of data["student"]) {
			for (let info of student) {
				let td = document.createElement("td");
				td.innerHTML = info;
				row.append(td);
			}
		}
		recordTable.appendChild(row);
	}
	closeAdmin();
	resultSection.style.display = "block";
	return;
}

function retrieveStudentRecords(event) {
	event.preventDefault();
	const formData = new FormData(event.target);

	const data = {
		studID: formData.get("studentId"),
		year: formData.get("academicYear"),
		targetGPA: formData.get("desiredGPA"),
	};

	if (!((data["studID"] != "") ^ (data["targetGPA"] != ""))) {
		systemError(`Only identifcation number or target GPA required.`);
		return;
	}

	if (!((data["studId"] == "") ^ (data["targetGPA"] == ""))) {
		systemError(`select either identification number or target GPA`);
		return;
	}

	const request = {
		method: "POST",
		body: JSON.stringify(data),
		headers: { "Content-Type": "application/json" },
	};

	try {
		if (data["studID"] != "" && data["targetGPA"] == "")
			displayrecords(request);

		if (data["studID"] == "" && data["targetGPA"] != "")
			displayTargetRecords(request);
	} catch (error) {
		systemError("Something went wrong with the server");
		console.log(error);
	}
}

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
		// display error message
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

async function registerNewStudent(event) {
	event.preventDefault();
	const endpoint = `${host}/register-student/new`;
	const formData = new FormData(event.target);

	const request = {
		fName: formData.get("firstName"),
		lName: formData.get("lastName"),
		stdID: formData.get("newStudentId"),
		email: formData.get("email"),
		programme: formData.get("programme"),
	};

	try {
		const response = await fetch(endpoint, {
			method: "POST",
			body: JSON.stringify(request),
			headers: { "Content-Type": "application/json" },
		});

		if (response.status == 409) {
			systemError("The user appears to be in the system already");
			return;
		}

		if (response.ok) {
			systemOk("I added the new student info to the database");
			return;
		}
	} catch (error) {
		systemError(error);
	}
}

async function addNewModuleDetails(event) {
	event.preventDefault();
	const endpoint = `${host}/add-module-details/new`;
	const formData = new FormData(event.target);

	const request = {
		stdID: formData.get("moduleStudentId"),
		moduleCode: formData.get("moduleCode"),
		moduleName: formData.get("moduleName"),
		gradepoint: formData.get("gradePoints"),
		year: formData.get("moduleYear"),
		semester: formData.get("semester"),
	};

	try {
		const response = await fetch(endpoint, {
			method: "POST",
			body: JSON.stringify(request),
			headers: { "Content-Type": "application/json" },
		});

		if (response.ok) {
			systemOk("I have added the data to database");
			return;
		}

		if (response.status == 500) {
			systemError("Something went wrong make sure the data format is correct");
			return;
		}
	} catch (error) {
		systemError(error);
	}
}

(async function () {
	const endpoint = `${host}/gpa-threshold`;
	try {
		const response = await fetch(endpoint, {
			method: "GET",
		});
		if (response.ok) {
			const data = await response.json();
			let gpa = `<span style="color:green;">${data["GPA"]}</span>`;
			let text = "Default GPA: [ " + gpa + " ]";
			gpaDefault.innerHTML = text;
			return;
		}
	} catch (error) {
		systemError("Something went wrong");
	}
})();

async function updateGPAthreshold(event) {
	const gpa = document.getElementById("newDefaultGPA").value;
	const endpoint = `${host}/update-gpa-threshold`;
	console.log("GPA updated");
	try {
		const response = await fetch(endpoint, {
			method: "POST",
			body: JSON.stringify({ gpa: gpa }),
			headers: { "Content-Type": "application/json" },
		});

		if (response.ok) {
			gpaDefault.innerHTML = `Default GPA: [ <span style="color:green;">${gpa}</span> ]`;
			systemOk("GPA has been updated");
			document.getElementById("newDefaultGPA").value = "";
		}
		if (response.status == 500) {
			systemError("Internal server error");
		}
	} catch (error) {
		systemError("Couldn't update the default GPA");
	}
}

function systemError(error) {
	console.log("System Error: ", error);
}

function systemOk(message) {
	console.log(message);
}
