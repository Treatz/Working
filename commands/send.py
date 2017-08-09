from evennia import default_cmds


class CmdSend(default_cmds.MuxCommand):
    """
       +send - Sends a message to another character with telepathy.
    
       Usage: 
        +send <character> = <message>
    
       Sends a telepathic message.
    
    """
    key = "+send"
    locks = "cmd:all()"
    auto_help=False
    def func(self):
        """confirms the target and initiates the search"""
        if not self.caller.db.magic:
            self.caller.msg("You can't use magic!")
            return
        if not self.caller.db.quintessence:
            self.caller.msg("You don't have enough quintessence for that!")
            return
        else:
            self.caller.db.quintessence -= 1
        # save the target object onto the command
        # this will use Evennia's default multimatch handling if more than one object matches
        self.target = self.caller.search(self.lhs, global_search=True)
        # initialize a list to store rooms we've visited
        self.target.msg('%s speaks to you in thought, "%s"' % (self.caller.name, self.rhs))
        