import { show_notification } from '../common/alert.js';
import { EXECUTE_MODEL } from './apiModel.js';

document.getElementById('allActivitiesCheckbox').addEventListener('click', ()=>{

    const SELECTED_ACTIVITY = document.getElementById('activitySelect');

    SELECTED_ACTIVITY.disabled = event.target.checked;

});

document.getElementById('executeModel').addEventListener('click', async () => {

    const SELECTED_MODEL = document.getElementById('modelSelect').value;
    const SELECTED_ACTIVITY = document.getElementById('activitySelect').value;
    const BTM_EXECUTE = document.getElementById('executeModel').style;
    const LOADING_SPINNER = document.getElementById("loading").style;

    LOADING_SPINNER.display = "block"; // Exibir o spinner
    BTM_EXECUTE.disabled = true;

    try {
        await EXECUTE_MODEL();
    } catch (error) {
        show_notification(`Erro ao executar o modelo. ${error}`, 'danger');
    } finally {
        LOADING_SPINNER.display = "none"; // Ocultar o spinner após o término da função plot_graph
        BTM_EXECUTE.disabled = false;
    }
});