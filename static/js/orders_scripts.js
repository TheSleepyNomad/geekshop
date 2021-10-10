window.onload = function () {
    let _quantity, _price, orderitem_num, delta_quantity, orderitem_quantity, delta_coast;
    let quantity_arr = [];
    let price_arr = [];

    let total_forms = parseInt($('input[name=orderitems-TOTAL_FORMS]').val());
    console.log(total_forms);

    let order_total_quantity = parseInt($('.order_total_quantity').text()) || 0;
    console.log(order_total_quantity);
}