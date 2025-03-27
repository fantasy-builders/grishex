/**
 * Lexer for the Grishex language
 *
 * Responsible for tokenizing source code into tokens
 * that can be processed by the parser.
 */
export declare enum TokenType {
    LEFT_PAREN = "LEFT_PAREN",
    RIGHT_PAREN = "RIGHT_PAREN",
    LEFT_BRACE = "LEFT_BRACE",
    RIGHT_BRACE = "RIGHT_BRACE",
    LEFT_BRACKET = "LEFT_BRACKET",
    RIGHT_BRACKET = "RIGHT_BRACKET",
    COMMA = "COMMA",
    DOT = "DOT",
    SEMICOLON = "SEMICOLON",
    COLON = "COLON",
    PLUS = "PLUS",
    MINUS = "MINUS",
    STAR = "STAR",
    SLASH = "SLASH",
    PERCENT = "PERCENT",
    EQUAL = "EQUAL",
    PLUS_EQUAL = "PLUS_EQUAL",
    MINUS_EQUAL = "MINUS_EQUAL",
    STAR_EQUAL = "STAR_EQUAL",
    SLASH_EQUAL = "SLASH_EQUAL",
    PERCENT_EQUAL = "PERCENT_EQUAL",
    EQUAL_EQUAL = "EQUAL_EQUAL",
    BANG_EQUAL = "BANG_EQUAL",
    GREATER = "GREATER",
    GREATER_EQUAL = "GREATER_EQUAL",
    LESS = "LESS",
    LESS_EQUAL = "LESS_EQUAL",
    BANG = "BANG",
    AND = "AND",
    OR = "OR",
    IDENTIFIER = "IDENTIFIER",
    STRING = "STRING",
    NUMBER = "NUMBER",
    CONTRACT = "CONTRACT",
    FUNCTION = "FUNCTION",
    STRUCT = "STRUCT",
    MAPPING = "MAPPING",
    IF = "IF",
    ELSE = "ELSE",
    FOR = "FOR",
    WHILE = "WHILE",
    RETURN = "RETURN",
    TRUE = "TRUE",
    FALSE = "FALSE",
    NULL = "NULL",
    PUBLIC = "PUBLIC",
    PRIVATE = "PRIVATE",
    INTERNAL = "INTERNAL",
    EXTERNAL = "EXTERNAL",
    UINT = "UINT",
    INT = "INT",
    BOOL = "BOOL",
    ADDRESS = "ADDRESS",
    STRING_TYPE = "STRING_TYPE",
    BYTES = "BYTES",
    MEMORY = "MEMORY",
    STORAGE = "STORAGE",
    PAYABLE = "PAYABLE",
    IMPORT = "IMPORT",
    FROM = "FROM",
    ERROR = "ERROR",
    EVENT = "EVENT",
    CONSTRUCTOR = "CONSTRUCTOR",
    ATOMIC = "ATOMIC",
    SHARD = "SHARD",
    HOLOGRAPHIC = "HOLOGRAPHIC",
    QUANTUM = "QUANTUM",
    EOF = "EOF"
}
export interface Token {
    type: TokenType;
    lexeme: string;
    literal: any;
    line: number;
    column: number;
}
export declare class Lexer {
    private source;
    private tokens;
    private start;
    private current;
    private line;
    private column;
    private keywords;
    constructor(source: string);
    tokenize(): Token[];
    private scanToken;
    private multiLineComment;
    private string;
    private number;
    private identifier;
    private match;
    private advance;
    private peek;
    private peekNext;
    private isDigit;
    private isAlpha;
    private isAlphaNumeric;
    private isAtEnd;
    private addToken;
}
