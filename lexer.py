#!/usr/bin/env python3
"""
Лексический анализатор для языка Grishex.

Преобразует исходный код в последовательность токенов.
"""

import re
from enum import Enum, auto


class TokenType(Enum):
    """Перечисление типов токенов в языке Grishex."""
    
    # Специальные токены
    EOF = auto()          # Конец файла
    ILLEGAL = auto()      # Неизвестный символ
    
    # Идентификаторы и литералы
    IDENT = auto()        # Идентификатор
    INT = auto()          # Целое число
    STRING = auto()       # Строковой литерал
    FLOAT = auto()        # Число с плавающей точкой
    
    # Операторы
    ASSIGN = auto()       # =
    PLUS = auto()         # +
    MINUS = auto()        # -
    BANG = auto()         # !
    ASTERISK = auto()     # *
    SLASH = auto()        # /
    
    # Операторы сравнения
    EQ = auto()           # ==
    NEQ = auto()          # !=
    LT = auto()           # <
    GT = auto()           # >
    LTE = auto()          # <=
    GTE = auto()          # >=
    
    # Разделители
    COMMA = auto()        # ,
    SEMICOLON = auto()    # ;
    COLON = auto()        # :
    LPAREN = auto()       # (
    RPAREN = auto()       # )
    LBRACE = auto()       # {
    RBRACE = auto()       # }
    LBRACKET = auto()     # [
    RBRACKET = auto()     # ]
    DOT = auto()          # .
    ARROW = auto()        # ->
    
    # Ключевые слова
    FUNCTION = auto()     # function
    CONTRACT = auto()     # contract
    PRAGMA = auto()       # pragma
    LET = auto()          # let
    TRUE = auto()         # true
    FALSE = auto()        # false
    IF = auto()           # if
    ELSE = auto()         # else
    WHILE = auto()        # while
    FOR = auto()          # for
    FOREACH = auto()      # foreach
    RETURN = auto()       # return
    INTERFACE = auto()    # interface
    STRUCT = auto()       # struct
    ENUM = auto()         # enum
    STATE = auto()        # state
    VIEW = auto()         # view
    PRIVATE = auto()      # private
    CONSTRUCTOR = auto()  # constructor
    EVENT = auto()        # event
    REQUIRE = auto()      # require
    ASSERT = auto()       # assert
    REVERT = auto()       # revert
    EMIT = auto()         # emit
    TRY = auto()          # try
    CATCH = auto()        # catch
    SELF = auto()         # self
    
    # Типы данных
    INT_TYPE = auto()     # int
    UINT_TYPE = auto()    # uint
    BOOL_TYPE = auto()    # bool
    ADDRESS_TYPE = auto() # address
    STRING_TYPE = auto()  # string
    BYTES_TYPE = auto()   # bytes
    HASH_TYPE = auto()    # hash
    ARRAY_TYPE = auto()   # array
    MAP_TYPE = auto()     # map


class Token:
    """Представляет токен в исходном коде."""
    
    def __init__(self, token_type, literal, line=1, column=1):
        self.token_type = token_type
        self.literal = literal
        self.line = line
        self.column = column
    
    def __str__(self):
        return f"Token({self.token_type}, '{self.literal}', line={self.line}, column={self.column})"
    
    def __repr__(self):
        return self.__str__()


