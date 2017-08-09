from evennia.commands.default.muxcommand import MuxCommand


class CmdSlowtime(MuxCommand):

    """
       +slowtime - Slows time down for other people.
    
       Usage: 
         +slowtime

       Slows time down.
    
    """   
   
    key = "+slowtime"
    locks = "cmd:all()"
    auto_help=False
    def func(self):     
        if not self.caller.db.magic:
            self.caller.msg("You can't use magic!")
            return
        if not self.caller.db.quintessence:
            self.caller.msg("You don't have enough quintessence for that!")
            return
        else:
            self.caller.db.quintessence -= 1
        self.caller.db.slowtime = 1
        self.caller.msg("The time around you slows down.")
