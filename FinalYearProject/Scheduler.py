from World import *
from System import Array

class Scheduler(object):

     def __init__(self):
         self.events = []
         self.world = None
         self.dayLimit = 4
         pass

     def GenerateSchedule(self):
         self.world = World(self.events, self.timetable)
                 

         while self.world.goalAchieved == False:
             
             for action in self.world.actions:
                 if (self.actionApplicable(action)):
                     self.executeAction(action.index)
                     print(action.name)
                     if self.checkState():
                        self.world.goalAchieved = True
                     break


         return self.world.scheduleSlots

     def setEvents(self, newEvents):
         self.events.extend(newEvents)
         
         #for i in range(len(newEvents)):
             
         #    self.events[i] = newEvents[i]
             

     def setTimetable(self, newTimetable):
         
         self.timetable = Array.CreateInstance(str,newTimetable.GetLength(0),newTimetable.GetLength(1))
         
         for x in range(newTimetable.GetLength(0)):
             for y in range(newTimetable.GetLength(1)):
                if (newTimetable[x,y] != None):         # 'tt' in newTimetable[x,y]
                    self.timetable[x,y] = newTimetable[x,y]

     def checkState(self):
         for event in self.world.events:
             if event.placed == False:
                 return False
             
         return True

     def getEvent(self, code):
         for event in self.world.events:
             if event.code == code:
                 return event

     def actionApplicable(self, action):
         for condition in action.preconditions:
             if (condition.name == 'at'):
                 if condition.value != self.world.at.value:
                     return False
                     pass
                 
             elif (condition.name == 'holding'):
                 if condition.value != self.world.holding.value:
                     return False
                     pass

             elif (condition.name == 'meetsConstraints'):
                 if condition.value != self.world.contraints.value:
                     return False
                     pass

             elif (condition.name == 'lowerRatio'):
                 if condition.value != self.world.lowerRatio.value:
                     return False
                     pass

             elif (condition.name == 'occupiedSlot'):
                 if condition.value != self.world.occupiedSlot.value:
                     return False
                     pass

             elif (condition.name == 'higherPriority'):
                 if condition.value != self.world.higherPriority.value:
                     return False
                     pass

             elif (condition.name == 'cycle'):
                 if condition.value != self.world.cycle.value:
                     return False
                     pass

             pass
         
         return True
         

     def executeAction(self, action):
         # switch statement for correct action
         switcher = {
         0: self.Pass,
         1: self.FirstSlot,
         2: self.NextSlot,
         3: self.ReplaceEvent,
         4: self.AddEvent,
         5: self.CycleEvent,
         6: self.AnalyseOptions,
     }
         func = switcher.get(action, lambda: "nothing")
         return func()
         pass

# actions
     def AnalyseOptions(self):
         dayOR = self.world.dayORs[self.world.day]

         if (dayOR > self.world.occupiedRatio.value):
             self.world.lowerRatio.value = 'or'
         else:
             self.world.lowerRatio.value = 'dx'
         
     
     def Pass(self):
         self.world.day = self.world.day + 1
         if (self.world.day == self.dayLimit) :
             self.world.at.value = 'dn'

     def FirstSlot(self):
         self.world.selection.value = 0
         
         if (self.world.scheduleSlots[self.world.day, self.world.selection.value] == 't'):
             self.world.occupiedSlot.value = False
             self.world.higherPriority.value = 'eH'
             
         elif 'et' in self.world.scheduleSlots[self.world.day, self.world.selection.value]:
             self.world.higherPriority.value = 'et'
             self.world.occupiedSlot.value = True
         else:
             self.world.occupiedSlot.value = True

     def NextSlot(self):
         if self.world.selection.value < 7:
            self.world.selection.value = self.world.selection.value + 1

            if (self.world.scheduleSlots[self.world.day, self.world.selection.value] == 't'):
                self.world.occupiedSlot.value = False
                self.world.higherPriority.value = 'eH'
             
            elif 'et' in self.world.scheduleSlots[self.world.day, self.world.selection.value]:
                self.world.higherPriority.value = 'et'
                self.world.occupiedSlot.value = True

         else:
            self.world.selection.value = -1
            self.world.day = self.world.day + 1
            self.occupiedSlot = None
         
         
     
     def ReplaceEvent(self):
         # store event temporarily
         eventTemp = self.world.scheduleSlots[self.world.day, self.world.selection.value]
         # set slot as holding event/swap placed flag
         self.world.scheduleSlots[self.world.at.value, self.world.selection.value] = self.world.eventHeld.code
         self.getEvent(self.world.eventHeld.code).placed = False
         # set holding as event that was in slot/swap placed flag
         world.eventHeld.value = eventTemp
         self.getEvent(self.world.eventHeld.code).placed = True
     
     def AddEvent(self):
         # add event to slot
         self.world.scheduleSlots[self.world.day, self.world.selection.value] = self.world.eventHeld.code
         # adjust dayOR
         self.world.dayORs[self.world.day] = self.world.calculateDayOR(self.world.day)
         # adjust or
         self.world.calculateOR()
         # set placed flag
         self.getEvent(self.world.eventHeld.code).placed = True

     def CycleEvent(self):
         self.world.cycle.value = self.world.cycle.value + 1

class Event(object):

    def __init__(self, name, code):
        self.name = name
        self.code = code
        self.holding = False
        self.placed = False