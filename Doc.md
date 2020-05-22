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
  <li>framse as Dictonary
    <p><em>Contains current frames of running SubEngines</em></p>
  </li>
  <li>controler
    <p><em>Contains the controler instance</em></p>
  </li>
  <li>pixellength
    <p><em>Contains the the pixellength of the controler, initalises in run() method</em></p>
  </li>
</ul>

#### Methods
<ul>
  <li>startMQTT(pAddres)
    <p><em>Initialises MQTT</em></p>
  </li>
  # Documentation of JB-LED



