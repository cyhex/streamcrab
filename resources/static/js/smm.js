
var SMM = {
    streamChannel: {
        stopTracking: '#stopTracking',
        restartTracking: '#restartTracking',
        stream: null,
        listen: function(kw) {

            if (SMM.stream == null) {
                SMM.stream = io.connect('/stream');
            }

            SMM.stream.on('stream_update', function(data) {
                SMM.streamData.push(data);
            });
            SMM.stream.on('error', function(data) {
                $('#errorMsg section').html(data)
                $('#errorMsg').slideDown();
                $("#keyword").removeClass('loading');
                SMM.stream.disconnect();
                SMM.stream = null;
                
            });

            $(SMM.streamChannel.stopTracking).click(function() {
                SMM.stream.disconnect();
                SMM.stream = null;
                $("#keyword").removeClass('loading');
                $(this).attr('disabled','disabled');
                return false;
            });

            $(SMM.streamChannel.restartTracking).click(function() {
                SMM.stream.disconnect();
                SMM.stream = null;
                $(this).submit();
            });
            
            SMM.stream.emit('track', kw);
            SMM.streamData.clear();
            SMM.charts.redraw()

            setInterval(function() {
                if(SMM.stream){
                    SMM.stream.emit('ping')
                }
            }, 2000);
            
            return true;
        }
        
    },
    streamData: {
        data: [],
        trend: {data: [], q: [], qSize: 10},
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
            if(SMM.streamData.sums.pSum + Math.abs(SMM.streamData.sums.nSum) == 0){
                return [];
            }
            
            return [
                {
                    key: 'Positive ',
                    value: SMM.streamData.sums.pSum},
                {
                    key: 'Negative ',
                    value: Math.abs(SMM.streamData.sums.nSum)},
            ];
        },
        getCountData: function() {
            var t = SMM.streamData.sums.pCount + SMM.streamData.sums.nCount;
            if(!t){
                return [];
            }
            return [
                {
                    key: 'Positive (%)',
                    value: (SMM.streamData.sums.pCount / t)*100},
                {
                    key: 'Negative (%)',
                    value: (SMM.streamData.sums.nCount / t)*100},
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
        countChartContainer: '#countChart svg',
        polartyChartContainer: '#polarityChart svg',
        trendChartContainer: '#trendChart svg',
        updateInt: 2000,
                
        init: function() {
            if(SMM.stream == null){
                return null;
            }
            
            nv.addGraph(function() {
                var chartSumColors = d3.scale.ordinal().range(['green', 'red']);

                var chartSum = nv.models.pieChart()
                        .showLegend(false).color(chartSumColors.range())
                        .x(function(d) {
                    return d.key 
                }).y(function(d) {
                    return d.value 
                });



                chartSum.updateManual = function() {
                    d3.select(SMM.charts.sumChartContainer).datum(SMM.streamData.getSumData).transition().duration(200).call(chartSum);
                }
                chartSum.updateManual();
                nv.utils.windowResize(chartSum.update);
                SMM.charts.chartPool.push(chartSum);
                
                var chartCount = nv.models.pieChart()
                        .showLegend(false).color(chartSumColors.range())
                        .x(function(d) {
                    return d.key 
                }).y(function(d) {
                    return d.value 
                });



                chartCount.updateManual = function() {
                    d3.select(SMM.charts.countChartContainer).datum(SMM.streamData.getCountData).transition().duration(200).call(chartCount);
                }
                chartCount.updateManual();
                nv.utils.windowResize(chartCount.update);
                SMM.charts.chartPool.push(chartCount);
                
                
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
    },
    htmlHelpers: function(){
        var _mye = atob('LXQtaS1tLW8tci1ALWMteS1oLWUteC0uLWMtby1tLQ==').replace(/-/g, '');
        $(".mailMe").attr('href', 'mailto:' + _mye);
    }

};

