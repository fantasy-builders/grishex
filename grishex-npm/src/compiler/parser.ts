/**
 * Parser for the Grishex language
 * 
 * Responsible for converting a sequence of tokens into an abstract syntax tree (AST)
 * that can be used for type checking, optimization, and code generation.
 */

import { Token, TokenType } from './lexer';

// Base class for all AST nodes
export abstract class Node {
  abstract accept<T>(visitor: Visitor<T>): T;
}

// Visitor pattern interface for AST nodes
export interface Visitor<T> {
  visitBinaryExpr(expr: BinaryExpr): T;
  visitGroupingExpr(expr: GroupingExpr): T;
  visitLiteralExpr(expr: LiteralExpr): T;
  visitUnaryExpr(expr: UnaryExpr): T;
  visitVariableExpr(expr: VariableExpr): T;
  visitAssignExpr(expr: AssignExpr): T;
  visitCallExpr(expr: CallExpr): T;
  visitGetExpr(expr: GetExpr): T;
  visitSetExpr(expr: SetExpr): T;
  visitThisExpr(expr: ThisExpr): T;
  
  visitExpressionStmt(stmt: ExpressionStmt): T;
  visitBlockStmt(stmt: BlockStmt): T;
  visitIfStmt(stmt: IfStmt): T;
  visitWhileStmt(stmt: WhileStmt): T;
  visitForStmt(stmt: ForStmt): T;
  visitReturnStmt(stmt: ReturnStmt): T;
  visitVarStmt(stmt: VarStmt): T;
  visitFunctionStmt(stmt: FunctionStmt): T;
  visitContractStmt(stmt: ContractStmt): T;
  visitStructStmt(stmt: StructStmt): T;
  visitEventStmt(stmt: EventStmt): T;
  visitErrorStmt(stmt: ErrorStmt): T;
  visitImportStmt(stmt: ImportStmt): T;
}

// Expression nodes
export class BinaryExpr extends Node {
  constructor(
    public left: Expr,
    public operator: Token,
    public right: Expr
  ) {
    super();
  }
  
  accept<T>(visitor: Visitor<T>): T {
    return visitor.visitBinaryExpr(this);
  }
}

export class GroupingExpr extends Node {
  constructor(public expression: Expr) {
    super();
  }
  
  accept<T>(visitor: Visitor<T>): T {
    return visitor.visitGroupingExpr(this);
  }
}

export class LiteralExpr extends Node {
  constructor(public value: any) {
    super();
  }
  
  accept<T>(visitor: Visitor<T>): T {
    return visitor.visitLiteralExpr(this);
  }
}

export class UnaryExpr extends Node {
  constructor(
    public operator: Token,
    public right: Expr
  ) {
    super();
  }
  
  accept<T>(visitor: Visitor<T>): T {
    return visitor.visitUnaryExpr(this);
  }
}

export class VariableExpr extends Node {
  constructor(public name: Token) {
    super();
  }
  
  accept<T>(visitor: Visitor<T>): T {
    return visitor.visitVariableExpr(this);
  }
}

export class AssignExpr extends Node {
  constructor(
    public name: Token,
    public value: Expr
  ) {
    super();
  }
  
  accept<T>(visitor: Visitor<T>): T {
    return visitor.visitAssignExpr(this);
  }
}

export class CallExpr extends Node {
  constructor(
    public callee: Expr,
    public paren: Token,
    public args: Expr[]
  ) {
    super();
  }
  
  accept<T>(visitor: Visitor<T>): T {
    return visitor.visitCallExpr(this);
  }
}

export class GetExpr extends Node {
  constructor(
    public object: Expr,
    public name: Token
  ) {
    super();
  }
  
  accept<T>(visitor: Visitor<T>): T {
    return visitor.visitGetExpr(this);
  }
}

export class SetExpr extends Node {
  constructor(
    public object: Expr,
    public name: Token,
    public value: Expr
  ) {
    super();
  }
  
  accept<T>(visitor: Visitor<T>): T {
    return visitor.visitSetExpr(this);
  }
}

export class ThisExpr extends Node {
  constructor(public keyword: Token) {
    super();
  }
  
  accept<T>(visitor: Visitor<T>): T {
    return visitor.visitThisExpr(this);
  }
}

// Type alias for all expression types
export type Expr =
  | BinaryExpr
  | GroupingExpr
  | LiteralExpr
  | UnaryExpr
  | VariableExpr
  | AssignExpr
  | CallExpr
  | GetExpr
  | SetExpr
  | ThisExpr;

// Statement nodes
export class ExpressionStmt extends Node {
  constructor(public expression: Expr) {
    super();
  }
  
