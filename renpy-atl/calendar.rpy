########
#calendar.rpy
#
#Purpose: To provide a Persona 4-like day to day transition screen.
#
#How to include: Simply place this file in the "game" folder of your
#RenPy game. This is the folder with options.rpy, script.rpy, etc.
#
#How to use: Before running this script, there are a few variables
#you should set up. They are:
#
#  dayofweek
#  dayofmonth
#  month
#
#The first three variables specify the day of the week (eg. Sunday),
#the day of the month (eg. the 1st) and the current month (eg. January).
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
#January 3rd, then display a message before ending.
#
#label start:
#    $ dayofweek = 1
#    $ dayofmonth = 1
#    $ month = 1
#
#    call calendar(2)
#
#    "The day transition has just ended."
#
########

init python:

    ###
    #Time variables
    #
    #These variables are used to depict dates and show transitions
    #from one day to the next. Ideally they should be set manually
    #once, then modified using move().
    #
    #Typical usage entails setting default dayofmonth, dayofweek
    #and month variables, then going from day to day with move().
    #
    #Example:
    #
    #    dayofmonth = 1
    #    dayofweek = 0
    #    month = 1
    #
    #    move(5)
    #
    #This would set the date to Sunday the 1st of January, then
    #move forward 5 days to Friday the 6th of January.
    ###

    months = [
        ["January", 31],
        ["February", 28],
        ["March", 31],
        ["April", 30],
        ["May", 31],
        ["June", 30],
        ["July", 31],
        ["August", 31],
        ["September", 30],
        ["October", 31],
        ["November", 30],
        ["December", 31]
    ]

    days = [
        "Sunday",
        "Monday",
        "Tuesday",
        "Wednesday",
        "Thursday",
        "Friday",
        "Saturday"
    ]

    dayofmonth = 20 #01-31
    #Set this to the current date if you're just showing the date,
    #or the starting date if you're showing a time lapse.
    dayofweek = 0 #Keeps track of Sun-Sat. 0 = Sunday, 6 = Saturday.
    month = 8 #Current month. 1 = January, 12 = December
    oldmonth = 8 #Previous month.
    #Only useful when going from one month to the next.
    year = False #Set to either false or a numeric value. eg. 2012.
    #If not False, the year will be displayed below the current month.
    #The year will also increment/decrement accordingly.
    oldyear = False #Will be set automatically as year is changed

    displayFullName = True #If True, display the full name of a week day
    #rather than the abbreviation. eg. Tuesday rather than Tue
    displayTime = False #If False, don't display. Otherwise display value.
    displayWeather = False #If False, don't display. Otherwise display value.

    ###
    #Movement Variables
    ###

    direction = 0
    #Reflects how many days forward or back to move.
    #eg. A direction of -2 goes back 2 days, a direction of 1
    #goes to the next day, etc.

    ###
    #Time Variables
    #
    #These variables can be edited manually.
    #The values express time delays in seconds.
    #eg. 1.5 equals a one and a half second delay.
    ###

    startDelay = 1.0 #Time to wait before beginning the animation.
    intDelay = 2.0 #Time for which to keep showing calendar after movement.

    ###
    #getRelativeDay(int mv)
    #@param mv How many days forward or back from the current date
    #           to get the day of. eg. -1 = yesterday.
    #
    #This function gets a day of the month relative to the
    #current day, then returns the number as a string.
    #eg. If the current date is 21, and mv is -1, then the
    #method will return "20".
    ###
    def getRelativeDay(mv):
        global dayofmonth
        global direction
        global month
        global months

        newVal = dayofmonth + mv

        if newVal < 1:
            newVal = months[11][1] + newVal if month == 0 else months[month - 1][1] + newVal
        elif newVal > months[month][1]:
            newVal -= months[month][1]

        if newVal == 1 or newVal == 21 or newVal == 31:
            strday = str(newVal) + "st"
        elif newVal == 2 or newVal == 22:
            strday = str(newVal) + "nd"
        elif newVal == 3 or newVal == 23:
            strday = str(newVal) + "rd"
        else:
            strday = str(newVal) + "th"

        return strday

    ###
    #getRelativeWeekDay(int mv, boolean displayFullName)
    #
    #See getRelativeDay(int).
    #Does the same, except returns name of the week day
    #instead of the number of the day in the month.
    ###
    def getRelativeWeekDay(mv, displayFullName):
        global dayofweek
        global days
        global direction

        newDay = dayofweek + mv - 1

        if newDay > 6:
            while newDay > 6:
                newDay -= 7
        elif newDay < 0:
            while newDay < 0:
                newDay += 7

        return days[newDay] if displayFullName else days[newDay][0:3]

    ###
    #move(int direction)
    #@param direction Number of days forward or back to move.
    #
    #This method checks whether we're moving forward or back in
    #time (eg. yesterday or tomorrow), checks if it'll be a different
    #month, sets the dayofmonth, oldmonth, etc.
    ###
    def move(direction):
        global months
        global month
        global dayofmonth
        global oldmonth
        global oldyear
        global dayofweek
        global year

        if direction > 0:
            dayofweek += 1
            if dayofmonth < months[month][1]:
                dayofmonth += 1
            else:
                dayofmonth = 1
                oldmonth = month
                oldyear = year
                if month == 11:
                    if year:
                        year += 1
                    month = 0
                else:
                    month += 1
        else:
            dayofweek -= 1
            if dayofmonth == 1:
                oldmonth = month
                oldyear = year
                month = 11 if month == 0 else month - 1
                if oldmonth == 0:
                    dayofmonth = months[11][1]
                    year -= 1
                else:
                    dayofmonth = months[month][1]
            else:
                dayofmonth -= 1

    def showCurrentDays(direction, imgSize, posX, posY, displayFullName, startDelay=0):
        direction = 1 if direction > 0 else -1
        posX -= imgSize
        for i in xrange(-2, 6):
            relDay = "{size=28}"+getRelativeDay(i)+"{/size}"
            cDay = "{size=24}"+getRelativeWeekDay(i, displayFullName)+"{/size}"

            if startDelay > 0:
                ui.add(At('dayButton', move_left_align_wait(direction, imgSize, posX, posY, startDelay)))
                ui.add(At(Text(relDay), move_left_align_wait(direction, imgSize, posX, posY, startDelay)))
                ui.add(At(Text(cDay), move_left_align_wait(direction, imgSize, posX-3, posY-98, startDelay)))
            else:
                ui.add(At('dayButton', move_left_align(direction, imgSize, posX, posY)))
                ui.add(At(Text(relDay), move_left_align(direction, imgSize, posX, posY)))
                ui.add(At(Text(cDay), move_left_align(direction, imgSize, posX-3, posY-98)))

            posX += imgSize

