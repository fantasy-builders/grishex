/**
 * Grishex Language - Main Entry Point
 * 
 * This file exports all the public APIs for the Grishex language
 */

// Export compiler components
export * from './compiler/lexer';
export * from './compiler/parser';

// Export CLI commands for programmatic use
export * from './cli/commands/init';
export * from './cli/commands/compile';
export * from './cli/commands/deploy';

// Export main compiler function
import { Lexer } from './compiler/lexer';
import { Parser } from './compiler/parser';

/**
 * Main compile function that takes Grishex source code and returns compiled output
 */
export function compile(source: string, options: { optimize?: boolean } = {}) {
  try {
    // Lexical analysis
    const lexer = new Lexer(source);
    const tokens = lexer.tokenize();
    
    // Parsing
    const parser = new Parser(tokens);
    const ast = parser.parse();
    
    // TODO: Type checking
    // TODO: Optimization (if options.optimize is true)
    // TODO: Code generation
    
    // For now, return a simplified output
    return {
      success: true,
      tokens,
      ast,
      bytecode: "0x", // Placeholder
      warnings: []
    };
  } catch (error) {
    return {
      success: false,
      error: error instanceof Error ? error.message : String(error),
      errorObject: error
    };
  }
}

/**
 * Version number of the Grishex language
 */
export const VERSION = '1.0.0'; 