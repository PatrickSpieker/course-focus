$(document).ready(function() {

    $.getJSON("../ext/course-data-uwccs.json", function(data) {
        loadDepts(data);
    });

    loadFDG("CSE");

    $('button.new-dept').click(function() {
        $("svg").remove();
        var nextDept = $("#depts").val();
        loadFDG(nextDept);
    });
});