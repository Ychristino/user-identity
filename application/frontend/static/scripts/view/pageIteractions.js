import { MOUSE_MOVE, FULL_DATA } from './apiView.js';
import { plotScatterPlot } from './generateScatterplot.js';
import { plot2DDensityPlot } from './generate2DDensity.js';
import { plotGroupBar } from './generateGroupBar.js';
import { show_notification } from '../common/alert.js';

document.getElementById('graphType').addEventListener('change', (event)=>{
    const SELECT_USER = document.getElementById('user');
    const USER_DIV = document.getElementById('userArea');

    if (event.target.value.toLowerCase() === 'comparative'){
        SELECT_USER.disabled = true;
        USER_DIV.style.display = 'none';
    }
    else{
        SELECT_USER.disabled = false;
        USER_DIV.style.display = 'block';
    }
});

document.getElementById('generateGraph').addEventListener('click', async () => {
    const PLOT_SELECTED = document.getElementById('graphType').value;
    const SELECTED_USER = document.getElementById('user').value;
    const GRAPH_PLOT = document.getElementById('graphPlot');
    const LOADING_SPINNER = document.getElementById("loading").style;
    const BTM_GENERATE = document.getElementById('generateGraph').style;

    LOADING_SPINNER.display = "block"; // Exibir o spinner
    BTM_GENERATE.disabled = true;

    try {
        GRAPH_PLOT.innerHTML = '';
        await plot_graph(PLOT_SELECTED, SELECTED_USER);
    } catch (error) {
        show_notification(`Erro ao obter dados para o gráfico. ${error}`, 'success');
    } finally {
        LOADING_SPINNER.display = "none"; // Ocultar o spinner após o término da função plot_graph
        BTM_GENERATE.disabled = false;
    }
});

async function plot_graph(graph_type, username) {
    try {
        switch(graph_type.toLowerCase()) {
            case 'heatmap':
                const HEATMAP_DATA = await MOUSE_MOVE(username);
                plot2DDensityPlot(HEATMAP_DATA, 'graphPlot');
                break;
            case 'scatterplot':
                const SCATTER_DATA = await MOUSE_MOVE(username);
                plotScatterPlot(SCATTER_DATA, 'graphPlot');
                break;
            case 'statistics':
                show_notification('Esta opção ainda não está disponível...', 'info');
                break;
            case 'comparative':
                const GROUPBAR_DATA = await FULL_DATA();
                plotGroupBar(GROUPBAR_DATA, 'graphPlot')
                break;
            default:
                alert("You know that's an invalid option... Please, don't do that.");
        }
    } catch (error) {
        show_notification(`Erro ao obter dados do usuário. ${error}`, 'danger');
        throw error;
    }
}