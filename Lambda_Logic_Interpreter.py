class Name:
    def __init__(self, ID):
        self.ID = ID

    def makeSub(self, oldName, newExpr):
        if self.ID == oldName.ID:
            return newExpr
        else:
            return self
    
    def pp(self):
        return self.ID


class Function:
    def __init__(self, variable, body):
        self.variable = variable
        self.body = body

    def makeSub(self, oldName, newExpr): 

        # Set lists
        subBodies = []
        subOldNames = []
        subNewExpr = []
        if type(self.body) == list:
            for i in self.body:
                subBodies.append(i)
        else:
            subBodies.append(self.body)
            
        if type(oldName) == list:
            for i in oldName:
                subOldNames.append(i)
        else:
            subOldNames.append(oldName)
            
        if type(newExpr) == list:
            for i in newExpr:
                subNewExpr.append(i)
        else:
            subNewExpr.append(newExpr)

        # Apply substitution
        for i in subBodies:
            for j in subOldNames:
                if i == j:
                    
                    subBodies[subBodies.index(i)] = subBodies[subBodies.index(i)].makeSub(j, subNewExpr[subOldNames.index(j)])
                    break
        # Return result
        if len(subBodies) > 1:
            return Application(subBodies[0], subBodies[1:])
        else:
            return Function(self.variable, subBodies)
        

    def eval(self, argument):
        if type(self.body) == list :
            return self.makeSub(self.variable, argument).eval()
        elif type(self.variable) == list:
            arguments = []
            if type(argument) == list:
                for i in argument:
                    arguments.append(i)
            else:
                arguments.append(argument)
            return arguments[self.variable.index(self.body)]
        else:
            return self.body.makeSub(self.variable, argument)
        

    def pp(self): 

        if type(self.variable) == list:
            ppVariables = ""
            for i in self.variable:
                ppVariables += i.pp()
        else:
            ppVariables = self.variable.pp()

        if type(self.body) == list:
            ppBodies = ""
            for i in self.body:
                ppBodies += i.pp()
        else:
            ppBodies = self.body.pp()
        return "λ"+ppVariables+"."+ppBodies

# Will output T and F as full statements

class Application: 
    def __init__(self, operator, argument):
        self.operator = operator  
        self.argument = argument 

    def makeSub(self, oldName, newExpr):
        return Application(self.operator.makeSub(oldName, newExpr), self.argument.makeSub(oldName, newExpr))

    def eval(self):
        if type(self.argument) == Application:
            return self.operator.eval(self.argument.eval())
        else:
            return self.operator.eval(self.argument)

    def pp(self):
        if type(self.argument) == list:
            arguments = ""
            for i in self.argument:
                arguments += i.pp()
        else:
            arguments = self.argument.pp()
        return "(" + self.operator.pp() + ")" + arguments

#Doesn't work if multiple expressions in argument


x = Name("x")
y = Name("y")

T = Function([x,y], x)
F = Function([x,y], y)
AND = Function([x, y], [x, y, F])
OR = Function([x, y], [x, T, y])
NOT = Function(x, [x, F, T])

NT = Application(NOT, T)
NF = Application(NOT, F)
NNT = Application(NOT, NT)
NNNT = Application(NOT, NNT)
TORF = Application(OR, [T, F])
FORF = Application(OR, [F, F])
FANDT = Application(AND, [F, T])
TANDT = Application(AND, [T, T]) 
