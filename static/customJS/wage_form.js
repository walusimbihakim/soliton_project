$(document).ready(() => {

    $("#id_quantity").on("keyup",() => {
        // Set payment according to quantity and activity rate
        activity_id = document.querySelector('#id_activity').value;
        $.ajax({
            type: 'get',
            url: configuration['projects']['get_activity_rate'],
            data: { 'activity_id': activity_id },
            dataType: 'json',
            success: (data) => {
                if (data.success) {
                    quantity = document.querySelector("#id_quantity").value
                    if((quantity > 0) && (activity_id != null)){
                         payment = data.activity_rate * quantity;
                         document.querySelector('#id_payment').value = payment;
                    }
                    else {
                    document.querySelector('#id_payment').value = 0;
                    }
                }
            },
        });

    })

});