$(document).ready(function() {
  $('.edit-provider').click(function() {
    var providerId = $(this).data('id');
    var modal = $('#editProviderModal');
    modal.find('.modal-title').text('Редактировать поставщика');
    modal.find('.modal-body form').attr('action', '/edit_provider/' + providerId + '/');
    modal.modal('show');
  });

  $('#editProviderModal .modal-body form').submit(function(e) {
    e.preventDefault();
    console.log('AJAX-запрос отправлен');
    var form = $(this);
    var url = form.attr('action');
    var data = form.serialize();
    var modal = $('#editProviderModal'); // Переменная modal определена здесь
    $.ajax({
      url: url,
      type: 'POST',
      data: data,
      success: function(response) {
        if (response.success) {
          // Обновите таблицу или выполните другие действия при успешном сохранении
          modal.modal('hide'); // Используем переменную modal здесь
          location.reload(); // Обновляем страницу для отображения изменений
        } else {
          // Обработка ошибок формы
          console.log(response.errors);
        }
      },
      error: function(xhr, status, error) {
        console.log(error);
      }
    });
  });
});