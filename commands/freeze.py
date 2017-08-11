from evennia.commands.default.muxcommand import MuxCommand


class CmdFreeze(MuxCommand):
    """
       +Freeze - Freezes time in a location.
    
       Usage: 
         +freeze   
       Stops time in a location.
    
    """   
    key = "+freeze"
    locks = "cmd:all()"
    auto_help=False
    def func(self):
        if not self.caller.db.magic:
            self.caller.msg("You can't use magic!")
            return

        from evennia.contrib.dice import roll_dice

        if not self.caller.db.time:
            self.caller.msg("This spell requires knowledge of the time sphere.")
            return
        wins = 0
        if(self.caller.db.magic_fuel):
            self.caller.msg("You roll %s dice for the spell with a difficulty of %s, using %s quintessence." % (self.caller.db.arete + self.caller.db.time, 6-self.caller.db.magic_fuel, self.caller.db.magic_fuel))
        else:  
            self.caller.msg("You roll %s dice for the spell with a difficulty of %s." % (self.caller.db.arete + self.caller.db.time, 6-self.caller.db.magic_fuel))
        for x in range(0, self.caller.db.arete + self.caller.db.time):
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
        current_room = self.caller.location
        current_room.db.freeze = 1 
        for item in current_room.contents:
            item.msg("Time comes to a stop.") 
            item.db.present = 0
        self.caller.db.present = 1
        self.caller.db.frozen_room = current_room      
