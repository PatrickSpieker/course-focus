/*
 * -----------------------------------------------------
 * Various functions for modifying the container webpage
 * to set up a force-directed graph
 * -----------------------------------------------------
 */


// void function for adding select HTML element with all of UW's departments
var loadDepts = function(data) {
    for (var key in data) {
        $("#depts").append("<option value=\""+ key + "\">" + key + "</option>");
    }
};

// void function to load the force-directed graph into the webpage
// for a given department code at UW
var loadFDG = function(dept) {
    var w = 1000;
    var h = 800;
    var node_r = 25;

    // creating the SVG container for the force layout data
    // to be placed in
    var svg = d3.select("div.graph").append("svg")
        .attr("width", w)
        .attr("height", h);

    // creating the force layout itself
    var force = d3.layout.force()
        .gravity(.05)
        .distance(200) // distance between the nodes
        .charge(-600) // how much each node will repel the others
        .size([w, h]);

    // opening the relevant JSON file
    d3.json('ext/' + dept + '-force.json', function (error, json_data) {
        if (error) throw error;

        // adding node and link data to the layout itself
        force.nodes(json_data.nodes)
            .links(json_data.links)
            .start();

        // adding the link functionality and the SVG line
        // elements to all the elements with the link class
        var link = svg.selectAll(".link")
            .data(json_data.links)
            .enter().append("line")
            .attr("class", "link");

        // adding the node functionality to all the elements with
        // the node class (the circle elements are created below)
        var node = svg.selectAll(".node")
            .data(json_data.nodes).enter()
            .append("g")
            .on("click", function(d) {

                // removing the old course's info
                $old_crs = $(".selected-crs-info");
                $old_crs.remove();

                // appending the container for the new information
                $(".sidebar").append('<div class="selected-crs-info"></div>');
                $new_crs = $(".selected-crs-info");

                // retrieving info about the clicked course
                var name = d["course_id"];
                var reg_prereqs = d["reg_prereqs"];
                var choice_prereqs = d["choice_prereqs"];
                var info = d["course_info"];
                var is_prereq_for = d["is_prereq_for"];

                // adding the course description and link to MyPlan to the
                // sidebar
                $new_crs.append(info);


                // checking for and filling in all non-chooseable prereqs
                if (reg_prereqs.length > 0) {
                    $new_crs.append("<h6>Must complete all of:</h6>");
                    for (var i = 0; i < reg_prereqs.length; i++) {
                        $new_crs.append("<p>" + reg_prereqs[i] + "</p>");
                    }
                }

                // filling in choice prereqs
                for (var i = 0; i < choice_prereqs.length; i++) {
                    $new_crs.append("<h6>Must complete at least one of:</h6>");
                    for (var j = 0; j < choice_prereqs[i].length; j++) {
                        $new_crs.append("<p>" + choice_prereqs[i][j] + "</p>");
                    }
                }

                // filling in the classes the clicked on course is a prerequisite for
                if (is_prereq_for.length > 0) {
                    $new_crs.append("<h6>Class is a prerequisite for:</h6>");
                    for (var i = 0; i < is_prereq_for.length; i++) {
                        $new_crs.append("<p>" + is_prereq_for[i] + "</p>");
                    }
                }
            })
            .call(force.drag);

        // adding the circle elements to the SVG grouping
        node.append("circle")
            .attr("r", node_r)
            .attr("stroke", "black")
            .attr("fill", "white");

        // adding and formatting the node labels
        node.append("text")
            .attr("dx", -21)
            .attr("dy", 4)
            .attr("font-size", "12px")
            .attr("font-family", "Times New Roman")
            .attr("stroke", "black")
            .text(function (d) {
                return d["course_name"];
            });


        force.on("tick", function () {
            // updating the links with the new source x and y
            // of their respective sources and destinations
            link
                .attr("x1", function (d) {
                    return d.source.x;
                })
                .attr("y1", function (d) {
                    return d.source.y;
                })
                .attr("x2", function (d) {
                    return d.target.x;
                })
                .attr("y2", function (d) {
                    return d.target.y;
                });
            // updating the nodes' position and
            // making sure they are inside the SVG container
            node.attr("transform", function (d) {
                // setting x-boundries for the nodes
                if (d.x < node_r) {
                    d.x = node_r;
                } else if (d.x > w-node_r) {
                    d.x = w - node_r;
                }

                // setting y-boundries for the nodes
                if (d.y < node_r) {
                    d.y = node_r;
                } else if (d.y > h-node_r) {
                    d.y = h - node_r;
                }

                return "translate(" + d.x + "," + d.y + ")";
            });

        });
    });
};