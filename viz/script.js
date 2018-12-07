
loadSystem().then(data => {

    console.log('Data: ', data);

    this.ampData = data.ampData;
    this.busData = data.busData;
    this.xfmrData = data.xfmrData;

    drawSystem(data.busData);
    drawSlider(1);
});

function drawSystem(busData) {

    // Set up SVG
    let width = 800, height = 400;

    let networkSVG = d3.select('#network-Div')
        .append('svg')
        .attr('id', 'networkSVG')
        .attr('width', width)
        .attr('height', height);

    // Set up linear SVG scales
    let xScale = d3.scaleLinear()
        .domain([1, 4])
        .range([0.1*width, 0.9*width]);
    let yScale = d3.scaleLinear()
        .domain([1, 3])
        .range([0.1*height, 0.9*height]);

    let branches = d3.select('#networkSVG');   // SELECT

    let selectBranches = branches              // UPDATE
        .selectAll('g').data(busData);

    this.drawBranches = selectBranches         // ENTER
        .enter().append('g');

    this.drawBranches.exit().remove();

    console.log('Line', busData[0].Line)

    this.drawBranches
        .append('text')
        .attr('x', (d) => 0.5 * (xScale(d.fromX)+xScale(d.toX)) + 5)
        .attr('y', (d) => 0.5 * (yScale(d.fromY)+yScale(d.toY)) + 20)
        .text((d,i) => busData[i].Line + ' = ' + 0);

    this.drawBranches
        .append('line')
        .attr('x1', (d) => xScale(d.fromX))
        .attr('y1', (d) => yScale(d.fromY))
        .attr('x2', (d) => xScale(d.toX))
        .attr('y2', (d) => yScale(d.toY))
        .attr('stroke', 'black')
        .attr('id', (d,i) => busData[i].Line)

    let drawBuses = selectBranches
        .enter().append('rect');

    drawBuses
        .attr('x', (d) => xScale(d.toX)-7.5)
        .attr('y', (d) => yScale(d.toY)-7.5)
        //.attr('id', (d,i) => 'bus' + (i+1))
        .attr('class', 'bus');

    let drawTransformer =  d3.select('#networkSVG');

    drawTransformer
        .append('rect')
        .attr('x', xScale(3)-7.5)
        .attr('y', yScale(2)-7.5)
        .attr('class', 'bus');

    drawTransformer
        .append('text')
        .attr('x', xScale(3)+10)
        .attr('y', yScale(2))
        .text('Bus 1');
}

function drawSlider(activeHr) {

    let xfmrData = this.xfmrData;

    // Set up SVG
    let width = 800, height = 60;

    console.log('xfmrData: ', xfmrData)

    // Set up the scales
    let hrScale = d3.scaleLinear()
        .domain([1, 24])//d3.max(xfmrData, d => d.hr)])
        .range([30, 650]);
    let kwScale = d3.scaleLinear()
        .domain([0, 130]) //d3.max(xfmrData, d => d.kw)])
        .range([0, (height-10)]);

    let xfmrLoadSVG = d3.select('#sliderDiv')
        .append('svg')
        .attr('id', 'totLoadSVG')
        .attr('transform', 'translate(55,-5) scale(1,-1)') //'translate(70,-5)
        .attr('width', width)
        .attr('height', height);

    let areaGen = d3.area()
        .x(d => hrScale(d.hr))
        .y0(0)
        .y1(d => kwScale(d.kw));

    let areaData = areaGen(xfmrData);

    let selectArea = d3.select("#totLoadSVG")
        .append('path');

    selectArea
        .attr('d', areaData);


    //Slider to change the activeHr of the data
    let hourSlider = d3.select('#sliderDiv')
        .append('div').classed('slider-wrap', true)
        .append('input').classed('slider', true)
        .attr('type', 'range')
        .attr('min', 1)
        .attr('max', 24)
        .attr('value', activeHr);

    let sliderLabel = d3.select('.slider-wrap')
        .append('div').classed('slider-label', true)
        .append('svg');

    let sliderText = sliderLabel.append('text')
        .text(activeHr);

    sliderText.attr('x', hrScale(activeHr));
    sliderText.attr('y', 25);

    hourSlider.on('input', function() {

        sliderText.text(this.value);
        sliderText.attr('x', hrScale(this.value));

        updateHr(this.value);
    });
}


function updateHr(activeHr) {
    let ampData1 = this.ampData;

    let hr = 'hr' + activeHr;

    let hrAmps = [];
    hrAmps = ampData1.map( function(d,i) {
        hrAmps[i] = parseFloat(ampData1[i][hr])
        return hrAmps;
    });

    hrAmps = hrAmps[0];

    let min = d3.min(hrAmps);
    let max = d3.max(hrAmps);

    let width = 800, height = 400;

    let xScale = d3.scaleLinear()
        .domain([1, 4])
        .range([0.1*width, 0.9*width]);
    let yScale = d3.scaleLinear()
        .domain([1, 3])
        .range([0.1*height, 0.9*height]);

    // Setup ColorScale
    let colorScale = d3.scaleLinear()
        .domain([min-10, max])
        .range(['white', 'red']);

    //Update properties of path according to the bound data
    // let branchColors = this.drawBranches.selectAll('line');

    this.drawBranches
        .select('line')
        .attr('stroke', function(d,i) {
            //console.log(ampData1[i][hr], colorScale(ampData1[i][hr]));
            return colorScale(ampData1[i][hr])
        });

    this.drawBranches
        .selectAll('text').remove();

    this.drawBranches.append('text');

    this.drawBranches
        .select('text')
        .attr('x', (d) => 0.5 * (xScale(d.fromX)+xScale(d.toX)) + 5)
        .attr('y', (d) => 0.5 * (yScale(d.fromY)+yScale(d.toY)) + 20)
        .text((d,i) => d.Line + ' = ' + ampData1[i][hr]);
}



async function loadSystem () {
    const busData = await d3.csv('case12_bus.csv');
    const ampData = await d3.csv('lineAmps.csv');
    const xfmrData = await d3.csv('P_XFMR.csv');

    return {
        'busData': busData,
        'ampData': ampData,
        'xfmrData': xfmrData
    };
}
