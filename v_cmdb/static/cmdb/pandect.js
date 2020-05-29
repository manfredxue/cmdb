
function bingtu (data) {
        var chart = new Highcharts.Chart({
            chart: {
                renderTo: "idc_device",        //在哪个区域呈现，对应HTML中的一个元素ID
                plotBackgroundColor: null,    //绘图区的背景颜色
                plotBorderWidth: null,        //绘图区边框宽度
                plotShadow: false            //绘图区是否显示阴影
            },

            title: {
                text: "机房"
            },
            tooltip: {
                formatter: function() {
                    return '<b>'+ this.point.name +'</b>: '+ Highcharts.numberFormat(this.percentage, 1) +'% ('+Highcharts.numberFormat(this.y, 0, ',') +' 个)';
                }
                },
            plotOptions: {
                pie: {
                    allowPointSelect: true,
                    cursor: "pointer",
                    dataLabels: {
                        enabled: true,
                        color: "#000000",
                        connectorColor: "#000000",
                        formatter: function() {
                            return "<b>"+ this.point.name +"</b>: "+Highcharts.numberFormat(this.percentage,2) +" %";
                                    }
                                }
                            }
                        },
            series: [{
                type: "pie",
                name: "份额",
                data: data,
            }]
        });
    }