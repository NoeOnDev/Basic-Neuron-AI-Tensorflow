// Expresión regular numero #3
function esValida(cadena) {
    const regex = /^[Rr](?:[Oo]{0,4})?(?:[Mm]{0,4})?(?:[Nn]{0,4})?$/;

    return regex.test(cadena);
}
function generarAutomata() {
    let cadena = document.getElementById('cadena').value;
    let estados = [];
    let transiciones = [];

    if (!esValida(cadena)) {
        d3.select("#automata").selectAll("*").remove();
        alert('La cadena no es válida');
        document.getElementById('cadena').value = '';
        return;
    }

    d3.select("#automata").style("display", "block");

    for (let i = 0; i <= cadena.length; i++) {
        estados.push({id: 'q' + i, x: 100 + 200 * i, y: 40, inicial: i === 0, final: i === cadena.length});
        if (i > 0) {
            transiciones.push({from: 'q' + (i-1), to: 'q' + i, label: cadena[i-1]});
        }
    }
    let maxX = Math.max(...estados.map(estado => estado.x)) + 100;
    let maxY = Math.max(...estados.map(estado => estado.y)) + 40;

    let svg = d3.select("#automata")
        .attr("width", maxX)
        .attr("height", maxY);

        svg.selectAll("*").remove();

    let nodo = svg.selectAll("circle")
        .data(estados)
        .enter()
        .append("circle")
        .attr("r", 30)
        .attr("cx", d => d.x)
        .attr("cy", d => d.y)
        .style("fill", "none")
        .style("stroke", "#000")
        .style("stroke-width", 2);
    
    let etiquetaNodo = svg.selectAll("text")
        .data(estados)
        .enter()
        .append("text")
        .text(d => d.id)
        .attr("x", d => d.x)
        .attr("y", d => d.y)
        .attr("text-anchor", "middle")
        .attr("dy", ".35em");
    
    let radio = 30;
    svg.append("defs").append("marker")
        .attr("id", "arrow")
        .attr("viewBox", "0 -5 10 10")
        .attr("refX", 8)
        .attr("markerWidth", 6)
        .attr("markerHeight", 6)
        .attr("orient", "auto")
    .append("path")
        .attr("d", "M0,-5L10,0L0,5")
        .style("fill", "#000");

    let arista = svg.selectAll("line")
        .data(transiciones)
        .enter()
        .append("line")
        .attr("x1", d => estados.find(estado => estado.id === d.from).x + radio * Math.cos(Math.atan2(estados.find(estado => estado.id === d.to).y - estados.find(estado => estado.id === d.from).y, estados.find(estado => estado.id === d.to).x - estados.find(estado => estado.id === d.from).x)))
        .attr("y1", d => estados.find(estado => estado.id === d.from).y + radio * Math.sin(Math.atan2(estados.find(estado => estado.id === d.to).y - estados.find(estado => estado.id === d.from).y, estados.find(estado => estado.id === d.to).x - estados.find(estado => estado.id === d.from).x)))
        .attr("x2", d => estados.find(estado => estado.id === d.to).x - radio * Math.cos(Math.atan2(estados.find(estado => estado.id === d.to).y - estados.find(estado => estado.id === d.from).y, estados.find(estado => estado.id === d.to).x - estados.find(estado => estado.id === d.from).x)))
        .attr("y2", d => estados.find(estado => estado.id === d.to).y - radio * Math.sin(Math.atan2(estados.find(estado => estado.id === d.to).y - estados.find(estado => estado.id === d.from).y, estados.find(estado => estado.id === d.to).x - estados.find(estado => estado.id === d.from).x)))
        .style("stroke", "#000")
        .style("stroke-width", 2)
        .attr("marker-end", "url(#arrow)");

            
    
    let etiquetaArista = svg.selectAll(".etiquetaArista")
        .data(transiciones)
        .enter()
        .append("text")
        .text(d => d.label)
        .attr("x", d => (estados.find(estado => estado.id === d.from).x + estados.find(estado => estado.id === d.to).x) / 2)
        .attr("y", d => (estados.find(estado => estado.id === d.from).y + estados.find(estado => estado.id === d.to).y) / 2)
        .attr("text-anchor", "middle")
        .attr("dy", "-.35em");
        
        let nodoInicial = svg.selectAll(".inicial")
        .data(estados.filter(d => d.inicial))
        .enter()
        .append("polygon")
        .attr("points", d => `${d.x-30},${d.y} ${d.x-60},${d.y-30} ${d.x-60},${d.y+30}`)
        .style("fill", "#000");
    
    let nodoFinal = svg.selectAll(".final")
        .data(estados.filter(d => d.final))
        .enter()
        .append("circle")
        .attr("r", 35)
        .attr("cx", d => d.x)
        .attr("cy", d => d.y)
        .style("fill", "none")
        .style("stroke", "#000")
        .style("stroke-width", 2);
}

document.getElementById('generar').addEventListener('click', generarAutomata);