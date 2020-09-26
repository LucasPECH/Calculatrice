def parse(string):

    # list of tokens to return
    tokens = []

    # go through the string
    i = 0
    length = len(string)
    while i < length:

        # skip blanks
        while i < length and string[i] == ' ':
            i += 1

        # look for integer operators
        if string[i] in "+-*/":
            operator = string[i]
            tokens += [(operator, "operator")]
            i += 1
            continue

        #LOOK FOR VARIABLES
        if string[i] in 'abcdefghijklmnopqrstuvwxyz':
            j = i + 1
            while j < length and string[j] in 'abcdefghijklmnopqrstuvwxyz':
                j += 1
            variable = str(string[i:j])

            #SEARCH TRUE OPERAND
            if variable == "true":
                operand = True
                tokens += [(operand, "operandbool")]

            #SEARCH FALSE OPERAND
            elif variable == "false":
                operand = False
                tokens += [(operand, "operandbool")]

            #SEARCH OR AND AND
            elif variable == "or" or variable == "and" or variable =="not":
                tokens += [(variable, "operator")]


            #SEARCH VARIABLE
            else:
                tokens += [(variable, "variable")]
                
            i = j
            continue



        #SEARCH == OR =
        if string[i] in '=':
            j = i + 1
            while j < length and string[j] in '=':
                j += 1
            operator = str(string[i:j])
            tokens += [(operator, 'operator')]
            i = j
            continue



        #SEARCH <> OR <= OR <
        if string[i] in '<':
            j = i + 1
            while j < length and string[j] in '=>':
                j += 1
            operator = str(string[i:j])
            tokens += [(operator, 'operator')]
            i = j
            continue



        #SEARCH >= OR >
        if string[i] in '>':
            j = i + 1
            while j < length and string[j] in '=':
                j += 1
            operator = str(string[i:j])
            tokens += [(operator, 'operator')]
            i = j
            continue
            


        #SEARCH STRING OPERAND
        if string[i] in '"':
            j = i + 1
            while j < length and string[j] not in '"':
                j += 1
            operand = str(string[i+1:j])
            tokens += [(operand, 'operandstr')]
            i = j+1
            continue
        


        #SEARCH INTEGER OPERAND
        if string[i] in "0123456789":
            j = i + 1
            while j < length and string[j] in "0123456789":
                j += 1
            operand = int(string[i:j])
            tokens += [(operand, 'operand')]
            i = j
            continue


        #SEARCH PARENTHESIS
        if string[i] in "()":
            operator = string[i]
            tokens += [(operator, "parenthesis")]
            i += 1
            continue


    return tokens
    

