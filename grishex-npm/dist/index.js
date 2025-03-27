"use strict";
/**
 * Grishex Language - Main Entry Point
 *
 * This file exports all the public APIs for the Grishex language
 */
var __createBinding = (this && this.__createBinding) || (Object.create ? (function(o, m, k, k2) {
    if (k2 === undefined) k2 = k;
    var desc = Object.getOwnPropertyDescriptor(m, k);
    if (!desc || ("get" in desc ? !m.__esModule : desc.writable || desc.configurable)) {
      desc = { enumerable: true, get: function() { return m[k]; } };
    }
    Object.defineProperty(o, k2, desc);
}) : (function(o, m, k, k2) {
    if (k2 === undefined) k2 = k;
    o[k2] = m[k];
}));
var __exportStar = (this && this.__exportStar) || function(m, exports) {
    for (var p in m) if (p !== "default" && !Object.prototype.hasOwnProperty.call(exports, p)) __createBinding(exports, m, p);
};
Object.defineProperty(exports, "__esModule", { value: true });
exports.VERSION = exports.compile = void 0;
// Export compiler components
__exportStar(require("./compiler/lexer"), exports);
__exportStar(require("./compiler/parser"), exports);
// Export CLI commands for programmatic use
__exportStar(require("./cli/commands/init"), exports);
__exportStar(require("./cli/commands/compile"), exports);
__exportStar(require("./cli/commands/deploy"), exports);
// Export main compiler function
const lexer_1 = require("./compiler/lexer");
const parser_1 = require("./compiler/parser");
/**
 * Main compile function that takes Grishex source code and returns compiled output
 */
function compile(source, options = {}) {
    try {
        // Lexical analysis
        const lexer = new lexer_1.Lexer(source);
        const tokens = lexer.tokenize();
        // Parsing
        const parser = new parser_1.Parser(tokens);
        const ast = parser.parse();
        // TODO: Type checking
        // TODO: Optimization (if options.optimize is true)
        // TODO: Code generation
        // For now, return a simplified output
        return {
            success: true,
            tokens,
            ast,
            bytecode: "0x",
            warnings: []
        };
    }
    catch (error) {
        return {
            success: false,
            error: error instanceof Error ? error.message : String(error),
            errorObject: error
        };
    }
}
exports.compile = compile;
/**
 * Version number of the Grishex language
 */
exports.VERSION = '1.0.0';
//# sourceMappingURL=index.js.map