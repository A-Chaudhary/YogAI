$(document).ready(() => {
    const width = 640;
    const height = 400;
    const marginTop = 20;
    const marginRight = 20;
    const marginBottom = 30;
    const marginLeft = 40;
    const container = $('#score-container');

    // Generate random data
    console.log(scores);
    const data = Array.from(scores);
    console.log(data);

    // Calculate overall score
    const overallScore = overall_score;
    console.log(overallScore);

    // Define categorical labels
    const labels = [...Array(data.length).keys()].map(i => `pose ${i + 1}`);
    labels.push("Overall Score");

    // Declare the x (horizontal position) scale.
    const x = d3.scaleBand()
        .domain(labels)
        .range([marginLeft, width - marginRight])
        .padding(0.1);

    // Declare the y (vertical position) scale.
    const y = d3.scaleLinear()
        .domain([0, 100])
        .range([height - marginBottom, marginTop]);

    // Create the SVG container.
    const svg = d3.create("svg")
        .attr("width", width)
        .attr("height", height);

    // Add bars
    svg.selectAll(".bar")
        .data([...data, overallScore]) // Add overall score to data
        .enter().append("rect")
        .attr("class", (d, i) => i === data.length ? "overall-bar" : "bar") // Highlight overall score bar
        .attr("x", (d, i) => x(labels[i]))
        .attr("y", d => y(d))
        .attr("width", x.bandwidth())
        .attr("height", d => height - marginBottom - y(d))
        .style('fill', "rgb(20, 52, 67)");

    // Add the x-axis.
    svg.append("g")
        .attr("transform", `translate(0,${height - marginBottom})`)
        .call(d3.axisBottom(x));

    // Add the y-axis.
    svg.append("g")
        .attr("transform", `translate(${marginLeft},0)`)
        .call(d3.axisLeft(y));

    // Append the SVG element.
    container.append(svg.node());
});
