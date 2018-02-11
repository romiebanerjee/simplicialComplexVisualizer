svg = d3.select("#Viz"),
    width = +svg.attr("width"),
    height = +svg.attr("height");


var simulation = d3.forceSimulation()
  .force('charge', d3.forceManyBody().strength(-100))
  .force('center', d3.forceCenter(width / 2, height / 2))
  .force("link", d3.forceLink())
  


d3.json("complex.json", function(error, complex){
  if (error) throw error;
   
  //Force Link Network//

  simulation
      .nodes(complex.nodes)
      .on("tick", ticked);

  simulation.force("link")
      .links(complex.edges);

 var line = d3.line()
  .x(function(d) { return complex.nodes[d.node].x; })
  .y(function(d) { return complex.nodes[d.node].y; })
  .curve(d3.curveLinear);
	

  function updateLinks() {
    var u = d3.select('.links')
      .selectAll('line')
      .data(complex.edges)

    u.enter()
      .append('line')
      .merge(u)
      .attr('x1', function(d) {return d.source.x;})
      .attr('y1', function(d) {return d.source.y;})
      .attr('x2', function(d) {return d.target.x;})
      .attr('y2', function(d) {return d.target.y;})

    u.exit().remove()
  }

  function updateNodes() {
    u = d3.select('.nodes')
      .selectAll('circle')
      .data(complex.nodes)

    u.enter()
      .append('circle')
      .merge(u)
      .attr('cx', function(d) {return d.x;})
      .attr('cy', function(d) {return d.y;})
      .attr('r', 3)
      .call(d3.drag()	
          .on("start", dragstarted)
          .on("drag", dragged)
          .on("end", dragended));

    u.exit().remove()
  }

function updatePaths(){
  u = d3.select('.paths')
  .selectAll('path')
  .data(complex.faces)
  
  u.enter()
    .append('path')
  .merge(u)
    .attr('d', function(d){
    return line(d)})
  
  u.exit().remove()
}

  function ticked() {
    updateLinks()
    updateNodes()
    updatePaths()
  }

  function dragstarted(d) {
  if (!d3.event.active) simulation.alphaTarget(0.3).restart();
  d.fx = d.x;
  d.fy = d.y;
}

function dragged(d) {
  d.fx = d3.event.x;
  d.fy = d3.event.y;
}

function dragended(d) {
  if (!d3.event.active) simulation.alphaTarget(0);
  d.fx = null;
  d.fy = null;
 }
 
})

