const lookup = (id) => document.getElementById(id);

const port = 3001;
const host = `http://127.0.0.1:${port}`;

const logout = lookup("logout");
logout.addEventListener("click", () => signOut(host));

(async function (host) {
	try {
		const response = await fetch(`${host}/`, {
			method: "GET",
			credentials: "include",
		});

		if (response.ok) return;

		if (response.status === 401) {
			// window.location.href = "/public/login.html";
			window.location.replace("/public/login.html");
			return;
		}
		// display error message
	} catch (error) {
		console.error(error);
	}
})(host);

async function signOut(host) {
	try {
		const response = await fetch(`${host}/logout`, {
			method: "GET",
			credentials: "include",
		});

		if (response.ok) {
			// window.location.href = "/public/login.html";
			window.location.replace("/public/login.html");
			return;
		}
		console.error("Failed to logout:", response.statusText);
		alert("Logout failed. Try again.");

		// display error message
	} catch (error) {
		console.error("Network error during logout:", error);
		alert("Logout failed due to a network error.");
	}
}
