  // Initialize a Line chart in the container with the ID chart1

  // new Chartist.Bar('#chart1', {
  //   labels: ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'],
  //   series: [
  //     [5, 4, 3, 7, 5, 10, 3],
  //     [3, 2, 9, 5, 4, 6, 4]
  //   ]
  // }, {
  //   seriesBarDistance: 10,
  //   reverseData: true,
  //   horizontalBars: true, /*to make gantt chart !!*/
  //   axisY: {
  //     offset: 70
  //   }
  // });

    var chartA=new Chartist.Bar('#chart1', {
      labels: C1_pnames,
      series: [C1_Adays]
    }, {
    seriesBarDistance: 30,
    horizontalBars: false,
    axisY: {
      offset:100
    },
    axisX: {
      offset:70
    },
    plugins: [
      Chartist.plugins.ctAxisTitle({
        axisX: {
          axisTitle: 'Projects',
          axisClass: 'ct-axis-title',
          offset: {
            x: -60,
            y: 70
          },
          textAnchor: 'middle'
        },
        axisY: {
          axisTitle: 'Days',
          axisClass: 'ct-axis-title',
          offset: {
            x: 0,
            y: 0
          },
          textAnchor: 'top',
          flipTitle: true
        }
      }),
      Chartist.plugins.tooltip()
    ]});
   // new Chartist.Bar('#chart2', {
   //    labels: [1, 2, 3, 4],
   //    series: [[100, 120, 180, 200]]
   //  });

  var chart = new Chartist.Pie('#chart2', {
    series: C2_series,
    labels: ['In Progress','Completed']
  },{
    plugins: [
        Chartist.plugins.tooltip()
    ]}
  );

  var chartee = new Chartist.Pie('#chart5', {
    series: C2_series,
    labels: ['In Progress','Completed']
  }, {
    donut: true,
    showLabel: true
  });

  chart.on('draw', function(data) {
    if(data.type === 'slice') {
      // Get the total path length in order to use for dash array animation
      var pathLength = data.element._node.getTotalLength();

      // Set a dasharray that matches the path length as prerequisite to animate dashoffset
      data.element.attr({
        'stroke-dasharray': pathLength + 'px ' + pathLength + 'px'
      });

      // Create animation definition while also assigning an ID to the animation for later sync usage
      var animationDefinition = {
        'stroke-dashoffset': {
          id: 'anim' + data.index,
          dur: 1000,
          from: -pathLength + 'px',
          to:  '0px',
          easing: Chartist.Svg.Easing.easeOutQuint,
          // We need to use `fill: 'freeze'` otherwise our animation will fall back to initial (not visible)
          fill: 'freeze'
        }
      };

      // If this was not the first slice, we need to time the animation so that it uses the end sync event of the previous animation
      if(data.index !== 0) {
        animationDefinition['stroke-dashoffset'].begin = 'anim' + (data.index - 1) + '.end';
      }

      // We need to set an initial value before the animation starts as we are not in guided mode which would do that for us
      data.element.attr({
        'stroke-dashoffset': -pathLength + 'px'
      });

      // We can't use guided mode as the animations need to rely on setting begin manually
      // See http://gionkunz.github.io/chartist-js/api-documentation.html#chartistsvg-function-animate
      data.element.animate(animationDefinition, false);
    }
  });

  // For the sake of the example we update the chart every time it's created with a delay of 8 seconds
  chart.on('created', function() {
    if(window.__anim21278907124) {
      clearTimeout(window.__anim21278907124);
      window.__anim21278907124 = null;
    }
    window.__anim21278907124 = setTimeout(chart.update.bind(chart), 10000);
  });


   // new Chartist.Bar('#chart3', {
   //     labels: [1, 2, 3, 4],
   //    series: [[5, 2, 8, 3]]
   // });

  var chart = new Chartist.Line('#chart3', {
    labels: ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat'],
    series: [
      [1, 5, 2, 5, 4, 3],
      [2, 3, 4, 8, 1, 2],
      [5, 4, 3, 2, 1, 0.5]
    ]
  }, {
    low: 0,
    showArea: true,
    showPoint: false,
    fullWidth: true
  });

  chart.on('draw', function(data) {
    if(data.type === 'line' || data.type === 'area') {
      data.element.animate({
        d: {
          begin: 2000 * data.index,
          dur: 2000,
          from: data.path.clone().scale(1, 0).translate(0, data.chartRect.height()).stringify(),
          to: data.path.clone().stringify(),
          easing: Chartist.Svg.Easing.easeOutQuint
        }
      });
    }
  });

  // new Chartist.Pie('#chart3', {
      //   series: [20, 10, 30, 40]
      // }, {
      //   donut: true,
      //   donutWidth: 60,
      //   donutSolid: true,
      //   startAngle: 270,
      //   showLabel: true
      // });
      //
      //  var data = {
      //   labels: ['Bananas', 'Apples', 'Grapes'],
      //   series: [20, 15, 40]
      // };
      //
      // var options = {
      //   labelInterpolationFnc: function(value) {
      //     return value[0]
      //   }
      // };
      //
      // var responsiveOptions = [
      //   ['screen and (min-width: 640px)', {
      //     chartPadding: 30,
      //     labelOffset: 100,
      //     labelDirection: 'explode',
      //     labelInterpolationFnc: function(value) {
      //       return value;
      //     }
      //   }],
      //   ['screen and (min-width: 1024px)', {
      //     labelOffset: 80,
      //     chartPadding: 20
      //   }]
      // ];
      //
      // new Chartist.Pie('#chart3', data, options, responsiveOptions);
  //

  // var dataPreferences = {
  //             series: [
  //                 [25, 30, 20, 25]
  //             ]
  //         };
  //
  //         var optionsPreferences = {
  //             donut: true,
  //             donutWidth: 40,
  //             startAngle: 0,
  //             total: 100,
  //             showLabel: false,
  //             axisX: {
  //                 showGrid: false
  //             }
  //         };
  //         Chartist.Pie('#chart3', dataPreferences, optionsPreferences);