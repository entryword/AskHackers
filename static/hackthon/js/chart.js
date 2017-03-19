function load(id) {
    require.config({
        paths: {
            echarts: 'http://echarts.baidu.com/build/dist'
        }
    });


// 使用
    require(
        [
            'echarts',
            'echarts/chart/pie' // 使用柱状图就加载bar模块，按需加载
        ],
        function (ec) {
            var myChart = ec.init(document.getElementById('test'));

            option = {
                tooltip: {
                    trigger: 'item',
                    formatter: "{a} <br/>{b} : {c} ({d}%)"
                },

                series: [
                    {
                        type: 'pie',
                        radius: '36%',
                        center: ['50%', '50%'],
                        data: [
                            {value: data[id][0], name: '正面'},
                            {value: data[id][1], name: '负面'},
                            {value: data[id][2], name: '客观'},
                        ],
                        itemStyle: {
                            emphasis: {
                                shadowBlur: 10,
                                shadowOffsetX: 0,
                                shadowColor: 'rgba(0, 0, 0, 0.5)'
                            }
                        }
                    }
                ]
            };

            myChart.setOption(option);
        }
    );
}