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
    year = False #Set to either false or a numeric value. eg. 2012.
    #If not False, the year will be displayed below the current month.
    #The year will also increment/decrement accordingly.

    ###
    #Boolean variables
    #
    #nextMonth should NOT be modified manually.
    #The others can all be set manually.
    ###
    nextMonth = False #True when we're about to change months.
    displayFullName = True #If True, display the full name of a week day
    #rather than the abbreviation.
    #eg. Tuesday rather than Tue
    displayTime = "9:00 PM" #If False, don't display. Otherwise display value.
    displayWeather = "Sunny" #If False, don't display. Otherwise display value.

    ###
    #Size Variables
    #
    #This shouldn't be changed. It currently maps to the renpy size setting.
    ###
    size = (config.screen_width, config.screen_height)

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
    #Image resources
    #
    #Both of these values can be changed
    ###

    dayButton = str(size[0])+"x"+str(size[1])+"/gray.png"
    dayFrame = str(size[0])+"x"+str(size[1])+"/onyx.png"

    ###
    #getRelativeDay(int mv, boolean boolStart)
    #@param mv How many days forward or back from the current date
    #           to get the day of. eg. -1 = yesterday.
    #@param boolStart True if being run for the first time.
    #           Not tested if necessary outside of pygame.
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
            start = dayofmonth
        else:
            start = dayofmonth - 1 if direction > 0 else dayofmonth + 1
        newVal = start + mv

        if newVal < 1:
            newVal = months[11][1] + newVal if month == 0 else months[month - 1][1] + newVal
        elif newVal > months[month][1]:
            newVal -= months[month][1]

        return newVal

    ###
    #getRelativeWeekDay(int mv)
    #
    #See getRelativeDay(int, boolean).
    #Does the same, except returns name of the week day
    #instead of the number of the day in the month.
    ###
    def getRelativeWeekDay(mv, boolStart):
        global dayofweek
        global days
        global direction
        
        if boolStart:
            newDay = dayofweek + mv -1
        else:
            newDay = dayofweek + mv - (2 if direction > 0 else 0)

        if newDay > 6:
            while newDay > 6:
                newDay -= 7
        elif newDay < 0:
            while newDay < 0:
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
        global year

        nextMonth = False
        curmove = 0
        
        if direction > 0:
            dayofweek += 1
            if dayofmonth < months[month][1] - 1:
                dayofmonth += 1
            else:
                dayofmonth = 0
                nextMonth = True
                oldmonth = month
                if month == 11:
                    if year:
                        year += 1
                    month = 0
                else:
                    month += 1
        else:
            dayofweek -= 1
            if dayofmonth == 0:
                nextMonth = True
                oldmonth = month
                month = 11 if month == 0 else month - 1
                if oldmonth == 0:
                    dayofmonth = months[11][1]
                    year -= 1
                else:
                    dayofmonth = months[month][1]
            
            dayofmonth -= 1

    def displayDays(posX, posY, scalesize, imgSize, size, monthPos, months, month, boolStart, boolEnd=False):
        global dayButton
        global dayFrame
        global dayofmonth
        global year
        global nextMonth
        global oldmonth

        if boolStart:
            dayofmonth -= 1

        wScale = 1
        if config.screen_width != 800:
            wScale = float(config.screen_width) / float(800)
        #if config.screen_height != 600:
        #    pass
        if nextMonth:
            curX = ((imgSize + (baseX - posX if direction < 0 else posX - baseX))) / 5 - 15
            print "curX", str(curX)
            cmonth = oldmonth if curX > 0 else month
            curX = math.fabs(curX)
            if curX > 15:
                curX = 15
            curX = "%x" % curX
            ui.text("{color=#fff"+curX+"}"+months[cmonth][0]+"{/color}", xpos=50, ypos=monthPos, size=math.floor(42*wScale))
        else:
            ui.text(months[month][0], xpos=50, ypos=monthPos, size=math.floor(42*wScale))
        if year:
            ui.text(str(year), xpos=50, ypos=(monthPos + 42 * wScale), size=math.floor(36*wScale))
        if boolEnd:
            if displayTime:
                ui.text(displayTime, xpos=(size[0] - imgSize*wScale), ypos=(monthPos + 6 * wScale), size=math.floor(36*wScale))
            if displayWeather:
                ui.text(displayWeather, xpos=(size[0] - imgSize*wScale), ypos=(monthPos + 42 * wScale), size=math.floor(24*wScale))
        elif math.fabs(direction) == 1:
            curX = (150 - (imgSize + (baseX - posX if direction == -1 else posX - baseX))) / 10
            if curX > 15:
                curX = 15
            curX = "%x" % curX
            if displayTime:
                ui.text("{color=#fff"+curX+"}"+displayTime+"{/color}", xpos=(size[0] - imgSize*wScale), ypos=(monthPos + 6 * wScale), size=math.floor(36*wScale))
            if displayWeather:
                ui.text("{color=#fff"+curX+"}"+displayWeather+"{/color}", xpos=(size[0] - imgSize*wScale), ypos=(monthPos + 42 * wScale), size=math.floor(24*wScale))
        for i in xrange(-3, 7): #Display 7 days, starting 3 days ago
            relDay = getRelativeDay(i, boolStart)
            fWidth = 7 if relDay < 10 else 3
            nxPos = (int)(posX + (scalesize / 3) + math.floor(wScale * fWidth))
            nyPos = (int)(posY + (scalesize / 3))
            ui.image(dayButton, xpos=posX, ypos=posY)
            ui.text(str(relDay), xpos=nxPos, ypos=nyPos, size=math.floor(28*wScale))
            nxPos -= (int)(wScale * 40)
            nyPos -= (int)(wScale * 60)
            cDay = getRelativeWeekDay(i, boolStart)
            ui.text(cDay[0 if displayFullName else 1], xpos=nxPos, ypos=nyPos, size=math.floor(wScale * 18))
            posX += imgSize
        framepos = (size[0] / 2 - imgSize / 2 - imgSize / 25, posY - 3)
        ui.image(dayFrame, xpos=framepos[0], ypos=framepos[1])

