function plot2DDensityPlot(data, plot_destination) {

    // Extrair coordenadas X e Y dos dados
    const xCoords = data.map(item => item.x_position);
    const yCoords = data.map(item => item.y_position);

    // Criar os dados do gráfico de densidade 2D com transparência nas cores
    const densityPlotData = [{
        x: xCoords,
        y: yCoords,
        type: 'histogram2dcontour', // Definir o tipo de gráfico como histograma de contorno 2D
        colorscale: [[0, 'rgba(0, 0, 0, 0)'],
                     [0.1, 'rgba(0, 0, 255, 1)'],
                     [0.2, 'rgba(0, 128, 255, 1)'],
                     [0.3, 'rgba(0, 255, 255, 1)'],
                     [0.4, 'rgba(0, 255, 128, 1)'],
                     [0.5, 'rgba(0, 255, 0, 1)'],
                     [0.6, 'rgba(69, 255, 0, 1)'],
                     [0.7, 'rgba(128, 255, 0, 1)'],
                     [0.8, 'rgba(255, 255, 0, 1)'],
                     [0.9, 'rgba(255, 128, 0, 1)'],
                     [1.0, 'rgba(255, 69, 0, 1)']
                    ]
        , // Especificar a escala de cores
        reversescale: false, // Inverter a escala de cores
        contours: {
            start: 0, // Valor inicial das linhas de contorno
            end: 20, // Valor final das linhas de contorno
            size: 1 // Tamanho das linhas de contorno
        },
        colorbar: {
            title: 'Density' // Título da barra de cores
        },
        opacity: 1 // Definir a opacidade das cores
    }];

    // Definir o layout do gráfico de densidade 2D
    const layout = {
        title: 'Heatmap',
        xaxis: {
            title: 'Width'
        },
        yaxis: {
            title: 'Height',
            autorange: 'reversed'
        },
        // Definir o fundo como transparente
        plot_bgcolor: 'rgba(0, 0, 0, 0)',
        paper_bgcolor: 'rgba(0, 0, 0, 0)',
        annotations: [
            {
                text: `Total data length: ${data.length}`, // Mensagem da legenda
                showarrow: false,
                x: 0.5, // Posição horizontal do texto
                y: 1.1, // Posição vertical do texto
                xanchor: 'center', // Ancoragem horizontal
                yanchor: 'bottom', // Ancoragem vertical
                xref: 'paper', // Referência horizontal
                yref: 'paper', // Referência vertical
            }
        ]
    };

    // Plotar o gráfico de densidade 2D no elemento HTML com o id 'densityPlot'
    Plotly.newPlot(plot_destination, densityPlotData, layout, {responsive: true});
}

export { plot2DDensityPlot };
