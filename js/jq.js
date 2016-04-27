/**
 * Created by pspieker on 4/27/16.
 */
$(document).ready(function() {

    var slider = $('.bxslider').bxSlider({
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
        // emptying the slider and the selected course info 
        slider.empty();
        $(".selected-info").empty();

        var course_id = $("#courses").val();
        var dept = $("#depts").val();

        $.getJSON("../ext/course-data-uwccs.json", function(data) {
            var course = data[dept][course_id];
            $(".selected-info").append(course["course_info"]);
            if (course["reg_prereqs"].length + course["choice_prereqs"].length == 0) {
                $(".bxslider").append("<li><p>No prereqs</p></li>");
                slider.reloadSlider();
            }
            for (var i = 0; i < course["reg_prereqs"].length; i++) {
                $(".bxslider").append("<li><p>" + course["reg_prereqs"][i] + "</p></li>");
                slider.reloadSlider();
            }
            for (var i = 0; i < course["choice_prereqs"].length; i++) {
                $(".bxslider").append("<li><p>" + course["choice_prereqs"][i] + "</p></li>");
                slider.reloadSlider();
            }
        });
    });


});