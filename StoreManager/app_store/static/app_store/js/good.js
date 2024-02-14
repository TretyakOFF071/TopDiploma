document.addEventListener('DOMContentLoaded', function() {
  // Обработчик нажатия на кнопку "Добавить товар"
  var addGoodButton = document.getElementById('add-good-button');
  var addGoodModal = document.getElementById('add-good-modal');
  var closeSpan = document.getElementsByClassName('close')[0];

  // Когда пользователь нажимает на кнопку, открываем модальное окно
  addGoodButton.onclick = function() {
    addGoodModal.style.display = 'block';
  }

  // Когда пользователь нажимает на <span> (x), закрываем модальное окно
  closeSpan.onclick = function() {
    addGoodModal.style.display = 'none';
  }

  // Когда пользователь щелкает в любом месте за пределами модального окна, закрываем его
  window.onclick = function(event) {
    if (event.target == addGoodModal) {
      addGoodModal.style.display = 'none';
    }
  }
});
