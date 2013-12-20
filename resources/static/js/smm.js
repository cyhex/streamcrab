
var SMM = {
    
    streamChannel : {
        contentDiv : '#content',
        trackBtn : '#track',
        kwInput : '#keyords',
        stream : io.connect('/stream'),
        
        listen: function(){
            SMM.stream.on('stream_update', function(data) {
                $(SMM.streamChannel.contentDiv).append('<p>' + data.polarity + ' : ' + data.text + '</p>');
            });

            $(SMM.streamChannel.trackBtn).click(function() {
                $(SMM.streamChannel.contentDiv).html('');
                stream.emit('track', $(SMM.streamChannel.kwInput).val());
            });

            setInterval(function() {
                stream.emit('ping')
            }, 2000);
        }
    },
    streamData: {
        data: [],
        trend:{ data:[], q : [], qSize: 10}, 
        
        getData: function() {
            var d = [
                {key: 'Tweets', color:'green', values: SMM.streamData.data},
            ];
            return d;
        },
        getTrendData: function(){
            return [{key: 'Trend', color: 'gray', values: SMM.streamData.trend.data }]
        },
        
        push: function(y, x){
            var d = {y:y, x:x , size: 0.2,};
            
            if(y < 0){
                d.color = 'red'; 
            }
            
            SMM.streamData.data.push(d);
            SMM.streamData.trend.q.push(d);
            
            if(SMM.streamData.trend.q.length > SMM.streamData.trend.qSize){
               var x = SMM.streamData.trend.q[0].x;
               var y_sum = 0;
               
               for (var j = 0; j < SMM.streamData.trend.qSize; j++) {
                    y_sum +=  SMM.streamData.trend.q[0].y;
                    SMM.streamData.trend.q.shift();
                }
                var a = {
                    y:y_sum/SMM.streamData.trend.qSize, 
                    x:x,
                    size: 0.2,
                };
               SMM.streamData.trend.data.push(a);
            }
            
        },
        
        genRandom: function() {
            var points = 5;
            for (var j = 0; j < points; j++) {
                var x = new Date();
                var y = (Math.random() - 0.5) * 2;
                SMM.streamData.push(y, x);
            }
        }

    },
    
    charts : {
        chartPool : [],
        polartyChartContainer : '#polarityChart svg',
        trendChartContainer : '#trendChart svg',
        
        updateInt : 2000, 
        init : function(){
            SMM.streamData.genRandom();
            nv.addGraph(function() {
                
                var chart = nv.models.scatterChart()
                        .showDistX(true)
                        .showDistY(true);
                
                chart.xAxis.tickFormat(function(d) { return d3.time.format("%d.%m %M:%S")(new Date(d)) }).axisLabel('Time');
                chart.yAxis.tickFormat(d3.format('.02f')).axisLabel('Polarity');
                chart.tooltipContent(function(key) {
                    return "<h3>" + key + "</h3>";
                });

                d3.select(SMM.charts.polartyChartContainer).datum(SMM.streamData.getData()).transition().duration(200).call(chart);
                nv.utils.windowResize(chart.update);
               
                SMM.charts.chartPool.push(chart);
                
                var chart1 = nv.models.lineChart();
                
                chart1.xAxis.tickFormat(function(d) { return d3.time.format('%x')(new Date(d)) }).axisLabel('Time');
                chart1.yAxis.tickFormat(d3.format('.02f')).axisLabel('Trend');

                d3.select(SMM.charts.trendChartContainer).datum(SMM.streamData.getTrendData()).transition().duration(200).call(chart1);
                nv.utils.windowResize(chart1.update);
               
                SMM.charts.chartPool.push(chart1);
            });
            
           setInterval(function() { SMM.charts.redraw() }, SMM.charts.updateInt);
            
        },
        
        redraw: function() {
            SMM.streamData.genRandom();
            for (i in SMM.charts.chartPool){
                SMM.charts.chartPool[i].update();
            }
        }
    }
    
};

