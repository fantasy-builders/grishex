/**
 * Parser for the Grishex language
 *
 * Responsible for converting a sequence of tokens into an abstract syntax tree (AST)
 * that can be used for type checking, optimization, and code generation.
 */
import { Token } from './lexer';
export declare abstract class Node {
    abstract accept<T>(visitor: Visitor<T>): T;
}
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
export declare class BinaryExpr extends Node {
    left: Expr;
    operator: Token;
    right: Expr;
    constructor(left: Expr, operator: Token, right: Expr);
    accept<T>(visitor: Visitor<T>): T;
}
export declare class GroupingExpr extends Node {
    expression: Expr;
    constructor(expression: Expr);
    accept<T>(visitor: Visitor<T>): T;
}
export declare class LiteralExpr extends Node {
    value: any;
    constructor(value: any);
    accept<T>(visitor: Visitor<T>): T;
}
export declare class UnaryExpr extends Node {
    operator: Token;
    right: Expr;
    constructor(operator: Token, right: Expr);
    accept<T>(visitor: Visitor<T>): T;
}
export declare class VariableExpr extends Node {
    name: Token;
    constructor(name: Token);
    accept<T>(visitor: Visitor<T>): T;
}
export declare class AssignExpr extends Node {
    name: Token;
    value: Expr;
    constructor(name: Token, value: Expr);
    accept<T>(visitor: Visitor<T>): T;
}
export declare class CallExpr extends Node {
    callee: Expr;
    paren: Token;
    args: Expr[];
    constructor(callee: Expr, paren: Token, args: Expr[]);
    accept<T>(visitor: Visitor<T>): T;
}
export declare class GetExpr extends Node {
    object: Expr;
    name: Token;
    constructor(object: Expr, name: Token);
    accept<T>(visitor: Visitor<T>): T;
}
export declare class SetExpr extends Node {
    object: Expr;
    name: Token;
    value: Expr;
    constructor(object: Expr, name: Token, value: Expr);
    accept<T>(visitor: Visitor<T>): T;
}
export declare class ThisExpr extends Node {
    keyword: Token;
    constructor(keyword: Token);
    accept<T>(visitor: Visitor<T>): T;
}
export type Expr = BinaryExpr | GroupingExpr | LiteralExpr | UnaryExpr | VariableExpr | AssignExpr | CallExpr | GetExpr | SetExpr | ThisExpr;
export declare class ExpressionStmt extends Node {
    expression: Expr;
    constructor(expression: Expr);
    accept<T>(visitor: Visitor<T>): T;
}
export declare class BlockStmt extends Node {
    statements: Stmt[];
    constructor(statements: Stmt[]);
    accept<T>(visitor: Visitor<T>): T;
}
export declare class IfStmt extends Node {
    condition: Expr;
    thenBranch: Stmt;
    elseBranch: Stmt | null;
    constructor(condition: Expr, thenBranch: Stmt, elseBranch: Stmt | null);
    accept<T>(visitor: Visitor<T>): T;
}
export declare class WhileStmt extends Node {
    condition: Expr;
    body: Stmt;
    constructor(condition: Expr, body: Stmt);
    accept<T>(visitor: Visitor<T>): T;
}
export declare class ForStmt extends Node {
    initializer: VarStmt | ExpressionStmt | null;
    condition: Expr | null;
    increment: Expr | null;
    body: Stmt;
    constructor(initializer: VarStmt | ExpressionStmt | null, condition: Expr | null, increment: Expr | null, body: Stmt);
    accept<T>(visitor: Visitor<T>): T;
}
export declare class ReturnStmt extends Node {
    keyword: Token;
    value: Expr | null;
    constructor(keyword: Token, value: Expr | null);
    accept<T>(visitor: Visitor<T>): T;
}
export declare class VarStmt extends Node {
    name: Token;
    type: Token | null;
    initializer: Expr | null;
    visibility: Token | null;
    constructor(name: Token, type: Token | null, initializer: Expr | null, visibility: Token | null);
    accept<T>(visitor: Visitor<T>): T;
}
export declare class Parameter {
    name: Token;
    type: Token;
    storage: Token | null;
    constructor(name: Token, type: Token, storage: Token | null);
}
export declare class FunctionStmt extends Node {
    name: Token;
    params: Parameter[];
    returnType: Token | null;
    body: BlockStmt;
    visibility: Token | null;
    modifiers: Token[];
    constructor(name: Token, params: Parameter[], returnType: Token | null, body: BlockStmt, visibility: Token | null, modifiers: Token[]);
    accept<T>(visitor: Visitor<T>): T;
}
export declare class ContractStmt extends Node {
    name: Token;
    methods: FunctionStmt[];
    fields: VarStmt[];
    structs: StructStmt[];
    events: EventStmt[];
    errors: ErrorStmt[];
    constructor(name: Token, methods: FunctionStmt[], fields: VarStmt[], structs: StructStmt[], events: EventStmt[], errors: ErrorStmt[]);
    accept<T>(visitor: Visitor<T>): T;
}
export declare class StructStmt extends Node {
    name: Token;
    fields: VarStmt[];
    constructor(name: Token, fields: VarStmt[]);
    accept<T>(visitor: Visitor<T>): T;
}
export declare class EventStmt extends Node {
    name: Token;
    fields: Parameter[];
    constructor(name: Token, fields: Parameter[]);
    accept<T>(visitor: Visitor<T>): T;
}
export declare class ErrorStmt extends Node {
    name: Token;
    params: Parameter[];
    constructor(name: Token, params: Parameter[]);
    accept<T>(visitor: Visitor<T>): T;
}
export declare class ImportStmt extends Node {
    path: Token;
    identifiers: Token[];
    constructor(path: Token, identifiers: Token[]);
    accept<T>(visitor: Visitor<T>): T;
}
export type Stmt = ExpressionStmt | BlockStmt | IfStmt | WhileStmt | ForStmt | ReturnStmt | VarStmt | FunctionStmt | ContractStmt | StructStmt | EventStmt | ErrorStmt | ImportStmt;
export declare class Parser {
    private tokens;
    private current;
    constructor(tokens: Token[]);
    parse(): Stmt[];
    private declaration;
    private importDeclaration;
    private contractDeclaration;
    private structDeclaration;
    private errorDeclaration;
    private eventDeclaration;
    private functionDeclaration;
    private statement;
    private ifStatement;
    private whileStatement;
    private forStatement;
    private returnStatement;
    private block;
    private expressionStatement;
    private expression;
    private assignment;
    private match;
    private check;
    private advance;
    private isAtEnd;
    private peek;
    private previous;
    private consume;
    private error;
    private synchronize;
}
