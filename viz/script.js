''

let width = 800, height = 400;
let networkSVG = d3.select('#network-Div')
    .append('svg')
    .attr('id', 'networkSVG')
    .attr('width', width)
    .attr('height', height);

let data = readData();


/**
 * Update the data according to network definition
 */
async function readData() {

    try{
        const data = await d3.csv('case12_branch.csv');

        console.log("Datafile: ", data);

        update(data)

        return data;

    } catch (error) {
        alert('Could not load the dataset!');
    }
}

function update(data) {
    //console.log('Line 0 tbus: ', data[0].tbus);

    // Set up the scales
    let xScale = d3.scaleLinear()
        .domain([0, 6])
        .range([0, width]);
    let yScale = d3.scaleLinear()
        .domain([0, 3])
        .range([0, height]);


    // Data to be bound is the output of aLineGenerator
    let branchGen = d3.line()
        .x((d) => xScale(d.fbus))
        .y((d) => yScale(d.tbus));

    let branchPathData = branchGen(data);

    let selectBranch = d3.select('#networkSVG')
        .append('path');

    //Update properties of path according to the bound data
    selectBranch
        .attr('d', branchPathData)
        .attr('stroke', 'black')
        .attr('stroke-width', 2);


}