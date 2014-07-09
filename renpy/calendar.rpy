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
#  direction
#  label_cont
#
#The first three variables specify the day of the week (eg. Sunday),
#the day of the month (eg. the 1st) and the current month (eg. January).
#
#direction specifies the number of days forward or backward you want
#to move. eg. A direction of 1 = move to the next day, a direction of -1
#goes to the previous day, a direction of 7 will go forward one week, etc.
#
#label_cont specifies the label you want to move to after showing the
#day transition. eg. If I set label_cont to "chapter_01", I would move to
#that label after the transition ended.
#
#There are several other settings you can tweak as well. For example,
#the default resolution is 800x600; if you want to change that, override
#the size variable.
#Another example is the intDelay variable. This determines how long in
#seconds the calendar will display for after finishing the animation.
#
#After you've overridden the desired variables, and set the time, label &
#direction, you're ready to show the calendar. Simply use the jump command
#to jump to the calendar label. The animation will run, it will wait intDelay
#seconds, then jump to the label_cont label.
#
#A full example of the calendar being used is shown below.
#This entails a very basic script.rpy file.
#We start at the start label, set the date to Monday January 1st,
#set direction and label_cont. We then jump to calendar, which
#moves us forward 2 days to Wednesday January 3rd, which then
#jumps to chapter_01 and displays a message before ending.
#
#label start:
#    $ dayofweek = 1
#    $ dayofmonth = 1
#    $ month = 1
#    $ direction = 2
#    $ label_cont = "chapter_01"
#    jump calendar
#
#label chapter_01
#    "The day transition has just ended."
#
########

init python:

    import math

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
        ["Sunday", "Sun", 0],
        ["Monday", "Mon", 1],
        ["Tuesday", "Tue", 2],
        ["Wednesday", "Wed", 3],
        ["Thursday", "Thu", 4],
        ["Friday", "Fri", 5],
        ["Saturday", "Sat", 6]
    ]

    dayofmonth = 20 #01-31
    #Set this to the current date if you're just showing the date,
    #or the starting date if you're showing a time lapse.
    dayofweek = 0 #Keeps track of Sun-Sat. 0 = Sunday, 6 = Saturday.
    month = 8 #Current month. 1 = January, 12 = December
    oldmonth = 8 #Previous month.
    #Only useful when going from one month to the next.

    ###
    #Boolean variables
    #
    #None of these should be edited manually.
    ###
    nextMonth = False #True when we're about to change months.

    ###
    #Size Variables
    ###
    size = (800, 600)

    ###
    #Movement Variables
    #
    #Only direction should be edited manually.
    ###

    curmove = 0 #Used to keep track of movement.
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

    startDelay = 2.0 #Time to wait before beginning the animation.
    intDelay = 1.5 #Time to keep showing calendar for after movement

    ###
    #getRelativeDay(int mv, boolean boolStart)
    #@param mv How many days forward or back from the current date
    #			to get the day of. eg. -1 = yesterday.
    #@param boolStart True if being run for the first time.
    #			Not tested if necessary outside of pygame.
    #
    #This function gets a day of the month relative to the
    #current day, then returns the number as a string.
    #eg. If the current date is 21, and mv is -1, then the
    #method will return "20".
    ###
    def getRelativeDay(mv, boolStart):
        global dayofmonth
        global direction
        global month
        global months

        if boolStart:
            start = dayofmonth - 1
        else:
            start = dayofmonth - 2 if direction > 0 else dayofmonth
        newVal = start + mv
        if newVal < 1:
            newVal = months[11][1] + newVal if month == 0 else months[month - 1][1] + newVal
        elif newVal > months[month][1]:
            newVal -= months[month][1]

        return str(newVal)

    ###
    #getRelativeWeekDay(int mv)
    #
    #See getRelativeDay(int, boolean).
    #Does the same, except returns name of the week day
    #instead of the number of the day in the month.
    ###
    def getRelativeWeekDay(mv):
        global dayofweek
        global days

        newDay = dayofweek + mv

        if newDay > 6:
            newDay -= 7
        elif newDay < 0:
            newDay += 7

        return days[newDay]

    ###
    #move(int direction)
    #@param direction Number of days forward or back to move.
    #
    #This method checks whether we're moving forward or back in
    #time (eg. yesterday or tomorrow), checks if it'll be a different
    #month, sets the dayofmonth, oldmonth, etc.
    ###
    def move(direction):
        global curmove
        global months
        global month
        global dayofmonth
        global nextMonth
        global oldmonth
        global dayofweek

        curmove = 0
        if direction > 0:
            dayofweek += 1
            if dayofmonth < months[month][1]:
                dayofmonth += 1
            else:
                dayofmonth = 1
                nextMonth = True
                oldmonth = month
                month = 0 if month == 11 else month + 1
        else:
            dayofweek -= 1
            if dayofmonth == 1:
                nextMonth = True
                oldmonth = month
                month = 11 if month == 0 else month - 1
                dayofmonth = months[11][1] if oldmonth == 0 else months[month][1]
            else:
                dayofmonth -= 1

