
loadSystem().then(data => {

    console.log('Data: ', data);

    this.ampData = data.ampData;
    this.busData = data.busData;

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
        .attr('id', (d,i) => 'bus' + (i+1))
        .attr('height', 15)
        .attr('width', 15);

    let drawTransformer =  d3.select('#networkSVG')

    drawTransformer
        .append('rect')
        .attr('x', xScale(3)-7.5)
        .attr('y', yScale(2)-7.5)
        .attr('height', 15)
        .attr('width', 15);

    drawTransformer
        .append('text')
        .attr('x', xScale(3)+10)
        .attr('y', yScale(2))
        .text('Bus 1');

}

function drawSlider(activeHr) {

    //Slider to change the activeYear of the data
    let hourScale = d3.scaleLinear()
        .domain([1, 24]).range([30, 650]);

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

    sliderText.attr('x', hourScale(activeHr));
    sliderText.attr('y', 25);

    hourSlider.on('input', function() {

        sliderText.text(this.value);
        sliderText.attr('x', hourScale(this.value));

        updateHr(this.value);
    });
}


function updateHr(activeHr) {
    let ampData1 = this.ampData;
    let busData1 = this.busData;

    console.log('ampData1: ', ampData1);
    console.log('busData1: ', busData1);
    console.log('Hr: ', activeHr);

    let hr = 'hr' + activeHr;

    let min = d3.min(ampData1, function(d) {
        return d[hr]
    });

    let max = d3.max(ampData1, function(d) {
        return d[hr]
    });

    console.log('Min/Max', min, max);

    let width = 800, height = 400;

    let xScale = d3.scaleLinear()
        .domain([1, 4])
        .range([0.1*width, 0.9*width]);
    let yScale = d3.scaleLinear()
        .domain([1, 3])
        .range([0.1*height, 0.9*height]);

    // Setup ColorScale
    let colorScale = d3.scaleLinear()
        .domain([min-5, max])
        .range(['white', 'red']);

    //Update properties of path according to the bound data
    // let branchColors = this.drawBranches.selectAll('line');

    this.drawBranches
        .select('line')
        .attr('stroke', function(d,i) {
            console.log(ampData1[i][hr], colorScale(ampData1[i][hr]));
            return colorScale(ampData1[i][hr])
        });

    this.drawBranches
        .selectAll('text').remove();

    this.drawBranches.append('text');

    this.drawBranches
        .selectAll('text')
        .attr('x', (d) => 0.5 * (xScale(d.fromX)+xScale(d.toX)) + 5)
        .attr('y', (d) => 0.5 * (yScale(d.fromY)+yScale(d.toY)) + 20)
        .text((d,i) => d.Line + ' = ' + ampData1[i][hr]);

}

async function loadSystem () {
    const busData = await d3.csv('case12_bus.csv');
    const ampData = await d3.csv('lineAmps.csv');

    return {
        'busData': busData,
        'ampData': ampData
    };
}

//
// let networkSVG = d3.select('#network-Div')
//     .append('svg')
//     .attr('id', 'networkSVG')
//     .attr('width', width)
//     .attr('height', height);
//
// let width = 800, height = 400;
//
// let t = 1;
// readData();
//
// let slider = document.getElementById("myRange");
// // Update the current slider value (each time you drag the slider handle)
// slider.oninput = function() {
//     console.log('Hr: ', this.value);
//     t = this.value;
//     readData();
// };
//
// /**
//  * Update the data according to network definition
//  */
// async function readData() {
//
//     //try{
//         const busData = await d3.csv('case12_bus.csv');
//         const ampData = await d3.csv('lineAmps.csv');
//
//         console.log("Bus Config: ", busData);
//         console.log("Amp Data: ", ampData);
//
//
//         updateData(busData, ampData, t)
//
//     // } catch (error) {
//     //     alert('Could not load the dataset!');
//     // }
// }
//
// function updateData(busData, ampData, t) {
//     //console.log('Line 0 tbus: ', busData[0].tbus);
//
//     //let t = 1;
//     let hr = 'hr' + t;
//
//     console.log("Hr: ", hr);
//
//     // Set up linear SVG scales
//     let xScale = d3.scaleLinear()
//         .domain([1, 4])
//         .range([0.1*width, 0.9*width]);
//     let yScale = d3.scaleLinear()
//         .domain([1, 3])
//         .range([0.1*height, 0.9*height]);
//
//     let min = d3.min(ampData, function(d) {
//         return d[hr]});
//
//     let max = d3.max(ampData, function(d) {
//         return d[hr]});
//
//     console.log('Min/Max', min, max);
//
//     // Setup ColorScale
//     let colorScale = d3.scaleLinear()
//         .domain([min-5, max])
//         .range(['white', 'red']);
//
//     let branches = d3.select('#networkSVG');   // SELECT
//
//     let selectBranches = branches             // UPDATE
//         .selectAll('line').data(busData);
//
//     let drawBranches = selectBranches         // ENTER
//         .enter().append('line');
//
//     drawBranches.exit().remove();
//
//     console.log('ampHr: ', ampData[0][hr]);
//
//     //Update properties of path according to the bound data
//     drawBranches
//         .attr('x1', (d) => xScale(d.fromX))
//         .attr('y1', (d) => yScale(d.fromY))
//         .attr('x2', (d) => xScale(d.toX))
//         .attr('y2', (d) => yScale(d.toY))
//         .attr('id', (d,i) => 'line' + (i+1))
//         .attr('stroke', function(d,i) {
//             console.log(ampData[i][hr], colorScale(ampData[i][hr]));
//             return colorScale(ampData[i][hr])
//         });
//
//     let labelBranches = selectBranches
//         .enter().append('text');
//
//     labelBranches.exit().remove();
//
//     labelBranches
//         .text((d,i) => d.line + ' = ' + ampData[i][hr])
//         .attr('x', (d) => 0.5*(xScale(d.fromX) + xScale(d.toX))+5)
//         .attr('y', (d) => 0.5*(yScale(d.fromY) + yScale(d.toY))-10);
//
//     let drawBuses = selectBranches
//         .enter().append('rect');
//
//     drawBuses
//         .attr('x', (d) => xScale(d.toX)-7.5)
//         .attr('y', (d) => yScale(d.toY)-7.5)
//         .attr('height', 15)
//         .attr('width', 15);
//
//     console.log(ampData[0][hr])
//
// }
//
// function selectHr() {
//
//     //Slider to change the selectHr of the data
//     let dayScale = d3.scaleLinear()
//         .domain([0, width])
//         .range([0, 23]);
//
//     let hrSlider = networkSVG
//         .append('div').classed('slider-wrap', true)
//         .append('input').classed('slider', true)
//         .attr('type', 'range')
//         .attr('min', 1800)
//         .attr('max', 2020)
//         .attr('value', this.Hr);
//
//     let sliderLabel = d3.select('.slider-wrap')
//         .append('div').classed('slider-label', true)
//         .append('svg');
//
//     let sliderText = sliderLabel
//         .append('text')
//         .text(this.Hr);
//
//     sliderText.attr('x', dayScale(this.Hr));
//     sliderText.attr('y', 25);
//
//     console.log(this.Hr)
//
// }
//
//
