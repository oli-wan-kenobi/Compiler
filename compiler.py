#Vasileiadou Stavoula 2582 cse32582
#!/usr/bin/python3

import sys, traceback, enum
from itertools import count
import itertools

import string

class Lexer:
        
    # Constructor.
    def __init__(self, input):
        self.source = input # Source code to lex as a string. Append a newline to simplify lexing/parsing the last token/statement.
        print("Self sourse: \n " + self.source)
        self.count = 0
        self.read_char = ""   # Current character in the string.
        self.curPos = -1    # Current position in the string.
        self.startIdentPos = 0
        self.nextChar()
         
    # Process the next character.
    def nextChar(self):
        self.curPos += 1
        if self.curPos >= len(self.source):
            self.read_char = "\0"  # EOF
        else:
            self.read_char = self.source[self.curPos]
            #print("\nEPOMENOS XARAKTHRAS ---->       " + self.read_char)
            if self.read_char =="\n":
                    self.count += 1 

    # Return the lookahead character.
    def peek(self):
        if self.curPos + 1 >= len(self.source):
            return "\0"
        return self.source[self.curPos+1]
      
    # Error message handler.
    def abort(self, message):
        sys.exit("Lexing error. Line: " + message )

    # Skip whitespace.
    def skipWhitespace(self):
        while self.read_char == " " or self.read_char == "\t" or self.read_char == "\r":
            self.nextChar()

    # Skip comments in the code.
    def skipComment(self):
        if self.read_char == "#":
            lastChar = self.read_char
            self.nextChar()
            while self.read_char != "#":
                self.nextChar()
            if self.read_char == "#":
                self.nextChar()          
    
    # Return the next token.
    def getToken(self):
        
        # Skip whitespases.
        self.skipWhitespace()
        
        # Skip comments.
        self.skipComment()
        token = None
        
        # Calculations.
        if self.read_char == "+":
            token = Token(self.read_char, TokenType.PLUS, self.count)
        elif self.read_char == "-":
            token = Token(self.read_char, TokenType.MINUS, self.count)
        elif self.read_char == "*":
            token = Token(self.read_char, TokenType.ASTERISK, self.count)
        elif self.read_char == "/":
            token = Token(self.read_char, TokenType.SLASH, self.count)
            
        # Relations.
        elif self.read_char == "=":
            token = Token(self.read_char, TokenType.EQUAL, self.count)
        elif self.read_char == ">":
            # Check whether this is token is > or >=
            if self.peek() == "=":
                lastChar = self.read_char
                self.nextChar()
                token = Token(lastChar + self.read_char, TokenType.GREATEREQUAL, self.count)
            else:
                token = Token(self.read_char, TokenType.GREATER, self.count)
        elif self.read_char == "<":
            # Check whether this token is < or <=
            if self.peek() == "=":
                lastChar = self.read_char
                self.nextChar()
                token = Token(lastChar + self.read_char, TokenType.LESSEQUAL, self.count)
            # Check whether this token is < or <>
            elif self.peek() == ">":
                lastChar = self.read_char
                self.nextChar()
                token = Token(lastChar + self.read_char, TokenType.INBETWEEN, self.count)
            else:
                token = Token(self.read_char, TokenType.LESS, self.count)
        
        # Deviders.
        elif self.read_char == "\n":
            token = Token(self.read_char, TokenType.NEWLINE, self.count)
        elif self.read_char == ",":
            token = Token(self.read_char, TokenType.COMMA, self.count)
        elif self.read_char == ";":
            token = Token(self.read_char, TokenType.SEMI_COLON, self.count)
        elif self.read_char == ":":
            if self.peek() == "=":
                lastChar = self.read_char
                self.nextChar()
                token = Token(lastChar + self.read_char, TokenType.ASSIGN, self.count)
            else: 
                token = Token(self.read_char, TokenType.COLON, self.count)

        
        # Groups.
        # Brackets open operation.
        elif self.read_char == "[":
            token = Token(self.read_char, TokenType.SQUARE_BRACKET_OPEN, self.count)
            if self.read_char == "\n":
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
        elif self.read_char =="]":
            token = Token(self.read_char, TokenType.SQUARE_BRACKET_CLOSE, self.count)
 

        # Parenthesis open operations.
        elif self.read_char == "(":
            token = Token(self.read_char, TokenType.PARENTHESIS_OPEN, self.count)
            if self.read_char == "\n":
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
                    while self.read_char != ")": 
                        self.nextChar()
                    tokText = self.source[startPos : self.curPos + 1]
                    token = Token(tokText, TokenType.NUMBER, self.count)

        # Parenthesis close operations.
        elif self.read_char ==")":
            token = Token(self.read_char, TokenType.PARENTHESIS_CLOSE, self.count)
 
        # Angled brackets.
        elif self.read_char == "{":
            self.nextChar()
            if self.read_char == "\n":
                self.nextChar()                
                if self.read_char  != "}":
                    self.nextChar()                     
                token = Token(self.read_char, TokenType.ANGLED_BRACKET_OPEN, self.count)       
            else:
                self.abort(str(self.count) + " --> Illegal expression " + self.read_char) 
        elif self.read_char == "}":
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
        elif self.read_char == ".":
            token = Token(self.read_char, TokenType.EOP, self.count)


        # EOF.
        elif self.read_char == "\0":
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
    #Assignment
    ASSIGN = 501