###
#Background Image
###
image bg Calendar = "HomeStreet_01.png"

label calendar:

    $ hide_window() #Hide the text window. There's no point having it here.
    scene bg Calendar

    python:
        size = (config.screen_width, config.screen_height)
        monthPos = 25 #Y position (in px) of month label to display
        month -= 1 #So users can set month as 1-12 instead of 0-11
        newsize = size[1] / 4 #One quarter of window width
        scalesize = int(math.floor(newsize * 2 / 3)) #One sixth of window width
        
        imgSize = newsize
        baseX = size[0] / 2 - 9 * imgSize / 2
        posX = baseX
        posY = size[1] / 2 - 96 / 2

        ui.text(months[month][0], xpos=50, ypos=monthPos, size=42)

        for i in xrange(-3, 7): #Display 7 days, starting 3 days ago
            nxPos = posX + (scalesize / 3)
            nyPos = posY + (scalesize / 3)
            ui.image("gray.png", xpos=posX, ypos=posY)
            ui.text(getRelativeDay(i, True), xpos=nxPos, ypos=nyPos, size=28)
            nxPos -= 40
            nyPos -= 60
            cDay = getRelativeWeekDay(i)
            ui.text(cDay[1], xpos=nxPos, ypos=nyPos, size=18)
            posX += imgSize
        framepos = (size[0] / 2 - imgSize / 2 - imgSize / 25, posY - 3)
        ui.image("onyx.png", xpos=framepos[0], ypos=framepos[1])

    if direction == 0: 
        #If we aren't moving forward or back, 
        #just show the calendar for intDelay seconds
        pause(intDelay)
        scene black with dissolve
        python:
            renpy.jump(label_cont)

    python:
        oldmonth = month
        move(direction)

        if direction > 0:
            if dayofmonth < months[month][1]:
                dayofmonth += 1
            else:
                dayofmonth = 1
                nextMonth = True
                oldmonth = month
                month = 0 if month == 1 else month + 1
        else:
            if dayofmonth == 1:
                nextMonth = True
                oldmonth = month
                month = 11 if month == 0 else month - 1
                dayofmonth = months[11][1] if oldmonth == 0 else months[month][1]
            else:
                dayofmonth -= 1

        curmove = 0
        moved = 0
        monthHalf = False
        speed = imgSize / 30
        curmonth = months[month][0]
        lastMove = False

        renpy.pause(startDelay)

        done = False
        while not done:
            curmove += speed * direction
            if math.fabs(curmove) >= imgSize:
                lastMove = True
            #TODO: add animation?
            month = oldmonth if not monthHalf else month
            ui.text(months[month][0], xpos=50, ypos=monthPos, size=42)

            posX = baseX - curmove

            for i in xrange(-3, 7):
                nxPos = posX + (scalesize / 3)
                nyPos = posY + (scalesize / 3)
                ui.image("gray.png", xpos=posX, ypos=posY)
                ui.text(getRelativeDay(i, True), xpos=nxPos, ypos=nyPos, size=24)
                nxPos -= 40
                nyPos -= 60
                cDay = getRelativeWeekDay(i)
                ui.text(cDay[1], xpos=nxPos, ypos=nyPos, size=18)
                posX += imgSize
            #screen.blit(frame, framepos)
            framepos = (size[0] / 2 - imgSize / 2 - imgSize / 25, posY - 3)
            ui.image("onyx.png", xpos=framepos[0], ypos=framepos[1])
            if lastMove:
                lastMove = False
                if not math.fabs(curmove) >= imgSize * math.fabs(direction):
                    direction = direction - 1 if direction > 0 else direction + 1
                    move(direction)
                else:
                    done = True
                if nextMonth:
                    monthHalf = False
                    nextMonth = False
                    oldmonth = month

            renpy.pause(0.01)
            #1/100 of a second. Emulating 100hz refresh rate animation

        #Finished looping. Display end result for intDelay seconds.
        ui.text(months[month][0], xpos=50, ypos=monthPos, size=42)
        posX = baseX - curmove
        for i in xrange(-3, 7):
            nxPos = posX + (scalesize / 3)
            nyPos = posY + (scalesize / 3)
            ui.image("gray.png", xpos=posX, ypos=posY)
            ui.text(getRelativeDay(i, True), xpos=nxPos, ypos=nyPos, size=24)
            nxPos -= 40
            nyPos -= 60
            cDay = getRelativeWeekDay(i)
            ui.text(cDay[1], xpos=nxPos, ypos=nyPos, size=18)
            posX += imgSize
        framepos = (size[0] / 2 - imgSize / 2 - imgSize / 25, posY - 3)
        ui.image("onyx.png", xpos=framepos[0], ypos=framepos[1])

        renpy.pause(intDelay)

    scene black with dissolve
    python:
        renpy.jump(label_cont)