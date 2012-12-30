Bonsai!
======

Inkscape to BonsaiJS extension

* What is Bansai?
    This is a script extension for Inkscape.It was inspired by the splendid BonsaiJS library. As well as 
    my lazy disposition, which does not like "coding" graphics ;) 
    So in short Bansai lets you select one or elements in Inkscape, and export them to BonsaiJS JSON notation.
    
* What is supported by this version?
    
    A little, and still a lot :) At the moment I have had time to implement support for 
        - Path elements
        - Group elements (also nested)
        - Transformation matrix 
        - Filters
        - Gradients

    These initial features can get you pretty far as most, or all, SVG shapes can be described using
    one or more of the path types available.
    
* What is NOT supported by this version?
    
    A lot of course, such as
        - SVG shapes such as Rect and Ellipse 
        - Fonts and Text

        
    Thanks to Bonsai its really easy for anyone with a basic knowledge of Python, 
    JavaScript and SVG to help with development :)
