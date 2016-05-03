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

    /* OnClick for selecting department */
    $("button.new-dept").click(function() {
        var dept = $("#dept").val().toUpperCase();

        $.getJSON("../ext/course-data-uwccs.json", function(data) {
            $("#courses").empty();

            /* checking for existence of department */
            if (data.hasOwnProperty(dept))  {

                var dept_data = data[dept];
                // getting and sorting course_id's
                var ids = [];
                for (var course_id in dept_data) {
                    ids.push(course_id);
                }
                ids.sort();

                // adding courses to course selector
                for (var i = 0; i < ids.length; i++) {
                    var course_id = ids[i];
                    $("#courses").append("<option value=\"" + course_id + "\">"
                                         + dept_data[course_id]["course_name"]  + "</option>");
                }
            } else {
                alert("\"" + dept + "\"" + " doesn't exist in our database. Please try again.")
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
        var dept = $("#dept").val().toUpperCase();

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