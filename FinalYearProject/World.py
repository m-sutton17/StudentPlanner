from System import Array

class World(object):
    
    def __init__(self, events, timetable):
         # initialise predicates
         self.holding = Predicate('holding', 'eH')
         self.lowerRatio = Predicate('lowerRatio', 'none')
         self.occupiedRatio = Predicate('occupiedRatio', 0.0)
         self.higherPriority = Predicate('higherPriority', 'eH')
         self.meetsContraints = Predicate('meetsContraints', 'none')
         self.occupiedSlot = Predicate('occupiedSlot', None)
         self.at = Predicate('at', 'dx')
         self.cycle = Predicate('cycle', 1)
         self.selection = Predicate('selection', 0)
        
         self.events = events                # set of events
         self.eventHeld = self.events[0]
         self.eventIndex = 0
         self.eventMax = len(events)
         self.day = 0
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

        actionPass = Action('pass', 0, [Predicate('at', 'dx'), Predicate('lowerRatio', 'or')], [Predicate('at', 'dx+1'), Predicate('holding', 'eH')])
        actionFirstSlot = Action('firstSlot', 1, [Predicate('holding', 'eH'), Predicate('lowerRatio', 'dx'), Predicate('occupiedSlot', None)], [Predicate('lowerRatio', '')])
        actionNextSlot = Action('nextSlot', 2, [Predicate('holding', 'eH'), Predicate('occupiedSlot', True), Predicate('higherPriority', 'et')], [Predicate('lowerRatio', '')])
        actionReplaceEvent = Action('replaceEvent', 3, [Predicate('occupiedSlot', True), Predicate('higherPriority', 'eH')], [Predicate('holding', 'et')])
        actionAddEvent = Action('addEvent', 4, [Predicate('occupiedSlot', False), Predicate('higherPriority', 'eH')], [Predicate('available', False)])
        actionCycleEvent = Action('cycleEvent', 5, [Predicate('at', 'dn'), Predicate('holding', 'eH')], [Predicate('holding', 'ex+1'), Predicate('cycle', 1)])
        actionAnalyseOptions = Action('analyseOptions', 6, [Predicate('at', 'dx'), Predicate('holding', 'eH'), Predicate('selection', -1)], [Predicate('LowerRatio', 'or')])

        self.actions = [actionPass, actionFirstSlot, actionNextSlot, actionReplaceEvent, actionAddEvent, actionCycleEvent, actionAnalyseOptions]

    def calculateOR(self):
        total = 0.0;
        for i in range(len(self.dayORs)):
            print(self.dayORs[i])
            total = total + self.dayORs[i]
            
        self.occupiedRatio.value = total / len(self.dayORs)
        print(self.occupiedRatio.value)
        
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

        print(dayOR)

        return dayOR



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