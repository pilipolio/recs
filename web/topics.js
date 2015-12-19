function show(svg, path) {

    d3.json(path , function(error, data) {
	if (error) throw error;
		
	svg.selectAll('.point').data(data.articles).enter()
	    .append('svg:circle')
	    .attr('r', 4)
            .style("fill", function(d) { return sectionsToColor[d.section] })
            .style("fill-opacity", .4)
	    .append("svg:title")
	    .text(function(d) {return d.title });

	var x = featureNames[0]
	var y = featureNames[1]
	
	console.info("selected:" + x + " " + y)

	var scales = getScale(x, y)	
	
	var topicsGroups = svg.selectAll("g")
	    .data(multiLinesData(data)).enter().append("g")
	
	var topicLineFunction = d3.svg.line()
	    .x(function(d) { return scales.x(d[x]) })
	    .y(function(d) { return scales.y(d[y]) })
	    .interpolate("linear")
	
	var multilineGraph = topicsGroups
	    .append("path")
	    .attr("id", function(d) { return d.id})
	    .attr("class", "topicLine")
	    .attr("d", function(d) { return topicLine(scales, x, y)(d.vector)})
	    .attr("stroke", "blue")
	    .attr("stroke-width", 2)
	    .attr("fill", "none")

	topicsGroups
	    .append('text')
	    .append('textPath')
	    .attr('startOffset', '50%')
	    .attr('xlink:href', function (d) {return '#' + d.id})
	    .text(function (d) {return d.words})
	    .attr("fill", "blue")
	    	
	console.info("scales")

	draw(scales, svg.selectAll('circle'), featureNames[0], featureNames[1])
	
	svg.select(".xLabel").on("click", function() { switchDimension("X")})
	svg.select(".yLabel").on("click", function() { switchDimension("Y")})

    });
}

function topicLine(scales, x, y) {
    console.log("line func")
    var lineFunction = d3.svg.line()
	.x(function(d) { console.log(d); return scales.x(d[x]) })
	.y(function(d) { return scales.y(d[y]) })
	.interpolate("linear")
    return lineFunction
}

function multiLinesData(data) {
    var multiLines = []
    var nDims = 10
    var nTopics = 30;//data.topics.length
    for (i = 0; i < nTopics; i++) {
	var lineData = []
	var zeroPoint = {}
	var topicPoint = {}
	for (j = 0; j < nDims; j++) {
	    zeroPoint[j] = 0
	    topicPoint[j] = data.topics[i][j]
	}
	lineData.push(zeroPoint)
	lineData.push(topicPoint)
	var topicName = "topic" + i
	multiLines.push({ "id": topicName, "vector":lineData, "words": data.topics[i].words})
    }
    
    return multiLines
}

function draw(scales, svgCircles, featureForX, featureForY) {
    svgCircles
	.attr('cx', function(d) { return scales.x(d[featureForX]) })
	.attr('cy', function(d) { return scales.y(d[featureForY]) })
}

function getScale(featureForX, featureForY) { 
    
    var scales = {
	x : d3.scale.linear()
	    .domain(featureNamesToRanges[featureForX])
	    .range([widthMargin, width - 2 * widthMargin]),
	y : d3.scale.linear()
	    .domain(featureNamesToRanges[featureForY])
	    .range([height - 2 * heightMargin, heightMargin])
    }
    
    // http://chimera.labs.oreilly.com/books/1230000000345/ch08.html
    var xAxis = d3.svg.axis()
        .scale(scales.x)
        .orient("bottom")
        .ticks(5);
    
    // Only appending axis the first time
    var axisClass = svg.select(".xaxis")
    if (axisClass.empty()) {
        console.log("xaxisClass is empty")
        axisClass = svg.append("g")
            .attr("class", "axis xaxis")
            .attr("transform", "translate(0," + (height - 2 * heightMargin) + ")")

        // http://stackoverflow.com/questions/11189284/d3-axis-labeling
        svg.append("text")
            .attr("class", "axis xLabel")
            .attr("text-anchor", "middle")
            .attr("x", width / 2)
            .attr("y", height - heightMargin / 2)
    }
    axisClass.call(xAxis);
    svg.select(".xLabel").text(featureForX)
    
    var yAxis = d3.svg.axis()
        .scale(scales.y)
        .orient("left")
        .ticks(5);

    var axisClass = svg.select(".yaxis")
    if (axisClass.empty()) {
        console.log("yaxisClass is empty")
        axisClass = svg.append("g")
            .attr("class", "axis yaxis")
            .attr("transform", "translate(" + widthMargin + ",0)")

        svg.append("text")
            .attr("class", "axis yLabel")
            .attr("text-anchor", "middle")
            .attr("x", - height / 2)
            .attr("y", 0)
            .attr("dy", ".75em")
            .attr("transform", "rotate(-90)")
    }
    axisClass.call(yAxis);            
    svg.select(".yLabel").text(featureForY)

    return scales
}

function switchDimension(dims) {
    console.log("switchDimension")

    var indexOfFeatureForX = featureNames.indexOf( svg.select(".xLabel").text() )
    var indexOfFeatureForY = featureNames.indexOf( svg.select(".yLabel").text() )
    
    if (dims.indexOf("X") != -1) {
        indexOfFeatureForX = (indexOfFeatureForX + 1) % featureNames.length
    }
    if (dims.indexOf("Y") != -1) {
        indexOfFeatureForY = (indexOfFeatureForY + 1) % featureNames.length
    }

    var x = featureNames[indexOfFeatureForX]
    var y = featureNames[indexOfFeatureForY]
    var scales = getScale(x, y)
    
    	//.attr("d", line(scales, x, y)(xys))

    draw(scales, svg.selectAll('circle').transition().duration(2000), x, y)

    svg.selectAll('.topicLine')
	.transition().duration(2000)
	.attr("d", function(d) { return topicLine(scales, x, y)(d.vector)})
}
