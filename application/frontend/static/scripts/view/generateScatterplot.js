import { ApiRequest } from '../apiRequest.js';
import { BASE_URL, API_MOUSE_MOVE } from '../consts/apiConstants.js';

const API = new ApiRequest(BASE_URL);

async function plotScatterPlot() {
    // Fazer a solicitação à API
    const response = await API.get(API_MOUSE_MOVE + '/suspect');

    // Extrair dados da resposta da API
    const data = response; // Supondo que a resposta da API tenha um campo 'data' que contém os dados necessários

    // Extrair coordenadas x e y dos dados
    const xCoords = data.map(item => item.x_position);
    const yCoords = data.map(item => item.y_position);

    // Criar o layout do gráfico de dispersão
    const layout = {
        title: 'Gráfico de Dispersão',
        xaxis: {
            title: 'Coordenada X'
        },
        yaxis: {
            title: 'Coordenada Y'
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
    Plotly.newPlot('scatterPlot', scatterPlotData, layout);
}

// Chamar a função para plotar o gráfico de dispersão quando o documento estiver pronto
document.addEventListener('DOMContentLoaded', plotScatterPlot);
