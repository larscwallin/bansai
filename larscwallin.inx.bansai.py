#!/usr/bin/env python
import inkex
import simpletransform
import simplepath
import os.path
from simplestyle import *
from time import gmtime, strftime
import string
import webbrowser
import threading
from optparse import OptionParser


# This line below is only needed if you don't put the script directly into
# the installation directory
# sys.path.append('/usr/share/inkscape/extensions')

"""
Bansai! version 0.00001

* What is Bansai?
    This is a script extension for Inkscape.It was inspired by the splendid BonsaiJS library. As well as
    my lazy disposition, which does not like "coding" graphics ;)
    So in short Bansai lets you select one or elements in Inkscape, and export them to BonsaiJS JSON notation.

"""


class SVGElement():
    id=''
    label=''
    box=[]
    path=[]
    fill=''
    fill_opacity=1
    stroke=''
    stroke_width=0
    stroke_opacity=1
    transform=''
    x=0
    y=0
    width=0
    height=0
    nodeRef = None

    def __init__(self,node = None):
        self.nodeRef = node


class SVGPath(SVGElement):

    def __init__(self,node = None):
        SVGElement.__init__(self)


class SVGRect(SVGElement):
    def __init__(self,node = None):
        SVGElement.__init__(self)

class SVGArc(SVGElement):
    cx=0
    cy=0
    rx=0
    ry=0

    def __init__(self,node = None):
        SVGElement.__init__(self)

class SVGGroup(SVGElement):
    items=[]

    def __init__(self,node = None):
        SVGElement.__init__(self)

"""
This is where the actual fun stuff starts
"""

