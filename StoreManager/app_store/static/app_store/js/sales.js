$(document).ready(function() {
  var totalPrice = 0;

  // обработчик для добавления новых форм
  $('#add-item').click(function() {
    var formCount = parseInt($('[name="form-TOTAL_FORMS"]').val());
    $('[name="form-TOTAL_FORMS"]').val(formCount + 1);
    $('.sale-item-form.hidden:first').removeClass('hidden');
    updateTotalPrice();
  });

  // обработчик изменения для поля количества товара
  $(document).on('change keyup', '.sale-item-form input[name*="quantity"]', function() {
    updateTotalPrice();
  });

  // обработчик изменения для поля товара
  $(document).on('change', '.sale-item-form select[name*="good"]', function() {
    var goodId = $(this).val();
    var priceDisplay = $(this).closest('.sale-item-form').find('.price-display');
    var quantityInput = $(this).closest('.sale-item-form').find('input[name*="quantity"]');

    // Запрос к серверу для получения цены товара
    $.getJSON('/get_good_price/' + goodId, function(data) {
      if (data.price) {
        var priceText = 'Цена за единицу: <strong>' + data.price.toFixed(2) + '</strong> RUB.';
        priceDisplay.html(priceText);

        // Обновление общей суммы
        var quantity = parseInt(quantityInput.val()) || 0;
        totalPrice += data.price * quantity;
        updateTotalPriceDisplay();
        updateDiscountedPriceDisplay();
      } else {
        priceDisplay.text('Товар не найден');
      }
    });
  });

  // Функция для обновления общей суммы
  function updateTotalPrice() {
    totalPrice = 0;
    $('.sale-item-form').each(function() {
      var goodId = $(this).find('select[name*="good"]').val();
      var quantity = parseInt($(this).find('input[name*="quantity"]').val()) || 0;
      if (goodId) {
        var price = parseFloat($(this).find('.price-display strong').text());
        totalPrice += price * quantity;
      }
    });
    updateTotalPriceDisplay();
    updateDiscountedPriceDisplay();
  }

  // Функция для обновления отображения общей суммы
  function updateTotalPriceDisplay() {
    $('#total-price-display').html('<h3>Общая сумма: ' + totalPrice.toFixed(2) + ' RUB</h3>');
  }

  // Функция для обновления общей суммы с учетом скидки
  function updateDiscountedPriceDisplay() {
    var discount = parseFloat($('input[name="discount"]').val()) || 0;
    var discountedTotalPrice = totalPrice * (1 - discount / 100);
    $('#discounted-price-display').html('<h4>Общая сумма с учетом скидки: ' + discountedTotalPrice.toFixed(2) + ' RUB</h4>');
  }

  // обработчик изменения для поля скидки
  $(document).on('change keyup', 'input[name="discount"]', function() {
    updateDiscountedPriceDisplay();
  });

  // Валидация формы для скидки
  $(document).ready(function() {
    $('#id_discount').on('input', function() {
      var value = $(this).val();
      if (value.length > 2) {
        $(this).val(value.substring(0, 3));
      }
      var numericValue = parseInt(value);
      if (numericValue > 50) {
        $(this).val(50);
      }
    }).attr('title', 'Максимальное значение скидки: 50%');
  });
});

