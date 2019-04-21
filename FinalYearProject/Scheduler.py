from World import *
from System import Array

class Scheduler(object):

     def __init__(self):
         self.events = []
         self.world = None
         self.dayLimit = 4
         self.restrictionLevel = 0

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
            
            # check constraints
            self.world.meetsTimeConstraints.value = self.CheckTimeConstraints(self.world.eventHeld)

            # set suitability based on other predicates
            if (self.world.occupiedSlot.value == False and self.world.meetsTimeConstraints.value == True):
                self.world.suitableSlot.value = True
            else:
                self.world.suitableSlot.value = False

         else:
            # reset values to reflect next day
            self.world.slot = 0
            self.world.day = self.world.day + 1
            if (self.world.day == self.dayLimit) :
                self.world.at.value = 'dn'
            self.world.occupiedSlot.value = None
            self.world.selection.value = 't0'
            self.world.meetsTimeConstraints.value = None
            self.world.suitableSlot.value = None
            self.world.meetsDayConstraints.value = None
         
     
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
         print(str(self.world.eventHeld.name) + " added")
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
         # alter restriction level if appropriate
         if (self.world.cycle.value == len(self.world.events) * 2):
             print("restriction lowered")
             self.restrictionLevel = self.restrictionLevel + 1
         # change index for next event
         #if (self.world.eventIndex + 1 == len(self.world.events) * 2):
         #   self.world.eventIndex = 0
         #   self.restrictionLevel = self.restrictionLevel + 1
         #else:
         #   self.world.eventIndex = self.world.eventIndex + 1
         # cycle the event held
         self.world.setEventHeld()
         # move to start of week
         self.world.day = 0
         self.world.selection.value = 't0'
         self.world.slot = 0
         self.world.suitableSlot.value = None
         self.world.meetsDayConstraints.value = None


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
         valid = False
         for day in event.days:
             if day == self.world.getDayFromIndex(self.world.day):
                 valid = True
                 break
         
         if (self.world.lowerRatio.value == 'or' and self.restrictionLevel == 0):
             valid = False

         return valid

     def CheckTimeConstraints(self, event):
         if event.time == 'Any':
             pass
         elif event.time != self.world.getTimePeriod():
             return False
        
         return True


class TimeSlot(object):
    def __init__(self, name, code):
        self.name = name
        self.code = code
        
    def printSlot(self):
        return self.name

class EventSlot(TimeSlot):

    def __init__(self, name, code, days, time):
        TimeSlot.__init__(self, name, code)
        self.days = days
        self.time = time
        self.holding = False
        self.placed = False

    def printDays(self):
        output = ''
        for day in self.days:
            output = output + day + ","

        return output[:-1]


class TimetableSlot(TimeSlot):
    def __init__(self, name, code, room, teacher):
        TimeSlot.__init__(self, name, code)
        self.room = room
        self.teacher = teacher

    def printSlot(self):
        return TimeSlot.printSlot(self) + '\n' + self.room + '\n' + self.teacher