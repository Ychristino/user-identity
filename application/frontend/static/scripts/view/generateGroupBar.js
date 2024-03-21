async function plotGroupBar(data, plot_destination) {
    // Extrair dados relevantes para o gráfico de barras
    const keyboardData = {};
    const mouseData = {};

    data.forEach(item => {
      for (const key in item.keyboard_info) {
        if (!keyboardData[key]) keyboardData[key] = [];
        keyboardData[key].push({ username: item.username, value: item.keyboard_info[key] });
      }
      for (const key in item.mouse_info) {
        if (!mouseData[key]) mouseData[key] = [];
        mouseData[key].push({ username: item.username, value: item.mouse_info[key] });
      }
    });

    // Definir os dados para o gráfico de barras
    const keyboardTraces = [];
    const mouseTraces = [];

    for (const key in keyboardData) {
      const usernames = keyboardData[key].map(data => data.username);
      const values = keyboardData[key].map(data => data.value);

      keyboardTraces.push({
        x: usernames,
        y: values,
        type: 'bar',
        name: key + ' (Teclado)'
      });
    }

    for (const key in mouseData) {
      const usernames = mouseData[key].map(data => data.username);
      const values = mouseData[key].map(data => data.value);

      mouseTraces.push({
        x: usernames,
        y: values,
        type: 'bar',
        name: key + ' (Mouse)'
      });
    }

    const layout = {
      title: 'Comparação entre Teclado e Mouse por Usuário',
      barmode: 'group'
    };

    // Renderizar o gráfico de barras usando Plotly
    Plotly.newPlot(plot_destination, [...keyboardTraces, ...mouseTraces], layout);
}
export { plotGroupBar };
