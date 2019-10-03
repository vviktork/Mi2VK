$(document).ready(function (){
    $('#TableID1 tbody').on('click', '.btn-secondary', function(){
        var currow = $(this).closest('tr');
        var trable = 'Нет';
        var message = currow.find('td:eq(7)').text();
        var numer = currow.find('td:eq(8)').text();

        $("#checkbox2").prop("style", "display:none");
        $("#checkbox3").prop("style", "display:block");

        modal_edit(numer, trable, message);
    });

    $('#TableID2 tbody').on('click', '.btn-secondary', function(){
        var currow = $(this).closest('tr');
        var trable = currow.find('td:eq(7)').text();
        var message = currow.find('td:eq(8)').text();
        var numer = currow.find('td:eq(8)').text();

        $("#checkbox2").prop("style", "display:none");
        $("#checkbox3").prop("style", "display:block");

        modal_edit(numer, trable, message);
    });

    $('#TableID3 tbody').on('click', '.btn-secondary', function(){
        var currow = $(this).closest('tr');
        var trable = currow.find('td:eq(7)').text();
        var message = currow.find('td:eq(8)').text();
        var numer = currow.find('td:eq(8)').text();

        $("#checkbox2").prop("style", "display:block");
        $("#checkbox3").prop("style", "display:none");

        modal_edit(numer, trable, message);
    });

    $('.table tbody').on('click', '.btn-danger', function(){
        var currow = $(this).closest('tr');
        var trable = currow.find('td:eq(7)').text();
        var numer = currow.find('td:eq(8)').text();

        $('#deleteModalLabel').text('Удалить объект № ' + numer);
        $('#delete').val(numer);
        $('#trable-delete').val(trable);
        $('#deleteModal').modal('show');
    });

    $('#vk').on('click', function(){
        $('#vkModal').modal('show');
    });

});


function modal_edit(numer, trable, message) {
    $('#editModalLabel').text('Объект № ' + numer);
    $('#number-table').val(numer);
    $('#trable-number').val(trable);
    $('#message-text').val(message);
    $('#editModal').modal('show');

};