from World import *
from System import Array

class Scheduler(object):

     def __init__(self):
         self.events = []
         self.world = None
         self.dayLimit = 4
         self.restrictionLevel = 0
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
         self.events.Clear()
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

             elif (condition.name == 'selection'):
                 if condition.value != self.world.selection.value:
                     return False
                     pass
                 
             elif (condition.name == 'holding'):
                 if condition.value != self.world.holding.value:
                     return False
                     pass

             elif (condition.name == 'suitableSlot'):
                 if condition.value != self.world.suitableSlot.value:
                     return False
                     pass

             elif (condition.name == 'suitableDay'):
                 if condition.value != self.world.meetsDayConstraints.value:
                     return False
                     pass

             elif (condition.name == 'lowerRatio' and self.restrictionLevel == 0):
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
         # retrieve occupied ratio for current day
         dayOR = self.world.dayORs[self.world.day]

         # check if the occupied ratio is above or below the average
         if (dayOR > self.world.occupiedRatio.value):
             self.world.lowerRatio.value = 'or'
         else:
             self.world.lowerRatio.value = 'dx'
         
         self.world.meetsDayConstraints.value = self.CheckDayConstraints(self.world.eventHeld)
         self.world.occupiedSlot.value = None
     
     def Pass(self):
         # move to next day
         self.world.day = self.world.day + 1
         # check if the week limit has been reached
         if (self.world.day == self.dayLimit) :
             self.world.at.value = 'dn'

         # reset lower ratio tracker
         self.world.lowerRatio.value = 'none'
         self.world.meetsDayConstraints.value = None

     def FirstSlot(self):
         # reset selected time slot
         self.world.slot = 0
         
         if (self.world.scheduleSlots[self.world.day, self.world.slot] == 't'):
             self.world.occupiedSlot.value = False
             #self.world.higherPriority.value = 'eH'
             
         elif 'et' in self.world.scheduleSlots[self.world.day, self.world.slot]:
             #self.world.higherPriority.value = 'et'
             self.world.occupiedSlot.value = True
         else:
             self.world.occupiedSlot.value = True

         # check constraints
         self.world.meetsTimeConstraints.value = self.CheckTimeConstraints(self.world.eventHeld)

         # set suitability based on other predicates
         if (self.world.occupiedSlot.value == False and self.world.meetsTimeConstraints.value == True):
             self.world.suitableSlot.value = True
         else:
             self.world.suitableSlot.value = False

         self.world.selection.value = 'tx'

     def NextSlot(self):
         if self.world.slot < 6:
            self.world.slot = self.world.slot + 1

            if (self.world.scheduleSlots[self.world.day, self.world.slot] == 't'):
                self.world.occupiedSlot.value = False
                #self.world.higherPriority.value = 'eH'
             
            elif 'et' in self.world.scheduleSlots[self.world.day, self.world.slot]:
                #self.world.higherPriority.value = 'et'
                self.world.occupiedSlot.value = True

         else:
            self.world.slot = 0
            self.world.day = self.world.day + 1
            if (self.world.day == self.dayLimit) :
                self.world.at.value = 'dn'
            self.occupiedSlot = None
            self.world.selection.value = 't0'
         
         # check constraints
         self.world.meetsTimeConstraints.value = self.CheckTimeConstraints(self.world.eventHeld)

         # set suitability based on other predicates
         if (self.world.occupiedSlot.value == False and self.world.meetsTimeConstraints.value == True):
             self.world.suitableSlot.value = True
         else:
             self.world.suitableSlot.value = False
         
     
     def ReplaceEvent(self):
         # store event temporarily
         eventTemp = self.world.scheduleSlots[self.world.day, self.world.slot]
         # set slot as holding event/swap placed flag
         self.world.scheduleSlots[self.world.day, self.world.slot] = self.world.eventHeld.code
         self.getEvent(self.world.eventHeld.code).placed = False
         # set holding as event that was in slot/swap placed flag
         self.world.eventHeld = self.getEvent(eventTemp)
         self.getEvent(self.world.eventHeld.code).placed = True
         # reset selection to analyse day
         self.world.selection.value = 't0'
         self.world.slot = 0
         self.world.suitableSlot.value = None
     
     def AddEvent(self):
         # add event to slot
         self.world.scheduleSlots[self.world.day, self.world.slot] = self.world.eventHeld.code
         # adjust dayOR
         self.world.dayORs[self.world.day] = self.world.calculateDayOR(self.world.day)
         # adjust or
         self.world.calculateOR()
         # set placed flag
         self.getEvent(self.world.eventHeld.code).placed = True
         # set slot as occupied
         #self.world.occupiedSlot.value = True
         # set next event as held
         self.world.setEventHeld()
         # reset selection to analyse day
         self.world.selection.value = 't0'
         self.world.slot = 0
         self.world.suitableSlot.value = None
         self.world.meetsDayConstraints.value = None

     def CycleEvent(self):
         # reset at to not be at maximum
         self.world.at.value = 'dx'
         # increase cycle number
         self.world.cycle.value = self.world.cycle.value + 1
         # change index for next event
         if (self.world.eventIndex + 1 == len(self.world.events)):
            self.world.eventIndex = 0
            self.restrictionLevel = self.restrictionLevel + 1
         else:
            self.world.eventIndex = self.world.eventIndex + 1
         # cycle the event held
         self.world.eventHeld = self.world.events[self.world.eventIndex]
         # move to start of week
         self.world.day = 0


     def CheckConstraints(self):
         # set event
         event = self.world.eventHeld
         
         # check if in correct day
         if CheckDayConstraints(event) == False:
             return False

         # check if in correct time period
         if CheckTimeConstraints(event) == False:
             return False
            
         return True

     def CheckDayConstraints(self, event):
         found = False
         for day in event.days:
             if day == self.world.getDayFromIndex(self.world.day):
                 found = True
                 break
         
         return found

     def CheckTimeConstraints(self, event):
         if event.time == 'any':
             pass
         elif event.time != self.world.getTimePeriod():
             return False
        
         return True


class Event(object):

    def __init__(self, name, code, days, time):
        self.name = name
        self.code = code
        self.days = days
        self.time = time
        self.holding = False
        self.placed = False