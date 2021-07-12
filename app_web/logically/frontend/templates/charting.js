var symbol = "KLAC" // assume symbol 

// fetch list of symbols on load 
$.get("http://localhost:9502/", function (data) {
    jd = data
    $(".result").html(data);
    // alert( "Load was performed." );
}).done(function (jd) {
    var jdata = JSON.parse(jd).symbols;
    populateTable(jdata)
    createStockChart('SPY') // default load SPY 
    // jdata.forEach(function (item) {
    //     // console.log(item) // debug 
    // });


});


function populateTable(response) {
    // PARSE THE JSON 
    /*
    sample: [{"slot":12,"customer":"Lima","fab":null,"layer":"M1 Short Loop ","owner":"Oksen Baris "}]	
    */
    var markup = '';
    response.forEach(function (item) {
        markup += '<tr onclick="createStockChart(\'' + item.trim().toUpperCase() + '\')"><td id=' + item + '>' + item + '</td>' +
            // filler
            +'<td>' + item + '</td>'
            + '<td>' + item + '</td>'
            + '<td>' + item + '</td>'
            + '<td>' + item + '</td>'
            + '<td>' + item + '</td>'
            + '</tr>';

    })
    $('#symbolTable table tbody').append(markup);
}

// initialize global vars 
var chartElement = document.getElementById('chart');
var axisElement = document.getElementById('axis');
var chart = null;
var axis = null;
var axis2 = null;
var cwidth = 1200;
var cheight = 400;


function initializechart() {
    chart = LightweightCharts.createChart(chartElement, {
        width: cwidth,
        height: cheight,
        /*   crosshair: {
            mode: 0, // notrmal mode to magnet 
        }, */
        rightPriceScale: {
            width: 60,
            scaleMargins: {
                top: 0.05,
                bottom: 0.05,
            },
        },

        priceScale: {
            position: 'right',
            mode: 1,
            autoScale: true,
            /* drawTicks: false, */
        },


        /* grid: {
                vertLines: {
                    color: 'rgba(70, 130, 180, 0.5)',
                    style: 1,
                    visible: true,
                },
                horzLines: {
                    color: 'rgba(70, 130, 180, 0.5)',
                    style: 1,
                    visible: true,
                },
            }, */
    });


    axis = LightweightCharts.createChart(axisElement, {
        width: cwidth,
        height: 180,
        /*  crosshair: {
            mode: 0
        }, */
        rightPriceScale: {
            width: 60,
            scaleMargins: {
                top: 0.01,
                bottom: 0.01,
            },
        },
        priceScale: {
            position: 'right',
            /* mode: 1, */
            autoScale: true,
            /* drawTicks: false, */
        },
    });
    axis2 = LightweightCharts.createChart(axisElement, {
        width: cwidth,
        height: 160,
        /*   crosshair: {
            mode: 0
        }, */
        rightPriceScale: {
            width: 60,
            scaleMargins: {
                top: 0.01,
                bottom: 0.01,
            },
        },
        /* priceScale: {
            position: 'right',
            mode: 1,
            autoScale: true,
            drawTicks: false,
        }, */
    });
}

