#Vasileiadou Stavoula 2582 cse32582

import sys, traceback, enum
from itertools import count
import itertools
import os
import string

class Lexer:
    
    # Constructor.
    def __init__(self, input):
        self.source = input.strip() # Source code to lex as a string. Append a newline to simplify lexing/parsing the last token/statement.
        self.count = 0
        self.read_char = ''   # Current character in the string.
        self.curPos = -1    # Current position in the string.
        self.startIdentPos = 0
        self.nextChar()
         
    # Process the next character.
    def nextChar(self):
        self.curPos += 1
        if self.curPos >= len(self.source):
            self.read_char = '\0'  # EOF
        else:
            self.read_char = self.source[self.curPos]
            if self.read_char =='\n':
                    self.count += 1 

    # Return the lookahead character.
    def peek(self):
        if self.curPos + 1 >= len(self.source):
            return '\0'
        return self.source[self.curPos+1]
      
    # Error message handler.
    def abort(self, message):

        sys.exit("Lexing error. Line: " + message )

    # Skip whitespace.
    def skipWhitespace(self):
        while self.read_char == ' ' or self.read_char == '\t' or self.read_char == '\r' or self.read_char == '\n' or self.read_char =='\f' or self.read_char =='\v' or self.read_char =='\v\f':
            self.nextChar()

    # Skip comments in the code.
    def skipComment(self):
        if self.read_char == '#':
            lastChar = self.read_char
            self.nextChar()
            while self.read_char != '#':
                self.nextChar()
            if self.read_char == '#':
                self.nextChar()
                
    # Return the next token.
    def getToken(self):
        # Skip whitespases.
        self.skipWhitespace()
        # Skip comments.
        self.skipComment()
        token = None
       
        # Calculations.
        if self.read_char == '+':
            token = Token(self.read_char, TokenType.PLUS, self.count)
        elif self.read_char == '-':
            token = Token(self.read_char, TokenType.MINUS, self.count)
        elif self.read_char == '*':
            token = Token(self.read_char, TokenType.ASTERISK, self.count)
        elif self.read_char == '/':
            token = Token(self.read_char, TokenType.SLASH, self.count)
            
        # Relations.
        elif self.read_char == '=':
            token = Token(self.read_char, TokenType.EQUAL, self.count)
        elif self.read_char == '>':
            # Check whether this is token is > or >=
            if self.peek() == '=':
                lastChar = self.read_char
                self.nextChar()
                token = Token(lastChar + self.read_char, TokenType.GREATEREQUAL, self.count)
            else:
                token = Token(self.read_char, TokenType.GREATER, self.count)
        elif self.read_char == '<':
            # Check whether this token is < or <=
            if self.peek() == '=':
                lastChar = self.read_char
                self.nextChar()
                token = Token(lastChar + self.read_char, TokenType.LESSEQUAL, self.count)
            # Check whether this token is < or <>
            elif self.peek() == '>':
                lastChar = self.read_char
                self.nextChar()
                token = Token(lastChar + self.read_char, TokenType.INBETWEEN, self.count)
            else:
                token = Token(self.read_char, TokenType.LESS, self.count)
        
        # Deviders.
        elif self.read_char == '\n':
            token = Token(self.read_char, TokenType.NEWLINE, self.count)
        elif self.read_char == ',':
            token = Token(self.read_char, TokenType.COMMA, self.count)
        elif self.read_char == ';':
            token = Token(self.read_char, TokenType.SEMI_COLON, self.count)
        elif self.read_char == ':':
            if self.peek() == '=':
                lastChar = self.read_char
                self.nextChar()
                token = Token(lastChar + self.read_char, TokenType.ASSIGN, self.count)
            else: 
                token = Token(self.read_char, TokenType.COLON, self.count)

        
        # Groups.
        # Quotations open operation.
        elif self.read_char == '\"':
            token = Token(self.read_char, TokenType.QUOTES_OPEN, self.count)
            if self.read_char == '\n':
                self.nextChar()
                if self.read_char.isalpha():
                    startPos = self.curPos
                    while self.peek().isalnum():
                        self.nextChar()
                    tokText = self.source[startPos : self.curPos + 1]
                    keyword = Token.checkIfKeyword(tokText.upper())
                    if keyword == None: # Identifier
                        token = Token(tokText.upper(), TokenType.IDENT, self.count)
                    else:   # Keyword
                       self.abort(str(self.count) + " --> Illegal use of keyword!")
                elif self.read_char.isdigit():
                    startPos = self.curPos
                    while self.read_char != '\"': 
                        self.nextChar()
                    tokText = self.source[startPos : self.curPos + 1]
                    token = Token(tokText, TokenType.NUMBER, self.count)

        # Quotations close operation.
        elif self.read_char =='\"':
            token = Token(self.read_char, TokenType.QUOTES_CLOSE, self.count)

        # Brackets open operation.
        elif self.read_char == '[':
            token = Token(self.read_char, TokenType.SQUARE_BRACKET_OPEN, self.count)
            if self.read_char == '\n':
                self.nextChar()
                if self.read_char.isalpha():
                    startPos = self.curPos
                    while self.peek().isalnum():
                        self.nextChar()
                    tokText = self.source[startPos : self.curPos + 1]
                    keyword = Token.checkIfKeyword(tokText.upper())
                    if keyword == None: # Identifier
                        token = Token(tokText.upper(), TokenType.IDENT, self.count)
                    else:   # Keyword
                       self.abort(str(self.count) + " --> Illegal use of keyword!")

        # Brackets close operation.
        elif self.read_char ==']':
            token = Token(self.read_char, TokenType.SQUARE_BRACKET_CLOSE, self.count)
 

        # Parenthesis open operations.
        elif self.read_char == '(':
            token = Token(self.read_char, TokenType.PARENTHESIS_OPEN, self.count)
            if self.read_char == '\n':
                self.nextChar()
                if self.read_char.isalpha():               
                    startPos = self.curPos
                    while self.peek().isalnum():
                        self.nextChar()
                    tokText = self.source[startPos : self.curPos + 1]
                    keyword = Token.checkIfKeyword(tokText.upper())
                    if keyword == None: # Identifier
                        token = Token(tokText.upper(), TokenType.IDENT, self.count)
                    else:   # Keyword
                       self.abort(str(self.count) + " --> Illegal use of keyword!")
                elif self.read_char.isdigit():
                    startPos = self.curPos
                    while self.read_char != ')': 
                        self.nextChar()
                    tokText = self.source[startPos : self.curPos + 1]
                    token = Token(tokText, TokenType.NUMBER, self.count)

        # Parenthesis close operations.
        elif self.read_char ==')':
            token = Token(self.read_char, TokenType.PARENTHESIS_CLOSE, self.count)
 
        # Angled brackets.
        elif self.read_char == '{':
            self.nextChar()
            if self.read_char == '\n':
                self.nextChar()                
                if self.read_char  != '}':
                    self.nextChar()                     
                token = Token(self.read_char, TokenType.ANGLED_BRACKET_OPEN, self.count)       
            else:
                self.abort(str(self.count) + " --> Illegal expression " + self.read_char) 
        elif self.read_char == '}':
            token = Token (self.read_char, TokenType.ANGLED_BRACKET_CLOSE, self.count)

        # Check if the token is a number.
        elif self.read_char.isdigit():
            # Leading character is a digit, so this must be a number.
            startPos = self.curPos
            while self.peek().isdigit():
                self.nextChar()
                if not self.read_char.isdigit():
                    self.abort(str(self.count) + " --> Illegal character in number: " + self.read_char)
            tokText = self.source[startPos : self.curPos + 1] # Get the substring.
            if int(tokText) > -((2^32)-1) or int(tokText) < ((2^32 ) -1):
                token = Token(tokText, TokenType.NUMBER, self.count)
            else:
                self.abort(str(self.count) + " --> Number out of range. " )

        # Check if the token is a letter.
        elif self.read_char.isalpha():
            # Leading character is a letter, so this must be an identifier or a keyword.
            # Get all consecutive alpha numeric characters.
            startPos = self.curPos
            while self.peek().isalnum():
                self.nextChar()
            # Check if the token is in the list of keywords.
            tokText = self.source[startPos : self.curPos + 1] # Get the substring.            
            keyword = Token.checkIfKeyword(tokText.upper())
            if keyword == None: # Identifier
                token = Token(tokText.upper(), TokenType.IDENT, self.count)
            else:   # Keyword
                token = Token(tokText.upper(), keyword, self.count)


        # EOP.
        elif self.read_char == '.':
            token = Token(self.read_char, TokenType.EOP, self.count)


        # EOF.
        elif self.read_char == '\0':
            token = Token(self.read_char, TokenType.EOF, self.count)
        

        else:
            # Unknown token!
            self.abort(str(self.count) + "  Unknown token: " + self.read_char)

        self.nextChar()
        return token

