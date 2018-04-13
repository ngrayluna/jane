"use strict";

/**
 * @doc function
 * @name angular-openlayers3-directive.main:__getMapDefaults
 *
 * @description Function returning the default configuration parameters.
 */
function __getMapDefaults() {
    return {
        center: {
            latitude: 0,
            longitude: 0,
            zoom: 1
        }
    };
}


// XXX: Find a proper way to deal with different projections!
// From WGS84 to Spherical Mercator.
function __toMapCoods(coods) {
    return ol.proj.transform(coods, "EPSG:4326", "EPSG:3857");
}


// XXX: Find a proper way to deal with different projections!
// From Spherical Mercator to WGS84.
function __fromMapCoods(coods) {
    return ol.proj.transform(coods, "EPSG:3857", "EPSG:4326");
}


var width = 100,
    perfData = window.performance.timing, // The PerformanceTiming interface represents timing-related performance information for the given page.
    EstimatedTime = -(perfData.loadEventEnd - perfData.navigationStart),
    time = parseInt((EstimatedTime/1000)%60)*100;

// Loadbar Animation
$(".loadbar").animate({
  width: width + "%"
}, time);

// Percentage Increment Animation
var PercentageID = $("#precent"),
		start = 0,
		end = 100,
		durataion = time;
		animateValue(PercentageID, start, end, durataion);
		
function animateValue(id, start, end, duration) {
  
	var range = end - start,
      current = start,
      increment = end > start? 1 : -1,
      stepTime = Math.abs(Math.floor(duration / range)),
      obj = $(id);
    
	var timer = setInterval(function() {
		current += increment;
		$(obj).text(current + "%");
      //obj.innerHTML = current;
		if (current == end) {
			clearInterval(timer);
		}
	}, stepTime);
}

// Fading Out Loadbar on Finised
setTimeout(function(){
  $('.preloader-wrap').fadeOut(300);
}, time);
