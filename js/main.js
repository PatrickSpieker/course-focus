/**
 * Created by pspieker on 4/27/16.
 */
function createDepts() {
    $.getJSON("../ext/course-data-uwccs.json", function(data) {
        for (var key in data) {
            $("#depts").append("<option value=\"" + key + "\">" + key + "</option>");
        }
    });
}

function loadCourses(dept) {
    $.getJSON("../ext/course-data-uwccs.json", function(data) {
        $("#courses").empty();
        for (var course_id in data[dept]) {
            $("#courses").append("<option value=\"" + course_id + "\">" + course_id + "</option>")
        }
    });
}
/*
function selectCourse(course_id) {
    $.getJSON("../ext/course-data-uwccs.json", function(data) {

        $(".selected-info").empty();


        var dept = $("#depts").val();
        var course = data[dept][course_id];

        $(".selected-info").append(course["course_info"]);

        if (course["reg_prereqs"].length + course["choice_prereqs"].length == 0) {
            $(".bxslider").append("<li><p>No prereqs</p></li>");

        }
        for (var i = 0; i < course["reg_prereqs"].length; i++) {
            $(".bxslider").append("<li><p>" + course["reg_prereqs"][i] + "</p></li>");


        }
        for (var i = 0; i < course["choice_prereqs"].length; i++) {
            $(".bxslider").append("<li><p>" + course["choice_prereqs"][i] + "</p></li>");

        }
        $(".bxslider").bxSlider().reloadSlider();
    });

}*/