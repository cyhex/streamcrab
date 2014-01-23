
var SMM = {
    streamChannel: {
        trackBtn: '#track',
        kwInput: '#keyords',
        stream: null,
        listen: function() {

            if (SMM.stream == null) {
                SMM.stream = io.connect('/stream');
            }

            SMM.stream.on('stream_update', function(data) {
                SMM.streamData.push(data);
            });

            $(SMM.streamChannel.trackBtn).click(function() {
                SMM.stream.emit('track', $(SMM.streamChannel.kwInput).val());
                SMM.streamData.clear();
                SMM.charts.redraw()
            });

            setInterval(function() {
                SMM.stream.emit('ping')
            }, 2000);
        }
    },
    streamData: {
        data: [],
        trend: {data: [], q: [], qSize: 10},
        objectivity: {data: [], q: [], qSize: 10},
        sums: {pCount: 0, nCount: 0, pSum: 0, nSum: 0, },
        getData: function() {
            var d = [
                {key: 'Tweets', color: 'green', values: SMM.streamData.data, type: 'line'},
            ];

            return d;
        },
        getTrendData: function() {
            return [
                {key: 'Polarity trend', color: 'gray', values: SMM.streamData.trend.data},
            ];
        },
        getSumData: function() {
            var t = SMM.streamData.sums.pCount + SMM.streamData.sums.nCount;
            if(!t){
                return [];
            }
            return [
                {
                    key: 'Positive',
                    value: SMM.streamData.sums.pCount / t},
                {
                    key: 'Negative',
                    value: SMM.streamData.sums.nCount / t},
            ];
        },
        push: function(data) {

            var d0 = {y: data.polarity, x: new Date(data.stamp), size: 0.2, text: data.text};

            if (data.polarity < 0) {
                d0.color = 'red';
                SMM.streamData.sums.nCount += 1;
                SMM.streamData.sums.nSum += d0.y;
            } else {
                SMM.streamData.sums.pCount += 1;
                SMM.streamData.sums.pSum += d0.y;
            }

            SMM.streamData.data.push(d0);

            var d1 = {y: data.polarity, x: new Date(data.stamp)};
            SMM.streamData.smooth(SMM.streamData.trend, d1);

        },
        smooth: function(container, d) {
            container.q.push(d);
            if (container.q.length > container.qSize) {
                var x = container.q[0].x;
                var y_sum = 0;

                for (var j = 0; j < container.qSize; j++) {
                    y_sum += container.q[0].y;
                    container.q.shift();
                }
                var c = 'green';
                if (y_sum / container.qSize < 0) {
                    var c = 'red';
                }
                var a = {
                    y: y_sum / container.qSize,
                    x: x,
                    size: 2,
                    color: c
                };
                container.data.push(a);
            }
        },
        clear: function() {
            //SMM.streamData.data = [];
            //SMM.streamData.trend = { data:[], q : [], qSize: 10};
        },
    },
    charts: {
        chartPool: [],
        sumChartContainer: '#sumChart svg',
        polartyChartContainer: '#polarityChart svg',
        trendChartContainer: '#trendChart svg',
        updateInt: 2000,
        init: function() {
            nv.addGraph(function() {
                var chartSumColors = d3.scale.ordinal().range(['green', 'red']);

                var chartSum = nv.models.pieChart()
                        .showLegend(false).color(chartSumColors.range())
                        .x(function(d) {
                    return d.key
                })
                        .y(function(d) {
                    return d.value
                });



                chartSum.updateManual = function() {
                    d3.select(SMM.charts.sumChartContainer).datum(SMM.streamData.getSumData).transition().duration(200).call(chartSum);
                }

                d3.select(SMM.charts.sumChartContainer).datum(SMM.streamData.getSumData).transition().duration(200).call(chartSum);
                nv.utils.windowResize(chartSum.update);
                SMM.charts.chartPool.push(chartSum);

                var chartDist = nv.models.scatterChart()
                        .showDistX(true)
                        .showDistY(true)
                        .showLegend(false);

                chartDist.xAxis.tickFormat(function(d) {
                    return d3.time.format("%H:%M:%S")(new Date(d))
                }).axisLabel('Time');
                chartDist.yAxis.tickFormat(d3.format('.02f')).axisLabel('Polarity');
                chartDist.tooltipContent(function(key, x, y, d) {
                    return "<div class='tooltipContainer'>" + d.point.text + "</div>";
                });

                d3.select(SMM.charts.polartyChartContainer).datum(SMM.streamData.getData).transition().duration(200).call(chartDist);
                nv.utils.windowResize(chartDist.update);

                SMM.charts.chartPool.push(chartDist);

                var chartTrend = nv.models.lineChart();
                chartTrend.showLegend(false);
                chartTrend.xAxis.tickFormat(function(d) {
                    return d3.time.format("%H:%M:%S")(new Date(d))
                }).axisLabel('Time');
                chartTrend.yAxis.tickFormat(d3.format('.02f')).axisLabel('Polarity');

                d3.select(SMM.charts.trendChartContainer).datum(SMM.streamData.getTrendData).transition().duration(200).call(chartTrend);
                nv.utils.windowResize(chartTrend.update);

                SMM.charts.chartPool.push(chartTrend);



            });

            setInterval(function() {
                SMM.charts.redraw()
            }, SMM.charts.updateInt);

        },
        redraw: function() {
            for (i in SMM.charts.chartPool) {
                SMM.charts.chartPool[i].update();
                if (typeof SMM.charts.chartPool[i].updateManual === 'function') {
                    SMM.charts.chartPool[i].updateManual();
                }

            }
        }
    }

};

