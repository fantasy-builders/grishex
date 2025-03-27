"use strict";
/**
 * Lexer for the Grishex language
 *
 * Responsible for tokenizing source code into tokens
 * that can be processed by the parser.
 */
Object.defineProperty(exports, "__esModule", { value: true });
exports.Lexer = exports.TokenType = void 0;
var TokenType;
(function (TokenType) {
    // Single character tokens
    TokenType["LEFT_PAREN"] = "LEFT_PAREN";
    TokenType["RIGHT_PAREN"] = "RIGHT_PAREN";
    TokenType["LEFT_BRACE"] = "LEFT_BRACE";
    TokenType["RIGHT_BRACE"] = "RIGHT_BRACE";
    TokenType["LEFT_BRACKET"] = "LEFT_BRACKET";
    TokenType["RIGHT_BRACKET"] = "RIGHT_BRACKET";
    TokenType["COMMA"] = "COMMA";
    TokenType["DOT"] = "DOT";
    TokenType["SEMICOLON"] = "SEMICOLON";
    TokenType["COLON"] = "COLON";
    // Operators
    TokenType["PLUS"] = "PLUS";
    TokenType["MINUS"] = "MINUS";
    TokenType["STAR"] = "STAR";
    TokenType["SLASH"] = "SLASH";
    TokenType["PERCENT"] = "PERCENT";
    // Assignments
    TokenType["EQUAL"] = "EQUAL";
    TokenType["PLUS_EQUAL"] = "PLUS_EQUAL";
    TokenType["MINUS_EQUAL"] = "MINUS_EQUAL";
    TokenType["STAR_EQUAL"] = "STAR_EQUAL";
    TokenType["SLASH_EQUAL"] = "SLASH_EQUAL";
    TokenType["PERCENT_EQUAL"] = "PERCENT_EQUAL";
    // Comparisons
    TokenType["EQUAL_EQUAL"] = "EQUAL_EQUAL";
    TokenType["BANG_EQUAL"] = "BANG_EQUAL";
    TokenType["GREATER"] = "GREATER";
    TokenType["GREATER_EQUAL"] = "GREATER_EQUAL";
    TokenType["LESS"] = "LESS";
    TokenType["LESS_EQUAL"] = "LESS_EQUAL";
    // Logical operators
    TokenType["BANG"] = "BANG";
    TokenType["AND"] = "AND";
    TokenType["OR"] = "OR";
    // Literals
    TokenType["IDENTIFIER"] = "IDENTIFIER";
    TokenType["STRING"] = "STRING";
    TokenType["NUMBER"] = "NUMBER";
    // Keywords
    TokenType["CONTRACT"] = "CONTRACT";
    TokenType["FUNCTION"] = "FUNCTION";
    TokenType["STRUCT"] = "STRUCT";
    TokenType["MAPPING"] = "MAPPING";
    TokenType["IF"] = "IF";
    TokenType["ELSE"] = "ELSE";
    TokenType["FOR"] = "FOR";
    TokenType["WHILE"] = "WHILE";
    TokenType["RETURN"] = "RETURN";
    TokenType["TRUE"] = "TRUE";
    TokenType["FALSE"] = "FALSE";
    TokenType["NULL"] = "NULL";
    TokenType["PUBLIC"] = "PUBLIC";
    TokenType["PRIVATE"] = "PRIVATE";
    TokenType["INTERNAL"] = "INTERNAL";
    TokenType["EXTERNAL"] = "EXTERNAL";
    TokenType["UINT"] = "UINT";
    TokenType["INT"] = "INT";
    TokenType["BOOL"] = "BOOL";
    TokenType["ADDRESS"] = "ADDRESS";
    TokenType["STRING_TYPE"] = "STRING_TYPE";
    TokenType["BYTES"] = "BYTES";
    TokenType["MEMORY"] = "MEMORY";
    TokenType["STORAGE"] = "STORAGE";
    TokenType["PAYABLE"] = "PAYABLE";
    TokenType["IMPORT"] = "IMPORT";
    TokenType["FROM"] = "FROM";
    TokenType["ERROR"] = "ERROR";
    TokenType["EVENT"] = "EVENT";
    TokenType["CONSTRUCTOR"] = "CONSTRUCTOR";
    // HoloShard specific
    TokenType["ATOMIC"] = "ATOMIC";
    TokenType["SHARD"] = "SHARD";
    TokenType["HOLOGRAPHIC"] = "HOLOGRAPHIC";
    TokenType["QUANTUM"] = "QUANTUM";
    // End of file
    TokenType["EOF"] = "EOF";
})(TokenType = exports.TokenType || (exports.TokenType = {}));
class Lexer {
    constructor(source) {
        this.tokens = [];
        this.start = 0;
        this.current = 0;
        this.line = 1;
        this.column = 1;
        // Map of keywords
        this.keywords = {
            'contract': TokenType.CONTRACT,
            'function': TokenType.FUNCTION,
            'struct': TokenType.STRUCT,
            'mapping': TokenType.MAPPING,
            'if': TokenType.IF,
            'else': TokenType.ELSE,
            'for': TokenType.FOR,
            'while': TokenType.WHILE,
            'return': TokenType.RETURN,
            'true': TokenType.TRUE,
            'false': TokenType.FALSE,
            'null': TokenType.NULL,
            'public': TokenType.PUBLIC,
            'private': TokenType.PRIVATE,
            'internal': TokenType.INTERNAL,
            'external': TokenType.EXTERNAL,
            'uint': TokenType.UINT,
            'int': TokenType.INT,
            'bool': TokenType.BOOL,
            'address': TokenType.ADDRESS,
            'string': TokenType.STRING_TYPE,
            'bytes': TokenType.BYTES,
            'memory': TokenType.MEMORY,
            'storage': TokenType.STORAGE,
            'payable': TokenType.PAYABLE,
            'import': TokenType.IMPORT,
            'from': TokenType.FROM,
            'error': TokenType.ERROR,
            'event': TokenType.EVENT,
            'constructor': TokenType.CONSTRUCTOR,
            'atomic': TokenType.ATOMIC,
            'shard': TokenType.SHARD,
            'holographic': TokenType.HOLOGRAPHIC,
            'quantum': TokenType.QUANTUM
        };
        this.source = source;
    }
    tokenize() {
        while (!this.isAtEnd()) {
            // Beginning of the next lexeme
            this.start = this.current;
            this.scanToken();
        }
        this.tokens.push({
            type: TokenType.EOF,
            lexeme: '',
            literal: null,
            line: this.line,
            column: this.column
        });
        return this.tokens;
    }
    scanToken() {
        const c = this.advance();
        switch (c) {
            // Single character tokens
            case '(':
                this.addToken(TokenType.LEFT_PAREN);
                break;
            case ')':
                this.addToken(TokenType.RIGHT_PAREN);
                break;
            case '{':
                this.addToken(TokenType.LEFT_BRACE);
                break;
            case '}':
                this.addToken(TokenType.RIGHT_BRACE);
                break;
            case '[':
                this.addToken(TokenType.LEFT_BRACKET);
                break;
            case ']':
                this.addToken(TokenType.RIGHT_BRACKET);
                break;
            case ',':
                this.addToken(TokenType.COMMA);
                break;
            case '.':
                this.addToken(TokenType.DOT);
                break;
            case ';':
                this.addToken(TokenType.SEMICOLON);
                break;
            case ':':
                this.addToken(TokenType.COLON);
                break;
            // Operators
            case '+':
                this.addToken(this.match('=') ? TokenType.PLUS_EQUAL : TokenType.PLUS);
                break;
            case '-':
                this.addToken(this.match('=') ? TokenType.MINUS_EQUAL : TokenType.MINUS);
                break;
            case '*':
                this.addToken(this.match('=') ? TokenType.STAR_EQUAL : TokenType.STAR);
                break;
            case '/':
                if (this.match('/')) {
                    // Comment goes until the end of the line
                    while (this.peek() !== '\n' && !this.isAtEnd())
                        this.advance();
                }
                else if (this.match('*')) {
                    // Multi-line comment
                    this.multiLineComment();
                }
                else if (this.match('=')) {
                    this.addToken(TokenType.SLASH_EQUAL);
                }
                else {
                    this.addToken(TokenType.SLASH);
                }
                break;
            case '%':
                this.addToken(this.match('=') ? TokenType.PERCENT_EQUAL : TokenType.PERCENT);
                break;
            // Comparison operators
            case '!':
                this.addToken(this.match('=') ? TokenType.BANG_EQUAL : TokenType.BANG);
                break;
            case '=':
                this.addToken(this.match('=') ? TokenType.EQUAL_EQUAL : TokenType.EQUAL);
                break;
            case '<':
                this.addToken(this.match('=') ? TokenType.LESS_EQUAL : TokenType.LESS);
                break;
            case '>':
                this.addToken(this.match('=') ? TokenType.GREATER_EQUAL : TokenType.GREATER);
                break;
            // Logical operators
            case '&':
                if (this.match('&'))
                    this.addToken(TokenType.AND);
                break;
            case '|':
                if (this.match('|'))
                    this.addToken(TokenType.OR);
                break;
            // Whitespace
            case ' ':
            case '\r':
            case '\t':
                // Ignore whitespace
                break;
            case '\n':
                this.line++;
                this.column = 0;
                break;
            // String literals
            case '"':
                this.string();
                break;
            case "'":
                this.string("'");
                break;
            default:
                if (this.isDigit(c)) {
                    this.number();
                }
                else if (this.isAlpha(c)) {
                    this.identifier();
                }
                else {
                    console.error(`Unexpected character: ${c} at line ${this.line}`);
                }
                break;
        }
    }
    multiLineComment() {
        // Keep consuming until we find "*/"
        while (!this.isAtEnd()) {
            if (this.peek() === '*' && this.peekNext() === '/') {
                // Consume the */
                this.advance();
                this.advance();
                return;
            }
            if (this.peek() === '\n') {
                this.line++;
                this.column = 0;
            }
            this.advance();
        }
        // Unterminated comment
        console.error(`Unterminated comment at line ${this.line}`);
    }
    string(terminator = '"') {
        // Keep consuming until we find the terminator
        while (this.peek() !== terminator && !this.isAtEnd()) {
            if (this.peek() === '\n') {
                this.line++;
                this.column = 0;
            }
            this.advance();
        }
        if (this.isAtEnd()) {
            console.error(`Unterminated string at line ${this.line}`);
            return;
        }
        // Consume the closing terminator
        this.advance();
        // Extract the string value (without the quotes)
        const value = this.source.substring(this.start + 1, this.current - 1);
        this.addToken(TokenType.STRING, value);
    }
    number() {
        // Keep consuming digits
        while (this.isDigit(this.peek()))
            this.advance();
        // Look for a decimal point
        if (this.peek() === '.' && this.isDigit(this.peekNext())) {
            // Consume the decimal point
            this.advance();
            // Keep consuming digits after the decimal point
            while (this.isDigit(this.peek()))
                this.advance();
        }
        const value = parseFloat(this.source.substring(this.start, this.current));
        this.addToken(TokenType.NUMBER, value);
    }
    identifier() {
        // Keep consuming alphanumeric characters
        while (this.isAlphaNumeric(this.peek()))
            this.advance();
        // Check if the identifier is a keyword
        const text = this.source.substring(this.start, this.current);
        const type = this.keywords[text] || TokenType.IDENTIFIER;
        this.addToken(type);
    }
    match(expected) {
        if (this.isAtEnd())
            return false;
        if (this.source.charAt(this.current) !== expected)
            return false;
        this.current++;
        this.column++;
        return true;
    }
    advance() {
        this.current++;
        this.column++;
        return this.source.charAt(this.current - 1);
    }
    peek() {
        if (this.isAtEnd())
            return '\0';
        return this.source.charAt(this.current);
    }
    peekNext() {
        if (this.current + 1 >= this.source.length)
            return '\0';
        return this.source.charAt(this.current + 1);
    }
    isDigit(c) {
        return c >= '0' && c <= '9';
    }
    isAlpha(c) {
        return (c >= 'a' && c <= 'z') ||
            (c >= 'A' && c <= 'Z') ||
            c === '_';
    }
    isAlphaNumeric(c) {
        return this.isAlpha(c) || this.isDigit(c);
    }
    isAtEnd() {
        return this.current >= this.source.length;
    }
    addToken(type, literal = null) {
        const lexeme = this.source.substring(this.start, this.current);
        this.tokens.push({
            type,
            lexeme,
            literal,
            line: this.line,
            column: this.column - lexeme.length
        });
    }
}
exports.Lexer = Lexer;
//# sourceMappingURL=lexer.js.map