import { USER_LIST, MOUSE_MOVE } from './apiView.js';
import { plotScatterPlot } from './generateScatterplot.js';
import { plot2DDensityPlot } from './generate2DDensity.js';

document.addEventListener("DOMContentLoaded", function () {
    USER_LIST()
    .then(lista => {
        const usersSelect = document.getElementById('user');
        lista.forEach(user => {
            const option = document.createElement('option');
            option.value = user.username;
            option.textContent = user.username;
            usersSelect.appendChild(option);
        });
    })
    .catch(error => {
        console.error('Erro ao obter lista de usuários:', error);
    });
});

document.getElementById('generateGraph').addEventListener('click', ()=>{
    const PLOT_SELECTED = document.getElementById('graphType').value;
    const SELECTED_USER = document.getElementById('user').value;
    const GRAPH_PLOT = document.getElementById('graphPlot');
    const LOADING_SPINNER = document.getElementById("loading").style

    GRAPH_PLOT.innerHTML = '';
    LOADING_SPINNER.display = "block";

    switch(PLOT_SELECTED.toLowerCase()){
        case 'heatmap':
            MOUSE_MOVE(SELECTED_USER)
            .then(mouse_data=>{
                plot2DDensityPlot(mouse_data, 'graphPlot');
            })
            .catch(error => {
                console.error('Erro ao obter dados do usuários:', error);
            })
            .finally(()=>{
                LOADING_SPINNER.display = "none";
            });
            break;
        case 'scatterplot':
            MOUSE_MOVE(SELECTED_USER)
            .then(mouse_data=>{
                plotScatterPlot(mouse_data, 'graphPlot');
            })
            .catch(error => {
                console.error('Erro ao obter dados do usuários:', error);
            })
            .finally(()=>{
                LOADING_SPINNER.display = "none";
            });
            break;
        case 'statistics':
            break;
        case 'comparative':
            break;
        default:
            alert("You know that's an invalid option... don't do that...");
    }

});

document.getElementById('graphType').addEventListener('change', (event)=>{
    const SELECT_USER = document.getElementById('user');

    if (event.target.value.toLowerCase() === 'comparative'){
        SELECT_USER.disabled = true;
    }
    else{
        SELECT_USER.disabled = false;
    }
});