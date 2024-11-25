const lookup = (id) => document.getElementById(id);
const uploadForm = lookup("uploadForm");
const accountType = lookup("account_type"); // Corrected this line

uploadForm.addEventListener("submit", saveUser);
accountType.addEventListener("change", showFields);

let p1 =
	"Join the Academic Probation Alert System today!\
    Our platform helps students and staff stay on top of academic \
    performance by providing real-time GPA tracking, personalized alerts, \
    and valuable insights.Whether you're a student aiming for \
    academic excellence or a staff member managing academic \
    records, this system offers tools to ensure success.";

let p2 =
	"Create your account now to access a seamless experience\
   tailored to your needs. Students can track their GPA, receive\
   alerts if they fall below the probation threshold, and access \
   detailed performance reports. Staff can manage student records,\
   set probation thresholds,and generate reports with ease.";

let p3 = "Sign up and take control of your academic journey today!";

(async function (descript1, descript2, descript3) {
	const p1 = lookup("p1");
	const p2 = lookup("p2");
	const p3 = lookup("p3");

	try {
		await generateDescription(p1, descript1);
		await generateDescription(p2, descript2);
		await generateDescription(p3, descript3);
	} catch (error) {
		console.error("Error generating descriptions:", error);
	}
})(p1, p2, p3);

async function saveUser(event) {
	event.preventDefault();

	const formData = new FormData(event.target);
	const passwd = formData.get("password");
	const confirmPasswd = formData.get("confirm_password");

	const errorMsgHolder = lookup("error-message");
	errorMsgHolder.style.display = passwd !== confirmPasswd ? "block" : "none";
	errorMsgHolder.innerText =
		passwd !== confirmPasswd ? "Passwords do not match!" : "";

	if (passwd === confirmPasswd) {
		const data = {
			fName: formData.get("firstName"),
			lName: formData.get("lastName"),
			userID: formData.get("userID"),
			email: formData.get("email"),
			accountType: formData.get("account_type"),
			passwd: passwd,
		};

		if (data.accountType === "student") {
			data.programme = formData.get("programme");
		} else if (data.accountType === "staff") {
			data.staffType = formData.get("staff_type");
			data.school = formData.get("school");
		}

		try {
			const res = await fetch("http://127.0.0.1:3001/register", {
				method: "POST",
				body: JSON.stringify(data),
				headers: { "Content-Type": "application/json" },
			});

			if (res.ok) {
				alert("Your account was created successfully");
				window.location.href = "/public/login.html";
			} else {
				const error = await res.json();
				console.error("Error:", error.message || "Failed to create account");
				alert(error.message || "Failed to create account. Try again.");
			}
		} catch (error) {
			console.error("Network Error:", error);
			alert("Failed to connect to the server.");
		}
	}
}

function showFields() {
	const studentFields = lookup("student-fields");
	const staffFields = lookup("staff-fields");
	const accountTypeValue = accountType.value;

	if (accountTypeValue === "student") {
		studentFields.style.display = "block";
		staffFields.style.display = "none";
		// Add required attributes for student fields
		document.getElementById("programme").setAttribute("required", "true");
	} else if (accountTypeValue === "staff") {
		studentFields.style.display = "none";
		staffFields.style.display = "block";

		// Add required attributes for staff fields
		document.getElementById("staff_type").setAttribute("required", "true");
		document.getElementById("school").setAttribute("required", "true");

		// Remove required attributes for student fields
		document.getElementById("programme").removeAttribute("required");
	}
}

function generateDescription(element, description) {
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
		}, 5);
	});
}
