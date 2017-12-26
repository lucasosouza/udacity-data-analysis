var app = angular.module('chartApp', []);

app.controller('mainCtrl', function($scope, drawChart, drawMainChart, dataFactory, chartOptions){

	//draw svg
	var h = 550;
	var w = 1100;
	var svg = d3.select("#auxViz").attr({width: w, height: h})
	var svgMain = d3.select("#mainViz").attr({width: w, height: h})

	//default variables for the input fields
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
		drawChart(svg, filterByParams(data, opts), w,h);
		drawMainChart(svgMain, filterAggregated(data), w, h);
	});

	//watch input variables for scope change
	$scope.$watch('[selectedCountry, selectedAge, selectedGender]', function(opts){
		svg.selectAll("*").remove(); //remove current chart
		drawChart(svg,filterByParams(data, opts), w,h); //draw new chart
	});

	//function that filters data according to the selected parameters
	function filterByParams(data, opts){
		return data.filter(function(elem, idx){
			return elem['Country'] == opts[0] && elem['Age'] == opts[1] && elem['Gender'] == opts[2]
		});
	}

	//function that filters only data aggregated by age and gender to show in the main viz
	function filterAggregated(data){
		return data.filter(function(elem, idx){
			return elem['Age'] == 'All (above 15)' && elem['Gender'] == 'All'
		});
	}
	

});

app.service('drawChart', function(){

	//draws exploratory chart
    return function (svg, data, w, h){
    	//create chart and set its boundaries
        var chart = new dimple.chart(svg, data);
        chart.setBounds(50, 50, w-100, h-100);
        //add axises
        var x = chart.addTimeAxis("x", "Year", "%Y", "%Y");        
        var y1 = chart.addMeasureAxis("y", "Unemployment Rate");        
        var y2 = chart.addMeasureAxis("y", "Per Capita GDP")
        //format y1 to percent and change y2 title
        y1.tickFormat = ".2p";
        y2.title = "GDP/capita (US$, inflation-adjusted)"
        //add series - line and bubble for each
        chart.addSeries("GDP/Capita", dimple.plot.line, [x, y2]);
        chart.addSeries("GDP/Capita", dimple.plot.bubble, [x, y2]);
        chart.addSeries("Unemployment", dimple.plot.line, [x, y1]);
        chart.addSeries("Unemployment", dimple.plot.bubble, [x, y1]);
        //create legend
        chart.addLegend(w-200, 10, 200, 40, "right");
        //draw chart
        chart.draw();
    }

});

app.service('drawMainChart', function(){

	//draws explanatory chart
    return function (svg, data, w, h){
    	debugger;
    	//create chart and set its boundaries
        var chart = new dimple.chart(svg, data);
        chart.setBounds(50, 50, w-100, h-100);
        //add axises
        var x = chart.addTimeAxis("x", "Year", "%Y", "%Y");        
        var y1 = chart.addMeasureAxis("y", "Unemployment Rate");
        var y2 = chart.addMeasureAxis("y", "Per Capita GDP")
        //format y1 to percent and change y2 title
        y1.tickFormat = ".2p";
        y2.title = "GDP/capita (US$, inflation-adjusted)"
        //create gdp series
        var gdp1 = chart.addSeries("GDP/Capita", dimple.plot.line, [x, y2]);
        var gdp2 = chart.addSeries("GDP/Capita", dimple.plot.bubble, [x, y2]);
        //aggregate by average
        gdp1.aggregate = dimple.aggregateMethod.avg;
        gdp2.aggregate = dimple.aggregateMethod.avg;
        //create unemployment series
        var unemp1 = chart.addSeries("Weighted Rate", dimple.plot.line, [x, y1]);
        var unemp2 = chart.addSeries("Weighted Rate", dimple.plot.bubble, [x, y1]);
        //aggregate by average
        unemp1.aggregate = dimple.aggregateMethod.sum;
        unemp2.aggregate = dimple.aggregateMethod.sum;
        //add legend
        chart.addLegend(w-200, 10, 200, 40, "right");
        //draw chart
        chart.draw();
    }

});


//http://dimplejs.org/advanced_examples_viewer.html?id=advanced_price_range_lollipop

app.factory('dataFactory', function($q){

	//auxiliary function used below to fix population
	function replaceAll(string, search, replacement) {
		while (string.indexOf(search) > 0) {
			string = string.replace(search, replacement)
		}
		return string
	}

	//auxiliary function that calculates the total population at each year 
	function calcTotalPopulation(data) {
		//filters only relevant data for the weighted avarege
		data = data.filter(function(elem, idx){
			return elem['Age'] == 'All (above 15)' && elem['Gender'] == 't';
		});
		//creates population dictionary
		var totalPopulation = {};
		for (d in data) {
			var year = d['Year'];
			var population = +replaceAll(d['Population'],',', '');
			if (!year in totalPopulation) {
				totalPopulation[year] = population;
			} else {
				totalPopulation[year] = totalPopulation[year] + population;
			}
		}
		return totalPopulation;
	}

	//loads data
	var dataset;
	//creates promise
	var deferred = $q.defer()

	//loads through each datum and modify variables
	d3.csv('consolidated_unemployment_gdp.csv', function(data){
		var totalPopulation = calcTotalPopulation(data);
	    data.forEach(function (d){
	        //force string to integer
	        d['Unemployment Rate'] = (+d['Unemployment Rate'].replace(',', '.')/100.0);
	        d['Per Capita GDP'] = (+d['Per Capita GDP'].replace(',', '.'));
	        d['Population'] = +replaceAll(d['Population'],',', '');
	        //change gender
	        var gender = d['Gender']
	        if (gender == 'm') {
	            d['Gender'] = 'Men'
	        } else if (gender == 'f') {
	            d['Gender'] = 'Women'
	        } else {
	            d['Gender'] = 'All'
	        }
		    //add a weighted average
		    d['Population * Unemployment Rate'] = d['Population'] * d['Unemployment Rate']
			d['Weighted Rate'] = d['Population * Unemployment Rate'] / totalPopulation[d['Year']];

	    })
	    //only include rows which has data on unemployment
	    data = data.filter(function(elem, idx){
	        return elem['Unemployment Rate'] > 0;
	    })
	    //resolves promise
	    deferred.resolve(data)
	})
	return deferred.promise

});

app.factory('chartOptions', function(){

	//options to show in the input field
	var opts={}
	opts.countries = ['Australia','Canada', 'Estonia','Finland','France','Germany','Hong Kong, China','Ireland','Japan', 'Latvia','Lithuania','Netherlands','New Zealand','Norway','Philippines','Poland','Portugal','Romania','Singapore','Slovak Republic','Slovenia','Spain','Sweden','Switzerland','Turkey','United Kingdom','United States']
	opts.genders = ['All', 'Men', 'Women']
	opts.ages = ['15-24','25-54', 'above 55', 'All (above 15)']
	return opts

});
