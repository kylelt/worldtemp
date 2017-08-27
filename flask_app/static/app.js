//
// Configuration
//

// ms to wait after dragging before auto-rotating
var rotationDelay = 3000
// scale of the globe (not the canvas element)
var scaleFactor = 0.9
// autorotation speed
var degPerSec = 6
// start angles
var angles = { x: -20, y: 40, z: 0}
// colors
var colorWater = '#0081C6'
var colorLand = '#D3D3D3'
var colorGraticule = '#0081C6'
var colorCountry = '#ff39e7' //Yellow



function enter(country) {
  var country = countryList.find(function(c) {
    if (c != undefined && c.feature != undefined) {
      return c.feature.id === country.id
    }
  })

  // var countryId = countryList.find(function(c){
  //   return c.name === "Australia"
  // })
  // //console.log(countryId.id)
  // var feature = countries.features.find(function(f){return parseInt(f.id) === parseInt(countryId.id)})
  // console.log(feature)
  // fill(feature, colorCountry)

  
  // console.log(country)
  if (country != undefined) {
    current.text(country && country.name || '')
    sentiment_h.text(country.sentiment) 
    tweets_h.text(country.tweetCount + " tweets" );
  } else {
    leave(currentCountry);
  }
  
}

function leave(country) {
  current.text('')
  sentiment_h.text('')
  tweets_h.text('')
}



function color_single_country(countryName, color){

  countryList.forEach(function(countryObj) {
    if (countryObj.name === countryName) {
      countryObj.color = colorCountry;
     // break
    }
  });

}


var percentColors = [
    { pct: 0.0, color: { r: 0xff, g: 0x00, b: 0 } },
    { pct: 0.5, color: { r: 0xff, g: 0xff, b: 0 } },
    { pct: 1.0, color: { r: 0x00, g: 0xff, b: 0 } } ];

var getColorForPercentage = function(pct) {
    for (var i = 1; i < percentColors.length - 1; i++) {
        if (pct < percentColors[i].pct) {
            break;
        }
    }
    var lower = percentColors[i - 1];
    var upper = percentColors[i];
    var range = upper.pct - lower.pct;
    var rangePct = (pct - lower.pct) / range;
    var pctLower = 1 - rangePct;
    var pctUpper = rangePct;
    var color = {
        r: Math.floor(lower.color.r * pctLower + upper.color.r * pctUpper),
        g: Math.floor(lower.color.g * pctLower + upper.color.g * pctUpper),
        b: Math.floor(lower.color.b * pctLower + upper.color.b * pctUpper)
    };
    return 'rgb(' + [color.r, color.g, color.b].join(',') + ')';
}  



function processSensitivity(sensitivity){
  //Sensitivity will be between -1 and 1
  //Convert sensitivity to scale between 0 and 1
  sensitivity = ((sensitivity + 1)/2)

  // console.log(sensitivity);
  // var HSV = [toInteger(sensitivity * 360), 100, 100]
  // return Color().fromHsv(HSV)
  return getColorForPercentage(sensitivity) 
  // return hsvToRgb(sensitivity, 0.8, 1);
}

/* Test Input

var twitter_out1 = [{
    "country": "Spain",
    "averageSentiment": 1.0
  },
  {
    "country": "Australia",
    "averageSentiment": -1.0
  },
  {
    "country": "New Zealand",
    "averageSentiment": 0.0
  },
  { "country" : "United States",
    "averageSentiment" : 1
  },
  { "country" : "Honduras",
    "averageSentiment" : -0.56
  },
  { "country" : "Congo",
    "averageSentiment" : 0.36
  },
  { "country" : "Sri Lanka",
    "averageSentiment" : 0
  },
  { "country" : "United Kingdom",
    "averageSentiment" : 0.26
  },
  { "country" : "Iran",
    "averageSentiment" : -0.22
  },
  { "country" : "Brazil",
    "averageSentiment" : 0.36
  }
]
*/

function color_all_countries(twitter_out){
  //Process twitter feed
  twitter_out.forEach(function(twit_obj){
     // console.log(twit_obj)
    //Find country in countryList
    countryList.forEach(function(countryObj){
      if (countryObj.name === twit_obj.country) {
        // console.log(countryObj)
        var country_rgb = processSensitivity(twit_obj.averageSentiment);
        // countryObj.color =  processSensitivity(twit_obj.averageSentiment);
        // countryObj.color = "rgb(" + country_rgb[0].toString() + "," + country_rgb[1].toString() + "," + country_rgb[2].toString() + ")";
        countryObj.sentiment = (twit_obj.averageSentiment).toFixed(4);
        countryObj.tweetCount = twit_obj.count;
        countryObj.color = processSensitivity(twit_obj.averageSentiment);
      }
    });

  })
}

setInterval(function() {

  $.ajax({
    url: '/countries',
    type: 'GET'
  }).done(function(data){

  color_all_countries(JSON.parse(data))

  });
    
}, 60 * 100); // 60 * 1000 milsec


