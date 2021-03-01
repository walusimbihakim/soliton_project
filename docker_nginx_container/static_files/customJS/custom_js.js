$(document).ready(() => {
    // Save Client Contact
    $("#add_client_contact").click(() => {
        var form_data = $("#contact_form").serialize();
        $.ajax({
            type: 'POST',
            url: configuration['clients']['add_client_contact'],
            data: form_data,
            dataType: 'json',
            success: (data) => {
                location.reload();
                return false;
            }
        });
    })

    // Delete Client 
    $("#delete_client_btn").click(() => {
        var client_id = $('input[type=hidden]').val();
        alert("Hi: ", client_id);
        document.querySelector("#table").children[0].children[r].children[c].innerText
        $.ajax({
            type: 'get',
            url: configuration['clients']['delete_client'],
            data: { "client_id": client_id },
            dataType: 'json',
            success: (data) => {
                location.reload();
            }
        });
    })

    // Get number material unit cost
    $("#id_material").change(() => {
        material = document.querySelector('#id_material').value;

        $.ajax({
            type: 'get',
            url: configuration['projects']['get_material_unitcost'],
            data: { 'material': material },
            dataType: 'json',
            success: (data) => {
                if (data.success) {
                    document.querySelector('#id_unit_cost').value = data.unit_cost;

                    quantity = document.querySelector('#id_quantity').value;

                    if (quantity > 0) {
                        unit_cost = document.querySelector('#id_unit_cost').value;

                        total_cost = (quantity * unit_cost)
                        document.querySelector('#id_total_cost').value = total_cost;
                    }

                }
            },
        });
    });

    // Get expense rate
    $("#id_expense").change(() => {
        expense = document.querySelector('#id_expense').value;
        $.ajax({
            type: 'get',
            url: configuration['projects']['get_expense_rate'],
            data: { 'expense': expense },
            dataType: 'json',
            success: (data) => {
                if (data.success) {
                    document.querySelector('#id_rate').value = data.rate;

                    quantity = document.querySelector('#id_quantity').value;

                    if (quantity > 0) {
                        rate = document.querySelector('#id_rate').value;

                        total_cost = (quantity * rate)
                        document.querySelector('#id_total_cost').value = total_cost;
                    }

                }
            },
        });
    });

    // Compute Total cost
    document.querySelector("#id_quantity").onkeyup = () => {
        quantity = document.querySelector('#id_quantity').value;
        unit_cost = document.querySelector('#id_unit_cost').value;

        total_cost = (quantity * unit_cost)
        document.querySelector('#id_total_cost').value = total_cost;

    };






});