// fetch data and create chart 
function createStockChart(symbol) {

    $.get("http://localhost:9502/ohlc/" + symbol + "/4H", function (data) {
        jd = data
        // $( ".result" ).html( data );
        // alert( "Load was performed." );
    }).done(function (jd) {

        // /// Add legends 
        // document.body.style.position = 'relative';
        // var legend = document.createElement('div');
        // legend.style.display = 'block';
        // legend.style.left = 3 + 'px';
        // legend.style.top = 3 + 'px';
        // legend.classList.add('legend');
        // chartElement.appendChild(legend);

        // var firstRow = document.createElement('div');
        // firstRow.innerText = symbol + '';
        // firstRow.style.color = 'black';
        // legend.appendChild(firstRow);
        // // end add legends 


        //  clear previous drawings if any and initalize 
        $('#chart').html('');
        $('#axis').html('');
        chart = null;
        axis = null;
        initializechart();
        p = new Date(Date.now());
        jdata = JSON.parse(jd)
        // jdata.index.forEach(function (item) {
        //     p = new Date(item).toLocaleString();
        //     console.log(p); 
        // })
        // p = new Date(jdata.index[jdata.index.length - 1]);
        p = new Date(Date.now());
        $('#ctitle').html(symbol + " | " + p.toLocaleString());


        /* var barSeries = chart.addBarSeries(); // addCandlestickSeries*/
        var barSeries = chart.addCandlestickSeries({
            /* title: 'Price' */
            /* autoscaleInfoProvider: original => {
                    const res = original();
                    if (res !== null) {
                        rr = res.priceRange.maxValue - res.priceRange.minValue; 
                        res.priceRange.minValue += 0.1 * rr;
                        res.priceRange.maxValue -= 0.2 * rr;
                    }
                    return res;
                }, */
            priceLineVisible: true,
            lastValueVisible: true,
        });

        var lineSeries = axis.addLineSeries({
            /* title: 'Price' */
            /* autoscaleInfoProvider: original => {
                    const res = original();
                    if (res !== null) {
                        rr = res.priceRange.maxValue - res.priceRange.minValue; 
                        res.priceRange.minValue += 0.25 * rr;
                        res.priceRange.maxValue -= 0.25 * rr;
                    }
                    return res;
                }, */
            priceLineVisible: false,
            lastValueVisible: false,
            /* baseLineVisible: true,
            baseLineColor: '#ff0000',
            baseLineWidth: 3,
            baseLineStyle: 1, */
        });
        var lineSeries2 = axis2.addHistogramSeries({
            color: 'gray',
            /* base: -10, */
            /* autoscaleInfoProvider: original => {
                const res = original();
                if (res !== null) {
                    rr = res.priceRange.maxValue - res.priceRange.minValue; 
                    res.priceRange.minValue += 0.25 * rr;
                    res.priceRange.maxValue -= 0.25 * rr;
                }
                return res;
            }, */
            priceLineVisible: false,
            lastValueVisible: false,
        });

        lineSeries.applyOptions({
            lineWidth: 1,
            /* lineType: 2,
            lineStyle: 1,
            crosshairMarkerVisible: true,
            crosshairMarkerRadius: 6,
            crosshairMarkerBorderColor: '#ffffff',
            crosshairMarkerBackgroundColor: '#2296f3', */
        });

        var data = []

        /* var jdata = JSON.parse(jd);
        console.log(jdata.columns)
        var cols = jdata.columns
        var time = jdata.index */

        //function getNextData() {
        var jdata = JSON.parse(jd);
        var data = [];
        var vdata = [];
        var i;
        for (i = 0; i < jdata.index.length; ++i) {
            var d = jdata.data[i];
            //console.log(d)
            var row = {
                time: jdata.index[i],
                open: d[0],
                high: d[1],
                low: d[2],
                close: d[3],
            };
            /* var vrow = {
            time: jdata.index[i],
            value: jdata.v[i],
            color: 'rgba(108, 122, 137, 0.9)'
            }; */
            data.push(row);
            //vdata.push(vrow);
            barSeries.update(row);

        }
        /* console.log (data); */
        //};

        //getNextData();

        barSeries.setData(data);


        /* var keys = ['foo', 'bar', 'baz'];
        var values = [11, 22, 33]

        var result = {};
        keys.forEach((key, i) => result[key] = values[i]);
        console.log(result); */



        // calculate SMA and set data 
        /* var smaData = calculateSMA(data, 21);
        var smaLine = chart.addLineSeries({
        color: 'rgba(4, 111, 232, 1)',
        lineWidth: 2,
        });
        smaLine.setData(smaData); */
        ///////////////////////////////////

        /* 
        // indicator legends Eg. SMA 
        var toolTipMargin = 10;
        var priceScaleWidth = 50;
        var legend = document.createElement('div');
        legend.className = 'sma-legend';
        container.appendChild(legend);
        legend.style.display = 'block';
        legend.style.left = 3 + 'px';
        legend.style.top = 3 + 'px';
        function setLegendText(priceValue) {
        let val = 'n/a';
        if (priceValue !== undefined) {
            val = (Math.round(priceValue * 100) / 100).toFixed(2);
        }
        legend.innerHTML = 'MA10 <span style="color:rgba(4, 111, 232, 1)">' + val + '</span>';
        }
        setLegendText(smaData[smaData.length - 1].value);
        chart.subscribeCrosshairMove((param) => {
        setLegendText(param.seriesPrices.get(smaLine));
        });
        */


        ///// 			CREATE PRICELINE , SUPPORT RESISTANCE LEVELS, TARGETS etc. 
        /* 
        barSeries.createPriceLine({
        price: 201,
        color: 'rgba(229, 37, 69, 1)',
        lineWidth: 2,
        lineStyle: LightweightCharts.LineStyle.Dotted,
        title: 'sell order',
        draggable: true,
        });

        barSeries.createPriceLine({
        price: 190,
        color: 'rgba(53, 162, 74, 1)',
        lineWidth: 2,
        priceAxisLabelVisible: false,
        axisLabelVisible : true,
        alertString: 'Entry',
        lineStyle: LightweightCharts.LineStyle.Dotted,
        title: 'buy order draggable',
        draggable: true,
        }); */

        ///// 			DRAWING A BOX 

        // Define a line series (for drawing box)
        /* 	var series2 = chart.addLineSeries({
            color: 'rgb(45, 120, 255)',
            lineWidth: 0.7,
                priceLineVisible: false, // disable priceline 
                lastValueVisible: false, // disable last value visible on price axis 
            
            });
            
            // draw a box with line series 
            var data2 = [
                    
                    {time: { year: 2019 ,month: 4 ,day: 15 }, value: 190}, 
                    {time: { year: 2019,month: 4 ,day: 15 }, value: 211},       
                    {time: { year: 2019 ,month: 4 ,day: 30 }, value: 211}, 
                    {time: { year: 2019 ,month: 4 ,day: 30 }, value: 190}, 
                    {time: { year: 2019 ,month: 4 ,day: 15 }, value: 190},
                    ]; 
            series2.setData(data2);
            
            
            ////		DRAWING A TREND LINE 
            trendlineSeries = chart.addLineSeries({
                priceLineVisible: false, // disable priceline 
                lastValueVisible: false, // disable last value visible on price axis 
            });
            
            var tldata = [
            { time: '2018-12-26', value: 159.28 },
            { time: '2019-03-15', value: 180.82 }
            ]
            trendlineSeries.setData(tldata); */
        ////////////////////////////////////////////



        lineSeries.setData(data.map(x => {
            return {
                time: x.time,
                value: Math.random() * (Math.random() - Math.random()) * 5
            }
        }));
        lineSeries2.setData(data.map(x => {
            return {
                time: x.time,
                value: Math.random() - Math.random()
            }
        }));

        let isCrossHairMoving = false;
        chart.subscribeCrosshairMove(param => {
            if (!param.point) return;
            if (!param.time) return;
            if (isCrossHairMoving) return;

            isCrossHairMoving = true;
            axis.moveCrosshair(param.point);
            axis2.moveCrosshair(param.point);

            isCrossHairMoving = false;
        });

        axis.subscribeCrosshairMove(param => {
            // /// Legend Update Start 
            // if (param.time) {
            //     /* console.log(param) */
            //     /* console.log(param.seriesPrices.get(barSeries)) 
            //     */
            //     const price = param.seriesPrices.get(barSeries);
            //     /* console.log (price) // debug */

            //     if (price !== undefined)
            //         firstRow.innerText = 'ETC USD 7D VWAP' + '  ' + price.toFixed(2);
            // }
            // else {
            //     firstRow.innerText = 'ETC USD 7D VWAP';
            // }
            // /* console.log(param.seriesPrices.get(lineSeries)) */
            // /// Legend Update End

            if (isCrossHairMoving) return;

            isCrossHairMoving = true;
            chart.moveCrosshair(param.point);
            axis2.moveCrosshair(param.point);

            isCrossHairMoving = false;
        });

        axis2.subscribeCrosshairMove(param => {
            if (!param.point) return;
            if (!param.time) return;
            if (isCrossHairMoving) return;

            isCrossHairMoving = true;
            chart.moveCrosshair(param.point);
            axis.moveCrosshair(param.point);
            axis2.moveCrosshair(param.point);

            isCrossHairMoving = false;
        });

        var isChartActive = false;
        var isAxisActive = false;
        chartElement.addEventListener("mousemove", () => {
            if (isChartActive) return;
            isChartActive = true;
            isAxisActive = false;
            chart.applyOptions({
                crosshair: {
                    horzLine: {
                        visible: true,
                        labelVisible: true
                    }
                }
            });
            axis.applyOptions({
                crosshair: {
                    horzLine: {
                        visible: false,
                        labelVisible: false
                    }
                }
            });
            axis2.applyOptions({
                crosshair: {
                    horzLine: {
                        visible: false,
                        labelVisible: false
                    }
                }
            });
        });

        axisElement.addEventListener("mousemove", () => {
            if (isAxisActive) return;
            isAxisActive = true;
            isChartActive = false;
            axis.applyOptions({
                crosshair: {
                    horzLine: {
                        visible: true,
                        labelVisible: true
                    }
                }
            });
            axis2.applyOptions({
                crosshair: {
                    horzLine: {
                        visible: true,
                        labelVisible: true
                    }
                }
            });
            chart.applyOptions({
                crosshair: {
                    horzLine: {
                        visible: true,
                        labelVisible: true
                    }
                }
            });
        });


        /// this is a scaling function: zoom IN and OUT 
        chart.timeScale().subscribeVisibleLogicalRangeChange(range => {
            axis.timeScale().setVisibleLogicalRange(range);
            axis2.timeScale().setVisibleLogicalRange(range);
        })
        axis.timeScale().subscribeVisibleLogicalRangeChange(range => {
            chart.timeScale().setVisibleLogicalRange(range);
            axis2.timeScale().setVisibleLogicalRange(range);
        })
        axis2.timeScale().subscribeVisibleLogicalRangeChange(range => {
            chart.timeScale().setVisibleLogicalRange(range);
            axis.timeScale().setVisibleLogicalRange(range);
        })

        // apply some offset on the right 
        chart.timeScale().applyOptions({
            rightOffset: 10,
            fixLeftEdge: true,
            /* visible: false, */
            /* borderVisible: false */
        })
        axis.timeScale().applyOptions({
            rightOffset: 10,
            fixLeftEdge: true,
            visible: false,
        })

        /* axis2.timeScale().applyOptions({
        rightOffset: 10, 
        fixLeftEdge: true,
        visible: false,
        }) */

        /// ############			 		marker example 			###################
        /// markers can be be used to simulate 
        /// marker positions: (aboveBar | belowBar | inBar) or numeric value line 0 
        /// shape (circle | square | arrowUp | arrowDown) - item marker type
        /// can be used to mark squeeze indicator 

        var datesForMarkers = [data[data.length - 19], data[data.length - 39]];
        var indexOfMinPrice = 0;
        for (var i = 1; i < datesForMarkers.length; i++) {
            if (datesForMarkers[i].high < datesForMarkers[indexOfMinPrice].high) {
                indexOfMinPrice = i;
            }
        }
        var markers = [];
        for (var i = 0; i < datesForMarkers.length; i++) {
            if (i !== indexOfMinPrice) {
                markers.push({ time: datesForMarkers[i].time, position: 'aboveBar', color: '#e91e63', shape: 'arrowDown', text: 'Sell @ ' + Math.floor(datesForMarkers[i].high + 2) });
            } else {
                markers.push({ time: datesForMarkers[i].time, position: 'belowBar', color: '#2196F3', shape: 'arrowUp', text: 'Buy @ ' + Math.floor(datesForMarkers[i].low - 2) });
            }
        }
        markers.push({ time: data[data.length - 48].time, position: 0, color: '#f68410', shape: 'circle', text: 'D' });

        /* console.log(markers) */
        barSeries.setMarkers(markers);
        lineSeries.setMarkers(markers);
        lineSeries2.setMarkers(markers);

        /* chart.timeScale().fitContent(); */

        /// ######################		END MARKERS 		#########################


        /// can eliminate this function 
        function calculateSMA(data, count) {
            var avg = function (data) {
                var sum = 0;
                for (var i = 0; i < data.length; i++) {
                    sum += data[i].close;
                }
                return sum / data.length;
            };
            var result = [];
            for (var i = count - 1, len = data.length; i < len; i++) {
                var val = avg(data.slice(i - count + 1, i));
                result.push({ time: data[i].time, value: val });
            }
            return result;
        }

    });
}