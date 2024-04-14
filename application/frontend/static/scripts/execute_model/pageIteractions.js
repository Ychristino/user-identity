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
    const TABLE_CONTAINER = document.getElementById('tableContainer');

    LOADING_SPINNER.display = "block"; // Exibir o spinner
    BTM_EXECUTE.disabled = true;

    try {
        TABLE_CONTAINER.innerHTML = '';
        await show_table(SELECTED_MODEL, SELECTED_ACTIVITY);
    } catch (error) {
        show_notification(`Erro ao executar o modelo. ${error}`, 'danger');
    } finally {
        LOADING_SPINNER.display = "none"; // Ocultar o spinner após o término da função plot_graph
        BTM_EXECUTE.disabled = false;
    }
});

async function show_table(selected_model, selected_activity) {
    const TABLE_CONTAINER = document.getElementById('tableContainer');
    const TABLE_METRICS = document.createElement("table");
    const THEAD = document.createElement('thead');
    const TBODY = document.createElement('tbody');
    const HEADER_ROW = document.createElement('tr');

    TABLE_METRICS.classList.add('table');
    TABLE_METRICS.classList.add('table-striped');
    TABLE_METRICS.classList.add('table-hover');

    const HEADER_LABEL =  ['USER', 'FSCORE', 'PRECISION', 'RECALL', 'SUPPORT', 'TRAIN SIZE', 'TEST SIZE'];

    HEADER_LABEL.forEach(item=>{
        const th = document.createElement('th');
        th.textContent = item;
        HEADER_ROW.appendChild(th);
    });

    const data = await EXECUTE_MODEL(selected_model, selected_activity);

    for (let key in data.metrics_by_class) {

        const TRAIN_DATA = data.train_data.find(item => item.user === key);
        const TEST_DATA = data.test_data.find(item => item.user === key);
        const tr = document.createElement('tr');

        const td_user = document.createElement('td');
        const td_fscore = document.createElement('td');
        const td_precision = document.createElement('td');
        const td_recall = document.createElement('td');
        const td_support = document.createElement('td');
        const td_train_size = document.createElement('td');
        const td_test_size = document.createElement('td');

        td_user.textContent = key;
        td_fscore.textContent = data.metrics_by_class[key].fscore;
        td_precision.textContent = data.metrics_by_class[key].precision;
        td_recall.textContent = data.metrics_by_class[key].recall;
        td_support.textContent = data.metrics_by_class[key].support;

        td_train_size.textContent = TRAIN_DATA.quantity;
        td_test_size.textContent = TEST_DATA.quantity;

        tr.appendChild(td_user);
        tr.appendChild(td_fscore);
        tr.appendChild(td_precision);
        tr.appendChild(td_recall);
        tr.appendChild(td_support);
        tr.appendChild(td_train_size);
        tr.appendChild(td_test_size);

        TBODY.appendChild(tr);
    }

    const trFooter = document.createElement('tr');

    const tdFooterLabel = document.createElement('td');
    tdFooterLabel.textContent = 'Total';

    const tdFooterTrainTotal = document.createElement('td');
    tdFooterTrainTotal.textContent = data.train_data_size;

    const tdFooterTestTotal = document.createElement('td');
    tdFooterTestTotal.textContent = data.test_data_size;

    trFooter.appendChild(tdFooterLabel);
    trFooter.appendChild(document.createElement('td')); // Coluna vazia para as métricas
    trFooter.appendChild(document.createElement('td'));
    trFooter.appendChild(document.createElement('td'));
    trFooter.appendChild(document.createElement('td'));
    trFooter.appendChild(tdFooterTrainTotal);
    trFooter.appendChild(tdFooterTestTotal);

    TBODY.appendChild(trFooter);

    THEAD.appendChild(HEADER_ROW);
    TABLE_METRICS.appendChild(THEAD);
    TABLE_METRICS.appendChild(TBODY);
    TABLE_CONTAINER.appendChild(TABLE_METRICS);
}