###
#Background Image
###
#image bg Calendar = "bg/Personal/HomeStreet_01.png"
image bg Calendar = str(size[0])+"x"+str(size[1])+"/HomeStreet_01.png"

label calendar:

    $ hide_window() #Hide the text window. There's no point having it here.
    scene bg Calendar

    python:
        size = (config.screen_width, config.screen_height)
        monthPos = 25 #Y position (in px) of month label to display
        month -= 1 #So users can set month as 1-12 instead of 0-11
        oldmonth = month
        newsize = size[1] / 4 #One quarter of window width
        scalesize = int(math.floor(newsize * 2 / 3)) #One sixth of window width
        
        imgSize = newsize
        baseX = size[0] / 2 - 9 * imgSize / 2
        posX = baseX
        posY = size[1] / 2 - 96 / 2

        displayDays(posX, posY, scalesize, imgSize, size, monthPos, months, month, True)

    if direction == 0: 
        #If we aren't moving forward or back, 
        #just show the calendar for intDelay seconds
        pause(intDelay)
        scene black with dissolve
        python:
            renpy.jump(label_cont)

    python:
        move(direction)

        curmove = 0
        moved = 0
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

            posX = baseX - curmove

            displayDays(posX, posY, scalesize, imgSize, size, monthPos, months, month, False)

            if lastMove:
                lastMove = False
                if not math.fabs(curmove) >= imgSize * math.fabs(direction):
                    direction = direction - 1 if direction > 0 else direction + 1
                    move(direction)
                else:
                    done = True

            renpy.pause(1/60)

        #Finished looping. Display end result for intDelay seconds.
        displayDays(posX, posY, scalesize, imgSize, size, monthPos, months, month, False, boolEnd=True)

        renpy.pause(intDelay)

    scene black with dissolve
    python:
        renpy.jump(label_cont)