class Parser:

    # Constructor.
    def __init__(self, Lexer):
        self.lexer = Lexer   
        self.declaredVariables = set() # All variables we have declared so far.
        self.functionDeclaredNames = set()
        self.funcVariables = set()
        self.procedureDeclaredNames = set()
        self.procedureVariables = set()
        self.curToken = None
        self.peekToken = None
        self.curNestingLevel = 0 
        self.operVal = " "
        self.firstVal = " "
        self.secondVal = " "
        self.thirdVal = " "
        self.truelist = []
        self.falselist = []
        self.nextToken()
        self.nextToken()    # Call this twice to initialize current and peek.
        self.inter = Intermediate

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
        return self.checkToken(TokenType.GREATER) or self.checkToken(TokenType.GREATEREQUAL) or self.checkToken(TokenType.LESS) or self.checkToken(TokenType.LESSEQUAL) or self.checkToken(TokenType.EQUAL) or self.checkToken(TokenType.INBETWEEN) or self.checkToken(TokenType.ASSIGN)

    # Error message handler.
    def abort(self, message):
        sys.exit("Parser error. Line: " + message)

    # Production rules.

    # program ::= {statement}
    def program(self):
        print("STARTS THE PROGRAM")
        # Parse all the statements in the program.
        while not self.checkToken(TokenType.EOF):
            self.statement()

    # comparison ::= expression ((">" | ">=" | "<" | "<=" | "<>") expression)+
    def comparison(self):
        print("In comparison 1: " +self.curToken.tokenString)
        self.firstVal = self.curToken.tokenString
        self.expression()
        print("In comparison 2: " +self.curToken.tokenString)
        #Intermediate.genQuad(_,_,,firstVal )
        # Must be at least one comparison operator and another expression.
        if self.isComparisonOperator():
            self.operVal = self.curToken.tokenString
            print("In comparison 3: " +self.curToken.tokenString)
            self.nextToken()
            print("In comparison 4: " +self.curToken.tokenString)
            self.secondVal = self.curToken.tokenString
            self.expression()
            print("In comparison 5: " +self.curToken.tokenString)
        else:
            self.abort(str(self.curToken.lineNo + 1) + " --> Expected comparison operator at: " + self.curToken.tokenString)
        # Can have 0 or more comparison operator and expressions.
        while self.isComparisonOperator():
            print("In comparison 6: " +self.curToken.tokenString)
            self.nextToken()
            print("In comparison 7: " +self.curToken.tokenString)
            self.expression()
            print("In comparison 8: " +self.curToken.tokenString)
        
    # expression ::= term {( "-" | "+" ) term}
    def expression(self):
        print("In expression 1: " +self.curToken.tokenString)
        self.term()
        print("In expression 2: " +self.curToken.tokenString)
        # Can have 0 or more +/- and expressions.
        while self.checkToken(TokenType.PLUS) or self.checkToken(TokenType.MINUS):
            print("In expression 3: " +self.curToken.tokenString)
            self.operVal = self.curToken.tokenString
            self.nextToken()
            print("In expression 4: " +self.curToken.tokenString)
            self.term()
            print("In expression 5: " +self.curToken.tokenString)

    # term ::= unary {( "/" | "*" ) unary}
    def term(self):
        print("In term 1: " +self.curToken.tokenString)
        self.unary()
        print("In temp 2: " +self.curToken.tokenString)
        # Can have 0 or more *// and expressions.
        while self.checkToken(TokenType.ASTERISK) or self.checkToken(TokenType.SLASH):
            print("In temp 3: " +self.curToken.tokenString)
            self.operVal = self.curToken.tokenString
            self.nextToken()
            print("In temp 4: " +self.curToken.tokenString)
            self.unary()
            print("In temp 5: " +self.curToken.tokenString)

    # unary ::= ["+" | "-"] primary
    def unary(self):
        print("In unary 1: " +self.curToken.tokenString)
        # Optional unary +/-
        if self.checkToken(TokenType.PLUS) or self.checkToken(TokenType.MINUS):
            print("In unary 2: " +self.curToken.tokenString)
            self.nextToken()        
            print("In unary 3: " +self.curToken.tokenString)
        print("In unary 4: " +self.curToken.tokenString)
        self.primary()
        print("In unary 5: " +self.curToken.tokenString)

    # primary ::= number | ident
    def primary(self):
        print("In primary 1: " +self.curToken.tokenString)
        if self.checkToken(TokenType.NUMBER): 
            print("In primary 2: " +self.curToken.tokenString)
            self.nextToken()
            print("In primary 3: " +self.curToken.tokenString)
        elif self.checkToken(TokenType.IDENT):
            print("In primary 4: " +self.curToken.tokenString)
            # Ensure the variable already exists.
            if self.curToken.tokenString not in self.declaredVariables and self.curToken.tokenString not in self.funcVariables and self.curToken.tokenString not in self.procedureVariables and self.curToken.tokenString not in self.functionDeclaredNames:
                self.abort(str(self.curToken.lineNo + 1) + " --> Referencing variable before assignment: " + self.curToken.tokenString)
            print("In primary 5: " +self.curToken.tokenString)
            self.thirdVal = self.curToken.tokenString
            self.nextToken()
            print("In primary 6: " +self.curToken.tokenString)
        else:
            self.abort(str(self.curToken.lineNo+1) + " --> (in ASCII) Unexpected token at " + str(ord(self.curToken.tokenString.lower())))
    
    def calculations(self):
        return self.checkToken(TokenType.PLUS) or self.checkToken(TokenType.MINUS) or self.checkToken(TokenType.ASTERISK) or self.checkToken(TokenType.SLASH)

    def possitive_negative_nums(self):
        return self.checkToken(TokenType.PLUS) or self.checkToken(TokenType.MINUS)

    # recurtion in print and return
    def recurtion(self):
        if self.curToken.tokenString in self.functionDeclaredNames:
            self.nextToken()
            if not self.checkToken(TokenType.PARENTHESIS_OPEN):
                self.abort(str(self.curToken.lineNo + 1) + " --> Opening parenthesis missing")
            self.nextToken()
            while not self.checkToken(TokenType.PARENTHESIS_CLOSE):
                if not self.checkToken(TokenType.IN):
                    self.abort(str(self.curToken.lineNo + 1) + " --> In missing")
                self.nextToken()
                if not self.checkToken(TokenType.IDENT):
                    self.abort(str(self.curToken.lineNo + 1) + " --> Identifier missing")
                if self.curToken.tokenString not in self.declaredVariables and self.curToken.tokenString not in self.funcVariables and self.curToken.tokenString not in self.procedureVariables:
                    self.abort(str(self.curToken.lineNo + 1) + " --> Unidentified variable")
                self.nextToken()
                if self.checkToken(TokenType.COMMA):
                    self.nextToken()
                if self.checkToken(TokenType.PARENTHESIS_CLOSE):
                    self.nextToken()
                    self.nextToken()
                    break
                if self.calculations(): 
                    self.nextToken()
                    if self.checkToken(TokenType.NUMBER):
                        self.nextToken()
                if self.checkPeek(TokenType.COMMA):
                    self.nextToken()
                if self.checkToken(TokenType.PARENTHESIS_CLOSE):
                    if self.calculations:
                        self.nextToken()
                        if self.checkToken(TokenType.IDENT):
                            if self.curToken.tokenString in self.functionDeclaredNames:
                                self.nextToken()
                                if not self.checkToken(TokenType.PARENTHESIS_OPEN):
                                    self.abort(str(self.curToken.lineNo + 1) + " --> Opening parenthesis missing")
                                self.nextToken()
                                while not self.checkToken(TokenType.PARENTHESIS_CLOSE):
                                    self.nextToken()
                                    if not self.checkToken(TokenType.IN):
                                        self.abort(str(self.curToken.lineNo + 1) + " --> Angled bracket missing after function")
                                    self.nextToken()
                                    if not self.checkToken(TokenType.IDENT):
                                        self.abort(str(self.curToken.lineNo + 1) + " --> Identifier missing")
                                    if self.curToken.tokenString not in self.declaredVariables:
                                        self.abort(str(self.curToken.lineNo + 1) + " --> Unidentified variable")
                                    self.nextToken()
                                    if not self.checkPeek(TokenType.COMMA):
                                        self.abort(str(self.curToken.lineNo + 1) + " --> Comma is needed to seperate the identifiers")
                                    self.nextToken()

    # One of the following statements...
    def statement(self):
        #print("ENTER-STATEMENTS")
        
        # First token must be "PROGRAM"
        if self.checkToken(TokenType.PROGRAM):
            print("STATEMENT-PROGRAM")
            if self.curToken.lineNo != 0:
               self.abort(str(self.curToken.lineNo + 1) + " --> The declaration of the program must be in the first line")
            self.nextToken()    
            if self.checkToken(TokenType.IDENT):
                self.match(TokenType.IDENT)
                self.nextToken()
            else:
                self.abort(str(self.curToken.lineNo + 1) + " --> Invalid program name")     

        # "DECLARE" expression
        elif self.checkToken(TokenType.DECLARE):
            print("STATEMENT-DECLARE")
            self.nextToken()
            if not self.checkToken(TokenType.IDENT):
                self.abort(str(self.curToken.lineNo + 1) + " --> Identifier missing")
            else:
                if self.curToken.tokenString not in self.declaredVariables:
                    self.declaredVariables.add(self.curToken.tokenString.lower())
                else:
                    self.abort(str(self.curToken.lineNo + 1) +" --> Variable alreade declared")
                self.nextToken() 
                while not self.checkToken(TokenType.SEMI_COLON): 
                    if self.checkToken(TokenType.COMMA):
                        self.nextToken()
                        if self.checkToken(TokenType.IDENT):
                            if self.curToken.tokenString not in self.declaredVariables:
                                self.declaredVariables.add(self.curToken.tokenString.lower())
                            else:
                                self.abort(str(self.curToken.lineNo + 1) +" --> Variable alreade declared")
                        self.nextToken()
                    else:
                        self.abort(str(self.curToken.lineNo + 1) +" --> comma is missing")
                    
                if self.checkToken(TokenType.SEMI_COLON):
                    self.nextToken()

        # "IF" comparison.
        elif self.checkToken(TokenType.IF):
            print("STATEMENT-IF")
            Intermediate.genQuad("begin_block", "main if", " ", " ")
            thisQuad = Intermediate.nextQuad()
            self.nextToken()
            if not self.checkToken(TokenType.PARENTHESIS_OPEN):
                self.abort(str(self.curToken.lineNo + 1) + " --> Opening parenthesis missing after if")
            self.nextToken()
            self.comparison()
            Intermediate.genQuad(self.operVal, self.secondVal, self.thirdVal, self.firstVal)
            thisQuad = Intermediate.nextQuad()
            self.nextToken()
            Intermediate.backpatch(self.truelist.append(thisQuad), Intermediate.nextQuad())
            aList = Intermediate.makeList(Intermediate.nextQuad())
            Intermediate.genQuad("jump", " ", " ", " ")
            Intermediate.backpatch(self.falselist.append(Intermediate.nextQuad()),Intermediate.nextQuad())
            Intermediate.backpatch(aList, Intermediate.nextQuad())
            thisQuad = Intermediate.nextQuad()
            Intermediate.genQuad("halt", " ", " ", " ")
            thisQuad = Intermediate.nextQuad()
            Intermediate.genQuad("end_block", "main if", " ", " ")

        # "ELSE" implementation of "IF".
        elif self.checkToken(TokenType.ELSE):
            Intermediate.genQuad("begin_block", "main else", " ", " ")
            thisQuad = Intermediate.nextQuad()
            self.nextToken()
            if self.checkToken(TokenType.NEWLINE):
                self.nextToken()
            if not self.checkToken(TokenType.ANGLED_BRACKET_OPEN):
                self.abort(str(self.curToken.lineNo + 1) + " --> Angled bracket missing after else")
            self.nextToken() 
            Intermediate.backpatch(self.truelist.append(thisQuad), Intermediate.nextQuad())
            bList = Intermediate.makeList(Intermediate.nextQuad())
            Intermediate.genQuad("jump", " ", " ", " ")
            Intermediate.backpatch(self.falselist.append(Intermediate.nextQuad()),Intermediate.nextQuad())
            aList = Intermediate.mergeList(aList, bList)
            Intermediate.backpatch(aList, Intermediate.nextQuad())      
            thisQuad = Intermediate.nextQuad()
            Intermediate.genQuad("halt", " ", " ", " ")
            thisQuad = Intermediate.nextQuad()
            Intermediate.genQuad("end_block", "main else", " ", " ")

        # "WHILE" comparison 
        elif self.checkToken(TokenType.WHILE):
            print("STATEMENT-WHILE")
            self.inter.genQuad("begin_block", "main while", " ", " ")
            thisQuad = Intermediate.nextQuad()
            self.nextToken()
            if not self.checkToken(TokenType.PARENTHESIS_OPEN):
                self.abort(str(self.curToken.lineNo + 1) + " --> Opening parenthesis missing after while")
            self.nextToken()
            if self.checkToken(TokenType.IDENT):
                if self.curToken.tokenString in self.functionDeclaredNames:
                    self.recurtion()
                    self.nextToken()
                else:
                    self.comparison()
                    Intermediate.genQuad(self.operVal, self.secondVal, self.thirdVal, self.firstVal)
                    thisQuad = Intermediate.nextQuad()
            else:
                self.comparison()
                
                Intermediate.genQuad(self.operVal, self.secondVal, self.thirdVal, self.firstVal)
                thisQuad = Intermediate.nextQuad()
            if not self.checkToken(TokenType.PARENTHESIS_CLOSE):
                 self.abort(str(self.curToken.lineNo + 1) + " --> Closing parenthesis missing after while")
            self.nextToken()
            if self.checkToken(TokenType.NEWLINE):
                self.nextToken()
            if not self.checkToken(TokenType.ANGLED_BRACKET_OPEN):
                self.abort(str(self.curToken.lineNo + 1) + " --> Angled bracket missing after while")
            Intermediate.backpatch(self.truelist.append(thisQuad), Intermediate.nextQuad())
            Intermediate.genQuad("jump"," "," ", thisQuad)
            Intermediate.backpatch(self.falselist.append(Intermediate.nextQuad()), Intermediate.nextQuad())
            thisQuad = Intermediate.nextQuad()
            Intermediate.genQuad("halt", " ", " ", " ")
            thisQuad = Intermediate.nextQuad()
            Intermediate.genQuad("end_block", "main while", " ", " ")
            self.nextToken()

         # "SWITCHCASE" with "CASE" and "DEFAULT"
        elif self.checkToken(TokenType.SWITCHCASE):
            print("STATEMENT-SWITCHCASE")
            Intermediate.genQuad("begin_block", "main switchcase", " ", " ")
            thisQuad = Intermediate.nextQuad()
            self.nextToken()
            while not self.checkToken(TokenType.DEFAULT):
                if not self.checkToken(TokenType.CASE):
                     self.abort(str(self.curToken.lineNo + 1) + " --> Case missing after switchcase")
                self.nextToken()
                if not self.checkToken(TokenType.PARENTHESIS_OPEN):
                     self.abort(str(self.curToken.lineNo + 1) + " --> Parenthesis missing after case")
                self.nextToken()
                self.comparison()
                Intermediate.genQuad(self.operVal, self.secondVal, self.thirdVal, self.firstVal)
                thisQuad = Intermediate.nextQuad()
                self.match(TokenType.PARENTHESIS_CLOSE)
                self.nextToken()
                break
            if self.checkToken(TokenType.DEFAULT):
                self.match(TokenType.DEFAULT)
                self.nextToken()
            exitList = Intermediate.emptyList()
            Intermediate.backpatch(self.truelist.append(thisQuad),Intermediate.nextQuad())
            list1 = Intermediate.makeList(Intermediate.nextQuad())
            Intermediate.genQuad("jump", " ", " ", " ")
            exitList = Intermediate.mergeList(exitList, list1)
            Intermediate.backpatch(self.falselist.append(Intermediate.nextQuad()), Intermediate.nextQuad())
            Intermediate.backpatch(exitList, Intermediate.nextQuad())
            thisQuad = Intermediate.nextQuad()
            Intermediate.genQuad("halt", " ", " ", " ")
            thisQuad = Intermediate.nextQuad()
            Intermediate.genQuad("end_block", "main switchcase", " ", " ")

        # "FORCASE" wtih "CASE" and "DEFAULT"
        elif self.checkToken(TokenType.FORCASE):
            print("STATEMENT-FORCASE")
            Intermediate.genQuad("begin_block", "main forcase", " ", " ")
            thisQuad = Intermediate.nextQuad()
            self.nextToken()
            if self.checkToken(TokenType.NEWLINE):
                self.nextToken()
            while not self.checkToken(TokenType.DEFAULT):
                if not self.checkToken(TokenType.CASE):
                     self.abort(str(self.curToken.lineNo + 1) + " --> Case missing after forcase")
                self.nextToken()
                if not self.checkToken(TokenType.PARENTHESIS_OPEN):
                     self.abort(str(self.curToken.lineNo + 1) + " --> Parenthesis missing after case")
                self.nextToken()
                self.comparison()
                Intermediate.genQuad(self.operVal, self.secondVal, self.thirdVal, self.firstVal)
                thisQuad = Intermediate.nextQuad()
                self.match(TokenType.PARENTHESIS_CLOSE)
                self.nextToken()
                break
            Intermediate.backpatch(self.truelist.append(thisQuad),Intermediate.nextQuad())
            Intermediate.genQuad("jump", " ", " ", " ")
            Intermediate.backpatch(self.falselist.append(Intermediate.nextQuad()), Intermediate.nextQuad())
            thisQuad = Intermediate.nextQuad()
            Intermediate.genQuad("halt", " ", " ", " ")
            thisQuad = Intermediate.nextQuad()
            Intermediate.genQuad("end_block", "main forcase", " ", " ")
                       
        # "INCASE" wtih "CASE"
        elif self.checkToken(TokenType.INCASE):
            print("STATEMENT-INCASE")
            Intermediate.genQuad("begin_block", "main incase", " ", " ")
            thisQuad = Intermediate.nextQuad()
            self.nextToken()
            while not self.checkToken(TokenType.DEFAULT):
                if not self.checkToken(TokenType.CASE):
                     self.abort(str(self.curToken.lineNo + 1) + " --> Case missing after incase")
                self.nextToken()
                if not self.checkToken(TokenType.PARENTHESIS_OPEN):
                     self.abort(str(self.curToken.lineNo + 1) + " --> Parenthesis missing after case")
                self.nextToken()
                self.comparison()
                Intermediate.genQuad(self.operVal, self.secondVal, self.thirdVal, self.firstVal)
                thisQuad = Intermediate.nextQuad()
                self.match(TokenType.PARENTHESIS_CLOSE)
                self.nextToken()
                break
            flag = Intermediate.newTemp()
            firstCond = thisQuad
            Intermediate.genQuad(":=","0","_",flag)
            Intermediate.backpatch(self.truelist.append(Intermediate.nextQuad()), Intermediate.nextQuad())
            Intermediate.genQuad(":=","1","_",flag)
            Intermediate.backpatch(self.falselist.append(Intermediate.nextQuad()), Intermediate.nextQuad())
            Intermediate.genQuad(":=","1",flag, firstCond)
            thisQuad = Intermediate.nextQuad()
            Intermediate.genQuad("halt", " ", " ", " ")
            thisQuad = Intermediate.nextQuad()
            Intermediate.genQuad("end_block", "main incase", " ", " ")

        # "NOT" logical expression
        elif self.checkToken(TokenType.NOT):
            print("STATEMENT-NOT")
            Intermediate.genQuad("not"," "," "," ")
            thisQuad = Intermediate.nextQuad()
            self.match(TokenType.NOT)
            if self.checkToken(TokenType.NUMBER):
                self.abort(str(self.curToken.lineNo + 1) + " --> Keyword \"not\" used only in logical operations")
            self.nextToken()
        
        # "AND" logical expression
        elif self.checkToken(TokenType.AND):
            print("STATEMENT-AND")
            Intermediate.genQuad("and"," "," "," ")
            thisQuad = Intermediate.nextQuad()
            self.match(TokenType.AND)
            if self.checkToken(TokenType.NUMBER):
                self.abort(str(self.curToken.lineNo + 1) + " --> Keyword \"not\" used only in logical operations")
            self.nextToken()

        # "OR" logical expression
        elif self.checkToken(TokenType.OR):
            print("STATEMENT-OR")
            Intermediate.genQuad("or"," "," "," ")
            thisQuad = Intermediate.nextQuad()
            self.match(TokenType.OR)
            if self.checkToken(TokenType.NUMBER):
                self.abort(str(self.curToken.lineNo + 1) + " --> Keyword \"not\" used only in logical operations")
            self.nextToken()

        # "FUNCTION" statement
        elif self.checkToken(TokenType.FUNCTION):
            print("STATEMENT-FUNCTION")
            self.curNestingLevel += 1
            self.nextToken()
            if not self.checkToken(TokenType.IDENT):
                self.abort(str(self.curToken.lineNo + 1) + " --> Identifier missing")
            if self.curToken.tokenString not in self.functionDeclaredNames:
                self.functionDeclaredNames.add(self.curToken.tokenString)
            self.nextToken()
            if not self.checkToken(TokenType.PARENTHESIS_OPEN):
                self.abort(str(self.curToken.lineNo + 1) + " --> Parenthesis missing after function declaration")
            self.nextToken()
            if self.checkToken(TokenType.NEWLINE):
                self.nextToken()
            while not self.checkToken(TokenType.PARENTHESIS_CLOSE):
                if not self.checkToken(TokenType.IN):
                    self.abort(str(self.curToken.lineNo + 1) + " --> in missing in the parenthesis")
                self.nextToken()
                if not self.checkToken(TokenType.IDENT):
                    self.abort(str(self.curToken.lineNo + 1) + " --> Identifier missing")
                if self.curToken.tokenString not in self.funcVariables:
                    self.funcVariables.add(self.curToken.tokenString)
                self.nextToken()
                if self.checkToken(TokenType.COMMA):
                    self.nextToken()
                elif self.checkToken(TokenType.PARENTHESIS_CLOSE):
                    self.nextToken()                    
                    if not self.checkPeek(TokenType.ANGLED_BRACKET_OPEN):
                        self.abort(str(self.curToken.lineNo + 1) + " --> Angled bracket missing after function")
                    self.nextToken()
                    self.nextToken()
                    break
                   
        # "PROCEDURE" uses "INOUT"
        elif self.checkToken(TokenType.PROCEDURE):
            print("STATEMENT-PROCEDURE")
            self.curNestingLevel += 1
            self.nextToken()
            if not self.checkToken(TokenType.IDENT):
                self.abort(str(self.curToken.lineNo + 1) + " --> Identifier missing")
            if self.curToken.tokenString not in self.functionDeclaredNames:
                self.functionDeclaredNames.add(self.curToken.tokenString)
            self.nextToken()
            if not self.match(TokenType.PARENTHESIS_OPEN):
                self.abort(str(self.curToken.lineNo + 1) + " --> Parenthesis missing after procedure declaration")
            self.nextToken()
            if self.checkToken(TokenType.NEWLINE):
                self.nextToken()
            while not self.checkToken(TokenType.PARENTHESIS_CLOSE):
                self.nextToken()
                if not self.checkToken(TokenType.INOUT):
                    self.abort(str(self.curToken.lineNo + 1) + " --> Angled bracket missing after procedure")
                self.nextToken()
                if not self.checkToken(TokenType.IDENT):
                    self.abort(str(self.curToken.lineNo + 1) + " --> Identifier missing")
                if self.curToken.tokenString not in self.procedureVariables:
                    self.procedureVariables.add(self.curToken.tokenString)
                self.nextToken()
                if self.checkToken(TokenType.COMMA):
                    self.nextToken()
                elif self.checkToken(TokenType.PARENTHESIS_CLOSE):
                    self.nextToken()
                    if not self.checkPeek(TokenType.ANGLED_BRACKET_OPEN):
                        self.abort(str(self.curToken.lineNo + 1) + " --> Angled bracket missing after function")
                    self.nextToken()
                    self.nextToken()
                    break

        # "CALL" a "PROCEDURE"
        elif self.checkToken(TokenType.CALL):
            print("STATEMENT-CALL")
            self.nextToken()
            if not self.checkToken(TokenType.IDENT):
                self.abort(str(self.curToken.lineNo + 1) + " --> identifier missing")
            if self.curToken.tokenString not in self.procedureDeclaredNames:
                self.abort(str(self.curToken.lineNo + 1) + " --> The identifier is not declared")
            self.nextToken()
            if not self.checkToken(TokenType.PARENTHESIS_OPEN):
                self.abort(str(self.curToken.lineNo + 1) + " --> parenthesis missing")
            self.nextToken()
            if not self.checkToken(TokenType.INOUT):
                self.abort(str(self.curToken.lineNo + 1) + " --> The \"inout\" keyword is missing")
            self.nextToken()
            if not self.checkToken(TokenType.IDENT):
                self.abort(str(self.curToken.lineNo + 1) + " --> Identifier missing")
            if self.curToken.tokenString not in self.declaredVariables:
                self.abort(str(self.curToken.lineNo + 1) + " --> The identifier is not declared")

        # "RETURN" statement
        elif self.checkToken(TokenType.RETURN):
            print("STATEMENT-RETURN")
            self.nextToken()
            if not self.checkToken(TokenType.PARENTHESIS_OPEN):
                self.abort(str(self.curToken.lineNo + 1) + " --> Parenthesis missing after return")
            self.nextToken()
            if self.checkToken(TokenType.PARENTHESIS_CLOSE):
                self.abort(str(self.curToken.lineNo + 1) + " --> Returning argument missing")
            if self.comparison():
                Intermediate.genQuad(self.operVal, self.secondVal, self.thirdVal, self.firstVal)
                thisQuad = Intermediate.nextQuad()
                Intermediate.genQuad("par", self.firstVal, "ret", " ")
                thisQuad = Intermediate.nextQuad()
                self.nextToken()
                if not self.checkToken(TokenType.PARENTHESIS_CLOSE):
                    self.abort(str(self.curToken.lineNo + 1) + " --> Closing parenthesis missing")
            elif self.checkToken(TokenType.IDENT):
                if self.recurtion():
                    self.nextToken()
                elif self.curToken.tokenString in self.declaredVariables or self.curToken.tokenString in self.funcVariables or self.curToken.tokenString in self.procedureVariables:
                    
                    Intermediate.genQuad("par", self.curToken.tokenString, "ret", " ")
                    thisQuad = Intermediate.nextQuad()
                    self.nextToken()
                    if not self.checkToken(TokenType.PARENTHESIS_CLOSE):
                       self.abort(str(self.curToken.lineNo + 1) + " --> Parenthesis is missing after return")
            elif self.checkToken(TokenType.NUMBER):
                
                Intermediate.genQuad("par", self.curToken.tokenString, "ret", " ")
                thisQuad = Intermediate.nextQuad()
                self.nextToken()
                if not self.checkToken(TokenType.PARENTHESIS_CLOSE):
                    self.abort(str(self.curToken.lineNo + 1) + " --> Closing parenthesis missing")

        # "INPUT" ident.
        elif self.checkToken(TokenType.INPUT):
            print("STATEMENT-INPUT")
            self.nextToken()
            self.match(TokenType.PARENTHESIS_OPEN)
            if self.checkToken(TokenType.IDENT):
                if self.curToken.tokenString not in self.declaredVariables:
                    self.abort(str(self.curToken.lineNo + 1) +" --> Variable has not been declared")
                self.nextToken()
                self.match(TokenType.PARENTHESIS_CLOSE)
                self.match(TokenType.SEMI_COLON)
                self.nextToken()
            else:
                self.abort(str(self.curToken.lineNo + 1) +" --> Illegal use of input keyword")

        # "PRINT" (expression | string) 
        elif self.checkToken(TokenType.PRINT):
            print("STATEMENT-PRINT")
            self.nextToken()
            if not self.checkToken(TokenType.PARENTHESIS_OPEN):
                self.abort(str(self.curToken.lineNo + 1) +" --> Parenthesis missing")
            self.nextToken() 
            if self.checkToken(TokenType.PARENTHESIS_CLOSE):
                self.abort(str(self.curToken.lineNo + 1) + " --> Print argument missing")
            if self.checkToken(TokenType.IDENT):
                if self.curToken.tokenString in self.declaredVariables or self.curToken.tokenString in self.funcVariables or self.curToken.tokenString in self.procedureVariables:
                    self.nextToken()
                    if not self.checkToken(TokenType.PARENTHESIS_CLOSE):
                       self.abort(str(self.curToken.lineNo + 1) + " --> Parenthesis is missing after return")
                    self.nextToken()
                    if self.checkToken(TokenType.SEMI_COLON):
                        self.nextToken()
                elif self.recurtion():
                    self.nextToken()
            elif self.checkToken(TokenType.NUMBER):
                self.nextToken()
                if not self.checkToken(TokenType.PARENTHESIS_CLOSE):
                    self.abort(str(self.curToken.lineNo + 1) + " --> Closing parenthesis missing")
            elif self.expression():
                self.nextToken()
                if not self.checkToken(TokenType.PARENTHESIS_CLOSE):
                    self.abort(str(self.curToken.lineNo + 1) + " --> Closing parenthesis missing")        

        # HANDLERS

        # "IDENT" handler.
        elif self.checkToken(TokenType.IDENT):
            print("IDENT")
            if self.curToken.tokenString not in self.declaredVariables:
                self.abort(str(self.curToken.lineNo + 1) +" --> Unidentified variable: "+ self.curToken.tokenString+" Please declare it")
            if self.comparison():
                thisQuad = Intermediate.nextQuad()
                Intermediate.genQuad(self.operVal, self.secondVal, self.thirdVal, self.firstVal)
                self.nextToken()
            self.nextToken()

        # "CASE" handler
        elif self.checkToken(TokenType.CASE):
            print("CASE")
            self.nextToken()
            if not self.checkToken(TokenType.PARENTHESIS_OPEN):
                    self.abort(str(self.curToken.lineNo + 1) + " --> Parenthesis missing after case")
            self.nextToken()
            self.comparison()
            thisQuad = Intermediate.nextQuad()
            Intermediate.genQuad(self.operVal, self.secondVal, self.thirdVal, self.firstVal)
            self.match(TokenType.PARENTHESIS_CLOSE)
            self.nextToken()
       
        # "DEFAULT" handler
        elif self.checkToken(TokenType.DEFAULT):
            print("DEFAULT")
            self.nextToken()
        
        # "IN" handler
        elif self.checkToken(TokenType.IN):
            print("IN")
            self.nextToken()
            if self.checkToken(TokenType.IDENT):
                self.statement()

        # "ANGLED BRACKETS" opening handler
        elif self.checkToken(TokenType.ANGLED_BRACKET_OPEN):
            print("ANGLED BRACKETS OPEN")
           
            
            self.nextToken()

        # "ANGLED BRACKETS" closing handler.
        elif self.checkToken(TokenType.ANGLED_BRACKET_CLOSE):
            print("ANGLED BRACKETS CLOSE")
            self.match(TokenType.ANGLED_BRACKET_CLOSE)
            if self.checkToken(TokenType.NEWLINE):
                self.nextToken()
                if self.checkToken(TokenType.ANGLED_BRACKET_OPEN):
                    self.nextToken()
                elif self.checkToken(TokenType.ANGLED_BRACKET_CLOSE):
                    self.nextToken()
                elif self.checkToken(TokenType.FUNCTION):
                    self.statement()
                elif self.checkToken(TokenType.SEMI_COLON):
                    self.nextToken() 
                elif self.checkToken(TokenType.EOP):  
                    self.nextToken()        
                elif self.checkPeek(TokenType.ELSE):
                    self.statement()
            elif self.checkToken(TokenType.ANGLED_BRACKET_OPEN):
                self.nextToken()
            elif self.checkToken(TokenType.ANGLED_BRACKET_CLOSE):
                self.nextToken()
            elif self.checkToken(TokenType.FUNCTION):
                self.statement()
            elif self.checkToken(TokenType.SEMI_COLON):
                self.nextToken()
                
            elif self.checkToken(TokenType.EOP):  
                self.nextToken()       
            elif self.checkPeek(TokenType.ELSE):
                self.statement()
            else:
                self.abort(str(self.curToken.lineNo) + " --> Invalid use of angled brackets! Semi-colon or dot missing!") 
        
        # "PARENTHESIS CLOSE" handler
        elif self.checkToken(TokenType.PARENTHESIS_CLOSE):
            print("PARENTHESIS OPEN")
            self.nextToken()

        # "SQUARE BRACKETS" opening handler.
        elif self.checkToken(TokenType.SQUARE_BRACKET_OPEN):
            print("SQUARE BRACKETS OPEN")
            self.nextToken()
            if self.checkToken(TokenType.NUMBER):
                self.abort(str(self.curToken.lineNo +1) + " --> Illegal use of brackets!")

        # "ASSIGN" handler.
        elif self.checkToken(TokenType.ASSIGN):
            print("ASSIGN")
            self.nextToken()
            if self.possitive_negative_nums:
                self.nextToken()
            elif not self.checkToken(TokenType.IDENT):
                self.abort(str(self.curToken.lineNo +1) + " --> Idetifier missing from assignment")
            elif self.checkToken(TokenType.IDENT):
                self.nextToken()    
            elif not self.checkToken(TokenType.NUMBER):
                self.abort(str(self.curToken.lineNo +1) + " --> Number missing from assignment")
            self.nextToken()
            
        # "SEMI-COLON" handler
        elif self.checkToken(TokenType.SEMI_COLON):
            print("SEMI - COLON")
            self.nextToken()

        # "NEWLINE" handler
        elif self.checkToken(TokenType.NEWLINE):
            self.nextToken()
  
        # "EOP" handler
        elif self.checkToken(TokenType.EOP): 
            self.nextToken()

        # This is not a valid statement.
        else:           
            self.abort(str(self.curToken.lineNo +1) + " --> Invalid statement at " +"(" +self.curToken.tokenString.lower() +")"+ " (" + self.curToken.tokenType.name + ")")
           
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
        self.inFile = None
        self.listc = 1
        self.tempQuad = []
    
    def nextQuad(self):
        return self.label

    def genQuad(self, op, x, y, z):
        self.tempQuad.append[self.nextQuad,op,x,y,z]
        self.label += 10 # adding 10 to go to next label
        self.quads.append(self.tempQuad)
        return self.quads   

    # Creates new temporary values
    def newTemp(self):
        self.count += 1
        tmp = "T_" + str(self.count)
        SymTable.addEntity(SymTable.TempVar(tmp, SymTable.getCurrentOffset()))
        return tmp

    # Creates an empty list
    def emptyList(self):
        return []

    # Createas a list of the tags of quads
    def makeList(self, list1):
        return [list1]

    # Merges 2 lists    
    def mergeList(self, list1, list2):
        if (not list2 is None):
            list1.extend(list2)

    # Patches lists witout the last value     
    def backpatch(self, list, x):
        for i in range (0, len(self.quads)):
            if (self.quads[i][4] ==" "):
                if(self.quads[i][0] in list):
                    self.quads[i][4] = x 
        return 
    
    def printQuad(self,item):
        print(getattr(item, 'label'), getattr(item, 'op'), getattr(item, 'x'),
		getattr(item, 'y'), getattr(item, 'z'))

    def writeQuad(self, item):
        quadString = (str(getattr(item, 'label')) + " " +
        str(getattr(item, 'op')) + " " +
        str(getattr(item, 'x'))  + " " +
        str(getattr(item, 'y'))  + " " +
        str(getattr(item, 'z'))  + '\n')
        self.inFile.write(quadString)

    def GenerateIntFile(self):
        # Print generated quads to screen and output file
        self.inFile = open("test.int", "w")
        for item in self.quads:
            self.printQuad(item)
            self.writeQuad(item)
        self.inFile.close()

    def generateCFile(self):
        variablesList = []

        cFile = open("test.c", "w")
        cFile.write("int main(){\n\n\t")
        # Scan for all variables in intermiediate code,
        # declare and instantiate them to value 0.

        for i in range (0, len(self.quads)):

            op = self.quads[i][1]
            if (op == 'call' or op == 'par'):
                continue

            if (op == 'jmp'): continue
            if op == 'begin_block' or op == '' or op == 'end_block':continue
            x = str(self.quads[i][2])
            y = str(self.quads[i][3])
            z = str(self.quads[i][4])
        
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
        for i in range (0, len(self.quads)):
            op = self.quads[i][1]
            if (op == 'EXITjmp'):
                lab = self.quads[i][4]
                if (lab == ''):
                    print("Error: exit statement declared outside of repeat statement")
                    cFile.close()


        # Commands to c equivalent code file
        for i in range (0, len(self.quads)):
            label = str(self.quads[i][0])
            op = self.quads[i][1]
            x = str(self.quads[i][2])
            y = str(self.quads[i][3])
            z = str(self.quads[i][4])
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
  
class SymType(enum.Enum):
    PROGRAM = 0
    FUNCTION = 1
    PROCEDURE = 2
    MAIN = 3
    
class SymTable:
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
        for obj in self.items:
            print(obj)

    def checkSymbol(self, symbol):
        if symbol in SymType:
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

def main():

    print("\n---------------------")
    print("| Compiler Starting |")
    print("---------------------\n")
    
    if len(sys.argv) != 2:
        sys.exit("Error: Compiler needs source file as argument.")
    with open(sys.argv[1], "r") as inputFile:
        input = inputFile.read()

    # Initialize lexer and parser.
    print("Lexer Starts\n")
    lexer = Lexer(input)
    print("Parser Starts\n")
    parser = Parser(lexer)
    parser.program()
    print("Intermediate Code Generator Starts")
    inter = Intermediate()
    print("Symbol Table Starts")
    #   symbolTable = SymTable()
    print("\nProgram Complete With No Errors!\n")

if __name__ == "__main__":
    main()