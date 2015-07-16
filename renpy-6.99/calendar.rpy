########
#calendar.rpy
#
#Purpose: To provide a Persona 4-like day to day transition screen.
#
#How to include: Simply place this file in the "game" folder of your
#RenPy game. This is the folder with options.rpy, script.rpy, etc.
#You should also include relevant images, as defined in this script.
#
#How to use: Before running this script, you should set the default time.
#This is done like so: calDate.replace(second=0, hour=5, minute=0, day=1, month=1, year=2014)
#The arguments passed in are self-explanatory.
#
#There are several other settings you can tweak as well. For example,
#the intDelay variable. This determines how long in seconds the calendar
#will display for after finishing the animation.
#
#After you've overridden the desired variables and set the start time/date,
#you're ready to show the calendar. Simply use the call command
#to invoke the calendar label. The animation will run, it will wait intDelay
#seconds, then continue with the game.
#
#A full example of the calendar being used is shown below.
#This entails a very basic script.rpy file.
#We start at the start label and set the date to Monday January 1st.
#We then call calendar, which moves us forward 2 days to Wednesday
#January 3rd.
#
#label start:
#    $ calDate.replace(second=10, hour=12, minute=30, day=1, month=1, year=2014)
#
#    call calendar(2)
#
########

###
#Time variables
#
#These variables are used to depict dates and show transitions
#from one day to the next. They should be set manually once,
#after which the calendar will automatically update the values
#as it is used.
#
#These variables can be set again if you wish to change the date
#between instances of the calendar being shown.
#eg. The date could be set to Jan 1st, the calendar is called and
#moves the date forward 2 days. Then, in-game, the date variables
#are changed to March 5th, and the next time the calendar is shown
#it will start at March 5th instead. Like so:
#
#Example:
#
#    $ calDate.replace(day=1, month=1)
#    call calendar(2) #Moves from Jan 1st to Jan 3rd
#
#    $ calDate.replace(day=5, month=3)
#    call calendar(2) #Moves from Mar 5th to Mar 7th
###

default calDate = datetime.datetime(2001, 8, 20, 12, 0, 0) #20th August 2001, midday

#The date to display, or the starting date of a time lapse.
#Current month. 1 = January, 12 = December
default displayYear = False
default displayFullName = True #True = full name (Monday), False = abbreviation (Mon)
default displayTime = False
default displayWeather = False #If False, don't display. Otherwise display value.
default startDelay = 2.0 #Time to wait before beginning the calendar animation.
default intDelay = 2.0 #Time for which to keep showing calendar after animation.

init python:

    import calendar
    import datetime
    import math

    ###
    #getRDay(int mv) #getRelativeDay
    #
    #Gets date mv days away.
    #eg. Starting at 21st, mv of 2 would return 23rd.
    #Starting at 31st, mv of 2 would return 2nd.
    ###
    def getRDay(mv):
        newVal = calDate + datetime.timedelta(days=mv)
        newVal = newVal.day

        if 4 <= newVal <= 20 or 24 <= newVal <= 30:
            return str(newVal) + "th"
        else:
            return str(newVal) + ["st", "nd", "rd"][newVal % 10 - 1]

    ###
    #getRWDay(int mv) #getRelativeWeekDay
    #
    #Gets name of day mv days away.
    #eg. If the day is monday, and mv is -2, the day returned is saturday.
    ###
    def getRWDay(mv):
        global calDate
        global displayFullName

        day = calDate + datetime.timedelta(days=mv)
        day = day.weekday()
        return calendar.day_name[day] if displayFullName else calendar.day_abbr[day]

    ###
    #move(int direction)
    #@param direction Number of days forward or back to move.
    #
    #This method checks whether we're moving forward or back in
    #time (eg. yesterday or tomorrow) and changes the date appropriately.
    ###
    def move(direction):
        global calDate

        month = calDate.month
        year = calDate.year
        calDate += datetime.timedelta(days=direction)
        monthChanged = month != calDate.month
        yearChanged = year != calDate.year
        return (monthChanged, yearChanged)

###
#Image resources
###
image calendar_bg = "calendar/1280x720/bg.png" #Background image
image dayButton = "calendar/1280x720/gray.png" #Image representing each week day