# Effect main class
class Bansai(inkex.Effect):
    json_output = []
    debug_tab ='     '
    svg_doc = None
    svg_doc_width  = ''
    svg_doc_height  = ''
    svg_file = ''
    bonsaistyle = False
    reposition = True
    parsing_context = ''
    parse_stack = []

    def __init__(self):
        """
        Constructor.
        """

        """
        First we grab the input parameters that we got from the Inkscape plugin system (see the .inx file)
        """

        inkex.Effect.__init__(self)

        self.OptionParser.add_option('--where', action = 'store',
              type = 'string', dest = 'where', default = '',
              help = 'Where to save the resulting file?')

        self.OptionParser.add_option('--reposition', action = 'store',
              type = 'inkbool', dest = 'reposition', default = False,
              help = 'Reposition elements to 0,0?')

        self.OptionParser.add_option('--bonsaistyle', action = 'store',
              type = 'inkbool', dest = 'bonsaistyle', default = False,
              help = 'Should the output be BonsaiJS specific?')

        self.OptionParser.add_option('--viewresult', action = 'store',
              type = 'inkbool', dest = 'viewresult', default = True,
              help = 'Do you want to view the result?')


    def effect(self):
        """
        Effect behaviour.
        Overrides base class method
        """
        self.svg_file = self.args[-1]
        self.svg_doc = self.document.xpath('//svg:svg',namespaces=inkex.NSS)[0]
        self.svg_doc_width  = inkex.unittouu(self.svg_doc.get('width'))
        self.svg_doc_height  = inkex.unittouu(self.svg_doc.get('height'))
        self.where = self.options.where
        self.reposition = self.options.reposition
        self.bonsaistyle = self.options.bonsaistyle
        self.viewresult = self.options.viewresult
        filename = ''
        success = False

        #inkex.debug("filter:url(#g4567)".split('filter:url(#')[1].split(')'))

        self.getselected()

        if(self.selected.__len__() > 0):

            #inkex.debug(self.debug_tab + 'Elements selected\n');

            self.json_output.append({
                'defs':{
                    'filters':[],
                    'fonts':[],
                    'gradients':[]
                },
                'elements':[]
            })

            parent = self.json_output[0]['elements']
            selected = []
            layers = self.document.xpath('//svg:svg/svg:g/*',namespaces=inkex.NSS)

            # Iterate through all selected elements

            for element in self.selected.values():
                selected.append(element.get('id'))
                #inkex.debug(self.debug_tab + 'selected ' + element.get('id'))

            for element in layers:
                #inkex.debug(self.debug_tab + 'Looping element ' + element.get('id'))
                if(element.get('id') in selected):
                    self.parseElement(element,parent)
                    #inkex.debug(self.debug_tab + 'found ' + element.get('id'))


            self.debug_tab = self.debug_tab[:-4]

        else:
            #inkex.debug(self.debug_tab + 'No elements were selected')

            #layers = self.document.xpath('//svg:svg/svg:g[@style!="display:none"]',namespaces=inkex.NSS)
            layers = self.document.xpath('//svg:svg/svg:g',namespaces=inkex.NSS)

            self.json_output.append({
                'svg':'document',
                'id':'',
                'name':'',
                'transform':'',
                'box':[
                    0,
                    self.svg_doc_width,
                    0,
                    self.svg_doc_height
                ],
                'defs':{
                    'filters':[],
                    'fonts':[],
                    'gradients':[]
                },
                'elements':[]
            })
            parent = self.json_output[0]['elements']

            # Iterate through all selected elements
            for element in layers:
                self.parseElement(element,parent)

            self.debug_tab = self.debug_tab[:-4]

        #inkex.debug(self.debug_tab + '\nDone iterating.\n')
        #inkex.debug(self.debug_tab + ','.join([str(el) for el in self.json_output]))

        if(self.where!=''):

            # The easiest way to name rendered elements is by using their id since we can trust that this is always unique.
            time_stamp = strftime('%a%d%b%Y%H%M', gmtime())
            filename = os.path.join(self.where, 'bansai-'+time_stamp+'.html')
            content = self.templateOutput('larscwallin.inx.bansai.template.html','{/*bonsai_content*/}')
            success = self.saveToFile(content,filename)

            if(success and self.viewresult):
                self.viewOutput(filename)
            else:
                inkex.debug('Unable to write to file "' + filename + '"')

        #inkex.debug(self.debug_tab + ','.join([str(el) for el in self.json_output]))
    def normalizeSVG(self):
        pass

    def parseGroup(self,node,parent):
        #inkex.debug(self.debug_tab + 'Parsing group' + node.get('id'))
        self.debug_tab += '    '

        self.parsing_context = 'g'

        id = node.get('id')
        transform = simpletransform.parseTransform(node.get('transform',''))
        label = str(node.get(inkex.addNS('label', 'inkscape'),''))

        elements = node.xpath('./*',namespaces=inkex.NSS)

        box = simpletransform.computeBBox(elements)
        box = list(box) if box != None else []

        group = {
            'id':id,
            'name':label,
            'label':label,
            'svg':'g',
            'transform':transform,
            'box':box,
            'elements':[]
        }

        parent.append(group)

        self.parse_stack.append(group)

        #inkex.debug('Loop through all grouped elements')

        for child in elements:
            self.parseElement(child,group["elements"])

        self.debug_tab = self.debug_tab[:-4]

        self.parsing_context = ''
        self.parse_stack.pop()


    def parseElement(self,node,parent):
        type = node.get(inkex.addNS('type', 'sodipodi'))

        if(type == None):
            #remove namespace data {....}
            tag_name = node.tag
            tag_name = tag_name.split('}')[1]
        else:
            tag_name = str(type)

        id = node.get('id')

        #inkex.debug(self.debug_tab + 'Got "' + tag_name + '" element ' + id);

        if(tag_name == 'g'):
            self.parseGroup(node,parent)
        elif(tag_name == 'path'):
            self.parsePath(node,parent)
        elif(tag_name == 'arc'):
            self.parsePath(node,parent)
        elif(tag_name == 'rect'):
            self.parseRect(node,parent)


    def parseStyleAttribute(self,str):

        #inkex.debug(self.debug_tab + 'Got style ' + str)

        rules = str.split(';')
        parsed_set = {}
        result = ''
        for rule in rules:
            parts = rule.split(':')

            if(len(parts) > 1):

                key = self.camelConvert(parts[0])
                val = self.camelConvert(parts[1])

                if(key== 'filter'):
                    parsed_set['filter'] = self.parseFilter(val)
                elif(key == 'fill' and val.find('url(#') > -1):
                    parsed_set['fill-gradient'] = self.parseGradient(val)
                elif(key == 'stroke' and val.find('url(#') > -1):
                    parsed_set['stroke-gradient'] = self.parseGradient(val)
                else:
                    parsed_set[key] = val

        result =  parsed_set
        return result

    def parseFilter(self,filter_str):
        # Split out the id from the url reference
        filter_id = self.parseUrlParam(filter_str)
        result_list = []
        tag_name = ''

        # Got a valid id?
        if(filter_id!=''):
            # Ok lets get the filter element which holds all actual instructions
            filters = self.document.xpath('//svg:svg/svg:defs/svg:filter[@id="'+filter_id+'"]/*',namespaces=inkex.NSS)

            for node in filters:
                inkex.debug(self.debug_tab + 'Looping filter ' + node.get('id'))
                tag_name = self.parseTagName(node.tag)

                filter = {
                    'svg':tag_name
                }

                # Grab all the parameters and values for the current filter
                for param,val in node.items():
                    param = self.parseTagName(param)
                    inkex.debug(self.debug_tab + 'param ' + param + ' val ' + val)
                    filter[param] = val

                result_list.append(filter)

            return result_list



    def parsePath(self,node,parent):

        #self.parsing_context = 'path'

        style = node.get('style')
        style = self.parseStyleAttribute(style)
        transform = simpletransform.parseTransform(node.get('transform',''))
        path_array = simplepath.parsePath(node.get('d'))

        path = {
            'id':node.get('id'),
            'svg':'path',
            'label':str(node.get(inkex.addNS('label', 'inkscape'),'')),
            'box':list(simpletransform.computeBBox([node])),
            'transform':transform,
            'path':path_array,
            'd':node.get('d',''),
            'attr':{
                'fillColor':style.get('fill',''),
                'fillGradient':style.get('fillGradient',''),
                'fillOpacity':style.get('fillOpacity','1'),
                'opacity':style.get('opacity','1'),
                'strokeColor':style.get('stroke',''),
                'strokeGradient':style.get('strokeGradient',''),
                'strokeWidth':style.get('strokeWidth','0'),
                'strokeOpacity':style.get('strokeOpacity','1'),
                'filters':style.get('filter','')
            }

        }




        #inkex.debug('Path resides in group ' + self.parse_stack[len(self.parse_stack)-1]['id'])

        if(self.reposition):
            path['path'] = self.movePath(path,0,0,'tl')
        else:
            path['path'] = simplepath.formatPath(path_array)

        path['box'] = list(path['box']) if path['box'] != None else []
        parent.append(path)


    """
        movePath changes a paths bounding box x,y extents to a new, absolute, position.
        In other words, this function does not use translate for repositioning.

        Note: The origin parameter is not currently used but will soon let you choose
        which origin point (top left, top right, bottom left, bottom right, center)
        to use.

    """
    def movePath(self,node,x,y,origin):
        path = node.get('path')
        box = node.get('box')

        #inkex.debug(box)

        offset_x = (box[0] - x)
        offset_y = (box[2] - (y))

        #inkex.debug('Will move path "'+id+'" from x, y ' + str(box[0]) + ', ' + str(box[2]))
        #inkex.debug('to x, y ' + str(x) + ', ' + str(y))

        #inkex.debug('The x offset is ' + str(offset_x))
        #inkex.debug('The y offset is = ' + str(offset_y))


        for cmd in path:
            params = cmd[1]
            i = 0

            while(i < len(params)):
                if(i % 2 == 0):
                    #inkex.debug('x point at ' + str( round( params[i] )))
                    params[i] = (params[i] - offset_x)
                    #inkex.debug('moved to ' + str( round( params[i] )))
                else:
                    #inkex.debug('y point at ' + str( round( params[i]) ))
                    params[i] = (params[i] - offset_y)
                    #inkex.debug('moved to ' + str( round( params[i] )))
                i = i + 1


        #inkex.debug(simplepath.formatPath(path))
        return simplepath.formatPath(path)


    def parseRect(self,node,parent):

        #self.parsing_context = 'rect'

        style = node.get('style')
        style = self.parseStyleAttribute(style)

        rect = {
            'id':node.get('id',''),
            'svg':'rect',
            'label':str(node.get(inkex.addNS('label', 'inkscape'),'')),
            'x': node.get('x',0),
            'y': node.get('y',0),
            'width':node.get('width',0),
            'height':node.get('height',0),
            'box':[],
            'fill':style.get('fill',''),
            'fillOpacity':style.get('fillOpacity',''),
            'opacity':style.get('opacity',''),
            'stroke':style.get('stroke',''),
            'strokeWidth':style.get('strokeWidth',''),
            'strokeOpacity':style.get('strokeOpacity',''),
            'transform':node.get('transform','')
        }

        if(self.reposition):
            self.x = 0
            self.y = 0

        parent.append(rect)

    def parseArc(self,node,parent):

        #self.parsing_context = 'arc'

        style = node.get('style')
        style = self.parseStyleAttribute(style)

        arc = {
            'id':node.get('id',''),
            'svg':'arc',
            'label':str(node.get(inkex.addNS('label', 'inkscape'),'')),
            'cx': node.get(inkex.addNS('cx', 'sodipodi'),''),
            'cy':node.get(inkex.addNS('cy', 'sodipodi'),''),
            'rx':node.get(inkex.addNS('rx', 'sodipodi'),''),
            'ry':node.get(inkex.addNS('ry', 'sodipodi'),''),
            'path':simplepath.parsePath(node.get('d')),
            'd':node.get('d',''),
            'box':list(simpletransform.computeBBox([node])),
            'fill':style.get('fill',''),
            'fill-opacity':style.get('fillOpacity',''),
            'stroke':style.get('stroke',''),
            'stroke-width':style.get('strokeWidth',''),
            'stroke-opacity':style.get('strokeOpacity',''),
            'transform':node.get('transform','')
        }


        if(self.reposition):
            arc['path'] = self.movePath(node,0,0,'tl')
        else:
            arc['path'] = arc['d']

        parent.append(arc)

    def parseDef(self,node,parent):
        pass


    def parseGradient(self,gradient_str):
        # Split out the id from the url reference
        gradient_use_id = self.parseUrlParam(gradient_str)
        gradient_use = {}
        gradient_href_id = ''
        gradient_href = {}
        result_list = {}
        tag_name = ''
        gradient_stops = []
        gradient_params = {}

        # Got a valid id?
        if(gradient_use_id != ''):
            #
            gradient_use = self.document.xpath('//svg:svg/svg:defs/*[@id="'+ gradient_use_id +'"]',namespaces=inkex.NSS)[0]

            tag_name = self.parseTagName(gradient_use.tag)

            gradient_params['stops'] = []

            #inkex.debug(self.debug_tab + 'Gradient ' + tag_name)

            # Grab all the parameters and values for the current gradient
            for param,val in gradient_use.items():
                #inkex.debug(self.debug_tab + 'param ' + param + ' val ' + val)
                param = self.parseTagName(param)

                if(param == 'href'):

                    # Inkscape uses one-to-many rel for gradients. We need to get the base config
                    # element which has params for color and stops.
                    gradient_href_id = val.split('#')[1]
                    gradient_href = self.document.xpath('//svg:svg/svg:defs/*[@id="'+ gradient_href_id +'"]/*',namespaces=inkex.NSS)

                    #inkex.debug(self.debug_tab + 'href to ' + gradient_href_id)
                    #inkex.debug(self.debug_tab + 'Looping through ' + str(len(gradient_href)) + ' gradient parameter elements')

                    for node in gradient_href:

                        #inkex.debug(self.debug_tab + 'Current parameter element ' + node.tag)

                        gradient_stop = {}

                        for param,val in node.items():

                            param = self.parseTagName(param)

                            #inkex.debug(self.debug_tab + 'Looping through gradient parameter attributes of ' + param)

                            if(param == 'style'):
                                #inkex.debug(self.debug_tab + 'Parsing style ' + val)
                                gradient_stop.update(self.parseStyleAttribute(val))
                            else:
                                #inkex.debug(self.debug_tab + 'Adding param/value : ' + param + '/' +  val)
                                gradient_stop[param] = val

                        #inkex.debug(self.debug_tab + 'Adding stop ' + gradient_stop['id'])
                        gradient_params['stops'].append(gradient_stop)

                elif(param == 'gradientTransform'):
                    transform = simpletransform.parseTransform(val)
                    gradient_params[param] = transform
                else:
                    gradient_params[param] = val

            gradient_params['svg'] = tag_name

            result_list = gradient_params

            return result_list

        """
            stops Array | Object   Color stops in the form: `['red','yellow',...]` or `[['red', 0], ['green', 50], ['#FFF', 100]]` i.e. Sub-array [0] is color and [1] is percentage As an object: { 0: 'yellow', 50: 'red', 100: 'green' }
            direction Number | String   Direction in degrees or a string, one of: `top`, `left`, `right`, `bottom`, `top left`, `top right`, `bottom left`, `bottom right`
            matrix Matrix  <optional>
             Matrix transform for gradient
            repeat String  <optional>
             How many times to repeat the gradient
            units String  <optional>
             Either 'userSpace' or 'boundingBox'.


            stops Array   Color stops in the form: `['red','yellow',...]` or `[['red', 0], ['green', 50], ['#FFF', 100]]` i.e. Sub-array [0] is color and [1] is percentage
            r Number  <optional>
             Radius in percentage (default: 50)
            cx Number  <optional>
             X coordinate of center of gradient in percentage (default: 50)
            cy Number  <optional>
             Y coordinate of center of gradient in percentage (default: 50)
            matrix Matrix  <optional>
             Matrix transform for gradient
            repeat String  <optional>
             How many times to repeat the gradient
            units String  <optional>
             Either 'userSpace' or 'boundingBox'.


        """

    def parseFont(self,node,parent):
        pass

    def parseGlyph(self,node,parent):
        pass

    def pathToObject(self,node):
        pass

    def repositionGroupedElements(self, box, elements):
        pass

    def parseUrlParam(self,url):
        return url.split('url(#')[1].split(')')[0]

    def camelConvert(self,str):
        camel = str.split('-')

        if(len(camel) == 2):
            str = camel[0] + camel[1].title()

        return str

    def parseTagName(self,tag):
        tag_name = tag.split('}')
        if(len(tag_name) > 1):
            return tag_name[1]
        else:
            return tag

    def viewOutput(self,url):
        vwswli = VisitWebSiteWithoutLockingInkscape()
        vwswli.url = url
        vwswli.start()

    def templateOutput(self,templateName = '',placeholder = ''):

        if(placeholder == ''):
            inkex.debug('Bonsai.templateOutput: Mandatory argument "placeholder" missing. Aborting.')
            return False

        if(templateName == ''):
            inkex.debug('Bonsai.templateOutput: Mandatory argument "templateName" missing. Aborting.')
            return False


        FILE = open(templateName,'r')

        if(FILE):
            template = FILE.read()
            FILE.close()

            if(len(template) > 0):
                content = ','.join([str(el) for el in self.json_output])
                tplResult = string.replace(template,placeholder,content)
                return tplResult
            else:
                inkex.debug('Bonsai.templateOutput: Empty template file "'+templateName+'". Aborting.')
                return False

        else:
            inkex.debug('Bonsai.templateOutput: Unable to open template file "'+templateName+'". Aborting.')
            return False


    def saveToFile(self,content,filename):

        FILE = open(filename,'w')

        if(FILE):
            FILE.write(content)
            FILE.close()
            return True
        else:
            inkex.debug('Bonsai.templateOutput: Unable to open output file "'+filename+'". Aborting.')
            return False


class VisitWebSiteWithoutLockingInkscape(threading.Thread):
    url = ''
    def __init__(self):
        threading.Thread.__init__ (self)

    def run(self):
        webbrowser.open('file://' + self.url)



# Create effect instance and apply it.
effect = Bansai()
effect.affect(output=False)


