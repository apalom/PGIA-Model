

let width = 800, height = 400;
let networkSVG = d3.select('#network-Div')
    .append('svg')
    .attr('id', 'networkSVG')
    .attr('width', width)
    .attr('height', height);

readData();


/**
 * Update the data according to network definition
 */
async function readData() {

    //try{
        const busData = await d3.csv('case12_bus.csv');
        const ampData = await d3.csv('lineAmps.csv');

        console.log("Bus Config: ", busData);
        console.log("Line Loading: ", ampData);
        //console.log("Current: ", ampData);

        updateData(busData, ampData, t)

    // } catch (error) {
    //     alert('Could not load the dataset!');
    // }
}

function updateData(busData, ampData, t) {
    //console.log('Line 0 tbus: ', busData[0].tbus);

    //let t = 1;
    let hr = 'hr' + t;

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

}

