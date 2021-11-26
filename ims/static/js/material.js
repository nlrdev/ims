function sum_totals(t) {
    var net_measure = t.column(1, { search: "applied" }).data().sum();
    var total_cost = t.column(2, { search: "applied" }).data().sum();
    $("#net_measure").html(net_measure.toFixed(2));
    $("#total_cost").html(total_cost.toFixed(2));
}

$(function() {
    $("#recalculate_materials").click(function(event) {
        $.ajax({
            type: "POST",
            data: {
                request_type: "recalculate_materials",
                csrfmiddlewaretoken: $('input[name="csrfmiddlewaretoken"]').attr(
                    "value"
                ),
            },
            dataType: "json",
            error: function(request, error) {
                console.log(arguments);
                console.log(" Can't do because: " + error);
            },
            success: function(data) {
                table.ajax.reload();
            },
        });
    });

    var table = $("#mats_table").DataTable({
        dom: "Bfrtip",
        buttons: ["excel", "pdf"],
        ajax: {
            type: "GET",
            dataSrc: "",
        },
        columns: [{
                data: "name",
            },
            {
                data: "net_measure",
                render: function(data) {
                    return data + "g";
                },
            },
            {
                data: "total_cost",
                render: function(data) {
                    return "R" + data;
                },
            },
            {
                data: "cost_per_gram",
                render: function(data) {
                    return "R" + data;
                },
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
    }, 50);

    table.on("search.dt", function() {
        sum_totals(table);
    });
});