/**
 * Lexer for the Grishex language
 * 
 * Responsible for tokenizing source code into tokens
 * that can be processed by the parser.
 */

export enum TokenType {
  // Single character tokens
  LEFT_PAREN = 'LEFT_PAREN',
  RIGHT_PAREN = 'RIGHT_PAREN',
  LEFT_BRACE = 'LEFT_BRACE',
  RIGHT_BRACE = 'RIGHT_BRACE',
  LEFT_BRACKET = 'LEFT_BRACKET',
  RIGHT_BRACKET = 'RIGHT_BRACKET',
  COMMA = 'COMMA',
  DOT = 'DOT',
  SEMICOLON = 'SEMICOLON',
  COLON = 'COLON',
  
  // Operators
  PLUS = 'PLUS',
  MINUS = 'MINUS',
  STAR = 'STAR',
  SLASH = 'SLASH',
  PERCENT = 'PERCENT',
  
  // Assignments
  EQUAL = 'EQUAL',
  PLUS_EQUAL = 'PLUS_EQUAL',
  MINUS_EQUAL = 'MINUS_EQUAL',
  STAR_EQUAL = 'STAR_EQUAL',
  SLASH_EQUAL = 'SLASH_EQUAL',
  PERCENT_EQUAL = 'PERCENT_EQUAL',
  
  // Comparisons
  EQUAL_EQUAL = 'EQUAL_EQUAL',
  BANG_EQUAL = 'BANG_EQUAL',
  GREATER = 'GREATER',
  GREATER_EQUAL = 'GREATER_EQUAL',
  LESS = 'LESS',
  LESS_EQUAL = 'LESS_EQUAL',
  
  // Logical operators
  BANG = 'BANG',
  AND = 'AND',
  OR = 'OR',
  
  // Literals
  IDENTIFIER = 'IDENTIFIER',
  STRING = 'STRING',
  NUMBER = 'NUMBER',
  
  // Keywords
  CONTRACT = 'CONTRACT',
  FUNCTION = 'FUNCTION',
  STRUCT = 'STRUCT',
  MAPPING = 'MAPPING',
  IF = 'IF',
  ELSE = 'ELSE',
  FOR = 'FOR',
  WHILE = 'WHILE',
  RETURN = 'RETURN',
  TRUE = 'TRUE',
  FALSE = 'FALSE',
  NULL = 'NULL',
  PUBLIC = 'PUBLIC',
  PRIVATE = 'PRIVATE',
  INTERNAL = 'INTERNAL',
  EXTERNAL = 'EXTERNAL',
  UINT = 'UINT',
  INT = 'INT',
  BOOL = 'BOOL',
  ADDRESS = 'ADDRESS',
  STRING_TYPE = 'STRING_TYPE',
  BYTES = 'BYTES',
  MEMORY = 'MEMORY',
  STORAGE = 'STORAGE',
  PAYABLE = 'PAYABLE',
  IMPORT = 'IMPORT',
  FROM = 'FROM',
  ERROR = 'ERROR',
  EVENT = 'EVENT',
  CONSTRUCTOR = 'CONSTRUCTOR',
  
  // HoloShard specific
  ATOMIC = 'ATOMIC',
  SHARD = 'SHARD',
  HOLOGRAPHIC = 'HOLOGRAPHIC',
  QUANTUM = 'QUANTUM',
  
  // End of file
  EOF = 'EOF'
}

export interface Token {
  type: TokenType;
  lexeme: string;
  literal: any;
  line: number;
  column: number;
}

export class Lexer {
  private source: string;
  private tokens: Token[] = [];
  
  private start = 0;
  private current = 0;
  private line = 1;
  private column = 1;
  
  // Map of keywords
  private keywords: Record<string, TokenType> = {
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
  
  constructor(source: string) {
    this.source = source;
  }
  
  tokenize(): Token[] {
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
  
  private scanToken(): void {
    const c = this.advance();
    
    switch (c) {
      // Single character tokens
      case '(': this.addToken(TokenType.LEFT_PAREN); break;
      case ')': this.addToken(TokenType.RIGHT_PAREN); break;
      case '{': this.addToken(TokenType.LEFT_BRACE); break;
      case '}': this.addToken(TokenType.RIGHT_BRACE); break;
      case '[': this.addToken(TokenType.LEFT_BRACKET); break;
      case ']': this.addToken(TokenType.RIGHT_BRACKET); break;
      case ',': this.addToken(TokenType.COMMA); break;
      case '.': this.addToken(TokenType.DOT); break;
      case ';': this.addToken(TokenType.SEMICOLON); break;
      case ':': this.addToken(TokenType.COLON); break;
      
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
          while (this.peek() !== '\n' && !this.isAtEnd()) this.advance();
        } else if (this.match('*')) {
          // Multi-line comment
          this.multiLineComment();
        } else if (this.match('=')) {
          this.addToken(TokenType.SLASH_EQUAL);
        } else {
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
        if (this.match('&')) this.addToken(TokenType.AND);
        break;
      case '|': 
        if (this.match('|')) this.addToken(TokenType.OR);
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
      case '"': this.string(); break;
      case "'": this.string("'"); break;
      
      default:
        if (this.isDigit(c)) {
          this.number();
        } else if (this.isAlpha(c)) {
          this.identifier();
        } else {
          console.error(`Unexpected character: ${c} at line ${this.line}`);
        }
        break;
    }
  }
  
  private multiLineComment(): void {
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
  
  private string(terminator: string = '"'): void {
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
  
  private number(): void {
    // Keep consuming digits
    while (this.isDigit(this.peek())) this.advance();
    
    // Look for a decimal point
    if (this.peek() === '.' && this.isDigit(this.peekNext())) {
      // Consume the decimal point
      this.advance();
      
      // Keep consuming digits after the decimal point
      while (this.isDigit(this.peek())) this.advance();
    }
    
    const value = parseFloat(this.source.substring(this.start, this.current));
    this.addToken(TokenType.NUMBER, value);
  }
  
  private identifier(): void {
    // Keep consuming alphanumeric characters
    while (this.isAlphaNumeric(this.peek())) this.advance();
    
    // Check if the identifier is a keyword
    const text = this.source.substring(this.start, this.current);
    const type = this.keywords[text] || TokenType.IDENTIFIER;
    
    this.addToken(type);
  }
  
  private match(expected: string): boolean {
    if (this.isAtEnd()) return false;
    if (this.source.charAt(this.current) !== expected) return false;
    
    this.current++;
    this.column++;
    return true;
  }
  
  private advance(): string {
    this.current++;
    this.column++;
    return this.source.charAt(this.current - 1);
  }
  
  private peek(): string {
    if (this.isAtEnd()) return '\0';
    return this.source.charAt(this.current);
  }
  
  private peekNext(): string {
    if (this.current + 1 >= this.source.length) return '\0';
    return this.source.charAt(this.current + 1);
  }
  
  private isDigit(c: string): boolean {
    return c >= '0' && c <= '9';
  }
  
  private isAlpha(c: string): boolean {
    return (c >= 'a' && c <= 'z') ||
           (c >= 'A' && c <= 'Z') ||
           c === '_';
  }
  
  private isAlphaNumeric(c: string): boolean {
    return this.isAlpha(c) || this.isDigit(c);
  }
  
  private isAtEnd(): boolean {
    return this.current >= this.source.length;
  }
  
  private addToken(type: TokenType, literal: any = null): void {
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