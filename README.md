# ws28XX-LED
LED-Animation Engine (Object based)
## Overview
This libary is an easy to use Layer-Based Engine for common LED-Strips such as the ws2812b.
It is very easy to create an interactive effect (MQTT support) for your application.
The engine is capable of overlaying multiple effects into one displayable picture.

#### Many Thanks to Mithrandir...

## Getting Started
<p>Clone this reposetory and open it with a Python IDE. Some effects and objects need further package installation (See Doc).</p)

## Seting up the Engine
<p>Import Engine, Consol and Alarm</p>

    from Lib.Engine import Engine
    from Lib.Controller.Consol import Consol
    from Lib.Effects.AlarmClock import AlarmClock
    from Lib.Effects.Fading import Fading

<p>First create an object from the class Engine.</p>

    engine = Engine()
<p>Next, set the right controller for your device. In this case it will print every frame in the console. The integer defines the length of every frame.</p>

    engine.setControler(Consol(pPixellength))
<p>Now add all SubEngines, the boolean determans wether the SubEngine is going to start the beginning.
The order the SubEngines are added determans the priority for their overlaying, first added equals highest priority.</p>

    engine.addSubEngine(AlarmClock())
    engine.addSubEngine(Fading())
<p>At last run the Engine, this step finalizes the object. After that it is not posible to change the controler or add/remove SubEngines. The current thread will be captured </p>

    engine.run()
    
## Creating your own SubEngine
<p>Import SubEngine and Snake</p>

    from Lib.SubEngine import SubEngine
    from Lib.Objects.Snake import Snake
<p>To create a new effect inherit SubEngine into your class and call the superconstructor. Every effect needs a unique name represented
in a String. The parameter pLayerCount determines the number of layers. Some attributes from the SubEngine such as pixellength are not initialsed at this point (See Doc).</p>

    from Lib.SubEngine import SubEngine
    from Lib.Objects.Snake import Snake
    
    class newEffect(SubEngine):
    
      def __init__(self):
        SubEngine.__init__(self, "newEffect", 1)
        self.snake = None
<p>When the method setup() is called all attributes are initialsed. Overwrite the method and create a Snake with the given attribut pixellength from SubEngine. Then add the snake to the first layer(0)</p>

    from Lib.SubEngine import SubEngine
    from Lib.Objects.Snake import Snake
    
    class newEffect(SubEngine):
    
      def __init__(self):
        SubEngine.__init__(self, "newEffect", 1)
        self.snake = None
      
      def setup(self):
        self.snake = Snake(self.pixellength)
        self.addObj(self.snake)       
<p>Before each frame is rendered the method update() is called. In this method the animation is written. Overwrite the method update and call the method move() on the snake object.</p>

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

<p>Done! Just add an instance from this class to the Engine and run it...</p>



