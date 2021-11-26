function delete_recipe_ingredient(id) {
    $.ajax({
        type: "POST",
        data: {
            request_type: "delete_recipe_ingredient",
            id: id,
            csrfmiddlewaretoken: token,
        },
        dataType: "json",
        error: function(error) {
            console.log(" Can't do because: " + error);
        },
        success: function(data) {
            $('#ri_' + id).remove();
        },
    });
}

function clear_recipe_data() {
    $('#r_id').attr('value', "");
    $('#ri_id').attr('value', "");
    $("#r_name").val("");
    $("#r_notes").val("");
    $("#recipe_ingredient_list").html("");
    $('.toggle-hide').hide();
}

function append_ingredients(id, name, qty) {
    $("#recipe_ingredient_list").append(
        "<li id='ri_" + id + "' class='list-group-item p-0'>" +
        "<span class='justify-content-left'>" +
        name + " - " + qty +
        "</span><span class='float-right'>" +
        "<a onclick='delete_recipe_ingredient(" + id + ")'" +
        "class='ri_delete btn btn-sm btn-danger far fa-trash-alt'>" +
        "</a></span></li>"
    );
}

$(function() {
    token = $('input[name="csrfmiddlewaretoken"]').attr("value")
    $("#recipe_form").submit(function(event) {
        event.preventDefault();
        _name = $("#id_name").val();
        $.ajax({
            type: "POST",
            data: {
                request_type: "recipe_form",
                name: _name,
                csrfmiddlewaretoken: token,
            },
            dataType: "json",
            error: function(error) {
                console.log(" Can't do because: " + error);
            },
            success: function() {
                clear_recipe_data()
                table.ajax.reload();
                window.setTimeout(function() {
                    table.row(':contains(' + _name + ')').select()
                }, 25);
            },
        });
    });

    $("#recipe_update_form").submit(function(event) {
        event.preventDefault();
        _name = $("#r_name").val();
        $.ajax({
            type: "POST",
            data: {
                request_type: "recipe_update_form",
                id: $("#r_id").val(),
                name: $("#r_name").val(),
                notes: $("#r_notes").val(),
                csrfmiddlewaretoken: token,
            },
            dataType: "json",
            error: function(error) {
                console.log(" Can't do because: " + error);
            },
            success: function() {
                $("#recipe_ingredient_list").html("");
                table.ajax.reload();
                window.setTimeout(function() {
                    table.row(':contains(' + _name + ')').select()
                }, 25);
            },
        });
    });

    $("#recipe_ingredient_form").submit(function(event) {
        event.preventDefault();
        $.ajax({
            type: "POST",
            data: {
                request_type: "recipe_ingredient_form",
                id: $("#ri_id").val(),
                type: $("#ri_type option:selected").val(),
                qty: $("#ri_qty").val(),
                csrfmiddlewaretoken: token,
            },
            dataType: "json",
            error: function(error) {
                console.log(" Can't do because: " + error);
            },
            success: function(data) {
                console.log(data);
                append_ingredients(data[0].id, data[0].name, data[0].qty)
            },
        });
    });

    var table = $("#recipe_table").DataTable({
        ajax: {
            type: "GET",
            dataSrc: "",
        },
        columns: [{
            data: function(data) {
                return (data.name);
            },
        }, ],
        responsive: true,
        scrollY: "500px",
        scrollCollapse: true,
        paging: false,
        info: false,
        select: true,
    });

    table.on("select.dt", function(e, dt, type, indexes) {
        var id = dt.rows(indexes).data().pluck("id");
        var name = dt.rows(indexes).data().pluck("name");
        var notes = dt.rows(indexes).data().pluck("notes");
        $('#r_id').attr('value', id[0]);
        $('#ri_id').attr('value', id[0]);
        $("#r_name").val(name[0]);
        $('#r_notes').val(notes[0]);
        $.ajax({
            type: "POST",
            data: {
                request_type: "recipe_ingredients",
                id: id[0],
                name: name[0],
                csrfmiddlewaretoken: token,
            },
            dataType: "json",
            error: function(error) {
                console.log(" Can't do because: " + error);
            },
            success: function(data) {
                $('.toggle-hide').show();
                data.forEach(function(item) {
                    append_ingredients(item.id, item.name, item.qty)
                });
            },
        });
    });
    table.on("deselect.dt", function() {
        clear_recipe_data();
        $.ajax({
            type: "POST",
            data: {
                request_type: "deselect",
                csrfmiddlewaretoken: token,
            },
            dataType: "json",
        });
    });

    window.setTimeout(function() {
        table.row(':contains(' + $('input[name="selected_recipe"]').attr("value") + ')').select()
    }, 50);
});