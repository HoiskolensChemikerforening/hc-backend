(function ($) {
    $(function () {
        $('.button-collapse').sideNav();
    });
})(jQuery);

$(document).ready(function () {
    $('select').material_select();
});

$('.modal').modal({
        dismissible: true, // Modal can be dismissed by clicking outside of the modal
        opacity: .5, // Opacity of modal background
        inDuration: 300, // Transition in duration
        outDuration: 200, // Transition out duration
        startingTop: '4%', // Starting top style attribute
        endingTop: '10%', // Ending top style attribute
    }
);