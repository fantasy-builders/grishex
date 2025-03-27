/**
 * Grishex Language - Main Entry Point
 *
 * This file exports all the public APIs for the Grishex language
 */
export * from './compiler/lexer';
export * from './compiler/parser';
export * from './cli/commands/init';
export * from './cli/commands/compile';
export * from './cli/commands/deploy';
/**
 * Main compile function that takes Grishex source code and returns compiled output
 */
export declare function compile(source: string, options?: {
    optimize?: boolean;
}): {
    success: boolean;
    tokens: import("./compiler/lexer").Token[];
    ast: import("./compiler/parser").Stmt[];
    bytecode: string;
    warnings: never[];
    error?: undefined;
    errorObject?: undefined;
} | {
    success: boolean;
    error: string;
    errorObject: unknown;
    tokens?: undefined;
    ast?: undefined;
    bytecode?: undefined;
    warnings?: undefined;
};
/**
 * Version number of the Grishex language
 */
export declare const VERSION = "1.0.0";