//
// Variables
//

var current = d3.select('#current')
var sentiment_h = d3.select('#sentiment_h')
var tweets_h = d3.select('#tweets_h')
var canvas = d3.select('#globe')
var context = canvas.node().getContext('2d')
var water = {type: 'Sphere'}
var projection = d3.geoOrthographic().precision(0.1)
var graticule = d3.geoGraticule10()
var path = d3.geoPath(projection).context(context)
var v0 // Mouse position in Cartesian coordinates at start of drag gesture.
var r0 // Projection rotation as Euler angles at start.
var q0 // Projection rotation as versor at start.
var lastTime = d3.now()
var degPerMs = degPerSec / 1000
var width, height
var land, countries
var countryList = []
var autorotate, now, diff, roation
var currentCountry

//
// Functions
//

function setAngles() {
  var rotation = projection.rotate()
  rotation[0] = angles.y
  rotation[1] = angles.x
  rotation[2] = angles.z
  projection.rotate(rotation)
}

function scale() {
  width = document.documentElement.clientWidth
  height = document.documentElement.clientHeight
  canvas.attr('width', width).attr('height', height)
  projection
    .scale((scaleFactor * Math.min(width, height)) / 2)
    .translate([width / 2, height / 2])
  render()
}

function startRotation(delay) {
  autorotate.restart(rotate, delay || 0)
}

function stopRotation() {
  autorotate.stop()
}

function dragstarted() {
  v0 = versor.cartesian(projection.invert(d3.mouse(this)))
  r0 = projection.rotate()
  q0 = versor(r0)
  stopRotation()
}

function dragged() {
  var v1 = versor.cartesian(projection.rotate(r0).invert(d3.mouse(this)))
  var q1 = versor.multiply(q0, versor.delta(v0, v1))
  var r1 = versor.rotation(q1)
  projection.rotate(r1)
  render()
}

function dragended() {
  startRotation(rotationDelay)
}

function render() {
  context.clearRect(0, 0, width, height)
  fill(water, colorWater)
  stroke(graticule, colorGraticule)
  fill(land, colorLand)

  countryList.forEach(function(countryObj) {
    if (countryObj.color === '#000000') {
      
    } else {
      fill(countryObj.feature, countryObj.color)
    }
  });


  if (currentCountry) {
    fill(currentCountry, colorCountry)
  }
}


function fill(obj, color) {
  context.beginPath()
  path(obj)
  context.fillStyle = color
  context.fill()
}/* Test Input

var twitter_out1 = [{
    "country": "Spain",
    "averageSentiment": 1.0
  },
  {
    "country": "Australia",
    "averageSentiment": -1.0
  },
  {
    "country": "New Zealand",
    "averageSentiment": 0.0
  },
  { "country" : "United States",
    "averageSentiment" : 1
  },
  { "country" : "Honduras",
    "averageSentiment" : -0.56
  },
  { "country" : "Congo",
    "averageSentiment" : 0.36
  },
  { "country" : "Sri Lanka",
    "averageSentiment" : 0
  },
  { "country" : "United Kingdom",
    "averageSentiment" : 0.26
  },
  { "country" : "Iran",
    "averageSentiment" : -0.22
  },
  { "country" : "Brazil",
    "averageSentiment" : 0.36
  }
]
*/

function color_all_countries(twitter_out){
  //Process twitter feed
  twitter_out.forEach(function(twit_obj){
     // console.log(twit_obj)
    //Find country in countryList
    countryList.forEach(function(countryObj){
      if (countryObj.name === twit_obj.country) {
        // console.log(countryObj)
        var country_rgb = processSensitivity(twit_obj.averageSentiment);
        // countryObj.color =  processSensitivity(twit_obj.averageSentiment);
        // countryObj.color = "rgb(" + country_rgb[0].toString() + "," + country_rgb[1].toString() + "," + country_rgb[2].toString() + ")";
        countryObj.sentiment = (twit_obj.averageSentiment).toFixed(4);
        countryObj.tweetCount = twit_obj.count;
        countryObj.color = processSensitivity(twit_obj.averageSentiment);
      }
    });

  })
}

setInterval(function() {

  $.ajax({
    url: '/countries',
    type: 'GET'
  }).done(function(data){

  color_all_countries(JSON.parse(data))

  });
    
}, 60 * 100); // 60 * 1000 milsec


//
// Variables
//

var current = d3.select('#current')
var sentiment_h = d3.select('#sentiment_h')
var tweets_h = d3.select('#tweets_h')
var canvas = d3.select('#globe')
var context = canvas.node().getContext('2d')
var water = {type: 'Sphere'}
var projection = d3.geoOrthographic().precision(0.1)
var graticule = d3.geoGraticule10()
var path = d3.geoPath(projection).context(context)
var v0 // Mouse position in Cartesian coordinates at start of drag gesture.
var r0 // Projection rotation as Euler angles at start.
var q0 // Projection rotation as versor at start.
var lastTime = d3.now()
var degPerMs = degPerSec / 1000
var width, height
var land, countries
var countryList = []
var autorotate, now, diff, roation
var currentCountry

