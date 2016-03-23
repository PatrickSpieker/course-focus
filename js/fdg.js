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
                $(".selected-crs-info").remove();
                $(".sidebar").append('<div class="selected-crs-info"></div>');
                var name = d["course_id"];
                var reg_prereqs = d["reg_prereqs"];
                var choice_prereqs = d["choice_prereqs"];
                $(".selected-crs-info").append("<h5>" + name + "</h5>");
                for (var prereq in reg_prereqs) {
                    $(".selected-crs-info").append("<p>" + reg_prereqs[prereq] + "</p>");
                }

                for (var prereq in choice_prereqs) {
                    $(".selected-crs-info").append("<p>" + choice_prereqs[prereq] + "</p>");
                }
            })
            .call(force.drag);


        node.append("circle")
            .attr("r", 25)
            .attr("stroke", "black")
            .attr("fill", "white");

        node.append("text")
            .attr("dx", -12)
            .attr("font-size", "8px")
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