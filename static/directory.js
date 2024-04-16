
function searchByBodyPart() {
    var selectedBodyPart = $("#bodyPartSelect").val();
    window.location.href = "/directory?body_part=" + selectedBodyPart;
}

$(document).ready(()=>{
    console.log('hello');
    $('#bodyPartSearchButton').click(()=>{
        console.log($('#bodyPartSelect').val());
        searchByBodyPart()
    });
});