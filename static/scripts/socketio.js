document.addEventListener('DOMContentLoaded', () => {

	// Підключення до websocket
	var socket = io.connect(location.protocol + '//' + document.domain + ':' + location.port);

	// Отримати ім’я користувача
	const username = document.querySelector('#get-username').innerHTML;

	// Встановити номер за замовчуванням
	let room = "Вітальня"
	joinRoom("Вітальня");

	// Відправлення повідомлення
	document.querySelector('#send_message').onclick = () => {
		socket.emit('incoming-msg', {
			'msg': document.querySelector('#user_message').value,
			'username': username,
			'room': room
		});

		document.querySelector('#user_message').value = '';
	};

	// Показати всі вхідні повідомлення
	socket.on('message', data => {

		// Показати поточне повідомлення
		if (data.msg) {
			const p = document.createElement('p');
			const span_username = document.createElement('span');
			const span_timestamp = document.createElement('span');
			const br = document.createElement('br')
			// Показати власне повідомлення користувача
			if (data.username == username) {
				p.setAttribute("class", "my-msg");

				// Ім'я користувача
				span_username.setAttribute("class", "my-username");
				span_username.innerText = data.username;

				// Відмітка часу
				span_timestamp.setAttribute("class", "timestamp");
				span_timestamp.innerText = data.time_stamp;

				// HTML для додавання
				p.innerHTML += span_username.outerHTML + br.outerHTML + data.msg + br.outerHTML + span_timestamp.outerHTML

				// Додавати
				document.querySelector('#display-message-section').append(p);
			}
			// Відображення повідомлень інших користувачів
			else if (typeof data.username !== 'undefined') {
				p.setAttribute("class", "others-msg");

				// Ім'я користувача
				span_username.setAttribute("class", "other-username");
				span_username.innerText = data.username;

				// Відмітка часу
				span_timestamp.setAttribute("class", "timestamp");
				span_timestamp.innerText = data.time_stamp;

				// HTML для додавання
				p.innerHTML += span_username.outerHTML + br.outerHTML + data.msg + br.outerHTML + span_timestamp.outerHTML;

				// Додавати
				document.querySelector('#display-message-section').append(p);
			}
			// Відображення системного повідомлення
			else {
				printSysMsg(data.msg);
			}


		}
		scrollDownChatWindow();
	});

	// Виберіть номер
	document.querySelectorAll('.select-room').forEach(p => {
		p.onclick = () => {
			let newRoom = p.innerHTML
			// Перевірте, чи користувач уже в кімнаті
			if (newRoom === room) {
				msg = `Ви вже в кімнаті ${room}.`;
				printSysMsg(msg);
			} else {
				leaveRoom(room);
				joinRoom(newRoom);
				room = newRoom;
			}
		};
	});

	// Вихід із чату
	document.querySelector("#logout-btn").onclick = () => {
		leaveRoom(room);
	};

	// Запустити подію "залишити", якщо користувач раніше перебував у кімнаті
	function leaveRoom(room) {
		socket.emit('leave', {
			'username': username,
			'room': room
		});

		document.querySelectorAll('.select-room').forEach(p => {
			p.style.color = "black";
		});
	}

	// Тригер події "приєднатися"
	function joinRoom(room) {

		// Приєднуйтесь до кімнати
		socket.emit('join', {
			'username': username,
			'room': room
		});

		// Виділіть вибрану кімнату
		document.querySelector('#' + CSS.escape(room)).style.color = "#ffc107";
		document.querySelector('#' + CSS.escape(room)).style.backgroundColor = "white";

		// Очистити область повідомлень
		document.querySelector('#display-message-section').innerHTML = '';

		// Автофокусування на текстовому полі
		document.querySelector("#user_message").focus();
	}

	// Прокрутіть вікно чату вниз
	function scrollDownChatWindow() {
		const chatWindow = document.querySelector("#display-message-section");
		chatWindow.scrollTop = chatWindow.scrollHeight;
	}

	// Друк системних повідомлень
	function printSysMsg(msg) {
		const p = document.createElement('p');
		p.setAttribute("class", "system-msg");
		p.innerHTML = msg;
		document.querySelector('#display-message-section').append(p);
		scrollDownChatWindow()

		// Автофокус на текстовому полі
		document.querySelector("#user_message").focus();
	}
});