Update 20121221 17:30


Removed the "feature" that made toggeling of layer visibility neccesary. This however will
make all elements, also on hidden layers, present in the exported json.

Also fixed a file system bug thanks to Tobias

--------------------------------------------------------------------------------------------------

Update 20121221 16:25

Fixed some silly bugs. Now opacity works for fill and stroke again :)

--------------------------------------------------------------------------------------------------

Update 20121221 15:48

Started implementing gradient support. Lots of work compared to the previous stuff!
Help would be awesome :D

--------------------------------------------------------------------------------------------------

Update 20121219 19:06

Added blur filter support to the Bansai js code :)

--------------------------------------------------------------------------------------------------

Update 20121219

Gradients added to json output:

{
   'radialGradient':{
      'fx':'281.42856',
      'fy':'323.79074',
      'stops':[
         {
            'stop-color':'#000000',
            'stop-opacity':'1',
            'id':'stop840',
            'offset':'0'
         },
         {
            'stop-color':'#000000',
            'stop-opacity':'0.49803922',
            'id':'stop848',
            'offset':'0.35054708'
         },
         {
            'stop-color':'#000000',
            'stop-opacity':'0',
            'id':'stop842',
            'offset':'1'
         }
      ],
      'gradientUnits':'userSpaceOnUse',
      'collect':'always',
      'cy':'323.79074',
      'cx':'281.42856',
      'gradientTransform':[
         [
            0.96764083999999995,
            0.08781738,
            -19.327677000000001
         ],
         [
            -0.076970060000000007,
            1.1040095999999999,
            -12.015768
         ]
      ],
      'r':'95.714287',
      'id':'radialGradient850'
   }
}

--------------------------------------------------------------------------------------------------

Update 20121218 20:50

Implemented inclusion of filters:

{
   'filter':{
      'feTurbulence':{
         'baseFrequency':'0.2',
         'seed':'0',
         'result':'result7',
         'numOctaves':'1',
         'type':'fractalNoise',
         'id':'feTurbulence853'
      },
      'feGaussianBlur':{
         'result':'result91',
         'stdDeviation':'8',
         'id':'feGaussianBlur869',
         'in':'result0'
      },
      'feOffset':{
         'result':'result4',
         'id':'feOffset835',
         'dx':'0',
         'dy':'1.4'
      },
      'feMorphology':{
         'result':'result0',
         'radius':'4',
         'id':'feMorphology867',
         'in':'fbSourceGraphic'
      },
      'feConvolveMatrix':{
         'divisor':'6.03',
         'kernelMatrix':'0 -1 0 0 -1 0 0 2 0',
         'order':'3 3',
         'result':'result1',
         'in':'fbSourceGraphic',
         'id':'feConvolveMatrix823'
      }
   }

--------------------------------------------------------------------------------------------------

Update 20121216 23:07

Fixed crash in py code when retrieving fill color for paths.

--------------------------------------------------------------------------------------------------

Update 20121216 22:42

Separated out the Bansai code into its own "static" closure. This to make it more reusable.

--------------------------------------------------------------------------------------------------

Update 20121214 16:37

Added indexing of all added Bonsai objects. This makes it possible to reference them later in
your script like this:

var tree = stage.options.lookup.labels['tree1'];
or
var tree = stage.options.lookup.ids['g7816'];

And you get a reference back to that instance.

This means that you can preserve your Inkscape layer/shape/group naming in you script. Neat.... :) 

You JS console will also output all the contents of these two indexes.


--------------------------------------------------------------------------------------------------

Update 20121214 15:23

Externalized the template HTML code to a separate file. This should be placed, along with the
other files, in the Inkscape/share/extensions/ folder.

--------------------------------------------------------------------------------------------------

Update 20121213 10:51

Added check to make sure that bounding boxes are never "None" but instead empty arrays.

Update 20121213 10:21

I'm such a dork.  I forgot to add transform support for Path elements. 
Fixed now though :)
