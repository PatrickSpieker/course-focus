/**
 * Created by pspieker on 4/27/16.
 */
$(document).ready(function() {

    var prereqSlider = $("#prereq-slider").bxSlider({
        mode: 'horizontal',
        infiniteLoop: true

    });

    var postOptSlider = $("#postopt-slider").bxSlider({
        mode: 'horizontal',
        infiniteLoop: true
    });


    createDepts();

    $("button.new-dept").click(function() {
        var dept = $("#depts").val();
        $.getJSON("../ext/course-data-uwccs.json", function(data) {
            $("#courses").empty();
            for (var course_id in data[dept]) {
                $("#courses").append("<option value=\"" + course_id + "\">" + course_id + "</option>")
            }
        });
    });

    $("button.new-course").click(function(e) {
        e.preventDefault();
        // emptying the sliders and the selected course info
        prereqSlider.empty();
        postOptSlider.empty();
        $(".selected-info").empty();

        var course_id = $("#courses").val();
        var dept = $("#depts").val();

        $.getJSON("../ext/course-data-uwccs.json", function(data) {
            var course = data[dept][course_id];
            $(".selected-info").append(course["course_info"]);

            /* Dealing with the prereqs */
            if (course["reg_prereqs"].length + course["choice_prereqs"].length == 0) {
                $("#prereq-slider").append("<li><p>No prereqs</p></li>");
                prereqSlider.reloadSlider();
            }
            for (var i = 0; i < course["reg_prereqs"].length; i++) {
                var cid = course["reg_prereqs"][i];
                var toBeDisplayed = "";
                if (cid in data[dept]) {
                    toBeDisplayed = data[dept][cid]["course_info"];
                } else {
                    toBeDisplayed = cid;
                }
                $("#prereq-slider").append("<li><p>" + toBeDisplayed + "</p></li>");
                prereqSlider.reloadSlider();
            }
            for (var i = 0; i < course["choice_prereqs"].length; i++) {
                $("#prereq-slider").append("<li><p>" + course["choice_prereqs"][i] + "</p></li>");
                prereqSlider.reloadSlider();
            }

            /* Dealing with the post-options */
            if (course["is_prereq_for"].length == 0) {
                $("#postopt-slider").append("<li><p>This class isn't a prerequisite for any classes</p></li>");
                postOptSlider.reloadSlider();

            }
            for (var i = 0; i < course["is_prereq_for"].length; i++) {
                var cid = course["is_prereq_for"][i];
                var toBeDisplayed = "";
                if (cid in data[dept]) {
                    toBeDisplayed = data[dept][cid]["course_info"];
                } else {
                    toBeDisplayed = cid;
                }
                $("#postopt-slider").append("<li><p>" + toBeDisplayed + "</p></li>");
                postOptSlider.reloadSlider();
            }
        });
    });


});