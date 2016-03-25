var loadDepts = function(data) {
    for (var key in data) {
        $("#depts").append("<option value=\""+ key + "\">" + key + "</option>");
    }
};

var loadFDG = function(dept) {
    var w = 1000;
    var h = 800;

    var svg = d3.select("div.graph").append("svg")
        .attr("width", w)
        .attr("height", h);
    var force = d3.layout.force()
        .gravity(.05)
        .distance(200)
        .charge(-150)
        .size([w, h]);

    d3.json('ext/' + dept + '-force.json', function (error, json_data) {
        if (error) throw error;

        force.nodes(json_data.nodes)
            .links(json_data.links)
            .start();

        var link = svg.selectAll(".link")
            .data(json_data.links)
            .enter().append("line")
            .attr("class", "link");

        var node = svg.selectAll(".node")
            .data(json_data.nodes).enter()
            .append("g")
            .on("click", function(d) {
                $old_crs = $(".selected-crs-info");
                $old_crs.remove();
                $(".sidebar").append('<div class="selected-crs-info"></div>');
                $new_crs = $(".selected-crs-info");
                console.log(d);
                var name = d["course_id"];
                var reg_prereqs = d["reg_prereqs"];
                var choice_prereqs = d["choice_prereqs"];

                $new_crs.append("<h5>" + name + "</h5>");
                $new_crs.append("<h6>Must complete all of:</h6>");
                for (var prereq in reg_prereqs) {
                    $new_crs.append("<p>" + reg_prereqs[prereq] + "</p>");
                }
                $new_crs.append("<h6>Must complete at least one of:</h6>");
                
                for (var i = 0; i < choice_prereqs.length; i++) {
                    //$new_crs.append("<p>" + choice_prereqs[prereq] + "</p>");

                }
            })
            .call(force.drag);


        node.append("circle")
            .attr("r", 25)
            .attr("stroke", "black")
            .attr("fill", "white");

        node.append("text")
            .attr("dx", -16)
            .attr("font-size", "13px")
            .attr("font-family", "Times New Roman")
            .attr("stroke", "black")
            .text(function (d) {
                return d["course_id"];
            });


        force.on("tick", function () {
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
            node.attr("transform", function (d) {
                return "translate(" + d.x + "," + d.y + ")";
            });

        });
    });
};