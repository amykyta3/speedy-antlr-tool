from typing import List

class ContextData:
    """
    Represents a RuleContext from the parser
    """

    def __init__(self, ctx_classname:str, label_ctx_classname:str, is_label_parent:bool, labels:List[str]):
        self.ctx_classname = ctx_classname
        self.label_ctx_classname = label_ctx_classname
        self.is_label_parent = is_label_parent
        self.labels = labels

    def __str__(self):
        s = []
        if self.label_ctx_classname:
            s.append("%s#%s:" % (self.ctx_classname, self.label_ctx_classname))
        else:
            s.append("%s:" % self.ctx_classname)
        for label in self.labels:
            s.append("\t%s" % label)

        return "\n".join(s)

    @property
    def rule_name(self):
        if self.label_ctx_classname:
            ctx_name = self.label_ctx_classname
        else:
            ctx_name = self.ctx_classname
        
        assert(ctx_name.endswith('Context'))
        return ctx_name[0].lower() + ctx_name[1:-7] # Truncate "Context"
    
    @property
    def Rule_name(self):
        """
        Capitalized version of rule_name
        """
        return self.rule_name[0].upper() + self.rule_name[1:]

    @property
    def is_label_ctx(self):
        return self.label_ctx_classname is not None
