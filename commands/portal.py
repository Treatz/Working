from evennia.commands.default.muxcommand import MuxCommand
from evennia import DefaultRoom, DefaultExit, DefaultObject
from evennia.utils.create import create_object

class CmdPortal(MuxCommand):
    """
       +Portal - Creates a portal that anyone can pass through.
    
       Usage: 
         +portal    
       Opens a gateway between two locations.
    
    """   
    key = "+portal"
    locks = "cmd:all()"
    auto_help=False
    def func(self):
        if self.caller.db.med:
            self.caller.msg("You are forced to stop your meditation.")
            self.caller.db.med = 0
        if self.caller.ndb.ritual:
            self.caller.msg("You are forced to stop your ritual.")
            self.caller.ndb.ritual = 0
        if not self.caller.db.magic:
            self.caller.msg("You can't use magic!")
            return

        from evennia.contrib.dice import roll_dice

        if not self.caller.db.correspondence:
            self.caller.msg("This spell requires knowledge of the correspondence sphere.")
            return
        wins = 0
        if(self.caller.db.magic_fuel):
            self.caller.msg("You roll %s dice for the spell with a difficulty of %s, using %s quintessence." % (self.caller.db.arete + self.caller.db.correspondence, 6-self.caller.db.magic_fuel, self.caller.db.magic_fuel))
        else:  
            self.caller.msg("You roll %s dice for the spell with a difficulty of %s." % (self.caller.db.arete + self.caller.db.correspondence, 6-self.caller.db.magic_fuel))
        for x in range(0, self.caller.db.arete + self.caller.db.correspondence):
            roll = roll_dice(1,10)
            if(roll > 5 - self.caller.db.magic_fuel):
                wins += 1
        wins = wins + self.caller.db.autopoint
        if(self.caller.db.autopoint):
            self.caller.msg("You have %s successes out of 4 needed, using a point of willpower" % wins)
        else:
            self.caller.msg("You have %s successes out of 4 needed." % wins)
        self.caller.db.magic_fuel = 0
        self.caller.db.autopoint = 0
        if wins < 4:
            self.caller.msg("Your spell fizzles out and fails.")
            return
        if(sel.caller.ndb.source):
            self.caller.msg("You have opened a portal to %s." % self.caller.ndb.source)
            self.caller.ndb.portA = create_object(DefaultExit, key="portal",aliases=["in", "enter"],location=self.caller.location,destination=self.caller.ndb.source)
            self.caller.ndb.portB = create_object(DefaultExit, key="portal",aliases=["in", "enter"],location=self.caller.ndb.source,destination=self.caller.location)
            yield 60
            self.caller.msg("The portal has closed.")
            self.caller.ndb.portA.delete()
            self.caller.ndb.portB.delete()