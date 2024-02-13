document.addEventListener('DOMContentLoaded', function() {
    var registerButton = document.getElementById('register-button');
    registerButton.addEventListener('click', function(event) {
        event.preventDefault();

        var username = document.getElementById('username').value;
        var password = document.getElementById('password').value;
        var email = document.getElementById('email').value;
        var position = document.getElementById('position').value;
        var birthday = document.getElementById('birthday').value;
        var tel = document.getElementById('tel').value;
        var avatar = document.getElementById('avatar').files[0];

        var formData = new FormData();
        formData.append('username', username);
        formData.append('password', password);
        formData.append('email', email);
        formData.append('position', position);
        formData.append('birthday', birthday);
        formData.append('tel', tel);
        formData.append('avatar', avatar);

        fetch('/register/', {
            method: 'POST',
            body: formData
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                // Обработка успешной регистрации, например, перенаправление на страницу профиля
                window.location.href = '/profile/';
            } else {
                // Обработка ошибок регистрации
                console.error('Ошибка регистрации:', data.errors);
                // Вы можете отобразить ошибки на странице, если это необходимо
            }
        })
        .catch(error => {
            console.error('Ошибка при отправке запроса:', error);
        });
    });
});