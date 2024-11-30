// static/js/script.js

document.addEventListener('DOMContentLoaded', function() {
    // 获取图表数据
    fetch('/data')
        .then(response => response.json())
        .then(data => {
            // 解析数据
            const timestamps = data.timestamps;
            const apDown = data.ap_down;
            const switchDown = data.switch_down;
            const oldOntDown = data.old_ont_down;
            const newOntDown = data.new_ont_down;

            // 使用Plotly绘制图表
            const trace1 = {
                x: timestamps,
                y: apDown,
                mode: 'lines+markers',
                name: 'AP Down'
            };

            const trace2 = {
                x: timestamps,
                y: switchDown,
                mode: 'lines+markers',
                name: 'Switch Down'
            };

            const trace3 = {
                x: timestamps,
                y: oldOntDown,
                mode: 'lines+markers',
                name: 'Old ONT Down'
            };

            const trace4 = {
                x: timestamps,
                y: newOntDown,
                mode: 'lines+markers',
                name: 'New ONT Down'
            };

            const dataTraces = [trace1, trace2, trace3, trace4];

            const layout = {
                title: '设备在线情况',
                xaxis: { title: '时间' },
                yaxis: { title: '在线数量' }
            };

            Plotly.newPlot('chart', dataTraces, layout);
        })
        .catch(error => console.error('Error fetching data:', error));
});