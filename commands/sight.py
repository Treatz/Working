from evennia.commands.default.muxcommand import MuxCommand


class CmdSight(MuxCommand):
    """
       +sight - Temporarily see into the spirit world.
    
       Usage: 
         +sight

       Also allows ghosts to see into the physical world.
    
    """   
    key = "+sight"
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

        if not self.caller.db.spirit:
            self.caller.msg("This spell requires knowledge of the spirit sphere.")
            return
        wins = 0
        if(self.caller.db.magic_fuel):
            self.caller.msg("You roll %s dice for the spell with a difficulty of %s, using %s quintessence." % (self.caller.db.arete + self.caller.db.spirit, 6-self.caller.db.magic_fuel, self.caller.db.magic_fuel))
        else:  
            self.caller.msg("You roll %s dice for the spell with a difficulty of %s." % (self.caller.db.arete + self.caller.db.spirit, 6-self.caller.db.magic_fuel))
        for x in range(0, self.caller.db.arete + self.caller.db.spirit):
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
        self.caller.db.sight = 1
        if self.caller.db.alive:
            self.caller.msg("You can now see into the spirit world.")
        else:
            self.caller.msg("You can now see into the physical world.")
