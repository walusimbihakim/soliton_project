$(document).ready(() => {
    // Getting number of days for a given leave type
    $("#leave_type").change(() => {
        leave_type = document.querySelector('#leave_type').value;

        $.ajax({
            type: 'get',
            url: configuration['leave']['get_no_of_days'],
            data: { 'leave_type': leave_type },
            dataType: 'json',
            success: (data) => {
                if (data.success) {
                    document.querySelector('#no_days').value = data.no_of_days;
                    if (data.leave == "Annual") {
                        document.querySelector('#no_days').readOnly = false;
                    } else {
                        document.querySelector('#no_days').readOnly = true;
                    }
                } else {}
            },

        });
    });

    // Getting Leave End date
    $("#st_date").change(() => {
        start_date = document.querySelector('#st_date').value;
        no_days = document.querySelector('#no_days').value;

        $.ajax({
            type: 'get',
            url: configuration['leave']['get_end_date'],
            data: { 'startDate': start_date, 'no_of_days': no_days },
            dataType: 'json',
            success: (data) => {
                if (data.success) {
                    document.querySelector('#end_date').value = data.end_date;
                } else {
                    // alert(data.message);
                }

            },

        });
    });

    // Approving/rejecting Leave Application
    $("#submit_leave_application").click(() => {
        var selected = $("#select_action :selected").text();
        application_id = document.querySelector('#application_id').value;

        switch (selected) {
            case "Approve":
                var form_data = $("#leave_form").serialize();

                $.ajax({
                    type: 'POST',
                    url: configuration['leave']['approve_leave'],
                    data: form_data,
                    dataType: 'json',
                    success: (data) => {
                        window.location.href = configuration['leave']['leave_dashboard_page'];
                    }
                });
                break;
            case "Reject":
                var form_data = $("#leave_form").serialize();

                $.ajax({
                    type: 'POST',
                    url: configuration['leave']['reject_leave'],
                    data: form_data,
                    dataType: 'json',
                    success: (data) => {
                        window.location.href = configuration['leave']['leave_dashboard_page'];
                    }
                });
                break;
            default:
        }
    })

    // Editing Leave application
    $("#edit_leave_btn").click(() => {
        var form_data = $("#edit_leave_form").serialize();
        $.ajax({
            type: 'POST',
            url: configuration['leave']['edit_leave_application'],
            data: form_data,
            dataType: 'json',
            success: (data) => {
                window.location.href = configuration['leave']['apply_leave_page'];
            }
        });
    })

    // Deleting Leave application
    $("#delete_leave_btn").click(() => {
        $.ajax({
            type: 'POST',
            url: configuration['leave']['delete_leave_application'],
            data: form_data,
            dataType: 'json',
            success: (data) => {
                window.location.href = configuration['leave']['apply_leave_page'];
            }
        });
    })

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