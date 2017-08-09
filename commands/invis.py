from evennia.commands.default.muxcommand import MuxCommand


class CmdInvis(MuxCommand):
    """
       +Invis - Temporarily makes you invisible.
    
       Usage: 
         +invisible
   
       Can only be used on yourself..
    
    """   
    auto_help = True   
    key = "+invis"
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
        self.caller.db.invis = 1
        self.caller.msg("You are now invisible.")