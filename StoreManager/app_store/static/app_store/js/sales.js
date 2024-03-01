const enTranslations = {
    "addItem": "Add Item",
    "totalPrice": "Total Price",
    "discountedTotalPrice": "Total Price with Discount",
    "goodNotFound": "Good not found",
    "pricePerUnit": "Price per unit",
    "discount": "Discount",
    "totalPriceWithDiscount": "Total Price with Discount",
    "maxDiscount": "Maximum discount value: 50%"
};

const ruTranslations = {
    "addItem": "Добавить товар",
    "totalPrice": "Общая сумма",
    "discountedTotalPrice": "Общая сумма с учетом скидки",
    "goodNotFound": "Товар не найден",
    "pricePerUnit": "Цена за единицу товара",
    "discount": "Скидка",
    "totalPriceWithDiscount": "Общая сумма с учетом скидки",
    "maxDiscount": "Максимальное значение скидки: 50%"
};

i18next.init({
  lng: 'ru',
  resources: {
    en: {
      translation: enTranslations
    },
    ru: {
      translation: ruTranslations
    }
  }
}, function(err, t) {


});

$(document).ready(function() {
  var totalPrice = 0;

  // Добавляем обработчик для смены языка
  $('#language-selector').change(function() {
    changeLanguage($(this).val());
  });

  // Добавляем обработчик для добавления новых форм
  $('#add-item').click(function() {
    var formCount = parseInt($('[name="form-TOTAL_FORMS"]').val());
    $('[name="form-TOTAL_FORMS"]').val(formCount + 1);
    $('.sale-item-form.hidden:first').removeClass('hidden');
    updateTotalPrice();
  });

  // Добавляем обработчик изменения для поля количества товара
  $(document).on('change keyup', '.sale-item-form input[name*="quantity"]', function() {
    updateTotalPrice();
  });

  // Добавляем обработчик изменения для поля товара
  $(document).on('change', '.sale-item-form select[name*="good"]', function() {
    var goodId = $(this).val();
    var priceDisplay = $(this).closest('.sale-item-form').find('.price-display');
    var quantityInput = $(this).closest('.sale-item-form').find('input[name*="quantity"]');

    // Запрос к серверу для получения цены товара
    $.getJSON('/get_good_price/' + goodId, function(data) {
      if (data.price) {
        var priceText = i18next.t('pricePerUnit') + ': <strong>' + data.price.toFixed(2) + '</strong> RUB.';
        priceDisplay.html(priceText);

        // Обновляем общую сумму
        var quantity = parseInt(quantityInput.val()) || 0;
        totalPrice += data.price * quantity;
        updateTotalPriceDisplay();
        updateDiscountedPriceDisplay();
      } else {
        priceDisplay.text(i18next.t('goodNotFound'));
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
    $('#total-price-display').html('<h3>' + i18next.t('totalPrice') + ': ' + totalPrice.toFixed(2) + ' RUB</h3>');
  }

  // Функция для обновления общей суммы с учетом скидки
  function updateDiscountedPriceDisplay() {
    var discount = parseFloat($('input[name="discount"]').val()) || 0;
    var discountedTotalPrice = totalPrice * (1 - discount / 100);
    $('#discounted-price-display').html('<h4>' + i18next.t('totalPriceWithDiscount') + ': ' + discountedTotalPrice.toFixed(2) + ' RUB</h4>');
  }

  // Добавляем обработчик изменения для поля скидки
  $(document).on('change keyup', 'input[name="discount"]', function() {
    updateDiscountedPriceDisplay();
  });

  // Функция для смены языка
  function changeLanguage(language) {
    i18next.changeLanguage(language, function(err, t) {
      updateTotalPriceDisplay();
      updateDiscountedPriceDisplay();
    });
  }
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
    }).attr('title', i18next.t('maxDiscount'));
});