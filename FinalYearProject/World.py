from System import Array

class World(object):
    
    def __init__(self, events, timetable):
         # initialise predicates
         self.holding = Predicate('holding', 'eH')
         self.lowerRatio = Predicate('lowerRatio', 'none')
         self.occupiedRatio = Predicate('occupiedRatio', 0.0)
         self.higherPriority = Predicate('higherPriority', 'et')
         self.meetsDayConstraints = Predicate('meetsDayConstraints', None)
         self.meetsTimeConstraints = Predicate('meetsTimeConstraints', None)
         self.suitableSlot = Predicate('suitableSlot', None)
         self.occupiedSlot = Predicate('occupiedSlot', None)
         self.at = Predicate('at', 'dx')
         self.cycle = Predicate('cycle', 1)
         self.selection = Predicate('selection', 't0')
        
         # initiate variables
         self.events = events           # set of events
         self.eventIndex = 0                
         self.eventHeld = self.events[self.eventIndex]
         
         self.eventMax = len(events)
         self.day = 0
         self.slot = 0
         self.dayORs = Array.CreateInstance(float, 5)
         self.scheduleSlots = [[],[]]       # tx - open time slots # ttx - timetable slots # etx - event time slots


         # initial state
         self.setInitialState(timetable)

         # goal state
         self.goalAchieved = False
         pass

    def setInitialState(self, timetable):
        rows = timetable.GetLength(0)
        columns = timetable.GetLength(1)

        self.scheduleSlots = Array.CreateInstance(str, rows, columns)

        for x in range(rows):
            for y in range(columns):
                if (timetable[x,y] != None):     #'tt' in timetable[x,y]
                    self.scheduleSlots[x,y] = timetable[x,y]
                else:
                    self.scheduleSlots[x,y] = 't'
                
            self.dayORs[x] = self.calculateDayOR(x)

        self.calculateOR()

        actionPass = Action('pass', 0, [Predicate('at', 'dx'), Predicate('suitableDay', False)], [Predicate('at', 'dx+1'), Predicate('holding', 'eH')])
        actionFirstSlot = Action('firstSlot', 1, [Predicate('holding', 'eH'), Predicate('suitableDay', True), Predicate('occupiedSlot', None)], [Predicate('lowerRatio', '')])
        actionNextSlot = Action('nextSlot', 2, [Predicate('holding', 'eH'), Predicate('suitableSlot', False), Predicate('higherPriority', 'et'), Predicate('selection', 'tx')], [Predicate('lowerRatio', '')])
        actionReplaceEvent = Action('replaceEvent', 3, [Predicate('occupiedSlot', True), Predicate('higherPriority', 'eH'), Predicate('suitableSlot', True)], [Predicate('holding', 'et')])
        actionAddEvent = Action('addEvent', 4, [Predicate('occupiedSlot', False), Predicate('suitableSlot', True)], [Predicate('available', False)])
        actionCycleEvent = Action('cycleEvent', 5, [Predicate('at', 'dn'), Predicate('holding', 'eH'), Predicate('suitableDay', False)], [Predicate('holding', 'ex+1'), Predicate('cycle', 1)])
        actionAnalyseOptions = Action('analyseOptions', 6, [Predicate('suitableDay', None), Predicate('holding', 'eH'), Predicate('selection', 't0')], [Predicate('LowerRatio', 'or')])

        self.actions = [actionPass, actionFirstSlot, actionNextSlot, actionReplaceEvent, actionAddEvent, actionCycleEvent, actionAnalyseOptions]

    def calculateOR(self):
        total = 0.0;
        for i in range(len(self.dayORs)):
            print('cycle day ' + str(i) + ': ' + str(self.dayORs[i]))
            total = total + self.dayORs[i]
            
        self.occupiedRatio.value = total / len(self.dayORs)
        print('or: ' + str(self.occupiedRatio.value))
        
    def calculateDayOR(self, dayNum):
        occupiedCount = 0.0
        freeCount = 0.0
        dayOR = 0.0

        for y in range(self.scheduleSlots.GetLength(1)):
            if (self.scheduleSlots[dayNum, y] == 't'):
                freeCount = freeCount + 1
            else:
                occupiedCount = occupiedCount + 1

        dayOR = occupiedCount / (freeCount + occupiedCount)

        print('day ' + str(dayNum) + ': ' + str(dayOR))

        return dayOR

    def setEventHeld(self):
        self.holding.value = 'none'
        startingIndex = self.eventIndex
        self.eventIndex = self.eventIndex + 1
        while (self.eventIndex != startingIndex):
            if (self.eventIndex >= self.eventMax):
                self.eventIndex = 0
            else:
                if (self.events[self.eventIndex].placed == False):
                    self.eventHeld = self.events[self.eventIndex]
                    self.holding.value = 'eH'
                    print(str(self.eventHeld.name) + " held")
                    break
                else:
                    self.eventIndex = self.eventIndex + 1

        if (startingIndex == self.eventIndex) :
             self.holding.value = 'eH'

    def getDayFromIndex(self, day):
        # switch statement for day index
         switcher = {
         0: 'monday',
         1: 'tuesday',
         2: 'wednesday',
         3: 'thursday',
         4: 'friday',
     }
         dayName = switcher.get(day, lambda: "nothing")
         return dayName

    def getTimePeriod(self):
        if self.slot < 3:
            return 'Morning'
        elif self.slot >= 4:
            return 'Afternoon'



class Action(object):

    def __init__(self, name, index, preconditions, effects):
        self.name = name
        self.index = index
        self.preconditions = preconditions
        self.effects = effects
        pass

class Predicate(object):

    def __init__(self, name, value):
        self.name = name
        self.value = value