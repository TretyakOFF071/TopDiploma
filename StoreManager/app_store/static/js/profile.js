$(document).ready(function() {
    // Отправляем AJAX-запрос к серверу Django для получения данных профиля
    $.ajax({
        url: '/profile/data', // Замените на URL вашего Django view для получения данных профиля
        type: 'GET',
        success: function(response) {
            // Обрабатываем ответ сервера и отображаем данные на странице
            var profileContent = $('#profile-content');
            profileContent.empty();
            profileContent.append('<h1>Личный кабинет</h1>');
            profileContent.append('<p>Имя пользователя: ' + response.username + '</p>');
            profileContent.append('<p>Email: ' + response.email + '</p>');
            profileContent.append('<p>Дата рождения: ' + response.birthday + '</p>');
            profileContent.append('<p>Телефон: ' + response.tel + '</p>');
            profileContent.append('<p>Должность: ' + response.position + '</p>');
            if (response.avatar) {
                profileContent.append('<img src="' + response.avatar + '" width="500px" height="300px">');
            } else {
                profileContent.append('<p>No avatar provided.</p>');
            }
        },
        error: function(xhr, status, error) {
            console.error('Ошибка при получении данных профиля:', error);
        }
    });
});