class Token:
    # Properties: TokenString, TokenType, lineNo.
    def __init__(self, tokenString, tokenType, lineNo):
        self.tokenString = tokenString.lower()
        self.tokenType = tokenType
        self.lineNo = lineNo

    # Identifying the keyword
    def checkIfKeyword(tokenString):
        for tokenType in TokenType:
            # Relies on all keyword enum values being 1XX.
            if tokenType.name == tokenString and tokenType.value >= 100 and tokenType.value < 200:
                return tokenType
        return None

class TokenType(enum.Enum):
    EOF = -1
    EOP = 0
    NUMBER = 1
    IDENT = 2
    NEWLINE = 3
    # Keywords.
    PROGRAM = 101
    DECLARE = 102
    IF = 103
    ELSE = 104
    WHILE = 105
    SWITCHCASE = 106
    FORCASE = 107
    INCASE = 108
    CASE = 109
    DEFAULT = 110
    NOT = 111
    AND = 112
    OR = 113
    FUNCTION = 114
    PROCEDURE = 115
    CALL = 116
    RETURN = 117
    IN = 118
    INOUT = 119
    INPUT = 120
    PRINT = 121
    #Operators.
    EQUAL = 201  
    PLUS = 202
    MINUS = 203
    ASTERISK = 204
    SLASH = 205
    LESS = 206
    MORE = 207
    LESSEQUAL = 208
    GREATER = 209
    GREATEREQUAL = 210
    INBETWEEN = 211
    #Deviders
    SEMI_COLON = 301
    COMMA = 302
    COLON = 303
    QUOTES = 304
    #Groups
    PARENTHESIS_OPEN = 401
    PARENTHESIS_CLOSE = 402
    ANGLED_BRACKET_OPEN = 403
    ANGLED_BRACKET_CLOSE = 404
    SQUARE_BRACKET_OPEN = 405
    SQUARE_BRACKET_CLOSE = 406
    QUOTES_OPEN = 407
    QUOTES_CLOSE = 408
    #Assignment
    ASSIGN = 501

