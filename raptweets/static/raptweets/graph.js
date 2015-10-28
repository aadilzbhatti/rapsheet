/**
 * Created by aadil on 10/26/15.
 */

$(document).ready(function() {
    var $avg = $('#avg');
    var data = JSON.parse($avg.text());
    $avg.empty();

    var datamap = [];
    var dates = [];

    for (var key in data) {
        var date = new Date(key)
        date.setFullYear(new Date().getFullYear());
        datamap.push([date, data[key]]);
        dates.push(date);
    }

    var margin = {top: 100, right: 40, bottom: 100, left: 50};
    var r = 5;

    var w = 900 - margin.left - margin.right;
    var h = 600 - margin.top - margin.bottom;

    var max_date = new Date();
    var min_date = Math.min.apply(null, dates);

    // x-scale
    var xScale = d3.time.scale()
        .domain([min_date, max_date])
        .range([0, w - 20 * datamap.length]);

    console.log(dates);

    //x-axis
    var xAxis = d3.svg.axis()
        .scale(xScale)
        .orient('bottom')
        .ticks(Math.max(datamap.length, 1))
        .tickPadding(10)
        .tickFormat(function(d) {
            return d.toISOString().slice(0, 10);
        });

    // y-scale
    var yScale = d3.scale.linear()
        .domain([-1, 1])
        .range([h, 20]);

    // y-axis
    var yAxis = d3.svg.axis()
        .scale(yScale)
        .orient("left")
        .ticks(Math.max(datamap.length, 1));

    // create svg
    var svg = d3.select("body")
        .append("svg")
        .attr("width", w)
        .attr("height", h + 50);

    // add data points
    svg.selectAll("circle")
        .data(datamap)
        .enter()
        .append("circle")
        .attr("cx", function(d) {
            return xScale(d[0]) + 50;
        })
        .attr("cy", function(d) {
            return yScale(d[1]);
        })
        .attr("r", r);

    svg.selectAll("text")
        .data(datamap)
        .enter()
        .append("text")
        .text(function(d) {
            return d[1] + "";
        })
        .attr("x", function(d) {
            return xScale(d[0]) + 50;
        })
        .attr("y", function(d) {
            return yScale(d[1]);
        })
        .attr("font-family", "sans-serif")
        .attr("font-size", "11px")
        .attr("fill", "red")
        .on("mouseover", function() {
            var text = d3.select(this);
            text.transition()
                .duration(200)
                .attr("font-size", "22px");
        })
        .on("mouseout", function() {
            var text = d3.select(this)
            text.transition()
                .duration(200)
                .attr("font-size", "11px");
        });

    // add x-axis
    svg.append("g")
        .attr("class", "axis")
        .attr("transform", "translate(50," + h + ")")
        .style("font-family", "Source Sans Pro")
        .call(xAxis);

    // add text to x-axis
    svg.append("text")
        .attr("x", w/2)
        .attr("y", h + 50)
        .style("text-anchor", "middle")
        .style("font-family", "Source Sans Pro")
        .text("Date");

    // add y-axis
    svg.append("g")
        .attr("class", "axis")
        .attr("transform", "translate(50, 0)")
        .style("font-family", "Source Sans Pro")
        .call(yAxis);

    // add text to y-axis
    svg.append("text")
        .attr("transform", "rotate(-90)")
        .attr("y", 25)
        .attr("x", h / 2)
        .attr("dy", ".1em")
        .style("text-anchor", "middle")
        .style("font-family", "Source Sans Pro")
        .text("Sentiment");
});