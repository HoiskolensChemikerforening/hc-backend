// The table is printed out with a row for each grade
// But we want a column for each grade, therefore the table is transposed
// https://stackoverflow.com/a/6298066/2520711

$(document).ready(function () {
    $("table").each(function () {
        var $this = $(this);
        var newrows = [];
        $this.find("tr").each(function () {
            var i = 0;
            $(this).find("td,th").each(function () {
                i++;
                if (newrows[i] === undefined) {
                    newrows[i] = $("<tr></tr>");
                }

                newrows[i].append($(this));
            });
        });
        $this.find("tr").remove();
        $.each(newrows, function (index, element) {
            $this.append(element);
        });
    });
    return false;
});
