async function plotScatterPlot(data, plot_destination) {

    // Extrair coordenadas x e y dos dados
    const xCoords = data.map(item => item.x_position);
    const yCoords = data.map(item => item.y_position);

    // Criar o layout do gráfico de dispersão
    const layout = {
        title: 'Dispersion Graph',
        xaxis: {
            title: 'Coordinate X'
        },
        yaxis: {
            title: 'Coordinate Y',
            autorange: 'reversed'
        }
    };

    // Criar os dados do gráfico de dispersão
    const scatterPlotData = [{
        x: xCoords,
        y: yCoords,
        mode: 'markers', // Define o tipo de marcador como 'pontos'
        type: 'scatter'
    }];

    // Plotar o gráfico de dispersão no elemento HTML com o id 'scatterPlot'
    Plotly.newPlot(plot_destination, scatterPlotData, layout);
}

export { plotScatterPlot };