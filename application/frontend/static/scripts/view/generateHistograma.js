import { ApiRequest } from '../apiRequest.js';
import { BASE_URL, API_MOUSE_MOVE } from '../consts/apiConstants.js';

const API = new ApiRequest(BASE_URL);

async function plot2DDensityPlot() {
    // Fazer a solicitação à API
    const response = await API.get(API_MOUSE_MOVE + '/user');

    // Extrair dados da resposta da API
    const data = response; // Supondo que a resposta da API tenha um campo 'data' que contém os dados necessários

    // Extrair coordenadas X e Y dos dados
    const xCoords = data.map(item => item.x_position);
    const yCoords = data.map(item => item.y_position);

    // Criar os dados do gráfico de densidade 2D
    const densityPlotData = [{
        x: xCoords,
        y: yCoords,
        type: 'histogram2dcontour', // Definir o tipo de gráfico como histograma de contorno 2D
        colorscale: 'Jet', // Especificar a escala de cores
        reversescale: false, // Inverter a escala de cores
        contours: {
            start: 0, // Valor inicial das linhas de contorno
            end: 20, // Valor final das linhas de contorno
            size: 1 // Tamanho das linhas de contorno
        },
        colorbar: {
            title: 'Densidade' // Título da barra de cores
        }
    }];

    // Definir o layout do gráfico de densidade 2D
    const layout = {
        title: 'Gráfico de Densidade 2D',
        xaxis: {
            title: 'Coordenada X'
        },
        yaxis: {
            title: 'Coordenada Y'
        },
        // Definir o fundo como transparente
        plot_bgcolor: 'rgba(0, 0, 0, 0)',
        paper_bgcolor: 'rgba(0, 0, 0, 0)'
    };

    // Plotar o gráfico de densidade 2D no elemento HTML com o id 'densityPlot'
    Plotly.newPlot('densityPlot', densityPlotData, layout);
}

// Chamar a função para plotar o gráfico de densidade 2D quando o documento estiver pronto
document.addEventListener('DOMContentLoaded', plot2DDensityPlot);