label calendar(direction):

    scene black
    show calendar_bg at fade_in(0,0)

    python:
        startOriginalDelay = startDelay #Preserve startDelay
        imgWidth = 220 #Width of buttons; change if image changes
        posY = 475
        posX = 10
        dDir = 1 if direction > 0 else -1
        if direction < 1:
            mvDir = mini = -1
        else:
            mini = 0 #TODO: if not moving, don't show 8
            mvDir = 0 if direction == 0 else 1

    show screen CalendarMonth(calendar.month_name[calDate.month])
    if displayYear:
        show screen CalendarYear(str(calDate.year))

    while direction != 0:

        $ speed = 1.0 #/ math.fabs(direction) #Uncomment to speed up multi-day transitions

        call hideButtons
        show screen CBtn1((getRWDay(mini-1), getRDay(mini-1)), mvDir, imgWidth, posX+imgWidth*(mini+0), posY, startDelay, speed)
        show screen CBtn2((getRWDay(mini+0), getRDay(mini+0)), mvDir, imgWidth, posX+imgWidth*(mini+1), posY, startDelay, speed)
        show screen CBtn3((getRWDay(mini+1), getRDay(mini+1)), mvDir, imgWidth, posX+imgWidth*(mini+2), posY, startDelay, speed)
        show screen CBtn4((getRWDay(mini+2), getRDay(mini+2)), mvDir, imgWidth, posX+imgWidth*(mini+3), posY, startDelay, speed)
        show screen CBtn5((getRWDay(mini+3), getRDay(mini+3)), mvDir, imgWidth, posX+imgWidth*(mini+4), posY, startDelay, speed)
        show screen CBtn6((getRWDay(mini+4), getRDay(mini+4)), mvDir, imgWidth, posX+imgWidth*(mini+5), posY, startDelay, speed)
        show screen CBtn7((getRWDay(mini+5), getRDay(mini+5)), mvDir, imgWidth, posX+imgWidth*(mini+6), posY, startDelay, speed)
        show screen CBtn8((getRWDay(mini+6), getRDay(mini+6)), mvDir, imgWidth, posX+imgWidth*(mini+7), posY, startDelay, speed)
        
        if startDelay != 0:
            pause startDelay
            $ startDelay = 0
        $ print "mvdir"

        $ monthChanged, yearChanged = move(dDir)
        $ print "moved"

        if monthChanged:
            hide screen CalendarMonth
            show screen CalendarMonth(calendar.month_name[calDate.month])
        if displayYear and yearChanged:
            hide screen CalendarYear
            show screen CalendarYear(str(calDate.year))

        pause speed

        $ direction -= dDir

    if displayTime:
        show screen CalendarTime(calDate.hour, calDate.minute, calDate.second)
    if displayWeather:
        show screen CalendarWeather(displayWeather)
    
    pause intDelay
    $ print "hiding showCurrentDays"
    hide screen CalendarTime
    hide screen CalendarWeather
    hide screen CalendarMonth
    hide screen CalendarYear
    call hideButtons

    scene black with dissolve

    pause intDelay

    $ startDelay = startOriginalDelay

    return

label hideButtons:
    hide screen CBtn1
    hide screen CBtn2
    hide screen CBtn3
    hide screen CBtn4
    hide screen CBtn5
    hide screen CBtn6
    hide screen CBtn7
    hide screen CBtn8
    return

###
#Screens
###

screen CBtn1(day, direction, distance, posX, posY, startDelay, speed):
    use CalendarButton(day, direction, distance, posX, posY, startDelay, speed)

screen CBtn2(day, direction, distance, posX, posY, startDelay, speed):
    use CalendarButton(day, direction, distance, posX, posY, startDelay, speed)

screen CBtn3(day, direction, distance, posX, posY, startDelay, speed):
    use CalendarButton(day, direction, distance, posX, posY, startDelay, speed)

screen CBtn4(day, direction, distance, posX, posY, startDelay, speed):
    use CalendarButton(day, direction, distance, posX, posY, startDelay, speed)

screen CBtn5(day, direction, distance, posX, posY, startDelay, speed):
    use CalendarButton(day, direction, distance, posX, posY, startDelay, speed)

screen CBtn6(day, direction, distance, posX, posY, startDelay, speed):
    use CalendarButton(day, direction, distance, posX, posY, startDelay, speed)

screen CBtn7(day, direction, distance, posX, posY, startDelay, speed):
    use CalendarButton(day, direction, distance, posX, posY, startDelay, speed)

screen CBtn8(day, direction, distance, posX, posY, startDelay, speed):
    use CalendarButton(day, direction, distance, posX, posY, startDelay, speed)

screen CalendarButton(day, direction, distance, posX, posY, startDelay, speed):
    frame:
        background None
        xsize distance
        ysize distance + 35
        xpos posX
        ypos posY - 35

        if startDelay > 0:
            at move_align_wait(direction, distance, posX, startDelay, speed)
        else:
            at move_align(direction, distance, posX, speed)

        text day[0] size 24 xcenter 0.375
        add "dayButton" ypos 30
        text day[1] size 28 ypos 90 xcenter 0.375

screen CalendarMonth(mon):
    text mon size 72 color "#545454CC" xalign 0.5 at swipe_in(0, 62)

screen CalendarYear(yr):
    text yr size 48 color "#545454CC" at fade_in(1050, 20)

screen CalendarTime(hour, minute, second):
    text format(hour, '02')+":"+format(minute, '02') size 48 color "#545454CC" at fade_in(700, 30)

screen CalendarWeather(weather):
    text weather size 42 color "#545454CC" at fade_in(700, 76)

###
#Transforms
###

transform move_align(direction, distance, xPos, speed=1.0):
    on show:
        xpos xPos
        linear speed xpos (xPos - direction * distance)
    on hide:
        ease .5 alpha 0

transform move_align_wait(direction, distance, xPos, startDelay, speed=1.0):
    on show:
        alpha 0
        ease 1 alpha 1
        time startDelay
        linear speed xpos (xPos - direction * distance)
    on hide:
        ease .5 alpha 0

transform fade_in(xPos, yPos): #Fade in a displayable over 1 second at xPos yPos
    on show:
        alpha 0 pos (xPos, yPos)
        ease 1.0 alpha 1.0
    on hide:
        ease .5 alpha 0

transform swipe_in(xPos, yPos):
    on show:
        alpha 0 pos (1050 + xPos, yPos - 35)
        easein 1.0 alpha 1.0 ypos yPos
    on hide:
        alpha 1.0 pos (1050 + xPos, yPos)
        easeout 1.0 alpha 0 ypos (yPos - 35)