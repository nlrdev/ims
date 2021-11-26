function sum_totals(t) {
    var total_measure = t.column(1, { search: "applied" }).data().sum();
    var total_price = t.column(2, { search: "applied" }).data().sum();
    $("#total_measure").html(total_measure.toFixed(2));
    $("#total_price").html(total_price.toFixed(2));
}

function edit_note_model(t) {
    $("#editNoteModal").modal("toggle");
    $("#note_id").attr("value", t.getAttribute("id"));
    $("#note_value").val(t.getAttribute("val"));
}

function clear_note_form() {
    $("#note_value").val("");
}

$(function() {
    token = $('input[name="csrfmiddlewaretoken"]').attr("value")
    $("#note_form").submit(function(event) {
        event.preventDefault();
        $.ajax({
            type: "POST",
            data: {
                request_type: "note_form",
                id: $("#note_id").val(),
                note: $("#note_value").val(),
                csrfmiddlewaretoken: token,
            },
            dataType: "json",
            error: function(error) {
                console.log(" Can't do because: " + error);
            },
            success: function() {
                table.ajax.reload();
                $("#editNoteModal").modal("hide");
            },
        });
    });

    $("#material_form").submit(function(event) {
        event.preventDefault();
        $.ajax({
            type: "POST",
            data: {
                request_type: "material_form",
                name: $("#id_name").val(),
                csrfmiddlewaretoken: token,
            },
            dataType: "json",
            error: function(error) {
                console.log(" Can't do because: " + error);
            },
            success: function(data) {
                $("#id_type").append(
                    $("<option/>", {
                        value: data[0].id,
                        text: data[0].text,
                    })
                );
                $("#material_form")[0].reset();
                $("#id_type").val(data[0].id)
            },
        });
    });

    $("#puchaces_form").submit(function(event) {
        event.preventDefault();
        $.ajax({
            type: "POST",
            data: {
                request_type: "puchaces_form",
                type: $("#id_type").val(),
                price: $("#id_price").val(),
                measure: $("#id_measure").val(),
                notes: $("#id_notes").val(),
                date_of_purchase: $("#id_date_of_purchase").val(),
                csrfmiddlewaretoken: token,
            },
            dataType: "json",
            error: function(error) {
                console.log(" Can't do because: " + error);
            },
            success: function() {
                $("#puchaces_form")[0].reset();
                table.ajax.reload();
            },
        });
    });

    var table = $("#purchace_table").DataTable({
        dom: "Bfrtip",
        buttons: ["excel", "pdf"],
        ajax: {
            type: "GET",
            dataSrc: "",
        },
        columns: [{
                data: "type",
            },
            {
                data: "measure",
            },
            {
                data: "price",
            },
            {
                data: function(data) {
                    return (
                        "<div id='" +
                        data.id +
                        "' val='" +
                        data.notes +
                        "' onclick='edit_note_model(this)'> <span style='font-size: 0.9rem;'><i class='fas fa-edit fa-xs'> </i> </span>" +
                        data.notes +
                        "</div>"
                    );
                },
            },
            {
                data: "date_of_purchase",
            },
        ],
        responsive: true,
        scrollY: "720px",
        scrollCollapse: true,
        paging: false,
        info: false,
        select: true,
    });

    window.setTimeout(function() {
        sum_totals(table);
    }, 5);

    table.on("search.dt", function() {
        sum_totals(table);
    });

    $("#id_date_of_purchase").datepicker({ dateFormat: "yy-mm-dd" });
});