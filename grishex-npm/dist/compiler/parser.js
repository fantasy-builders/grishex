"use strict";
/**
 * Parser for the Grishex language
 *
 * Responsible for converting a sequence of tokens into an abstract syntax tree (AST)
 * that can be used for type checking, optimization, and code generation.
 */
Object.defineProperty(exports, "__esModule", { value: true });
exports.Parser = exports.ImportStmt = exports.ErrorStmt = exports.EventStmt = exports.StructStmt = exports.ContractStmt = exports.FunctionStmt = exports.Parameter = exports.VarStmt = exports.ReturnStmt = exports.ForStmt = exports.WhileStmt = exports.IfStmt = exports.BlockStmt = exports.ExpressionStmt = exports.ThisExpr = exports.SetExpr = exports.GetExpr = exports.CallExpr = exports.AssignExpr = exports.VariableExpr = exports.UnaryExpr = exports.LiteralExpr = exports.GroupingExpr = exports.BinaryExpr = exports.Node = void 0;
const lexer_1 = require("./lexer");
// Base class for all AST nodes
class Node {
}
exports.Node = Node;
// Expression nodes
class BinaryExpr extends Node {
    constructor(left, operator, right) {
        super();
        this.left = left;
        this.operator = operator;
        this.right = right;
    }
    accept(visitor) {
        return visitor.visitBinaryExpr(this);
    }
}
exports.BinaryExpr = BinaryExpr;
class GroupingExpr extends Node {
    constructor(expression) {
        super();
        this.expression = expression;
    }
    accept(visitor) {
        return visitor.visitGroupingExpr(this);
    }
}
exports.GroupingExpr = GroupingExpr;
class LiteralExpr extends Node {
    constructor(value) {
        super();
        this.value = value;
    }
    accept(visitor) {
        return visitor.visitLiteralExpr(this);
    }
}
exports.LiteralExpr = LiteralExpr;
class UnaryExpr extends Node {
    constructor(operator, right) {
        super();
        this.operator = operator;
        this.right = right;
    }
    accept(visitor) {
        return visitor.visitUnaryExpr(this);
    }
}
exports.UnaryExpr = UnaryExpr;
class VariableExpr extends Node {
    constructor(name) {
        super();
        this.name = name;
    }
    accept(visitor) {
        return visitor.visitVariableExpr(this);
    }
}
exports.VariableExpr = VariableExpr;
class AssignExpr extends Node {
    constructor(name, value) {
        super();
        this.name = name;
        this.value = value;
    }
    accept(visitor) {
        return visitor.visitAssignExpr(this);
    }
}
exports.AssignExpr = AssignExpr;
class CallExpr extends Node {
    constructor(callee, paren, args) {
        super();
        this.callee = callee;
        this.paren = paren;
        this.args = args;
    }
    accept(visitor) {
        return visitor.visitCallExpr(this);
    }
}
exports.CallExpr = CallExpr;
class GetExpr extends Node {
    constructor(object, name) {
        super();
        this.object = object;
        this.name = name;
    }
    accept(visitor) {
        return visitor.visitGetExpr(this);
    }
}
exports.GetExpr = GetExpr;
class SetExpr extends Node {
    constructor(object, name, value) {
        super();
        this.object = object;
        this.name = name;
        this.value = value;
    }
    accept(visitor) {
        return visitor.visitSetExpr(this);
    }
}
exports.SetExpr = SetExpr;
class ThisExpr extends Node {
    constructor(keyword) {
        super();
        this.keyword = keyword;
    }
    accept(visitor) {
        return visitor.visitThisExpr(this);
    }
}
exports.ThisExpr = ThisExpr;
// Statement nodes
class ExpressionStmt extends Node {
    constructor(expression) {
        super();
        this.expression = expression;
    }
    accept(visitor) {
        return visitor.visitExpressionStmt(this);
    }
}
exports.ExpressionStmt = ExpressionStmt;
class BlockStmt extends Node {
    constructor(statements) {
        super();
        this.statements = statements;
    }
    accept(visitor) {
        return visitor.visitBlockStmt(this);
    }
}
exports.BlockStmt = BlockStmt;
class IfStmt extends Node {
    constructor(condition, thenBranch, elseBranch) {
        super();
        this.condition = condition;
        this.thenBranch = thenBranch;
        this.elseBranch = elseBranch;
    }
    accept(visitor) {
        return visitor.visitIfStmt(this);
    }
}
exports.IfStmt = IfStmt;
class WhileStmt extends Node {
    constructor(condition, body) {
        super();
        this.condition = condition;
        this.body = body;
    }
    accept(visitor) {
        return visitor.visitWhileStmt(this);
    }
}
exports.WhileStmt = WhileStmt;
class ForStmt extends Node {
    constructor(initializer, condition, increment, body) {
        super();
        this.initializer = initializer;
        this.condition = condition;
        this.increment = increment;
        this.body = body;
    }
    accept(visitor) {
        return visitor.visitForStmt(this);
    }
}
exports.ForStmt = ForStmt;
class ReturnStmt extends Node {
    constructor(keyword, value) {
        super();
        this.keyword = keyword;
        this.value = value;
    }
    accept(visitor) {
        return visitor.visitReturnStmt(this);
    }
}
exports.ReturnStmt = ReturnStmt;
class VarStmt extends Node {
    constructor(name, type, initializer, visibility) {
        super();
        this.name = name;
        this.type = type;
        this.initializer = initializer;
        this.visibility = visibility;
    }
    accept(visitor) {
        return visitor.visitVarStmt(this);
    }
}
exports.VarStmt = VarStmt;
class Parameter {
    constructor(name, type, storage) {
        this.name = name;
        this.type = type;
        this.storage = storage;
    }
}
exports.Parameter = Parameter;
class FunctionStmt extends Node {
    constructor(name, params, returnType, body, visibility, modifiers) {
        super();
        this.name = name;
        this.params = params;
        this.returnType = returnType;
        this.body = body;
        this.visibility = visibility;
        this.modifiers = modifiers;
    }
    accept(visitor) {
        return visitor.visitFunctionStmt(this);
    }
}
exports.FunctionStmt = FunctionStmt;
class ContractStmt extends Node {
    constructor(name, methods, fields, structs, events, errors) {
        super();
        this.name = name;
        this.methods = methods;
        this.fields = fields;
        this.structs = structs;
        this.events = events;
        this.errors = errors;
    }
    accept(visitor) {
        return visitor.visitContractStmt(this);
    }
}
exports.ContractStmt = ContractStmt;
class StructStmt extends Node {
    constructor(name, fields) {
        super();
        this.name = name;
        this.fields = fields;
    }
    accept(visitor) {
        return visitor.visitStructStmt(this);
    }
}
exports.StructStmt = StructStmt;
class EventStmt extends Node {
    constructor(name, fields) {
        super();
        this.name = name;
        this.fields = fields;
    }
    accept(visitor) {
        return visitor.visitEventStmt(this);
    }
}
exports.EventStmt = EventStmt;
class ErrorStmt extends Node {
    constructor(name, params) {
        super();
        this.name = name;
        this.params = params;
    }
    accept(visitor) {
        return visitor.visitErrorStmt(this);
    }
}
exports.ErrorStmt = ErrorStmt;
class ImportStmt extends Node {
    constructor(path, identifiers) {
        super();
        this.path = path;
        this.identifiers = identifiers;
    }
    accept(visitor) {
        return visitor.visitImportStmt(this);
    }
}
exports.ImportStmt = ImportStmt;
// The Parser class that builds the AST
class Parser {
    constructor(tokens) {
        this.current = 0;
        this.tokens = tokens;
    }
    parse() {
        const statements = [];
        while (!this.isAtEnd()) {
            try {
                statements.push(this.declaration());
            }
            catch (error) {
                this.synchronize();
            }
        }
        return statements;
    }
    declaration() {
        if (this.match(lexer_1.TokenType.IMPORT))
            return this.importDeclaration();
        if (this.match(lexer_1.TokenType.CONTRACT))
            return this.contractDeclaration();
        if (this.match(lexer_1.TokenType.STRUCT))
            return this.structDeclaration();
        if (this.match(lexer_1.TokenType.ERROR))
            return this.errorDeclaration();
        if (this.match(lexer_1.TokenType.EVENT))
            return this.eventDeclaration();
        if (this.match(lexer_1.TokenType.FUNCTION))
            return this.functionDeclaration();
        return this.statement();
    }
    importDeclaration() {
        // TO BE IMPLEMENTED: Import declaration parsing
        throw new Error("Import declarations not yet implemented");
    }
    contractDeclaration() {
        // TO BE IMPLEMENTED: Contract declaration parsing
        throw new Error("Contract declarations not yet implemented");
    }
    structDeclaration() {
        // TO BE IMPLEMENTED: Struct declaration parsing
        throw new Error("Struct declarations not yet implemented");
    }
    errorDeclaration() {
        // TO BE IMPLEMENTED: Error declaration parsing
        throw new Error("Error declarations not yet implemented");
    }
    eventDeclaration() {
        // TO BE IMPLEMENTED: Event declaration parsing
        throw new Error("Event declarations not yet implemented");
    }
    functionDeclaration() {
        // TO BE IMPLEMENTED: Function declaration parsing
        throw new Error("Function declarations not yet implemented");
    }
    statement() {
        if (this.match(lexer_1.TokenType.IF))
            return this.ifStatement();
        if (this.match(lexer_1.TokenType.WHILE))
            return this.whileStatement();
        if (this.match(lexer_1.TokenType.FOR))
            return this.forStatement();
        if (this.match(lexer_1.TokenType.RETURN))
            return this.returnStatement();
        if (this.match(lexer_1.TokenType.LEFT_BRACE))
            return new BlockStmt(this.block());
        return this.expressionStatement();
    }
    ifStatement() {
        // TO BE IMPLEMENTED: If statement parsing
        throw new Error("If statements not yet implemented");
    }
    whileStatement() {
        // TO BE IMPLEMENTED: While statement parsing
        throw new Error("While statements not yet implemented");
    }
    forStatement() {
        // TO BE IMPLEMENTED: For statement parsing
        throw new Error("For statements not yet implemented");
    }
    returnStatement() {
        // TO BE IMPLEMENTED: Return statement parsing
        throw new Error("Return statements not yet implemented");
    }
    block() {
        // TO BE IMPLEMENTED: Block parsing
        throw new Error("Blocks not yet implemented");
    }
    expressionStatement() {
        const expr = this.expression();
        this.consume(lexer_1.TokenType.SEMICOLON, "Expect ';' after expression.");
        return new ExpressionStmt(expr);
    }
    expression() {
        return this.assignment();
    }
    assignment() {
        // TO BE IMPLEMENTED: Assignment parsing
        throw new Error("Assignments not yet implemented");
    }
    // Helper methods
    match(...types) {
        for (const type of types) {
            if (this.check(type)) {
                this.advance();
                return true;
            }
        }
        return false;
    }
    check(type) {
        if (this.isAtEnd())
            return false;
        return this.peek().type === type;
    }
    advance() {
        if (!this.isAtEnd())
            this.current++;
        return this.previous();
    }
    isAtEnd() {
        return this.peek().type === lexer_1.TokenType.EOF;
    }
    peek() {
        return this.tokens[this.current];
    }
    previous() {
        return this.tokens[this.current - 1];
    }
    consume(type, message) {
        if (this.check(type))
            return this.advance();
        throw this.error(this.peek(), message);
    }
    error(token, message) {
        // Report the error
        if (token.type === lexer_1.TokenType.EOF) {
            console.error(`Error at end: ${message}`);
        }
        else {
            console.error(`Error at '${token.lexeme}' line ${token.line}: ${message}`);
        }
        return new Error(message);
    }
    synchronize() {
        this.advance();
        while (!this.isAtEnd()) {
            if (this.previous().type === lexer_1.TokenType.SEMICOLON)
                return;
            switch (this.peek().type) {
                case lexer_1.TokenType.CONTRACT:
                case lexer_1.TokenType.STRUCT:
                case lexer_1.TokenType.FUNCTION:
                case lexer_1.TokenType.EVENT:
                case lexer_1.TokenType.ERROR:
                case lexer_1.TokenType.IF:
                case lexer_1.TokenType.WHILE:
                case lexer_1.TokenType.FOR:
                case lexer_1.TokenType.RETURN:
                    return;
            }
            this.advance();
        }
    }
}
exports.Parser = Parser;
//# sourceMappingURL=parser.js.map