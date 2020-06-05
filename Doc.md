# Documentation of JB-LED

## Engine
<p>The Engine handles everything around all SubEngines (starting/terminating/communication).</p>  

#### Attributes
<ul>
  <li>isRunning as Boolean
    <p><em>Determens wether the Engine is Running, while running setting it to False will Terminate the Engine </em></p>
  </li>
  <li>brightness as Integer
    <p><em>Brightnis is Percent for all pixels in frame</em></p>
  </li>
  <li>processes as List
    <p><em>Contains all ProcessWrap instances</em></p>
  </li>
  <li>frames as Dictonary
    <p><em>Contains current frames of running SubEngines</em></p>
  </li>
  <li>controler as Controller
    <p><em>Contains the controler instance</em></p>
  </li>
  <li>pixellength as Integer
    <p><em>Contains the the pixellength of the controler, initalises in run() method</em></p>
  </li>
</ul>

#### Methods
<ul>
<li>startMQTT(pAddres:String)
<p><em>Initialises MQTT</em></p>
</li>
<li>setControler(pControler)
<p><em>Sets the Controller for the Engine. While the Engine is running it is not possible to change it.</em></p>
</li>
<li>on_Message(client as ??, userdata as ??, msg as Message)
<p><em>Input method for Paho-MQTT.</em></p>
</li>
<li>addSubEngine(pSub as SubEngine, pIsEnabled as Boolean)
<p><em>Wraps the SubEngine and starting parameter into a ProcessWrap and adds it to processes </em></p>
</li>
<li>run()
<p><em>Captures starting thread with a while loops and coordinates all steps.</em></p>
</li>
<li>startSubEngine(prWrap as ProcessWrap)
<p><em>Starts with in a new created process the SubEngine.</em></p>
</li>
<li>terminateSubEngine(prWrap as ProcessWrap)
<p><em>Orders the SubEngine to Terminate it self. Processes are joined.</em></p>
</li>
<li>terminateAll()
<p><em>Calls with every ProcessWrap from processes the Method terminateSubEngine(prWrap as ProcessWrap). Sets isRunning to False</em></p>
</li>
</ul>

##SubEngine
<p>The Subengine handles layers and objects. Every active SubEngine runns with a dedicated process.</p>
<p>Engine and SubEngine are connected and synchronized through a Pipe.</p>

#### Attributes
<ul>
<li>layList as List
<p><em>Contains all Layer, sorted by priority.</em></p>
</li>
<li>name as String
<p><em>Equals an Id for the Engine</em></p>
<li>compClass as CompressionClass
<p><em>Contains the Compression Class, None equals no compression</em></p>
</li>
<li>isRunning as Boolean
<p><em>Is used to capture the process and keep it alive</em></p>
</li>
<li>pixellength as Integer
<p><em>Cointains the number of available pixel. This variable is in the method setup initialized</em></p>
</li>
<li>transparent as List
<p><em>Contains the transparent colorkey [-1, -1, -1]</em></p>
</li>
</ul>

#### Methods
<ul>
<li>
<p><em></em></p>
</li>
<li>
<p><em></em></p>
</li>
<li>
<p><em></em></p>
</li>
<li>
<p><em></em></p>
</li>
<li>
<p><em></em></p>
</li>
<li>
<p><em></em></p>
</li>
<li>
<p><em></em></p>
</li>
<li>
<p><em></em></p>
</li>
<li>
<p><em></em></p>
</li>
<li>
<p><em></em></p>
</li>
<li>
<p><em></em></p>
</li>

</ul>

