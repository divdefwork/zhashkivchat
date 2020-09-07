document.addEventListener('DOMContentLoaded', () => {

	// Зробити згортання бічної панелі при натисканні
	document.querySelector('#show-sidebar-button').onclick = () => {
		document.querySelector('#sidebar').classList.toggle('view-sidebar');
	};

	// Зробити повідомлення "Enter" для надсилання ключа
	let msg = document.getElementById("user_message");
	msg.addEventListener("keyup", function (event) {
		event.preventDefault();
		if (event.keyCode === 13) {
			document.getElementById("send_message").click();
		}
	});
});