class Parser:

    # Constructor.
    def __init__(self, Lexer, Intermediate):
        self.lexer = Lexer  
        self.inter = Intermediate
        self.list = []
        self.list2 = []
        self.list3 = []
        self.list4 = []
        self.declaredVariables = set()# All variables we have declared so far.
        self.declaredNames = set()
        self.curToken = None
        self.peekToken = None
        self.tmp = None
        self.tmp1 = None
        self.tmp2 = None
        self.tmp3 = None
        self.nextToken()
        self.nextToken()    # Call this twice to initialize current and peek.

    # Return true if the current token matches.
    def checkToken(self, tokenType):

        return tokenType == self.curToken.tokenType

    # Return true if the next token matches.
    def checkPeek(self, tokenType):

        return tokenType == self.peekToken.tokenType

    # Try to match current token. If not, error. Advances the current token.
    def match(self, tokenType):
        if not self.checkToken(tokenType):
            self.abort(str(self.curToken.lineNo +1)+ " --> Expected " + tokenType.name + ", got " + self.curToken.tokenType.name)
        self.nextToken()

    # Advances the current token.
    def nextToken(self):
        self.curToken = self.peekToken
        self.peekToken = self.lexer.getToken()
        # No need to worry about passing the EOF, lexer handles that.

    # Return true if the current token is a comparison operator.
    def isComparisonOperator(self):

        return self.checkToken(TokenType.GREATER) or self.checkToken(TokenType.GREATEREQUAL) or self.checkToken(TokenType.LESS) or self.checkToken(TokenType.LESSEQUAL) or self.checkToken(TokenType.EQUAL) or self.checkToken(TokenType.INBETWEEN)

    # Error message handler.
    def abort(self, message):

        sys.exit("Parser error. Line: " + message)

    # Production rules.

    # program ::= {statement}
    def program(self):
        print("STARTS THE PROGRAM")
        print("--------------------")
        # Since some newlines are required in our grammar, need to skip the excess.
        while self.checkToken(TokenType.NEWLINE):
            self.nextToken()
        # Parse all the statements in the program.
        while not self.checkToken(TokenType.EOF):
            self.statement()

    # comparison ::= expression ((">" | ">=" | "<" | "<=" | "<>") expression)+
    def comparison(self):
        operant = self.curToken.tokenString
        self.expression()
        # Must be at least one comparison operator and another expression.
        if self.isComparisonOperator():
            sign = self.curToken.tokenString
            self.nextToken()
            operant2 = self.curToken.tokenString
            self.inter.genquad(sign,operant,operant2,'')
            self.list.append(self.inter.getNextQuad())
            self.inter.backpatch(self.list, self.inter.newtemp())
            self.expression()
        else:
            self.abort(str(self.curToken.lineNo + 1) + " --> Expected comparison operator at: " + self.curToken.tokenString)
         # Can have 0 or more comparison operator and expressions.
        while self.isComparisonOperator():
            self.nextToken()
            self.expression()

    # expression ::= term {( "-" | "+" ) term}
    def expression(self):
        operator = self.curToken.tokenString
        self.term()
        
        # Can have 0 or more +/- and expressions.
        while self.checkToken(TokenType.PLUS) or self.checkToken(TokenType.MINUS):
            sign = self.curToken.tokenString
            self.nextToken()
            operator2 = self.curToken.tokenString
            self.inter.genquad(sign,operator,operator2,'')
            self.list.append(self.inter.getNextQuad()) 
            self.inter.backpatch(self.list, self.inter.newtemp())
            self.term()

    # term ::= unary {( "/" | "*" ) unary}
    def term(self):
        operator = self.curToken.tokenString
        self.unary()
        # Can have 0 or more *// and expressions.
        while self.checkToken(TokenType.ASTERISK) or self.checkToken(TokenType.SLASH):
            sign = self.curToken.tokenString
            self.nextToken()
            operator2 = self.curToken.tokenString
            self.inter.genquad(sign,operator,operator2,'')
            self.list.append(self.inter.getNextQuad())
            self.inter.backpatch(self.list, self.inter.newtemp())
            self.unary()

    # unary ::= ["+" | "-"] primary
    def unary(self):

        # Optional unary +/-
        if self.checkToken(TokenType.PLUS) or self.checkToken(TokenType.MINUS):
            self.nextToken()        
        self.primary()

    # primary ::= number | ident
    def primary(self):
        
        if self.checkToken(TokenType.NUMBER): 
            self.nextToken()
        elif self.checkToken(TokenType.IDENT):
            # Ensure the variable already exists.
            if (self.curToken.tokenString not in self.declaredVariables) and (self.curToken.tokenString not in self.declaredNames):
                self.abort(str(self.curToken.lineNo + 1) + " --> Referencing variable before assignment: " + self.curToken.tokenString)
            
            self.nextToken()
        else:
           
            self.abort(str(self.curToken.lineNo+1) + " --> Unexpected token at " + self.curToken.tokenString.lower())
    
    # handles recursive calls
    def recurtion(self):
        if self.checkToken(TokenType.IDENT):
            if self.curToken.tokenString not in self.declaredNames:
                    self.abort(str(self.curToken.lineNo + 1) +" --> Function name has not been declared")
            self.match(TokenType.IDENT)
            self.match(TokenType.PARENTHESIS_OPEN)
            self.match(TokenType.IN)
            self.statement()    

    # peeks for calculation token ("+" | "-" | "*" | "/")
    def calculations(self):
        return self.checkPeek(TokenType.PLUS) or self.checkPeek(TokenType.MINUS) or self.checkPeek(TokenType.ASTERISK) or self.checkPeek(TokenType.SLASH)

    def condition(self):
        global tempToken
        self.orlist = self.boolterm()
        tempList = self.orlist
        while self.checkToken(TokenType.OR):
            self.inter.backpatch(tempList[1], self.inter.nextquad())
            tempList1 = self.boolterm()
            self.inter.mergelist(tempList[0], tempList1[0])
            tempList[1] = tempList1[1]
        return tempList

    def boolterm(self):

        self.andlist  = ['', '']

        tempList = self.boolfactor()
        self.andlist = list(tempList)
        while self.checkToken(TokenType.AND):
            self.inter.backpatch(self.andlist[0], self.inter.nextquad())
            tempList1 = self.boolfactor()
            self.inter.mergelist(self.andlist[1], tempList1[1])
            self.qlist[0] = list(tempList1[0][:])
        return self.andlist 

    def boolfactor(self):
        self.notList = ['', '']
        if self.checkToken(TokenType.NOT):
            tempvar = self.condition()
            # Invert true and false list pointer
            temppointer = tempvar[1]
            tempvar[1] = tempvar[0]
            tempvar[0] = temppointer
            self.notList[0]  = self.inter.makelist(self.inter.nextquad())
            self.expression()
            self.notList[1]  = self.inter.makelist(self.inter.nextquad())
            self.inter.genquad('jmp', '', '', '')
            return tempvar
        else: 
            return self.notList

    # One of the following statements...
    def statement(self):
        #print("ENTER-STATEMENTS")
        #print("--------------------")

        # First token must be "PROGRAM"
        if self.checkToken(TokenType.PROGRAM):
            print("STATEMENT-PROGRAM")
            print("--------------------")
            if self.curToken.lineNo != 0:
               self.abort(str(self.curToken.lineNo + 1) + " --> The declaration of the program must be in the first line")
            print("Program "+ self.curToken.tokenString)
            self.inter.setNameTable(self.curToken.tokenString)
            self.nextToken() 
            if self.checkToken(TokenType.IDENT):
                #self.checkToken(TokenType.IDENT)
                self.programName = self.curToken.tokenString
                print("Program "+ self.curToken.tokenString)
                self.inter.setNameTable(self.programName) 
                self.nextToken()
            else:
                self.abort(str(self.curToken.lineNo + 1) + " --> Invalid program name")     

        # "PRINT" (expression | string) 
        elif self.checkToken(TokenType.PRINT):
            print("STATEMENT-PRINT")
            print("--------------------")
            self.nextToken()
            self.match(TokenType.PARENTHESIS_OPEN)
            if self.curToken.tokenString in self.declaredNames:
                self.recurtion()
                if self.checkToken(TokenType.COMMA):
                    self.match(TokenType.COMMA)
                    self.recurtion()  
            if self.checkToken(TokenType.IDENT):
                self.statement()
  
        # "DECLARE" expression
        elif self.checkToken(TokenType.DECLARE):
            print("STATEMENT-DECLARE")
            print("--------------------")
            self.nextToken()
            if self.checkToken(TokenType.IDENT):
                if self.curToken.tokenString not in self.declaredVariables:
                    self.declaredVariables.add(self.curToken.tokenString)
                else:
                    self.abort(str(self.curToken.lineNo + 1) +" --> Variable alreade declared")
                self.nextToken()
                while not self.checkToken(TokenType.SEMI_COLON):
                    if self.checkToken(TokenType.COMMA):
                        self.nextToken()
                        if self.checkToken(TokenType.IDENT):
                            if self.curToken.tokenString not in self.declaredVariables:
                                self.declaredVariables.add(self.curToken.tokenString.lower())
                    self.nextToken()
                if self.checkToken(TokenType.SEMI_COLON):
                    self.nextToken()

        # "IF" comparison.
        elif self.checkToken(TokenType.IF):
            print("STATEMENT-IF")
            print("--------------------")
            self.backList = self.condition()
            self.nextToken()
            if not self.checkToken(TokenType.PARENTHESIS_OPEN):
                self.abort(str(self.curToken.lineNo + 1) + ' --> Parenthesis missing after while')
            if self.checkToken(TokenType.PARENTHESIS_OPEN):
                self.nextToken()
                self.comparison()
            self.match(TokenType.PARENTHESIS_CLOSE)
            self.match(TokenType.ANGLED_BRACKET_OPEN)
            self.inter.makelist(self.inter.nextquad())
            self.inter.backpatch(self.backList[0], self.inter.nextquad())
            self.inter.genquad('jmp', '', '', '')
            self.statement()
            self.inter.backpatch(self.backList[1], self.inter.nextquad())
 
        # "ELSE" implementation of "IF".
        elif self.checkToken(TokenType.ELSE):
            print("STATEMENT-ELSE")
            print("--------------------")
            self.nextToken()
            self.inter.genquad('jmp', '', '', '')
            self.inter.backpatch(self.backList[0], self.inter.nextquad())
            self.match(TokenType.ANGLED_BRACKET_OPEN)

        # "WHILE" comparison 
        elif self.checkToken(TokenType.WHILE):
            print("STATEMENT-WHILE")
            print("--------------------")
            q = self.inter.nextquad()
            bList = self.condition()
            self.inter.genquad('jump', '', '', '')
            self.inter.backpatch(bList[0], self.inter.nextquad())
            self.nextToken()
            if not self.checkToken(TokenType.PARENTHESIS_OPEN):
                self.abort(str(self.curToken.lineNo + 1) + ' --> Parenthesis missing after while')
            if self.checkToken(TokenType.PARENTHESIS_OPEN):
                self.nextToken()
                self.comparison()
            self.match(TokenType.PARENTHESIS_CLOSE)
            self.match(TokenType.ANGLED_BRACKET_OPEN)

        # "SWITCHCASE" with "CASE"
        elif self.checkToken(TokenType.SWITCHCASE):
            print("STATEMENT-SWITCHCASE")
            print("--------------------")
            self.inter.genquad('jump', '', '', '')
            self.list2.append(self.inter.getNextQuad())
            self.list2.append(a)
            self.nextToken()
            while not self.checkToken(TokenType.DEFAULT):
                self.match(TokenType.CASE)
                self.match(TokenType.PARENTHESIS_OPEN)
                self.comparison()
                self.match(TokenType.PARENTHESIS_CLOSE)
                self.statement()
                temp = self.inter.getNextQuad()
                self.inter.backpatch(self.list2, temp)
            if self.checkToken(TokenType.DEFAULT):
                self.match(TokenType.DEFAULT)
                if self.checkToken(TokenType.SEMI_COLON):
                    self.statement()
                else:
                    self.comparison()
                    temp = self.inter.getNextQuad()
                    self.inter.backpatch(self.list2, temp)
                    self.statement()

        # "FORCASE" wtih "CASE"
        elif self.checkToken(TokenType.FORCASE):
            print("STATEMENT-FORCASE")
            print("--------------------")
            self.inter.genquad('jump', '', '', '')
            self.list2.append(self.inter.getNextQuad())
            self.nextToken()
            while not self.checkToken(TokenType.DEFAULT) and not self.checkToken(TokenType.SEMI_COLON):
                self.match(TokenType.CASE)
                self.match(TokenType.PARENTHESIS_OPEN)
                self.comparison()
                self.match(TokenType.PARENTHESIS_CLOSE)
                self.statement()
                temp = self.inter.getNextQuad()
                self.inter.backpatch(self.list2, temp)
            if self.checkToken(TokenType.DEFAULT):
                self.match(TokenType.DEFAULT)
                if self.checkToken(TokenType.SEMI_COLON):
                    self.statement()
                else:
                    self.comparison()
                    temp1 = self.inter.getNextQuad()
                    self.inter.backpatch(self.list2, temp1)
                    self.statement()

        # "INCASE" wtih "CASE"
        elif self.checkToken(TokenType.INCASE):
            print("STATEMENT-INCASE")
            print("--------------------")
            self.inter.genquad('jump', '', '', '')
            self.list2.append(self.inter.getNextQuad())
            self.nextToken()
            while self.checkToken(TokenType.SEMI_COLON):
                self.match(TokenType.CASE)
                self.match(TokenType.PARENTHESIS_OPEN)
                self.comparison()
                self.match(TokenType.PARENTHESIS_CLOSE)
                self.statement()
                temp = self.inter.getNextQuad()
                self.inter.backpatch(self.list2, temp)
       
        # "FUNCTION" 
        elif self.checkToken(TokenType.FUNCTION):
            print("STATEMENT-FUNCTION")
            print("--------------------")
            self.inter.setNameTable(self.curToken.tokenString)
            self.nextToken()
            self.funcName = self.curToken.tokenString
            self.inter.setNameTable(self.funcName)
            self.inter.setParamTable(self.funcName)
            self.inter.genquad('begin_block', self.funcName, '','')
            self.list4.append(self.inter.getNextQuad())
            if self.checkToken(TokenType.IDENT):
                if self.curToken.tokenString not in self.declaredNames:
                    self.declaredNames.add(self.curToken.tokenString)
                self.match(TokenType.IDENT)
                self.match(TokenType.PARENTHESIS_OPEN)
                while not self.checkToken(TokenType.PARENTHESIS_CLOSE):
                    self.nextToken()
                    if self.checkToken(TokenType.IN):
                        self.nextToken()
                        tmp_0 = self.checkToken(TokenType.IDENT)
                        self.inter.setParamTable(tmp_0)
                        self.nextToken()
            if self.checkToken(TokenType.PARENTHESIS_CLOSE):
                self.match(TokenType.PARENTHESIS_CLOSE)
                self.match(TokenType.ANGLED_BRACKET_OPEN)
      
        # "PROCEDURE" uses "INOUT"
        elif self.checkToken(TokenType.PROCEDURE):
            print("STATEMENT-PROCEDURE")
            print("--------------------")
            self.inter.setNameTable(self.curToken.tokenString)
            print("Program "+ self.curToken.tokenString)
            self.nextToken()
            self.procName = self.curToken.tokenString
            self.inter.setNameTable(self.procName)
            self.inter.setParamTable(self.procName)
            self.inter.genquad('begin_block', self.procName, '',' ')
            self.list4.append(self.inter.getNextQuad())
            if self.checkToken(TokenType.IDENT):
                if self.curToken.tokenString not in self.declaredNames:
                    self.declaredNames.add(self.curToken.tokenString)
                self.match(TokenType.IDENT)
                self.match(TokenType.PARENTHESIS_OPEN)
                while not self.checkToken(TokenType.PARENTHESIS_CLOSE):
                    self.nextToken()
                    if self.checkToken(TokenType.INOUT):
                        self.nextToken()
                        tmp_1 = self.checkToken(TokenType.IDENT)
                        self.inter.setParamTable(tmp_1)
                if self.checkToken(TokenType.PARENTHESIS_CLOSE):
                    self.match(TokenType.PARENTHESIS_CLOSE)
                    self.match(TokenType.ANGLED_BRACKET_OPEN)

        # "CALL" a "FUNCTION"
        elif self.checkToken(TokenType.CALL):
            print("STATEMENT-CALL")
            print("--------------------")
            self.nextToken()
            if self.curToken.tokenString in self.declaredNames:
                self.match(TokenType.IDENT)
                self.match(TokenType.PARENTHESIS_OPEN)
                while not self.checkToken(TokenType.PARENTHESIS_CLOSE):
                    self.nextToken()
                    if self.checkToken(TokenType.IN):
                        self.nextToken()
                        self.checkToken(TokenType.IDENT)
                        s = self.curToken.tokenString
                        self.inter.genquad('par', s, 'REF', ' ' )
                        self.list4.append(self.inter.getNextQuad())

        # "RETURN" statement
        elif self.checkToken(TokenType.RETURN):
            print("STATEMENT-RETURN")
            print("--------------------")
            self.nextToken()
            self.match(TokenType.PARENTHESIS_OPEN)
            while not self.checkToken(TokenType.PARENTHESIS_CLOSE):
                if self.checkToken(TokenType.NUMBER):
                    self.abort(str(self.curToken.lineNo + 1) + ' --> Returning numbers is not allowed')
                elif self.curToken.tokenString not in self.declaredNames:
                    if self.curToken.tokenString in self.declaredVariables and self.calculations():
                        self.expression()
                        a = self.list[-1]
                        for i in range (0, len(self.inter.quads)):
                            for a in self.inter.quads[i][1]:
                                x = self.inter.quads[i][4]
                        self.inter.genquad('par', x, 'RET', ' ')
                        self.inter.setArguments("RET")
                        self.list4.append(self.inter.getNextQuad())
                        self.inter.genquad('end_block', self.funcName, '', ' ')
                        self.list4.append(self.inter.getNextQuad())
                    elif self.curToken.tokenString in self.declaredVariables and self.checkPeek(TokenType.EQUAL):
                        self.comparison()
                        b = self.list[-1]
                        for i in range (0, len(self.inter.quads)):
                            for b in self.inter.quads[i][1]:
                                x = self.inter.quads[i][4]
                        self.inter.genquad('par', x, 'RET', ' ')
                        self.inter.setArguments("RET")
                        self.list4.append(self.inter.getNextQuad())
                        self.inter.genquad('end_block', self.funcName, '', ' ')
                        self.list4.append(self.inter.getNextQuad())
                    elif self.curToken.tokenString in self.declaredVariables:
                        self.checkToken(TokenType.IDENT)
                        s = self.curToken.tokenString
                        self.inter.genquad('par', s, 'RET', ' ')
                        self.inter.setArguments("RET")
                        self.list4.append(self.inter.getNextQuad())
                        self.inter.genquad('end_block', self.funcName, '', ' ')
                        self.list4.append(self.inter.getNextQuad())
                elif self.curToken.tokenString in self.declaredNames:
                    self.match(TokenType.IDENT)
                    self.match(TokenType.PARENTHESIS_OPEN)
                    self.match(TokenType.IN)
                    while not self.checkToken(TokenType.PARENTHESIS_CLOSE):
                        if self.curToken.tokenString in self.declaredVariables and self.calculations():
                            self.expression()
                            a = self.list[-1]
                            for i in range (0, len(self.inter.quads)):
                                for a in self.inter.quads[i][1]:
                                    x = self.inter.quads[i][4]
                            self.inter.genquad('par', x, 'RET', ' ')
                            self.inter.setArguments("RET")
                            self.list4.append(self.inter.getNextQuad())
                            self.inter.genquad('end_block', self.funcName, '', '')
                            self.list4.append(self.inter.getNextQuad())
                        elif self.curToken.tokenString in self.declaredVariables and self.checkPeek(TokenType.EQUAL):
                            self.comparison()
                            b = self.list[-1]
                            for i in range (0, len(self.inter.quads)):
                                for b in self.inter.quads[i][1]:
                                    x = self.inter.quads[i][4]
                            self.inter.genquad('par', x, 'RET', ' ')
                            self.inter.setArguments("RET")
                            self.list4.append(self.inter.getNextQuad())
                            self.inter.genquad('end_block', self.funcName, '', '')
                            self.list4.append(self.inter.getNextQuad())
                        elif self.curToken.tokenString in self.declaredVariables: 
                            self.match(TokenType.IDENT)
                    if self.checkToken(TokenType.PARENTHESIS_CLOSE):
                        self.nextToken()
                else: 
                    self.abort(str(self.curToken.lineNo + 1) +" --> Invalid use of return")
            
        # "INPUT" ident.
        elif self.checkToken(TokenType.INPUT):
            print("STATEMENT-INPUT")
            print("--------------------")
            self.nextToken()
            self.match(TokenType.PARENTHESIS_OPEN)
            if self.checkToken(TokenType.IDENT):
                s = self.curToken.tokenString
                self.inter.genquad('par', s, 'REF', '')
                self.inter.setArguments("REF")
                self.list4.append(self.inter.getNextQuad())
                if self.curToken.tokenString not in self.declaredVariables:
                    self.abort(str(self.curToken.lineNo + 1) +" --> Variable has not been declared")
                self.nextToken()
                self.match(TokenType.PARENTHESIS_CLOSE)
                self.match(TokenType.SEMI_COLON)
            else:
                self.abort(str(self.curToken.lineNo + 1) +" --> Illegal use of input keyword")       
           
        # "NOT" logical expression
        elif self.checkToken(TokenType.NOT):
           # print("STATEMENT-NOT")
            self.boolfactor()

        # "AND" logical expression
        elif self.checkToken(TokenType.AND):
            #print("STATEMENT-AND")
            self.boolterm()
                    
        # "OR" logical expression
        elif self.checkToken(TokenType.OR):
            #print("STATEMENT-OR")
            self.condition()
        
        # "ANGLED BRACKETS" opening handler.
        elif self.checkToken(TokenType.ANGLED_BRACKET_OPEN):
            #print("ANGLE BRACKET OPEN")
            self.inter.genquad('begin_block', self.programName, '', '')
            self.inter.setNameTable("Main")
            print("Main")
            self.list4.append(self.inter.getNextQuad())
            self.nextToken()
            self.statement()

        # "ANGLED BRACKETS" closing handler.
        elif self.checkToken(TokenType.ANGLED_BRACKET_CLOSE):
            #print("ANGLE BRACKET CLOSE")
            self.nextToken()
            if self.checkToken(TokenType.ANGLED_BRACKET_OPEN):
                self.nextToken()
            elif self.checkToken(TokenType.ANGLED_BRACKET_CLOSE):
                self.nextToken()
            else:
                self.statement()

        # 'PARENTHESIS' closing operation.
        elif self.checkToken(TokenType.PARENTHESIS_CLOSE):
             #print("PARENTHESIS CLOSE")
             self.nextToken()
             if self.checkToken(TokenType.SEMI_COLON):
                self.nextToken()
             elif self.checkToken(TokenType.PARENTHESIS_CLOSE):
                self.nextToken()
                self.match(TokenType.SEMI_COLON)

        # "IDENT" handler.
        elif self.checkToken(TokenType.IDENT):
            #print("IDENT")
            if self.curToken.tokenString not in self.declaredVariables:
                self.abort(str(self.curToken.lineNo + 1) +" --> Unidentified variable: "+ self.curToken.tokenString+" Please declare it")
            argument = self.curToken.tokenString
            self.nextToken()
            if self.checkToken(TokenType.ASSIGN):
                assignment = self.curToken.tokenString
                self.nextToken()
                self.expression()
                if self.list != []:
                    a = self.list[len(self.list)-1]
                    for i in range (0, len(self.inter.quads)):
                        for a in self.inter.quads[i][1]:
                            x = self.inter.quads[i][4]
                    self.inter.genquad(assignment, x,'', argument)
                    self.list4.append(self.inter.getNextQuad())
                self.match(TokenType.SEMI_COLON)
            elif self.checkToken(TokenType.ANGLED_BRACKET_CLOSE):
                self.match(TokenType.ANGLED_BRACKET_CLOSE)

        # 'IN' operation handler
        elif self.checkToken(TokenType.IN):
           # print("IN")
            self.match(TokenType.IN)
            self.checkToken(TokenType.IDENT)
            s = self.curToken.tokenString
            self.inter.setParamTable(s)
            self.inter.genquad('par', s, 'REF', '')
            self.inter.setArguments("REF")
            self.list4.append(self.inter.getNextQuad())
            self.statement()

        # 'COMMA' operation handler
        elif self.checkToken(TokenType.COMMA):
            #print("COMMA")
            self.match(TokenType.COMMA)

        # 'NEWLINE' handler
        elif self.checkToken(TokenType.NEWLINE):
            #print('NEWLINE')
            self.match(TokenType.NEWLINE)
        
        # 'SEMI-COLON' 
        elif self.checkToken(TokenType.SEMI_COLON):

            self.nextToken()     

        # 'EOP' handler
        elif self.checkToken(TokenType.EOP): 
            self.inter.genquad('halt', '', '', '')
            self.tmp3 = self.inter.getNextQuad()
            self.list2.append(self.tmp3)
            for i in range (0, len(self.inter.quads)):
                if self.inter.quads[i][0] == self.tmp:
                    self.inter.backpatch(self.list3, self.tmp1+10)
                elif self.inter.quads[i][0] == self.tmp1:
                    self.inter.backpatch(self.list2, self.tmp3)
                elif self.inter.quads[i][0] == self.tmp2:
                    self.inter.backpatch(self.list2, self.tmp3)
            self.inter.genquad('end_block', self.programName, '', '')
            self.list4.append(self.inter.getNextQuad())
            list12 = self.inter.merge(self.list,self.list2)
            list34 = self.inter.merge(self.list3,self.list4)
            finalList = self.inter.merge(list12, list34)
            for i in range (0, len(finalList)):
                self.inter.makelist(finalList[i])
            self.nextToken()
        
        # This is not a valid statement.
        else:
           
            self.abort(str(self.curToken.lineNo +1) + " --> Invalid statement at " +'(' +self.curToken.tokenString.lower() +')'+ " (" + self.curToken.tokenType.name + ")")
           
