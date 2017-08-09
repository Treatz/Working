from evennia.commands.default.muxcommand import MuxCommand


class CmdSummon(MuxCommand):
    """
       +summon - Opens a room to the spirit world.
    
       Usage: 
         +summon    
       Allows ghosts and people in a room to hold an audience.
    
    """   
    key = "+summon"
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
        players = [con for con in self.caller.location.contents if con.has_player]
        for player in players:
            if(player.db.alive == 1):
                player.msg("The spirit world is drawing closer.")
            if(player.db.alive == 0):
                player.msg("The physical plane is drawing closer.")
            player.db.sight = 1
            player.db.touch = 1        
