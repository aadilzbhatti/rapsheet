/**
 * Created by aadil on 10/26/15.
 */

$(document).ready(function() {
    var $avg = $('#avg');
    var data = JSON.parse($avg.text());
    $avg.empty();

    var datamap = [];
    var dates = [];
    var keys = [];

    for (var key in data) {
        var date = new Date(key);
        date.setFullYear(new Date().getFullYear());
        dates.push(date);
        keys.push(key);
    }

    for (var key in dates) {
        var date = dates[key];
        var item = keys[key];
        datamap.push([date, data[item]]);
    }

    var margin = {top: 100, right: 40, bottom: 100, left: 50};
    var r = 5;

    var w = 900 - margin.left - margin.right;
    var h = 600 - margin.top - margin.bottom;

    var max_date = Math.max.apply(null, dates);
    var min_date = Math.min.apply(null, dates);

    // x-scale
    var xScale = d3.time.scale()
        .domain([min_date, max_date])
        .range([0, w - 20]);

    //x-axis
    var xAxis = d3.svg.axis()
        .scale(xScale)
        .orient('bottom')
        .ticks(datamap.length)
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
        .ticks(datamap.length);

    // create svg
    var svg = d3.select(".graph")
        .append("svg")
        .attr("width", w + margin.left + margin.right)
        .attr("height", h + margin.top + margin.bottom);

    // the pop up for each data point
    var tip = d3.tip()
        .attr("class", "d3-tip")
        .offset([-10, 0])
        .html(function(d) {
            return "<strong>Sentiment:</strong> <span style='color: red'>" + d[1] + "</span>";
        });

    svg.call(tip);

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
        .attr("r", r)
        .on("mouseover", tip.show)
        .on("mouseout", tip.hide);

    // add lines
    var line = d3.svg.line()
        .x(function(d) {
            return xScale(d[0]) + 50;
        })
        .y(function(d) {
            return yScale(d[1]);
        })
        .interpolate("linear");

    // the line
    svg.append("path")
        .attr("class", "line")
        .attr("fill", "none")
        .attr("stroke", "black")
        .attr("d", line(datamap));

    // add x-axis
    svg.append("g")
        .attr("class", "axis")
        .attr("transform", "translate(50," + h + ")")
        .style("font-family", "Source Sans Pro")
        .call(xAxis);

    // add text to x-axis
    svg.append("text")
        .attr("class", "x-label")
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
        .attr("class", "y-label")
        .attr("text-anchor", "middle")
        .attr("dy", ".75em")
        .attr("transform", "rotate(-90)")
        .attr("x", w * 2)
        .attr("y", h)
        .style("font-family", "Source Sans Pro")
        .text("Sentiment");
});