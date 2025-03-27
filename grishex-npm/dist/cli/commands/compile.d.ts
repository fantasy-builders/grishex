/**
 * Compile command - Compiles Grishex contracts to bytecode
 */
interface CompileOptions {
    output: string;
    optimize: boolean;
    path: string;
}
/**
 * Compiles Grishex contracts in the specified directory
 */
export declare function compileCommand(options: CompileOptions): Promise<void>;
export {};