transform move_left_align(direction, distance, xPos, yPos):
    yalign (yPos + 80) xcenter (xPos + 80) ycenter (yPos + 80)
    linear 1.0 xcenter (xPos + 80 - direction * distance)

transform move_left_align_wait(direction, distance, xPos, yPos, startDelay):
    yalign (yPos + 80) xcenter (xPos + 80) ycenter (yPos + 80)
    time startDelay + 1

transform fade_in(xPos, yPos): #Fade in a displayable over 1 second at xPos yPos
    alpha 0 pos (xPos, yPos)
    ease 1.0 alpha 1.0

transform fade_in_immediately(xPos, yPos): #Over 1 second, then begin to fade in a displayable over 1 second at xPos yPos
    xalign (xPos + 80) yalign (yPos + 80) xcenter (xPos + 80) ycenter (yPos + 80)

transform swipe_out(xPos, yPos):
    alpha 1.0 pos (xPos, yPos)
    easeout 1.0 alpha 0 ypos (yPos - 100)

transform swipe_in(xPos, yPos):
    alpha 0 pos (xPos, yPos - 100)
    easein 1.0 alpha 1.0 ypos yPos

###
#Image resources
###
image calendar_bg = "calendar/1280x720/bg.png" #Background image
image dayButton = "calendar/1280x720/gray.png" #Image representing each week day