class Intermediate:

    def __init__(self):
        self.indexOfquad = [] # stores the index of the quads
        self.quads = [] # stores the quads
        self.label = 0
        self.count = 0
        self.nameTable = []
        self.paramTable = []
        self.arguments = []
        self.empty_list = [] # empty list 
        self.thisLine = 0

    def nextquad(self):
        self.label += 10
        return self.label
    
    def genquad(self, op, x, y, z):
        self.nextQuad = self.nextquad()
        self.quads.append([self.nextQuad,op,x,y,z])
        return self.quads

    # Creates new temporary values
    def newtemp(self):
        self.count +=1
        s= "T_"+str(self.count)
        return s

    # Creates an empty list
    def emptylist(self):
        return self.empty_list

    # Createas a list of the tags of quads
    def makelist(self, x):
        for i in range (0,len(self.quads)):
            if x == self.quads[i][0]:
              self.indexOfquad.append(self.quads[i][0])
              return self.indexOfquad[i]

    # Merges 2 lists    
    def merge(self, list1, list2):
        self.final_list=list(itertools.chain(list1, list2))
        list1.clear() #deletes contents of list1
        list2.clear() #deletes contents of list2
        return self.final_list

    # Patches lists witout the last value     
    def backpatch(self, list, z):
        for x in range (0, len(self.quads)):
            if self.quads[x][4] == '':
                if str(self.quads[x][0]) in list:
                    self.quads[x][4] = z
    
    # Set and get the functionNames.
    def setNameTable(self,a):
        self.nameTable.append(a.isupper())
        print("Intermediate add: ", self.nameTable)

    # Set and get the parameters of the function.
    def setParamTable(self,a):
        self.paramTable.append(a.isupper())

    #Set and get the aguments( CV | RET | REF ).
    def setArguments(self, a):
        self.arguments.append(a.isupper())

    # Returns the next quad number.
    def getNextQuad(self):
        return self.nextQuad
  