//
// Functions
//

function setAngles() {
  var rotation = projection.rotate()
  rotation[0] = angles.y
  rotation[1] = angles.x
  rotation[2] = angles.z
  projection.rotate(rotation)
}

function scale() {
  width = document.documentElement.clientWidth
  height = document.documentElement.clientHeight
  canvas.attr('width', width).attr('height', height)
  projection
    .scale((scaleFactor * Math.min(width, height)) / 2)
    .translate([width / 2, height / 2])
  render()
}

function startRotation(delay) {
  autorotate.restart(rotate, delay || 0)
}

function stopRotation() {
  autorotate.stop()
}

function dragstarted() {
  v0 = versor.cartesian(projection.invert(d3.mouse(this)))
  r0 = projection.rotate()
  q0 = versor(r0)
  stopRotation()
}

function dragged() {
  var v1 = versor.cartesian(projection.rotate(r0).invert(d3.mouse(this)))
  var q1 = versor.multiply(q0, versor.delta(v0, v1))
  var r1 = versor.rotation(q1)
  projection.rotate(r1)
  render()
}

function dragended() {
  startRotation(rotationDelay)
}

function render() {
  context.clearRect(0, 0, width, height)
  fill(water, colorWater)
  stroke(graticule, colorGraticule)
  fill(land, colorLand)

  countryList.forEach(function(countryObj) {
    if (countryObj.color === '#000000') {
      
    }else{
      fill(countryObj.feature, countryObj.color)
    }
  });


  if (currentCountry) {
    fill(currentCountry, colorCountry)
  }
}


function fill(obj, color) {
  context.beginPath()
  path(obj)
  context.fillStyle = color
  context.fill()
}

function stroke(obj, color) {
  context.beginPath()
  path(obj)
  context.strokeStyle = color
  context.stroke()
}

function rotate(elapsed) {
  now = d3.now()
  diff = now - lastTime
  if (diff < elapsed) {
    rotation = projection.rotate()
    rotation[0] += diff * degPerMs
    projection.rotate(rotation)
    render()
  }
  lastTime = now
}

function loadData(cb) {
  d3.json('https://unpkg.com/world-atlas@1/world/110m.json', function(error, world) {
    if (error) throw error
    d3.tsv('https://gist.githubusercontent.com/mbostock/4090846/raw/07e73f3c2d21558489604a0bc434b3a5cf41a867/world-country-names.tsv', function(error, countries) {
      if (error) throw error
      cb(world, countries)
    })
  })
}

// https://github.com/d3/d3-polygon
function polygonContains(polygon, point) {
  var n = polygon.length
  var p = polygon[n - 1]
  var x = point[0], y = point[1]
  var x0 = p[0], y0 = p[1]
  var x1, y1
  var inside = false
  for (var i = 0; i < n; ++i) {
    p = polygon[i], x1 = p[0], y1 = p[1]
    if (((y1 > y) !== (y0 > y)) && (x < (x0 - x1) * (y - y1) / (y0 - y1) + x1)) inside = !inside
    x0 = x1, y0 = y1
  }
  return inside
}

function mousemove() {
  //hange_country_color();

  var c = getCountry(this)
  // console.log(this)
  // console.log(c)
  if (!c) {
    if (currentCountry) {
      leave(currentCountry)
      currentCountry = undefined
      render()
    }
    return
  }
  if (c === currentCountry) {
    return
  }
 // console.log(currentCountry)
  currentCountry = c

  enter(c)
  render()
  
}






function getCountry(event) {
  var pos = projection.invert(d3.mouse(event))
  return countries.features.find(function(f) {
    return f.geometry.coordinates.find(function(c1) {
      return polygonContains(c1, pos) || c1.find(function(c2) {
        return polygonContains(c2, pos)
      })
    })
  })
}




//
// Initialization
//

setAngles()

canvas
  .call(d3.drag()
    .on('start', dragstarted)
    .on('drag', dragged)
    .on('end', dragended)
   )
 .on('mousemove', mousemove)

loadData(function(world, cList) {
  land = topojson.feature(world, world.objects.land)
  countries = topojson.feature(world, world.objects.countries)

  // Populate country list
  cList.forEach(function(obj) { 
    // console.log(obj.id)
    countryList.push({name: obj.name,
                      id: obj.id, 
                      color: '#000000',
                      feature: countries.features.find(function(f){return parseInt(f.id) === parseInt(obj.id)}),
                      tweetCount: 0,
                      sentiment: 'N/A'
                    });
  });

  // color_all_countries(twitter_out1)
  window.addEventListener('resize', scale)
  scale()
  autorotate = d3.timer(rotate)
})