label calendar(toMove):

    scene black
    show calendar_bg

    python:
        startOriginalDelay = startDelay
        startMonth = month
        
        direction = toMove
        monthPos = 65 #Y position (in px) of month label to display
        monthPosX = 1050
        month -= 1 #So users can set month as 1-12 instead of 0-11
        oldmonth = month
        oldyear = year
        newsize = 220
        scalesize = 213
        
        imgSize = newsize
        baseX = 10 #TODO: move 62px right;  478y 154h
        posY = 475
        posX = baseX

        dDir = 1 if direction > 0 else -1

    show text "{size=72}{color=#545454CC}"+str(months[month][0])+"{/color}{/size}" as new_month at Position(xpos=monthPosX, ypos=monthPos+62)
    if year:
        show text "{size=48}{color=#545454CC}[year]{/color}{/size}" as new_year at Position(xpos=monthPosX+70, ypos=monthPos)

    if startDelay != 0:
        $ showCurrentDays(direction, imgSize, posX, posY, displayFullName, startDelay)
        pause startDelay
        $ startDelay = 0

    while direction != 0:

        $ showCurrentDays(direction, imgSize, posX, posY, displayFullName, startDelay)
        $ move(dDir)

        if oldmonth != month:
            show text "{size=72}{color=#545454CC}"+str(months[oldmonth][0])+"{/color}{/size}" as old_month at swipe_out(monthPosX, monthPos+62)
            show text "{size=72}{color=#545454CC}"+str(months[month][0])+"{/color}{/size}" as new_month at swipe_in(monthPosX, monthPos+62)
            $ oldmonth = month
            if year and oldyear != year:
                show text "{size=48}{color=#545454CC}[oldyear]{/color}{/size}" as old_year at swipe_out(monthPosX+70, monthPos)
                show text "{size=48}{color=#545454CC}[year]{/color}{/size}" as new_year at swipe_in(monthPosX+70, monthPos)
                $ oldyear = year

        pause 1.0

        $ direction -= dDir

    if displayTime:
        show text "{size=48}{color=#545454CC}[displayTime]{/color}{/size}" as calendar_time at fade_in(700, monthPos + 6)
    if displayWeather:
        show text "{size=42}{color=#545454CC}[displayWeather]{/color}{/size}" as calendar_weather at fade_in(700, monthPos + 52)

    show dayButton as db_1 at fade_in_immediately(posX, posY)
    show text ("{size=28}"+getRelativeDay(-1)+"{/size}") as dr_1 at fade_in_immediately(posX, posY)
    show text ("{size=24}"+getRelativeWeekDay(-1, displayFullName)+"{/size}") as dc_1 at fade_in_immediately(posX-3, posY-98)
    $ posX += imgSize

    show dayButton as db_2 at fade_in_immediately(posX, posY)
    show text ("{size=28}"+getRelativeDay(0)+"{/size}") as dr_2 at fade_in_immediately(posX, posY)
    show text ("{size=24}"+getRelativeWeekDay(0, displayFullName)+"{/size}") as dc_2 at fade_in_immediately(posX-3, posY-98)
    $ posX += imgSize

    show dayButton as db_3 at fade_in_immediately(posX, posY)
    show text ("{size=28}"+getRelativeDay(1)+"{/size}") as dr_3 at fade_in_immediately(posX, posY)
    show text ("{size=24}"+getRelativeWeekDay(1, displayFullName)+"{/size}") as dc_3 at fade_in_immediately(posX-3, posY-98)
    $ posX += imgSize

    show dayButton as db_4 at fade_in_immediately(posX, posY)
    show text ("{size=28}"+getRelativeDay(2)+"{/size}") as dr_4 at fade_in_immediately(posX, posY)
    show text ("{size=24}"+getRelativeWeekDay(2, displayFullName)+"{/size}") as dc_4 at fade_in_immediately(posX-3, posY-98)
    $ posX += imgSize

    show dayButton as db_5 at fade_in_immediately(posX, posY)
    show text ("{size=28}"+getRelativeDay(3)+"{/size}") as dr_5 at fade_in_immediately(posX, posY)
    show text ("{size=24}"+getRelativeWeekDay(3, displayFullName)+"{/size}") as dc_5 at fade_in_immediately(posX-3, posY-98)
    $ posX += imgSize

    show dayButton as db_6 at fade_in_immediately(posX, posY)
    show text ("{size=28}"+getRelativeDay(4)+"{/size}") as dr_6 at fade_in_immediately(posX, posY)
    show text ("{size=24}"+getRelativeWeekDay(4, displayFullName)+"{/size}") as dc_6 at fade_in_immediately(posX-3, posY-98)
    $ posX += imgSize

    show dayButton as db_7 at fade_in_immediately(posX, posY)
    show text ("{size=28}"+getRelativeDay(5)+"{/size}") as dr_7 at fade_in_immediately(posX, posY)
    show text ("{size=24}"+getRelativeWeekDay(5, displayFullName)+"{/size}") as dc_7 at fade_in_immediately(posX-3, posY-98)

    pause intDelay
    scene black with dissolve

    python:
     startDelay = startOriginalDelay
     month = startMonth

    return