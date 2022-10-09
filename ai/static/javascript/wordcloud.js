$.getJSON("/tophashtags", function (data) {
    reading(data)
});

function reading(data) {
    Highcharts.chart('container', {
        accessibility: {
            screenReaderSection: {
                beforeChartFormat: '<h5>{chartTitle}</h5>' +
                    '<div>{chartSubtitle}</div>' +
                    '<div>{chartLongdesc}</div>' +
                    '<div>{viewTableButton}</div>'
            }
        },
        series: [{
            type: 'wordcloud',
            data,
            name: 'Occurrences'
        }],
        title: {
            text: 'Top 100 used hashtags:'
        },
        subtitle: {
            text: '  '
        },
        tooltip: {
            headerFormat: '<span style="font-size: 16px"><b>{point.key}</b></span><br>'
        }
    });
}