import { Lexer, TokenType } from '../src/compiler/lexer';

describe('Lexer', () => {
  test('tokenizes empty input', () => {
    const lexer = new Lexer('');
    const tokens = lexer.tokenize();
    
    expect(tokens.length).toBe(1);
    expect(tokens[0].type).toBe(TokenType.EOF);
  });
  
  test('tokenizes basic symbols', () => {
    const lexer = new Lexer('(){}[];,.');
    const tokens = lexer.tokenize();
    
    expect(tokens.length).toBe(9); // 8 symbols + EOF
    expect(tokens[0].type).toBe(TokenType.LEFT_PAREN);
    expect(tokens[1].type).toBe(TokenType.RIGHT_PAREN);
    expect(tokens[2].type).toBe(TokenType.LEFT_BRACE);
    expect(tokens[3].type).toBe(TokenType.RIGHT_BRACE);
    expect(tokens[4].type).toBe(TokenType.LEFT_BRACKET);
    expect(tokens[5].type).toBe(TokenType.RIGHT_BRACKET);
    expect(tokens[6].type).toBe(TokenType.SEMICOLON);
    expect(tokens[7].type).toBe(TokenType.COMMA);
    expect(tokens[8].type).toBe(TokenType.DOT);
  });
  
  test('tokenizes operators', () => {
    const lexer = new Lexer('+ - * / % = == != > >= < <= ! && ||');
    const tokens = lexer.tokenize();
    
    expect(tokens[0].type).toBe(TokenType.PLUS);
    expect(tokens[1].type).toBe(TokenType.MINUS);
    expect(tokens[2].type).toBe(TokenType.STAR);
    expect(tokens[3].type).toBe(TokenType.SLASH);
    expect(tokens[4].type).toBe(TokenType.PERCENT);
    expect(tokens[5].type).toBe(TokenType.EQUAL);
    expect(tokens[6].type).toBe(TokenType.EQUAL_EQUAL);
    expect(tokens[7].type).toBe(TokenType.BANG_EQUAL);
    expect(tokens[8].type).toBe(TokenType.GREATER);
    expect(tokens[9].type).toBe(TokenType.GREATER_EQUAL);
    expect(tokens[10].type).toBe(TokenType.LESS);
    expect(tokens[11].type).toBe(TokenType.LESS_EQUAL);
    expect(tokens[12].type).toBe(TokenType.BANG);
    expect(tokens[13].type).toBe(TokenType.AND);
    expect(tokens[14].type).toBe(TokenType.OR);
  });
  
  test('tokenizes keywords', () => {
    const lexer = new Lexer('contract function struct mapping if else for while return');
    const tokens = lexer.tokenize();
    
    expect(tokens[0].type).toBe(TokenType.CONTRACT);
    expect(tokens[1].type).toBe(TokenType.FUNCTION);
    expect(tokens[2].type).toBe(TokenType.STRUCT);
    expect(tokens[3].type).toBe(TokenType.MAPPING);
    expect(tokens[4].type).toBe(TokenType.IF);
    expect(tokens[5].type).toBe(TokenType.ELSE);
    expect(tokens[6].type).toBe(TokenType.FOR);
    expect(tokens[7].type).toBe(TokenType.WHILE);
    expect(tokens[8].type).toBe(TokenType.RETURN);
  });
  
  test('tokenizes identifiers', () => {
    const lexer = new Lexer('myVar _privateVar snake_case CamelCase');
    const tokens = lexer.tokenize();
    
    expect(tokens.length).toBe(5); // 4 identifiers + EOF
    tokens.slice(0, 4).forEach(token => {
      expect(token.type).toBe(TokenType.IDENTIFIER);
    });
    expect(tokens[0].lexeme).toBe('myVar');
    expect(tokens[1].lexeme).toBe('_privateVar');
    expect(tokens[2].lexeme).toBe('snake_case');
    expect(tokens[3].lexeme).toBe('CamelCase');
  });
  
  test('tokenizes numbers', () => {
    const lexer = new Lexer('123 45.67');
    const tokens = lexer.tokenize();
    
    expect(tokens.length).toBe(3); // 2 numbers + EOF
    expect(tokens[0].type).toBe(TokenType.NUMBER);
    expect(tokens[0].literal).toBe(123);
    expect(tokens[1].type).toBe(TokenType.NUMBER);
    expect(tokens[1].literal).toBe(45.67);
  });
  
  test('tokenizes strings', () => {
    const lexer = new Lexer('"hello world" \'single quoted\'');
    const tokens = lexer.tokenize();
    
    expect(tokens.length).toBe(3); // 2 strings + EOF
    expect(tokens[0].type).toBe(TokenType.STRING);
    expect(tokens[0].literal).toBe('hello world');
    expect(tokens[1].type).toBe(TokenType.STRING);
    expect(tokens[1].literal).toBe('single quoted');
  });
  
  test('ignores whitespace and comments', () => {
    const lexer = new Lexer(`
      // This is a line comment
      contract Test {
        /* This is a 
           multi-line comment */
        function test() {}
      }
    `);
    const tokens = lexer.tokenize();
    
    // Filter out whitespace tokens (which are ignored by the lexer)
    const significantTokens = tokens;
    
    // Verify we get the expected tokens
    const expectedTypes = [
      TokenType.CONTRACT,
      TokenType.IDENTIFIER,
      TokenType.LEFT_BRACE,
      TokenType.FUNCTION,
      TokenType.IDENTIFIER,
      TokenType.LEFT_PAREN,
      TokenType.RIGHT_PAREN,
      TokenType.LEFT_BRACE,
      TokenType.RIGHT_BRACE,
      TokenType.RIGHT_BRACE,
      TokenType.EOF
    ];
    
    expect(significantTokens.length).toBe(expectedTypes.length);
    
    for (let i = 0; i < expectedTypes.length; i++) {
      expect(significantTokens[i].type).toBe(expectedTypes[i]);
    }
  });
  
  test('tokenizes a simple contract', () => {
    const source = `
      contract Token {
        string public name = "MyToken";
        uint public totalSupply = 0;
        
        function mint(address to, uint amount) public {
          totalSupply += amount;
          emit Transfer(address(0), to, amount);
        }
      }
    `;
    
    const lexer = new Lexer(source);
    const tokens = lexer.tokenize();
    
    // Checking only key tokens to keep the test manageable
    expect(tokens.find(t => t.type === TokenType.CONTRACT)).toBeTruthy();
    expect(tokens.find(t => t.type === TokenType.STRING_TYPE)).toBeTruthy();
    expect(tokens.find(t => t.type === TokenType.PUBLIC)).toBeTruthy();
    expect(tokens.find(t => t.type === TokenType.FUNCTION)).toBeTruthy();
    expect(tokens.find(t => t.type === TokenType.ADDRESS)).toBeTruthy();
    expect(tokens.find(t => t.type === TokenType.UINT)).toBeTruthy();
  });
}); 