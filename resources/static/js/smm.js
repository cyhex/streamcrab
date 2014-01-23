
var SMM = {
    
    streamChannel : {
        trackBtn : '#track',
        kwInput : '#keyords',
        stream : null,
        
        listen: function(){
            
            if(SMM.stream == null){
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
        trend:{ data:[], q : [], qSize: 10}, 
        objectivity:{ data:[], q : [], qSize: 10},
        sums: {pCount:0, nCount:0, pSum:0, nSum:0, objSum:0},
        
        getData: function() {
            var d = [
                {key: 'Tweets', color:'green', values: SMM.streamData.data, type: 'line'},
            ];
            
            return d;
        },
        getTrendData: function(){
            return [
                {key: 'Polarity trend', color: 'gray', values: SMM.streamData.trend.data },
                {key: 'Objectivity', color: 'yellow', values: SMM.streamData.objectivity.data }
            ];
        },
        
        push: function(data){
            console.log(data);
            
            var d0 = {y:data.polarity, x: new Date(data.stamp) , size: 0.2, text: data.text};
            
            if(data.polarity < 0){
                d0.color = 'red';
                SMM.streamData.sums.nCount +=1;
                SMM.streamData.sums.nSum += d0.y;
            }else{
                SMM.streamData.sums.pCount +=1;
                SMM.streamData.sums.pSum += d0.y;
            }
            
            SMM.streamData.data.push(d0);
            
            var d1 = {y:data.polarity, x: new Date(data.stamp)};
            SMM.streamData.smooth(SMM.streamData.trend, d1);
            
            var d2 = {y:data.objectivity, x: new Date(data.stamp)};
            SMM.streamData.smooth(SMM.streamData.objectivity, d2);
            
        },
        smooth: function(container, d){
            container.q.push(d);
            if(container.q.length > container.qSize){
               var x = container.q[0].x;
               var y_sum = 0;
               
               for (var j = 0; j < container.qSize; j++) {
                    y_sum +=  container.q[0].y;
                    container.q.shift();
                }
                var a = {
                    y:y_sum/container.qSize, 
                    x:x,
                    size: 0.2,
                };
               container.data.push(a);
            }
        },
        clear: function(){
            //SMM.streamData.data = [];
            //SMM.streamData.trend = { data:[], q : [], qSize: 10};
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
            nv.addGraph(function() {
                
                var chartDist = nv.models.scatterChart()
                        .showDistX(true)
                        .showDistY(true);
                
                chartDist.xAxis.tickFormat(function(d) { return d3.time.format("%H:%M:%S")(new Date(d)) }).axisLabel('Time');
                chartDist.yAxis.tickFormat(d3.format('.02f')).axisLabel('Polarity');
                chartDist.tooltipContent(function(key, x, y, d) {
                    return "<div class='tooltipContainer'>" + d.point.text + "</div>";
                });

                d3.select(SMM.charts.polartyChartContainer).datum(SMM.streamData.getData).transition().duration(200).call(chartDist);
                nv.utils.windowResize(chartDist.update);
               
                SMM.charts.chartPool.push(chartDist);
                
                var chartTrend = nv.models.lineChart();
                
                chartTrend.xAxis.tickFormat(function(d) { return d3.time.format("%H:%M:%S")(new Date(d)) }).axisLabel('Time');
                chartTrend.yAxis.tickFormat(d3.format('.02f')).axisLabel('Polarity');

                d3.select(SMM.charts.trendChartContainer).datum(SMM.streamData.getTrendData).transition().duration(200).call(chartTrend);
                nv.utils.windowResize(chartTrend.update);
               
                SMM.charts.chartPool.push(chartTrend);
            });
            
           setInterval(function() { SMM.charts.redraw() }, SMM.charts.updateInt);
            
        },
        
        redraw: function() {
            //SMM.streamData.genRandom();
            for (i in SMM.charts.chartPool){
                SMM.charts.chartPool[i].update();
            }
        }
    }
    
};