# Evaluates an expression represented as a list of
# tagged tokens and returns the evaluation result.
#
# All operators are left-associative.
#
def evaluate (expression,variable): 

    length = len(expression)

    i = 0 #INDEX 

    is_variable = False
    

    # expression is: empty (should not happen)
    if length == 0:
        return None

    #
    if length == 1:
        #WE CHECK WHAT TYPE OF EXPRESSION IS THIS
        for i in variable.keys():
            if i == expression[0][0]:
                is_variable = True


        if is_variable == True: # ITS A VARIABLE
            return variable[expression[0][0]]


        elif expression[0][1] == "variable": #ITS AN UNKNOWN VARIABLE
            return'Error, unknown variable'


        elif expression[0][1] == "operator": #IT MEANS THE EXPRESSION IS ONLY AN OPERATOR
            return "Error, missing operand"


        else: #ITS AN OPERAND
            return expression[0][0]

    if length > 1:

        newExpression = []
        
        #CHECK IF THERE IS A NOT WITHOUT OPERAND
        if expression[length-1][1] == "operator":
            return "Error, missing operand"

        # PARENTHESIS
        while i < length:
            if expression[i][0] == '(':
                j = i + 1
                save = i
                while j < length and expression[j][0] != ')':
                    j += 1
                parenthesis = expression[i+1:j]
                #EVALUATE EXPRESSION BETWEEN PARENTHESIS BEFORE
                parenthesis2 = evaluate(parenthesis,variable)
                w = 0
                while w < length :
                    if w != save:
                        newExpression += [(expression[w][0],expression[w][1])]
                        w += 1
                    if w == save:
                        newExpression += [(parenthesis2,"parenthesis")]
                        w += 1+(j-w)
                return evaluate(newExpression,variable)
                    
            i += 1

        # RESET I TO EVALUATE FROM THE END
        i = length-1

        # OR
        while 0 < i:
            if expression[i][0] == 'or':
                leftExpression = expression[:i]
                rightExpression = expression[i+1:]
                # STR OR STR ERROR
                #if type(leftExpression[0][1])!=bool and type(rightExpression[0][0])!=bool:
                    #return "impossible operation (str or str)"
                #else: 
                return evaluate(leftExpression,variable) or evaluate(rightExpression,variable)
            i -= 1

        i = length-1

        # AND 
        while 0 < i:
            if expression[i][0] == 'and':
                leftExpression = expression[:i]
                rightExpression = expression[i+1:]
                #if type(leftExpression[0][0])!=bool and type(rightExpression[0][0])!=bool:
                    #return "impossible operation (str and str)"
                #else:
                return evaluate(leftExpression,variable) and evaluate(rightExpression,variable)
            i -= 1

        i = length-1

        # VARIABLE
        while 0<i:
            if expression[i][0] == '=':
                leftExpression = expression[:i]
                rightExpression = expression[i+1:]
                #ASSOCIATING KEY(VARIABLE) TO VALUE
                variable[leftExpression[0][0]] = evaluate(rightExpression,variable)
                return " "
            i -= 1

        i = length-1

        # NOT
        if expression[0][0] == 'not':
            notExpression = expression[1:length]
            notExp = evaluate(notExpression,variable)
            newExpression += [(not notExp,"operandbool")]
            return evaluate(newExpression,variable)

        # BOOLEAN OPERATOR
        while 0 < i:
            if expression[i][0] == '==':
                leftExpression = expression[:i]
                rightExpression = expression[i+1:]
                return evaluate(leftExpression,variable) == evaluate(rightExpression,variable)

            if expression[i][0] == '<':
                leftExpression = expression[:i]
                rightExpression = expression[i+1:]
                #if type(rightExpression[0][0])==type(leftExpression[0][0]):
                return evaluate(leftExpression,variable) < evaluate(rightExpression,variable)
                #else:
                    #return "Error, you can't compare different type of variable"

            if expression[i][0] == '<>':
                leftExpression = expression[:i]
                rightExpression = expression[i+1:]
                return evaluate(leftExpression,variable) != evaluate(rightExpression,variable)

            if expression[i][0] == '<=':
                leftExpression = expression[:i]
                rightExpression = expression[i+1:]
                #if type(rightExpression[0][0])==type(leftExpression[0][0]):
                return evaluate(leftExpression,variable) <= evaluate(rightExpression,variable)
                #else:
                    #return "Error, you can't compare different type of variable"

            if expression[i][0] == '>=':
                leftExpression = expression[:i]
                rightExpression = expression[i+1:]
                #if type(rightExpression[0][0])==type(leftExpression[0][0]):
                return evaluate(leftExpression,variable) >= evaluate(rightExpression,variable)
                #else:
                    #return "Error, you can't compare different type of variable"
            if expression[i][0] == '>':
                leftExpression = expression[:i]
                rightExpression = expression[i+1:]
                #if type(rightExpression[0][0])==type(leftExpression[0][0]):
                return evaluate(leftExpression,variable) > evaluate(rightExpression,variable)
                #else:
                    #return "Error, you can't compare different type of variable"
            i -= 1

        i = length-1
        
        # +
        while 0 < i:

            if expression[i][0] == '+':
                leftExpression = expression[:i]
                rightExpression = expression[i+1:]

                #STR + BOOL OR INT
                if leftExpression[0][1] == 'operandstr':
                    return evaluate(leftExpression,variable) + str(evaluate(rightExpression,variable))
                
                #ERROR
                #elif  type(rightExpression[0][0])!=int and type(leftExpression[0][0])!=int:
                    #return "Impossible operation :", type(leftExpression[0][0])," + ",type(rightExpression[0][0])

                #NORMAL CASE
                else:
                    return evaluate(leftExpression,variable) + evaluate(rightExpression,variable)
            i -= 1

        i = length-1

        #SEARCH NEGATIVE NUMBERS
        if expression[0][0] == '-':

            newExpression += [(-expression[1][0],"integer")] #TAKING INVERSE OF THE NB
            for w in range(2,length):
                newExpression += [(expression[w][0],expression[w][1])]
            return evaluate(newExpression,variable)

        # -
        while 0 < i:
            if expression[i][0] == '-' and expression[i-1][1] != 'operator':
                leftExpression = expression[:i]
                rightExpression = expression[i+1:]
                #STR - STR ERROR
                if type(leftExpression[0][0]) != int and type(rightExpression[0][0]) != int:
                    return "Impossible operation"
                else:
                    return evaluate(leftExpression,variable) - evaluate(rightExpression,variable)
            
            i -= 1

        i = length-1

        # * AND /
        while 0 < i:
            if expression[i][0] == '*':
                leftExpression = expression[:i]
                rightExpression = expression[i+1:]
                #STR * STR ERROR
                if type(leftExpression[0][0])!=int and type(rightExpression[0][0])!=int:
                    return "Impossible operation"
                else:
                    return evaluate(leftExpression,variable) * evaluate(rightExpression,variable)
                
            if expression[i][0] == '/':
                leftExpression = expression[:i]
                rightExpression = expression[i+1:]
                #STR / STR ERROR
                if type(leftExpression[0][0])!=int and type(rightExpression[0][0])!=int:
                    return "impossible operation"
                else:
                    return evaluate(leftExpression,variable) / evaluate(rightExpression,variable)

            i -= 1

        i = length-1

# Evaluates a sequence of user-input expressions.
#
def calculator():
    emptyCount = 0
    #DICTIONNARIE OF VARIABLE
    variable = {}
    while True:

        # prompt for new expression
        line = input("? ")

        # check for empty line
        if line == "":
            emptyCount += 1
            if emptyCount == 2:
                break
            continue
        else:
            emptyCount = 0


        # evaluate expression and print result
        print(evaluate((parse(line)),variable))

    print("done")

calculator()
