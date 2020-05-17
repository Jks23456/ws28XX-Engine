# JB-LED
LED-Animation Engine (Object based)
## Overview
This Libary is an easy to use Layer-Based Engine for common LED-Strips such as the ws2812b.
It is very simple to create an interactive effect (MQTT support) for your application.
The engine is capable of overlaying multible effects into one displayeble picture.

#### Many Thanks to Mithrandir...

## Getting Started
<p>Clone this reposetory and open it with a Python IDE. Some effekts and object need further packages (See Doc).</p)
## Seting up the Engine
<p>Import Engine, Consol and Alarm</p>

    from Lib.Engine import Engine
    from Lib.Controller.Consol import Consol
    from Lib.Effects.AlarmClock import AlarmClock
    from Lib.Effects.Fading import Fading

<p>First create an object from the class Engine.</p>

    engine = Engine()
<p>Next, set the right Controler for your device. In this case it will display every frame in form from text in the consol. The integer defines the length of evrey frame.</p>

    engine.setControler(Consol(pPixellength))
<p>Now add all SubEngines, the boolean determans wether the SubEngine is started at the begining or not.
The order the SubEngines are added determans the priority for ther overlaying, first added equals highest priority.</p>

    engine.addSubEngine(AlarmClock())
    engine.addSubEngine(Fading())
<p>At last run the Engine, this step finalses the object. After that it is not posible to change the controler or add/remove SubEngines. The current thread will be captchured </p>

    engine.run()
    
## Creating your own SubEngine
<p>Import SubEngine and Snake</p>

    from Lib.SubEngine import SubEngine
    from Lib.Objects.Snake import Snake
<p>To create a new effect inherit SubEngine into your class and call the superconstructor. Every effects needs a unique name represented
as String. The parameter pLayerCount determines the number of layers. Some attributes from the SubEngine such as pixellength are 
at this point not initialsed (See Doc).</p>

    from Lib.SubEngine import SubEngine
    from Lib.Objects.Snake import Snake
    
    class newEffect(SubEngine):
    
      def __init__(self):
        SubEngine.__init__(self, "newEffect", 1)
        self.snake = None
<p>When the method setup() is called all attributes are initialsed. Overwrite the method and create one Snake with the from SubEngine 
given attribut pixellength. Then add the snake to the first layer(0)</p>

    from Lib.SubEngine import SubEngine
    from Lib.Objects.Snake import Snake
    
    class newEffect(SubEngine):
    
      def __init__(self):
        SubEngine.__init__(self, "newEffect", 1)
        self.snake = None
      
      def setup(self):
        self.snake = Snake(self.pixellength)
        self.addObj(self.snake)       
<p>Befor each frame is rendered the method update() is called. In this method the animation is written. Overwrite the method update and call 
on the object the method move().</p>

    from Lib.SubEngine import SubEngine
    from Lib.Objects.Snake import Snake
    
    class newEffect(SubEngine):
    
      def __init__(self):
        SubEngine.__init__(self, "newEffect", 1)
        self.snake = None
      
      def setup(self):
        self.snake = Snake(self.pixellength)
        self.addObj(self.snake)
      
      def update(self):
        self.snake.move()

<p>Done! Now just add an instance from this class to the Engine and run it...</p>