  accept<T>(visitor: Visitor<T>): T {
    return visitor.visitExpressionStmt(this);
  }
}

export class BlockStmt extends Node {
  constructor(public statements: Stmt[]) {
    super();
  }
  
  accept<T>(visitor: Visitor<T>): T {
    return visitor.visitBlockStmt(this);
  }
}

export class IfStmt extends Node {
  constructor(
    public condition: Expr,
    public thenBranch: Stmt,
    public elseBranch: Stmt | null
  ) {
    super();
  }
  
  accept<T>(visitor: Visitor<T>): T {
    return visitor.visitIfStmt(this);
  }
}

export class WhileStmt extends Node {
  constructor(
    public condition: Expr,
    public body: Stmt
  ) {
    super();
  }
  
  accept<T>(visitor: Visitor<T>): T {
    return visitor.visitWhileStmt(this);
  }
}

export class ForStmt extends Node {
  constructor(
    public initializer: VarStmt | ExpressionStmt | null,
    public condition: Expr | null,
    public increment: Expr | null,
    public body: Stmt
  ) {
    super();
  }
  
  accept<T>(visitor: Visitor<T>): T {
    return visitor.visitForStmt(this);
  }
}

export class ReturnStmt extends Node {
  constructor(
    public keyword: Token,
    public value: Expr | null
  ) {
    super();
  }
  
  accept<T>(visitor: Visitor<T>): T {
    return visitor.visitReturnStmt(this);
  }
}

export class VarStmt extends Node {
  constructor(
    public name: Token,
    public type: Token | null,
    public initializer: Expr | null,
    public visibility: Token | null
  ) {
    super();
  }
  
  accept<T>(visitor: Visitor<T>): T {
    return visitor.visitVarStmt(this);
  }
}

export class Parameter {
  constructor(
    public name: Token,
    public type: Token,
    public storage: Token | null
  ) {}
}

export class FunctionStmt extends Node {
  constructor(
    public name: Token,
    public params: Parameter[],
    public returnType: Token | null,
    public body: BlockStmt,
    public visibility: Token | null,
    public modifiers: Token[]
  ) {
    super();
  }
  
  accept<T>(visitor: Visitor<T>): T {
    return visitor.visitFunctionStmt(this);
  }
}

export class ContractStmt extends Node {
  constructor(
    public name: Token,
    public methods: FunctionStmt[],
    public fields: VarStmt[],
    public structs: StructStmt[],
    public events: EventStmt[],
    public errors: ErrorStmt[]
  ) {
    super();
  }
  
  accept<T>(visitor: Visitor<T>): T {
    return visitor.visitContractStmt(this);
  }
}

export class StructStmt extends Node {
  constructor(
    public name: Token,
    public fields: VarStmt[]
  ) {
    super();
  }
  
  accept<T>(visitor: Visitor<T>): T {
    return visitor.visitStructStmt(this);
  }
}

export class EventStmt extends Node {
  constructor(
    public name: Token,
    public fields: Parameter[]
  ) {
    super();
  }
  
  accept<T>(visitor: Visitor<T>): T {
    return visitor.visitEventStmt(this);
  }
}

export class ErrorStmt extends Node {
  constructor(
    public name: Token,
    public params: Parameter[]
  ) {
    super();
  }
  
  accept<T>(visitor: Visitor<T>): T {
    return visitor.visitErrorStmt(this);
  }
}

export class ImportStmt extends Node {
  constructor(
    public path: Token,
    public identifiers: Token[]
  ) {
    super();
  }
  
  accept<T>(visitor: Visitor<T>): T {
    return visitor.visitImportStmt(this);
  }
}

// Type alias for all statement types
export type Stmt =
  | ExpressionStmt
  | BlockStmt
  | IfStmt
  | WhileStmt
  | ForStmt
  | ReturnStmt
  | VarStmt
  | FunctionStmt
  | ContractStmt
  | StructStmt
  | EventStmt
  | ErrorStmt
  | ImportStmt;

// The Parser class that builds the AST
export class Parser {
  private tokens: Token[];
  private current = 0;
  
  constructor(tokens: Token[]) {
    this.tokens = tokens;
  }
  
  parse(): Stmt[] {
    const statements: Stmt[] = [];
    
    while (!this.isAtEnd()) {
      try {
        statements.push(this.declaration());
      } catch (error) {
        this.synchronize();
      }
    }
    
    return statements;
  }
  