class SymbolType(enum.Enum):
    PROGRAM = 0
    FUNCTION = 1
    PROCEDURE = 2
    MAIN = 3
    
class SymbolTable:
# A namespace table for a block.

    def __init__(self, filename, Intermediate, nTable, pTable, aTable):
        self.inter = Intermediate
        self.filename = filename
        self.scope = 0
        self.nTable = nTable
        self.pTable = pTable
        self.aTable = aTable
        self._index = 0
        self.curSymbol
        self.nested = 0
        self.curNestingLevel = 0
        self.items = []
        self.symbolTable = []

    def getScope(self):
        return self.pTable[self.curNestingLevel]
        for item in self.pTable:
            if self.nested == self.curNestingLevel:
                return item

    def addEntity(self, entity):
        scope = self.getScope()
        self.symbolTable.append(entity)

    def removeScope(self):
        tempScope = self.symbolTable.pop()
        for obj in tempScope:
            print(obj)

    def checkSymbol(self, symbol):
        if symbol in SymbolType:
            return symbol
        else:
            return -1

    def abort(self, message):
        sys.exit("Symbol error. " + message)

    #Return the type of the symbol table. Possible values are 'program', 'procedure', and 'function'.
    def get_type(self):
        print('The list is: ', self.nTable)  
        if "PROGRAM" in self.nTable:
            index = self.nTable.index("PROGRAM")
            if index< len(self.nTable):
                self.addEntity(self.nTable[index])
                return self.nTable[index]
            print ("\nProgram\n")
        if "FUNCTION" in self.nTable:
            index = self.nTable.index("FUNCTION")
            if index< len(self.nTable):
                self.addEntity(self.nTable[index])
                self.nested+=1
                self.addEntity(self.nTable[index])
                return self.nTable[index]
            print("\nFunction\n")
        if "MAIN" in self.nTable:
            index = self.nTable.index("MAIN")
            if index< len(self.nTable):
                self.addEntity(self.nTable[index])
                self.nested+=1
                return self.nTable[index]
            print("\nMain\n")
        if "PROCEDURE" in self.nTable:
            index = self.nTable.index("PROCEDURE")
            if index< len(self.nTable):
                self.addEntity(self.nTable[index])
                self.nested+=1
                return self.nTable[index]
            print("\nProcedure\n")

    #Return the name of the program, the name of the function or the name of the procedure 
    def get_name(self):
        print('The list is: ', self.nTable)  
        if "PROGRAM" in self.nTable:
            self.nested+=1
            index = self.nTable.index("PROGRAM")
            if index< len(self.nTable):
                return self.nTable[index+1]
                print ("\n" + self.nTable[index+1])
        if "FUNCTION" in self.nTable:
            self.is_nested+=1
            index = self.nTable.index("FUNCTION")
            if index< len(self.nTable):
                return self.nTable[index+1]
                print ("\n" + self.nTable[index+1])
        if "PROCEDURE" in self.nTable:
            self.is_nested+=1
            index = self.nTable.index("PROCEDURE")
            if index< len(self.nTable):
                return self.nTable[index+1]
                print ("\n" + self.nTable[index+1])
    
    #Return True if the block is a nested procedure or function.
    def is_nested(self): 
        if self.nested >0:
            return self.nested
        else:
            return 0
    
    #Return a list of names of symbols in this table.
    def get_identifiers(self):
        if "FUNCTION" in self.nTable:
            index = self.pTable.index("FUNCTION")
            if index< len(self.pTable):
                while self.checkSymbol(self.pTable[index+1])!= -1:
                    print ("\n" + self.pTable[index+1])
        if "PROCEDURE" in self.pTable:
            index = self.pTable.index("PROCEDURE")
            if index< len(self.pTable):
                while self.checkSymbol(self.pTable[index+1])!= -1:
                    print ("\n" + self.pTable[index+1])

    def is_main(self):
        if "MAIN" in self.nTable:
            index = self.nTable.index("MAIN")
            if index< len(self.nTable):
                return self.nTable[index]
            print("\nMain\n")

    def createTable(self):
        for nItem in self.nTable:
            for pItem in self.pTable:
                for aItem in self.aTable:
                    while nItem!=pItem!=aItem:
                        self.symbolTable.append(nItem)
                        self.symbolTable.append(pItem)
                        self.symbolTable.append(aItem)

    def writeSFile(self):
        variablesList = []

        sFile = open(self.filename+".c", "w")
        sFile.write("Symbol Table\n\n")

        for i in range (0, self.curNestingLevel+1):
            
            type = self.get_type()
            name = self.get_name()
            nestingLevel = self.is_nested()
            if type == "PROGRAM" and nestingLevel == 0:
                sFile.write(type+' '+ name + ' Nesting level' , nestingLevel)
            if type == "FUNCTION" and nestingLevel != 0:
                sFile.write(type+' '+ name + ' Nesting level' , nestingLevel)
            if type == "PROCEDURE" and nestingLevel != 0:
                sFile.write(type+' '+ name + ' Nesting level' , nestingLevel)
            if type == "MAIN" and nestingLevel != 0:
                sFile.write(type+' '+ name + ' Nesting level' , nestingLevel)

        sFile.close() 
    