class Lexer:
    """Лексический анализатор для языка Grishex."""
    
    def __init__(self, input_text):
        self.input = input_text
        self.position = 0          # текущая позиция в input (указывает на текущий символ)
        self.read_position = 0     # текущая позиция чтения в input (после текущего символа)
        self.ch = ''               # текущий символ
        self.line = 1              # текущая строка
        self.column = 1            # текущая колонка
        
        # Ключевые слова
        self.keywords = {
            "function": TokenType.FUNCTION,
            "contract": TokenType.CONTRACT,
            "pragma": TokenType.PRAGMA,
            "let": TokenType.LET,
            "true": TokenType.TRUE,
            "false": TokenType.FALSE,
            "if": TokenType.IF,
            "else": TokenType.ELSE,
            "while": TokenType.WHILE,
            "for": TokenType.FOR,
            "foreach": TokenType.FOREACH,
            "return": TokenType.RETURN,
            "interface": TokenType.INTERFACE,
            "struct": TokenType.STRUCT,
            "enum": TokenType.ENUM,
            "state": TokenType.STATE,
            "view": TokenType.VIEW,
            "private": TokenType.PRIVATE,
            "constructor": TokenType.CONSTRUCTOR,
            "event": TokenType.EVENT,
            "require": TokenType.REQUIRE,
            "assert": TokenType.ASSERT,
            "revert": TokenType.REVERT,
            "emit": TokenType.EMIT,
            "try": TokenType.TRY,
            "catch": TokenType.CATCH,
            "self": TokenType.SELF,
            
            # Типы данных
            "int": TokenType.INT_TYPE,
            "uint": TokenType.UINT_TYPE,
            "bool": TokenType.BOOL_TYPE,
            "address": TokenType.ADDRESS_TYPE,
            "string": TokenType.STRING_TYPE,
            "bytes": TokenType.BYTES_TYPE,
            "hash": TokenType.HASH_TYPE,
            "array": TokenType.ARRAY_TYPE,
            "map": TokenType.MAP_TYPE,
        }
        
        self.read_char()
    
    def read_char(self):
        """Читает следующий символ и обновляет позицию."""
        if self.read_position >= len(self.input):
            self.ch = ''  # EOF
        else:
            self.ch = self.input[self.read_position]
        
        # Обновляем позицию и колонку
        self.position = self.read_position
        self.read_position += 1
        self.column += 1
        
        # Проверяем перенос строки
        if self.ch == '\n':
            self.line += 1
            self.column = 0
    
    def peek_char(self):
        """Возвращает следующий символ без обновления позиции."""
        if self.read_position >= len(self.input):
            return ''
        else:
            return self.input[self.read_position]
    
    def skip_whitespace(self):
        """Пропускает пробельные символы."""
        while self.ch.isspace():
            self.read_char()
    
    def skip_comment(self):
        """Пропускает комментарий."""
        # Однострочный комментарий
        if self.ch == '/' and self.peek_char() == '/':
            while self.ch != '\n' and self.ch != '':
                self.read_char()
            # Перенос строки обработается при следующем вызове read_char
        
        # Многострочный комментарий
        elif self.ch == '/' and self.peek_char() == '*':
            self.read_char()  # пропускаем /
            self.read_char()  # пропускаем *
            
            while not (self.ch == '*' and self.peek_char() == '/'):
                if self.ch == '':  # EOF до окончания комментария
                    return
                self.read_char()
            
            self.read_char()  # пропускаем *
            self.read_char()  # пропускаем /
    
    def read_identifier(self):
        """Читает идентификатор."""
        position = self.position
        col_start = self.column
        
        # Идентификатор может начинаться с буквы или подчеркивания
        if self.ch.isalpha() or self.ch == '_':
            while self.ch.isalnum() or self.ch == '_':
                self.read_char()
            
            return self.input[position:self.position]
        
        return None
    
    def read_number(self):
        """Читает число (целое или с плавающей точкой)."""
        position = self.position
        col_start = self.column
        has_dot = False
        
        # Читаем цифры перед десятичной точкой
        while self.ch.isdigit():
            self.read_char()
        
        # Проверяем, есть ли десятичная точка
        if self.ch == '.' and self.peek_char().isdigit():
            has_dot = True
            self.read_char()  # пропускаем точку
            
            # Читаем цифры после десятичной точки
            while self.ch.isdigit():
                self.read_char()
        
        # Возвращаем прочитанное число
        return self.input[position:self.position]
    
    def read_string(self):
        """Читает строковой литерал."""
        position = self.position + 1  # Пропускаем начальные кавычки
        col_start = self.column
        
        self.read_char()  # Пропускаем открывающую кавычку
        
        # Читаем до закрывающей кавычки
        while self.ch != '"' and self.ch != '':
            # Обработка экранированных символов
            if self.ch == '\\' and self.peek_char() in ['"', '\\', 'n', 't', 'r']:
                self.read_char()  # Пропускаем обратный слеш
            self.read_char()
        
        if self.ch == '':  # EOF до закрывающей кавычки
            return self.input[position:self.position]
        
        result = self.input[position:self.position]
        self.read_char()  # Пропускаем закрывающую кавычку
        
        return result
    
    def next_token(self):
        """Возвращает следующий токен."""
        token = None
        
        # Пропускаем пробельные символы
        self.skip_whitespace()
        
        # Пропускаем комментарии
        if (self.ch == '/' and (self.peek_char() == '/' or self.peek_char() == '*')):
            self.skip_comment()
            self.skip_whitespace()
        
        # Запоминаем начальную позицию для токена
        line = self.line
        column = self.column
        
        # Проверяем различные типы токенов
        if self.ch == '=':
            if self.peek_char() == '=':
                ch = self.ch
                self.read_char()
                literal = ch + self.ch
                token = Token(TokenType.EQ, literal, line, column)
            else:
                token = Token(TokenType.ASSIGN, self.ch, line, column)
        
        elif self.ch == '+':
            token = Token(TokenType.PLUS, self.ch, line, column)
        
        elif self.ch == '-':
            if self.peek_char() == '>':
                ch = self.ch
                self.read_char()
                literal = ch + self.ch
                token = Token(TokenType.ARROW, literal, line, column)
            else:
                token = Token(TokenType.MINUS, self.ch, line, column)
        
        elif self.ch == '!':
            if self.peek_char() == '=':
                ch = self.ch
                self.read_char()
                literal = ch + self.ch
                token = Token(TokenType.NEQ, literal, line, column)
            else:
                token = Token(TokenType.BANG, self.ch, line, column)
        
        elif self.ch == '*':
            token = Token(TokenType.ASTERISK, self.ch, line, column)
        
        elif self.ch == '/':
            token = Token(TokenType.SLASH, self.ch, line, column)
        
        elif self.ch == '<':
            if self.peek_char() == '=':
                ch = self.ch
                self.read_char()
                literal = ch + self.ch
                token = Token(TokenType.LTE, literal, line, column)
            else:
                token = Token(TokenType.LT, self.ch, line, column)
        
        elif self.ch == '>':
            if self.peek_char() == '=':
                ch = self.ch
                self.read_char()
                literal = ch + self.ch
                token = Token(TokenType.GTE, literal, line, column)
            else:
                token = Token(TokenType.GT, self.ch, line, column)
        
        elif self.ch == ';':
            token = Token(TokenType.SEMICOLON, self.ch, line, column)
        
        elif self.ch == ':':
            token = Token(TokenType.COLON, self.ch, line, column)
        
        elif self.ch == ',':
            token = Token(TokenType.COMMA, self.ch, line, column)
        
        elif self.ch == '(':
            token = Token(TokenType.LPAREN, self.ch, line, column)
        
        elif self.ch == ')':
            token = Token(TokenType.RPAREN, self.ch, line, column)
        
        elif self.ch == '{':
            token = Token(TokenType.LBRACE, self.ch, line, column)
        
        elif self.ch == '}':
            token = Token(TokenType.RBRACE, self.ch, line, column)
        
        elif self.ch == '[':
            token = Token(TokenType.LBRACKET, self.ch, line, column)
        
        elif self.ch == ']':
            token = Token(TokenType.RBRACKET, self.ch, line, column)
        
        elif self.ch == '.':
            token = Token(TokenType.DOT, self.ch, line, column)
        
        elif self.ch == '"':
            string = self.read_string()
            return Token(TokenType.STRING, string, line, column)
        
        elif self.ch == '':
            token = Token(TokenType.EOF, "", line, column)
        
        else:
            # Идентификаторы
            if self.ch.isalpha() or self.ch == '_':
                identifier = self.read_identifier()
                token_type = self.keywords.get(identifier, TokenType.IDENT)
                return Token(token_type, identifier, line, column)
            
            # Числа
            elif self.ch.isdigit():
                number = self.read_number()
                if '.' in number:
                    return Token(TokenType.FLOAT, number, line, column)
                else:
                    return Token(TokenType.INT, number, line, column)
            
            else:
                token = Token(TokenType.ILLEGAL, self.ch, line, column)
        
        self.read_char()
        return token
    
    def tokenize(self):
        """Возвращает все токены в исходном коде."""
        tokens = []
        
        token = self.next_token()
        while token.token_type != TokenType.EOF:
            tokens.append(token)
            token = self.next_token()
        
        tokens.append(token)  # Добавляем EOF токен
        return tokens 