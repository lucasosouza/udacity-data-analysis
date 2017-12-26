var app = angular.module('chartApp', []);

app.controller('mainCtrl', function($scope, drawChart, drawMainChart, dataFactory, chartOptions){

	//draw svg
	var h = 550;
	var w = 1100;
	var svg = d3.select("#auxViz").attr({width: w, height: h})
	var svgMain = d3.select("#mainViz").attr({width: w, height: h})

	$scope.selectedCountry = 'Germany'
	$scope.selectedAge = 'All (above 15)'
	$scope.selectedGender = 'All'
	var opts = [$scope.selectedCountry, $scope.selectedAge, $scope.selectedGender]

	//extend scope
	angular.extend($scope, chartOptions);

	//get dataset
	var data;
	dataFactory.then(function(results){
		data = results;	
		drawChart(svg, filter(data, opts), w,h);
		drawMainChart(svgMain, data, w, h);
	});

	//watch variables for scope change
	$scope.$watch('[selectedCountry, selectedAge, selectedGender]', function(opts){
		svg.selectAll("*").remove(); //remove current chart
		drawChart(svg,filter(data, opts), w,h); //draw new chart
	});

	//filter function
	function filter(data, opts){
		return data.filter(function(elem, idx){
			return elem['Country'] == opts[0] && elem['Age'] == opts[1] && elem['Gender'] == opts[2]
		});
	}

});

app.service('drawChart', function(){

    return function (svg, data, w, h){
        var chart = new dimple.chart(svg, data);
        chart.setBounds(50, 50, w-100, h-100);
        var x = chart.addTimeAxis("x", "Year", "%Y", "%Y");        
        var y1 = chart.addMeasureAxis("y", "Unemployment Rate");        
        var y2 = chart.addMeasureAxis("y", "Per Capita GDP")
        y1.tickFormat = ".2p";
        y2.title = "GDP/capita (US$, inflation-adjusted)"
        chart.addSeries("GDP/Capita", dimple.plot.line, [x, y2]);
        chart.addSeries("GDP/Capita", dimple.plot.bubble, [x, y2]);
        chart.addSeries("Unemployment", dimple.plot.line, [x, y1]);
        chart.addSeries("Unemployment", dimple.plot.bubble, [x, y1]);
        chart.addLegend(w-200, 10, 200, 40, "right");
        chart.draw();
    }

});

app.service('drawMainChart', function(){

    return function (svg, data, w, h){
        var chart = new dimple.chart(svg, data);
        chart.setBounds(50, 50, w-100, h-100);
        var x = chart.addTimeAxis("x", "Year", "%Y", "%Y");        
        var y1 = chart.addMeasureAxis("y", "Unemployment Rate");
        var y2 = chart.addMeasureAxis("y", "Per Capita GDP")
        y1.tickFormat = ".2p";
        y2.title = "GDP/capita (US$, inflation-adjusted)"
        var gdp1 = chart.addSeries("GDP/Capita", dimple.plot.line, [x, y2]);
        var gdp2 = chart.addSeries("GDP/Capita", dimple.plot.bubble, [x, y2]);
        gdp1.aggregate = dimple.aggregateMethod.avg;
        gdp2.aggregate = dimple.aggregateMethod.avg;
        var unemp1 = chart.addSeries("Unemployment", dimple.plot.line, [x, y1]);
        var unemp2 = chart.addSeries("Unemployment", dimple.plot.bubble, [x, y1]);
        unemp1.aggregate = dimple.aggregateMethod.avg;
        unemp2.aggregate = dimple.aggregateMethod.avg;
        chart.addLegend(w-200, 10, 200, 40, "right");
        chart.draw();
    }

});



//http://dimplejs.org/advanced_examples_viewer.html?id=advanced_price_range_lollipop

app.factory('dataFactory', function($q){

	var dataset;
	var deferred = $q.defer()
	d3.csv('consolidated_unemployment_gdp.csv', function(data){
	    data.forEach(function (d){
	        //force string to integer
	        d['Unemployment Rate'] = (+d['Unemployment Rate'].replace(',', '.')/100.0);
	        d['Per Capita GDP'] = (+d['Per Capita GDP'].replace(',', '.'));
	        //change gender
	        var gender = d['Gender']
	        if (gender == 'm') {
	            d['Gender'] = 'Men'
	        } else if (gender == 'f') {
	            d['Gender'] = 'Women'
	        } else {
	            d['Gender'] = 'All'
	        }
	    })
	    data = data.filter(function(elem, idx){
	        return elem['Unemployment Rate'] > 0;
	    })
	    deferred.resolve(data)
	})
	return deferred.promise

});

app.factory('chartOptions', function(){

	var opts={}
	opts.countries = ['Australia','Canada','Czech Rep.','Estonia','Finland','France','Germany','Hong Kong, China','Ireland','Japan','Korea, Rep.','Latvia','Lithuania','Netherlands','New Zealand','Norway','Philippines','Poland','Portugal','Romania','Singapore','Slovak Republic','Slovenia','Spain','Sweden','Switzerland','Turkey','United Kingdom','United States']
	opts.genders = ['All', 'Men', 'Women']
	opts.ages = ['15-24','25-54', 'above 55', 'All (above 15)']
	return opts

});
