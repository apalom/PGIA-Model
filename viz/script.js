

let width = 800, height = 400;
let networkSVG = d3.select('#network-Div')
    .append('svg')
    .attr('id', 'networkSVG')
    .attr('width', width)
    .attr('height', height);

let t = 1;
readData();

let slider = document.getElementById("myRange");
// Update the current slider value (each time you drag the slider handle)
slider.oninput = function() {
    console.log('Hr: ', this.value);
    t = this.value;
    readData();
};

/**
 * Update the data according to network definition
 */
async function readData() {

    //try{
        const busData = await d3.csv('case12_bus.csv');
        const ampData = await d3.csv('lineAmps.csv');

        console.log("Bus Config: ", busData);
        console.log("Amp Data: ", ampData);


        updateData(busData, ampData, t)

    // } catch (error) {
    //     alert('Could not load the dataset!');
    // }
}

function updateData(busData, ampData, t) {
    //console.log('Line 0 tbus: ', busData[0].tbus);

    //let t = 1;
    let hr = 'hr' + t;

    console.log("Hr: ", hr);

    // Set up linear SVG scales
    let xScale = d3.scaleLinear()
        .domain([1, 4])
        .range([0.1*width, 0.9*width]);
    let yScale = d3.scaleLinear()
        .domain([1, 3])
        .range([0.1*height, 0.9*height]);

    let min = d3.min(ampData, function(d) {
        return d[hr]});

    let max = d3.max(ampData, function(d) {
        return d[hr]});

    console.log('Min/Max', min, max)

    // Setup ColorScale
    let colorScale = d3.scaleLinear()
        .domain([min-5, max])
        .range(['white', 'red']);

    let branches = d3.select('#networkSVG')   // SELECT

    let selectBranches = branches             // UPDATE
        .selectAll('line').data(busData);

    let drawBranches = selectBranches         // ENTER
        .enter().append('line');

    drawBranches.exit().remove();

    console.log('ampHr: ', ampData[0][hr])

    //Update properties of path according to the bound data
    drawBranches
        .attr('x1', (d) => xScale(d.fromX))
        .attr('y1', (d) => yScale(d.fromY))
        .attr('x2', (d) => xScale(d.toX))
        .attr('y2', (d) => yScale(d.toY))
        .attr('id', (d,i) => 'line' + (i+1))
        .attr('stroke', function(d,i) {
            console.log(ampData[i][hr], colorScale(ampData[i][hr]))
            return colorScale(ampData[i][hr])
        });

    let labelBranches = selectBranches
        .enter().append('text');

    labelBranches.exit().remove();

    labelBranches
        .text((d,i) => d.line + ' = ' + ampData[i][hr])
        .attr('x', (d) => 0.5*(xScale(d.fromX) + xScale(d.toX))+5)
        .attr('y', (d) => 0.5*(yScale(d.fromY) + yScale(d.toY))-10);

    let drawBuses = selectBranches
        .enter().append('rect');

    drawBuses
        .attr('x', (d) => xScale(d.toX)-7.5)
        .attr('y', (d) => yScale(d.toY)-7.5)
        .attr('height', 15)
        .attr('width', 15);

    console.log(ampData[0][hr])

}

function selectHr() {

    //Slider to change the selectHr of the data
    let dayScale = d3.scaleLinear()
        .domain([0, width])
        .range([0, 23]);

    let hrSlider = networkSVG
        .append('div').classed('slider-wrap', true)
        .append('input').classed('slider', true)
        .attr('type', 'range')
        .attr('min', 1800)
        .attr('max', 2020)
        .attr('value', this.Hr);

    let sliderLabel = d3.select('.slider-wrap')
        .append('div').classed('slider-label', true)
        .append('svg');

    let sliderText = sliderLabel
        .append('text')
        .text(this.Hr);

    sliderText.attr('x', dayScale(this.Hr));
    sliderText.attr('y', 25);

    console.log(this.Hr)

}


