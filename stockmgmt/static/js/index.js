$(document).ready(function () {
    $(document).on('click','#thisclosebutton',function (e) {
        e.preventDefault();
        $(this).parent().remove();
    })
})