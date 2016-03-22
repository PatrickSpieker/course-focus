var w = 800;
var h = 800;

var svg = d3.select("div.graph").append("svg")
        .attr("width", w)
        .attr("height", h);
var force = d3.layout.force()
        .gravity(.05)
        .distance(100)
        .charge(-150)
        .size([w, h]);

/*
d3.select("#depts").selectAll("li")
            .data(json_data.nodes)
            .enter()
            .append("li")
            .text(function(d){
                return d['']
            });*/
d3.json('ext/force-data.json', function(error, json_data) {
    if (error) throw error;

    force.nodes(json_data.nodes)
            .links(json_data.links)
            .start();

    var node = svg.selectAll("g")
            .data(json_data.nodes);

    var nodeEnter = node.enter()
            .append("g")
            .call(force.drag);

    var circle = nodeEnter.append("circle")
            .attr("r", 25)
            .attr("stroke", "black")
            .attr("fill", "white");

    nodeEnter.append("text")
            .attr("dx", -12)
            .attr("font-size", "8px")
            .text(function (d) {
                return d["course_id"];
            });

    var link = svg.selectAll(".link")
            .data(json_data.links)
            .enter().append("line")
            .attr("class", "link");

    force.on("tick", function () {
        link
                .attr("x1", function(d) {
                    return d.source.x;
                })
                        .attr("y1", function(d) {
                            return d.source.y;
                        })
                        .attr("x2", function(d) {
                            return d.target.x;
                        })
                        .attr("y2", function(d) {
                            return d.target.y;
                        });
                node.attr("transform", function (d) {
                    return "translate(" + d.x + "," + d.y + ")";
                });

            });
});