def generateCFile(inter, File, name):
    variablesList = []

    cFile = open(name+".c", "w")
    cFile.write("int main(){\n\n\t")
    # Scan for all variables in intermiediate code,
    # declare and instantiate them to value 0.


    for i in range (0, len(inter.quads)):

        op = inter.quads[i][1]
        if (op == 'call' or op == 'par'):
            continue

        if (op == 'jmp'): continue
        if op == 'begin_block' or op == '' or op == 'end_block':continue
        x = str(inter.quads[i][2])
        y = str(inter.quads[i][3])
        z = str(inter.quads[i][4])
        
        if (not x.isdigit()):
            if x not in variablesList:
                variablesList.append(x)

        if (not y.isdigit()):
            if y not in variablesList:
                variablesList.append(y)

        if (not z.isdigit()):
            if z not in variablesList:
                variablesList.append(z)


    # If we found some variables.
    if (variablesList):

        # Filter out compiler's tokens.
        variablesList =  [c for c in variablesList if c != '' and c != '-1']
        cFile.write("int ")
        
        for item in variablesList:
            if item != '':
                if item == variablesList[-1]:
                    cFile.write(item+';')
                else:
                    cFile.write(item + ", ")
        
        cFile.write("\n\tL_0: \n")


    # Check for 'empty' jumps, created by exit statements outside repeat statements
    for i in range (0, len(inter.quads)):
        op = inter.quads[i][1]
        if (op == 'EXITjmp'):
            lab = inter.quads[i][4]
            if (lab == ''):
                print("Error: exit statement declared outside of repeat statement")
                cFile.close()
                return (1)


    # Commands to c equivalent code file
    for i in range (0, len(inter.quads)):
        label = str(inter.quads[i][0])
        op = inter.quads[i][1]
        x = str(inter.quads[i][2])
        y = str(inter.quads[i][3])
        z = str(inter.quads[i][4])
        if z == '':
            z=str(0)
        if (op == '+'):
            cFile.write("\tL_" + label + ":\t" + z +  " = " + x + " + " + y + ";\n")

        elif (op == '*'):
            cFile.write("\tL_" + label + ":\t" + z + " = " + x + " * " + y + ";\n")  

        elif (op == '-'):
            cFile.write("\tL_" + label + ":\t" + z + " = " + x + " - " + y + ";\n") 

        elif (op == '/'):
            cFile.write("\tL_" + label +  ":\t" + z + " = " + x + " / " + y + ";\n")

        elif (op == ':='):
            cFile.write("\tL_" + label + ":\t" + z + " = " + x + ";\n")

        elif (op == '='):
            cFile.write("\tL_" + label + ":\tif (" + x + " == " + y + ") goto L_" + z + ";\n")

        elif (op == '<'):
            cFile.write("\tL_" + label + ":\tif (" + x + " < " + y + ") goto L_" + z + ";\n")

        elif (op == '>'):
            cFile.write("\tL_" + label + ":\tif (" + x + " > " + y + ") goto L_" + z + ";\n")

        elif (op == '<='):
            cFile.write("\tL_" + label + ":\tif (" + x + " <= " + y + ") goto L_" + z + ";\n")

        elif (op == '>='):
            cFile.write("\tL_" + label + ":\tif (" + x + " >= " + y + ") goto L_" + z + ";\n")

        elif (op == '<>'):
            cFile.write("\tL_" + label + ":\tif (" + x + " != " + y + ") goto L_" + z + ";\n")

        elif (op == 'jmp'):
            cFile.write("\tL_" + label + ":\tgoto " + "L_" + z + ";\n")

        elif (op == 'input'):
            cFile.write("\tL_" + label + ":\tscanf(&" + x + ");\n")           

        elif (op == 'print'):
            cFile.write("\tL_" + label + ":\tprintf(" + x + ");\n") 

        elif (op == 'ret' or op == 'call'):
            continue

    cFile.write("}")
    cFile.close()     

def main():
    print("\n---------------------")
    print("| Compiler Starting |")
    print("---------------------\n")
    if len(sys.argv) != 2:
        sys.exit("Error: Compiler needs source file as argument.")
    with open(sys.argv[1], 'r') as inputFile:
        input = inputFile.read()
    
    lexer = Lexer(input) 
    intermediate = Intermediate()
    parser = Parser(lexer, intermediate)
    parser.program()
    s = os.path.basename(sys.argv[1])
    x = s.split('.')
    name = x[0]
    symbolTable = SymbolTable(name, intermediate, intermediate.nameTable, intermediate.paramTable, intermediate.arguments)
    symbolTable.writeSFile()

    with open(name+'.int', 'w') as intFile:
        for listitem in intermediate.quads:
            intFile.write('%s\n' % listitem)
    print(intermediate.quads)
    generateCFile(intermediate, intFile, name)

if __name__ == '__main__':
    main()