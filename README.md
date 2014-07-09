python-calendar
===============
Game transition calendar written in python.<br>
<br>
The aim of this project is to provide a day to day calendar to show
time transitions using basic animation.<br>
By adding the relevant resources to a project, a developer can add
the calendar's functionality to their own game.<br>
eg. Someone writing a Ren'Py Visual Novel could easily integrate the
resources in the renpy folder, then call the required function to graphically
express the transition from one day to the next between scenes/labels.<br>
<br>
There are currently 2 supported engines: Ren'Py and PyGame.<br>
The differences between the two are as follows.<br>
<br>
The PyGame module includes support for:
<ul>
	<li>repeating backgrounds</li>
	<li>SVG graphics</li>
	<li>multiple, non-standard resolutions</li>
	<li>keystroke control to change days</li>
</ul>
You should also note that, in its current state, the PyGame module is more
of a demo than a resource to be included directly into a project. It would need
to be modified to work the same as the Ren'Py module.<br>
<br>
The Ren'Py module is:
<ul>
	<li>more portable</li>
	<li>well-documented</li>
	<li>more up to date (ie. contains more features & settings)</li>
</ul>
The main advantage of the Ren'Py game module is how simple it is to use.<br>
Simply copy the included files into the main folder of the "game" folder of your project and follow the instructions in the documentation.<br>
<br>
Also worthy of note is the fact that the code for the PyGame module is currently much cleaner, and has been tested far more, but isn't documented.<br>
<br>
<h3>How to use</h3>
<h4>Ren'Py</h4>
Thorough instructions are included in the calendar.rpy file, but basically:
<ul>
	<li>Copy the files from the renpy directory into your project's game folder</li>
	<li>When you want to invoke the calendar for the first time, set the dayofweek, dayofmonth, month, direction and label_cont variables</li>
	<li>Jump to "calendar"</li>
</ul>
and that's it. For a more in-depth explanation, as well as a list of the different settings available, please read the comments within the calendar.rpy file.
<h4>PyGame</h4>
At this point in time, PyGame can't just be dragged and dropped into a project.<br>
Instead, the PyGame module is currently a standalone demo.<br>
Simply run the Start.py file and use the left and right arrows to back and forward between days. You can change the values in self.move(int) within moveLeft() and moveRight() to change how many days forward or backward keystrokes will take you.