  private declaration(): Stmt {
    if (this.match(TokenType.IMPORT)) return this.importDeclaration();
    if (this.match(TokenType.CONTRACT)) return this.contractDeclaration();
    if (this.match(TokenType.STRUCT)) return this.structDeclaration();
    if (this.match(TokenType.ERROR)) return this.errorDeclaration();
    if (this.match(TokenType.EVENT)) return this.eventDeclaration();
    if (this.match(TokenType.FUNCTION)) return this.functionDeclaration();
    
    return this.statement();
  }
  
  private importDeclaration(): ImportStmt {
    // TO BE IMPLEMENTED: Import declaration parsing
    throw new Error("Import declarations not yet implemented");
  }
  
  private contractDeclaration(): ContractStmt {
    // TO BE IMPLEMENTED: Contract declaration parsing
    throw new Error("Contract declarations not yet implemented");
  }
  
  private structDeclaration(): StructStmt {
    // TO BE IMPLEMENTED: Struct declaration parsing
    throw new Error("Struct declarations not yet implemented");
  }
  
  private errorDeclaration(): ErrorStmt {
    // TO BE IMPLEMENTED: Error declaration parsing
    throw new Error("Error declarations not yet implemented");
  }
  
  private eventDeclaration(): EventStmt {
    // TO BE IMPLEMENTED: Event declaration parsing
    throw new Error("Event declarations not yet implemented");
  }
  
  private functionDeclaration(): FunctionStmt {
    // TO BE IMPLEMENTED: Function declaration parsing
    throw new Error("Function declarations not yet implemented");
  }
  
  private statement(): Stmt {
    if (this.match(TokenType.IF)) return this.ifStatement();
    if (this.match(TokenType.WHILE)) return this.whileStatement();
    if (this.match(TokenType.FOR)) return this.forStatement();
    if (this.match(TokenType.RETURN)) return this.returnStatement();
    if (this.match(TokenType.LEFT_BRACE)) return new BlockStmt(this.block());
    
    return this.expressionStatement();
  }
  
  private ifStatement(): IfStmt {
    // TO BE IMPLEMENTED: If statement parsing
    throw new Error("If statements not yet implemented");
  }
  
  private whileStatement(): WhileStmt {
    // TO BE IMPLEMENTED: While statement parsing
    throw new Error("While statements not yet implemented");
  }
  
  private forStatement(): ForStmt {
    // TO BE IMPLEMENTED: For statement parsing
    throw new Error("For statements not yet implemented");
  }
  
  private returnStatement(): ReturnStmt {
    // TO BE IMPLEMENTED: Return statement parsing
    throw new Error("Return statements not yet implemented");
  }
  
  private block(): Stmt[] {
    // TO BE IMPLEMENTED: Block parsing
    throw new Error("Blocks not yet implemented");
  }
  
  private expressionStatement(): ExpressionStmt {
    const expr = this.expression();
    this.consume(TokenType.SEMICOLON, "Expect ';' after expression.");
    return new ExpressionStmt(expr);
  }
  
  private expression(): Expr {
    return this.assignment();
  }
  
  private assignment(): Expr {
    // TO BE IMPLEMENTED: Assignment parsing
    throw new Error("Assignments not yet implemented");
  }
  
  // Helper methods
  
  private match(...types: TokenType[]): boolean {
    for (const type of types) {
      if (this.check(type)) {
        this.advance();
        return true;
      }
    }
    
    return false;
  }
  
  private check(type: TokenType): boolean {
    if (this.isAtEnd()) return false;
    return this.peek().type === type;
  }
  
  private advance(): Token {
    if (!this.isAtEnd()) this.current++;
    return this.previous();
  }
  
  private isAtEnd(): boolean {
    return this.peek().type === TokenType.EOF;
  }
  
  private peek(): Token {
    return this.tokens[this.current];
  }
  
  private previous(): Token {
    return this.tokens[this.current - 1];
  }
  
  private consume(type: TokenType, message: string): Token {
    if (this.check(type)) return this.advance();
    
    throw this.error(this.peek(), message);
  }
  
  private error(token: Token, message: string): Error {
    // Report the error
    if (token.type === TokenType.EOF) {
      console.error(`Error at end: ${message}`);
    } else {
      console.error(`Error at '${token.lexeme}' line ${token.line}: ${message}`);
    }
    
    return new Error(message);
  }
  
  private synchronize(): void {
    this.advance();
    
    while (!this.isAtEnd()) {
      if (this.previous().type === TokenType.SEMICOLON) return;
      
      switch (this.peek().type) {
        case TokenType.CONTRACT:
        case TokenType.STRUCT:
        case TokenType.FUNCTION:
        case TokenType.EVENT:
        case TokenType.ERROR:
        case TokenType.IF:
        case TokenType.WHILE:
        case TokenType.FOR:
        case TokenType.RETURN:
          return;
      }
      
      this.advance();
    }
  }
} 