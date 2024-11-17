const { response } = require("express");

const lookup = (id) => document.getElementById(id);

let isAuthenticated = false;

const port = 3001;
const host = `http://127.0.0.1:${port}`;

const logout = lookup("logout");
logout.addEventListener("click", () => signOut(host));

async function establish(host) {
	const data = { method: "GET" };
   try {
      const response = await fetch(`${host}/`);

   }
}

async function signOut(host) {
	console.log("Host:", host);
	const data = { method: "GET" };
	try {
		const response = await fetch(`${host}/logout`, data);
		if (response.ok) {
			alert("You have been logged out.");
			window.location.href = "/public/login.html"; // Redirect to login page
			isAuthenticated = false;
		} else {
			console.error("Failed to logout:", response.statusText);
			alert("Logout failed. Try again.");
		}
	} catch (error) {
		console.error("Network error during logout:", error);
		alert("Logout failed due to a network error.");
	}
}
