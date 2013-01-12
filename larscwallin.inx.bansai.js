var bansai = {
                            ids: {},
                            labels:{},
                            groups:{},
                            stage:null,

                            init:function(stage,svgDoc){
                                backgroundLayer = bansai.createBackgroundLayer();
                                bansai.stage = stage;

                                svgDoc.elements.forEach(function(el) {
                                    if(el.svg === 'g'){
                                        bansai.addGroup(el,backgroundLayer);
                                    }else{
                                        bansai.addPath(el,backgroundLayer);
                                    }
                                });

                                console.log("Dump of indexed SVG label attributes:" + bansai.objToString(bansai.labels));
                                console.log("Dump of indexed SVG id attributes:" + bansai.objToString(bansai.ids));
                            },

                             createBackgroundLayer:function(){
                                return new Group().attr({x:0, y:0}).addTo(stage);
                             },

                            addGroup:function(node,parent){
                                var group = new Group();

                                node.elements.forEach(function(el){
                                    if(el.svg === 'g'){
                                        bansai.addGroup(el,group);
                                    }else if(el.svg === 'path'){
                                        bansai.addPath(el,group);
                                    }
                                });

  
                                if(node.transform!==''){
                                    m = new Matrix();
                                    transform = node.transform;
                                    
                                    m.rotate(transform.rotation.radiance); 
                                    m.scale(transform.scale.x,transform.scale.y);
                                    m.translate(transform.translation.x,transform.translation.y);
                                    group.attr('matrix',m);
                                }
                                if(node.origin){
                                  group.setOrigin(( node.box[0] + node.origin.x ),(node.box[2] + node.origin.y ));                   
                                }
                                

                                bansai.ids[node.id] = group;

                                if (node.label !== '') {

                                    if(!bansai.labels[node.label]){
                                        bansai.labels[node.label] = [];
                                    }

                                    bansai.labels[node.label].push(group);
                                }

                                group.addTo(parent);
                            },

                            addPath:function(node,parent){
                                path = new Path(node.path).attr({
                                    fillColor: node.attr.fillColor,
                                    fillOpacity: node.attr.opacity,
                                    strokeColor: node.attr.strokeColor,
                                    strokeWidth: node.attr.strokeWidth,
                                });

                                if(node.origin){
                                  path.setOrigin(( node.box[0] + node.origin.x ),(node.box[2] + node.origin.y ));                      
                                }else{
                                  //console.log('No origin defined for '+node.id);
                                }

                                if(node.transform!==''){
                                    m = new Matrix();
                                    transform = node.transform;

                                    m.rotate(transform.rotation.radiance); 
                                    m.scale(transform.scale.x,transform.scale.y);
                                    m.translate(transform.translation.x,transform.translation.y);

                                    path.attr('matrix',m);
                                }

                                if(node.attr.filters!==''){
                                    node.attr.filters.forEach(function(el) {
                                        switch(el.svg){
                                            case 'feGaussianBlur':
                                                f = new filter.Blur(el.stdDeviation);
                                                path.attr('filters',f);
                                                break;
                                        }
                                    });
                                }

                                if(node.attr.fillGradient!==''){
                                    //console.log('Got a fill gradient');
                                    gradientType = node.attr.fillGradient.svg;

                                    switch(gradientType){

                                        case 'linearGradient':
                                            //console.log('Type, linear gradient');
                                            gradient = node.attr.fillGradient;
                                            rotation = gradient.transform.rotation.degree;
                                            stops = [];

                                            // Set up stops array
                                            gradient.stops.forEach(function(el){
                                                color =  bansai.hexToRgba(el.stopColor,el.stopOpacity);
                                                color = ('rgb('+color.r+','+color.g+','+color.b+')');
                                                console.log('stop color / offset ' + color + ' / ' + (el.offset * 100));
                                                stops.push(color,(el.offset * 100));
                                            });

                                            bonsaiGradient = bonsai.gradient.linear((rotation+'deg'),stops,false);
                                            //console.log(bonsaiGradient);
                                            path.attr({
                                                fillGradient:bonsaiGradient
                                            });
/*
                                            fillGradient = bonsai.gradient.linear('left', [
                                                ['rgb(255,25,5)',20],
                                                ['green', 60],
                                                ['yellow',20]
                                              ]);
                                            bonsai.Path.rect(400, 0, 100, 250).attr({
                                              'fillGradient' : fillGradient
                                            }).addTo(stage);

                                              'fillGradient':{
                                                 'gradientUnits':'userSpaceOnUse',
                                                 'y2':'115.21932',
                                                 'svg':'linearGradient',
                                                 'stops':[
                                                    {
                                                       'stop-color':'#000000',
                                                       'stop-opacity':'1',
                                                       'id':'stop14',
                                                       'offset':'0'
                                                    },
                                                    {
                                                       'stop-color':'#000000',
                                                       'stop-opacity':'0',
                                                       'id':'stop16',
                                                       'offset':'1'
                                                    }
                                                 ],
                                                 'x2':'400',
                                                 'collect':'always',
                                                 'y1':'489.50504',
                                                 'x1':'397.14285',
                                                 'id':'linearGradient18'
                                              }
                                            */
                                            break;
                                        case 'radialGradient':
                                            console.log('Type, radial gradient');
                                            gradient = node.attr.fillGradient;
                                            rotation = gradient.transform.rotation.degree;
                                            stops = [];

                                            // Set up stops array
                                            gradient.stops.forEach(function(el){
                                                color =  bansai.hexToRgba(el.stopColor,el.stopOpacity);
                                                color = ('rgb('+color.r+','+color.g+','+color.b+')');
                                                //console.log('stop color / offset ' + color + ' / ' + el.offset);
                                                stops.push(color,(el.offset * 100));
                                            });

                                            bonsaiGradient = bonsai.gradient.radial('top',stops,false);
                                            //console.log(bonsaiGradient);
                                            path.attr({
                                                fillGradient:bonsaiGradient
                                            });
                                            /*
                                                  'fillGradient':{
                                                     'fx':'355.71429',
                                                     'fy':'308.07648',
                                                    'stops':[
                                                        {
                                                           'stop-color':'#000000',
                                                           'stop-opacity':'1',
                                                           'id':'stop14',
                                                           'offset':'0'
                                                        },
                                                        {
                                                           'stop-color':'#000000',
                                                           'stop-opacity':'0',
                                                           'id':'stop16',
                                                           'offset':'1'
                                                        }
                                                     ],
                                                     'gradientUnits':'userSpaceOnUse',
                                                     'collect':'always',
                                                     'cy':'308.07648',
                                                     'cx':'355.71429',
                                                     'gradientTransform':[
                                                        [
                                                           1.0,
                                                           0.0,
                                                           0.0
                                                        ],
                                                        [
                                                           0.0,
                                                           1.0370439,
                                                           -11.41234
                                                        ]
                                                     ],
                                                     'svg':'radialGradient',
                                                     'r':'154.25716',
                                                     'id':'radialGradient827'
                                                  }
                                            */
                                            break;
                                        default:
                                            //console.log('Unrecognized gradient');

                                    }
                                }

                                if(node.attr.strokeGradient!==''){
                                    //console.log('Got a stroke gradient');

                                    gradientType = node.attr.strokeGradient.svg;

                                    switch(gradientType){
                                        case 'linearGradient':
                                            //console.log('Type, linear gradient');

                                            break;
                                        case 'radialGradient':
                                            console.log('Type, radial gradient');
                                            break;
                                        default:
                                            console.log('Unrecognized gradient');
                                    }

                                }

                                bansai.ids[node.id] = path;

                                if (node.label !== '') {

                                    if(!bansai.labels[node.label]){
                                        bansai.labels[node.label] = [];
                                    }

                                    bansai.labels[node.label].push(path);
                                }

                                path.addTo(parent);
                            },

                            addFlowRoot:function (node,parent){

                            },

                            addFlowPara:function (node,parent){

                            },

                             addFlowRegion:function(node,parent){

                            },

                            getRotationAngle:function(coords){

                                if(coords.length < 4) return false;
                                var deg2rad = Math.PI/180;
                                var rad2deg = 180/Math.PI;

                                var dx = coords[0] - coords[1];
                                var dy = coords[2] - coords[3];

                                var rads = Math.atan2(dx,dy);
                                var degs = rads * rad2deg;

                                return degs;
                            },

                            setRotationAngle:function(coords, direction){
                                    var resultCoords = [];

                                    if(direction === "left"){
                                        resultCoords = [100,0,0,0];
                                    } else if(direction === "right"){
                                        resultCoords = [0,100,0,0];
                                    } else if(direction === "down"){
                                        resultCoords = [0,0,0,100];
                                    } else if(direction === "up"){
                                        resultCoords = [0,0,100,0];
                                    } else if(typeof direction === "number"){

                                        var pointOfAngle = function(a) {
                                            return {
                                                x:Math.cos(a),
                                                y:Math.sin(a)
                                            };
                                        };

                                        var degreesToRadians = function(d) {
                                            return (d * (180 / Math.PI));
                                        };

                                        var eps = Math.pow(2, -52);
                                        var angle = (direction % 360);
                                        var startPoint = pointOfAngle(degreesToRadians(180 - angle));
                                        var endPoint = pointOfAngle(degreesToRadians(360 - angle));

                                        if(startPoint.x <= 0 || Math.abs(startPoint.x) <= eps)
                                            startPoint.x = 0;

                                        if(startPoint.y <= 0 || Math.abs(startPoint.y) <= eps)
                                            startPoint.y = 0;

                                        if(endPoint.x <= 0 || Math.abs(endPoint.x) <= eps)
                                            endPoint.x = 0;

                                        if(endPoint.y <= 0 || Math.abs(endPoint.y) <= eps)
                                            endPoint.y = 0;

                                        resultCoords = [startPoint.x,endPoint.x,startPoint.y,endPoint.y];
                                    }

                                return resultCoords;
                            },

                            objToString:function(obj) {
                                var str = '';
                                for (var p in obj) {
                                    if (obj.hasOwnProperty(p)) {
                                        str += p + '::' + obj[p] + '\n';
                                    }
                                }
                                return "\n" + str;
                            },

                            hexToRgba:function(hex,alpha) {
                                // Expand shorthand form (e.g. "03F") to full form (e.g. "0033FF")
                                var shorthandRegex = /^#?([a-f\d])([a-f\d])([a-f\d])$/i;
                                hex = hex.replace(shorthandRegex, function(m, r, g, b) {
                                    return r + r + g + g + b + b;
                                });

                                var result = /^#?([a-f\d]{2})([a-f\d]{2})([a-f\d]{2})$/i.exec(hex);
                                return result ? {
                                    r: parseInt(result[1], 16),
                                    g: parseInt(result[2], 16),
                                    b: parseInt(result[3], 16),
                                    a: alpha
                                } : null;
                            },

                            normalizeMatrix:function(mat){
                              var degree = 180 / Math.PI;
                              var radian = Math.PI / 180;
                              var a = mat[0];
                              var b = mat[1];
                              var c = mat[2];
                              var d = mat[3];
                              var tx = mat[4];
                              var ty = mat[5];
                              var rad;
                              var deg;
                              var sign;
                              var rotationInDegree;
                              var rotation;
                              var scaleX;
                              var scaleY;
                              var skewX;
                              var skewY;

                              /**
                               * scaleX = √(a^2+c^2)
                               * scaleY = √(b^2+d^2)
                               * rotation = tan^-1(c/d) = tan^-1(-b/a) it will not work sometimes 
                               * rotation = a / scaleX  = d / scaleY
                               */

                              scaleX = Math.sqrt((a * a) + (c * c));
                              scaleY = Math.sqrt((b * b) + (d * d));

                              sign = Math.atan(-c / a);
                              rad  = Math.acos(a / scaleX);
                              deg  = rad * degree;
                              
                              if (deg > 90 && sign > 0)
                              {
                                rotation = (360 - deg) * radian;
                              }
                              else if (deg < 90 && sign < 0)
                              {
                                rotation = (360 - deg) * radian;
                              }
                              else
                              {
                                rotation = rad;
                              }
                              rotationInDegree = rotation * degree;
                              
                              return {
                                scale:{
                                  x:scaleX,
                                  y:scaleY
                                },
                                rotation:{
                                  degree:rotationInDegree,
                                  radiance:rotation
                                },
                                translation:{
                                  x:tx,
                                  y:ty
                                }
                              };
                            }

                        };
