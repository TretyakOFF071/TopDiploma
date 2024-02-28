$(document).ready(function() {
    var formCount = $('.good-form').length;
    var emptyForm = $('.good-form:first').clone();

    $('#add-good').click(function() {
        formCount++;
        var newForm = emptyForm.clone().find('input, select').val('').end();
        newForm.find('input[name*="good"]').attr('name', 'form-' + (formCount - 1) + '-good');
        newForm.find('input[name*="quantity"]').attr('name', 'form-' + (formCount - 1) + '-quantity');
        newForm.appendTo('#goods-formset');
    });

    $('#show-forms').click(function() {
        $('.good-form.hidden:first').removeClass('hidden');
    });
});