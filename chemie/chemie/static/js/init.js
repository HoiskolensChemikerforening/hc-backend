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
        inDuration: 200, // Transition in duration
        outDuration: 100, // Transition out duration
        startingTop: '2%', // Starting top style attribute
        endingTop: '2%' // Ending top style attribute
    }
);