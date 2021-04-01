$(document).ready(() => {

    $("#reject-btn").on("click", () => {
        alert("Hey");

        wage_id = document.querySelector('#id_wage').value;
        $.ajax({
            type: 'post',
            url: configuration['projects']['reject_wage'],
            data: { 'id': id_wage },
            dataType: 'json',
            success: (data) => {
                if (data.success) {

                }
            },
        });

    })

});