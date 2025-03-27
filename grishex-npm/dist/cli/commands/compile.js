"use strict";
/**
 * Compile command - Compiles Grishex contracts to bytecode
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
var __setModuleDefault = (this && this.__setModuleDefault) || (Object.create ? (function(o, v) {
    Object.defineProperty(o, "default", { enumerable: true, value: v });
}) : function(o, v) {
    o["default"] = v;
});
var __importStar = (this && this.__importStar) || function (mod) {
    if (mod && mod.__esModule) return mod;
    var result = {};
    if (mod != null) for (var k in mod) if (k !== "default" && Object.prototype.hasOwnProperty.call(mod, k)) __createBinding(result, mod, k);
    __setModuleDefault(result, mod);
    return result;
};
var __importDefault = (this && this.__importDefault) || function (mod) {
    return (mod && mod.__esModule) ? mod : { "default": mod };
};
Object.defineProperty(exports, "__esModule", { value: true });
exports.compileCommand = void 0;
const fs = __importStar(require("fs-extra"));
const path = __importStar(require("path"));
const chalk_1 = __importDefault(require("chalk"));
const ora_1 = __importDefault(require("ora"));
const lexer_1 = require("../../compiler/lexer");
const parser_1 = require("../../compiler/parser");
/**
 * Compiles Grishex contracts in the specified directory
 */
async function compileCommand(options) {
    console.log(chalk_1.default.cyan('\nCompiling Grishex contracts...\n'));
    const spinner = (0, ora_1.default)('Finding contract files...').start();
    try {
        // Ensure output directory exists
        await fs.ensureDir(options.output);
        // Find all .gx files in the contracts directory
        const contractsDir = path.resolve(options.path);
        if (!await fs.pathExists(contractsDir)) {
            spinner.fail(`Contracts directory not found: ${contractsDir}`);
            process.exit(1);
        }
        const contractFiles = await findContractFiles(contractsDir);
        if (contractFiles.length === 0) {
            spinner.info('No contract files found');
            return;
        }
        spinner.succeed(`Found ${contractFiles.length} contract file(s)`);
        // Compile each contract
        let successCount = 0;
        let failCount = 0;
        for (const file of contractFiles) {
            const relativePath = path.relative(process.cwd(), file);
            const spinner = (0, ora_1.default)(`Compiling ${chalk_1.default.blue(relativePath)}...`).start();
            try {
                // Read the contract source
                const source = await fs.readFile(file, 'utf8');
                // TODO: Implement actual compilation
                const compiledOutput = await compileContract(source, file, options.optimize);
                // Write the output to the build directory
                const outputFilename = path.basename(file, '.gx') + '.json';
                const outputPath = path.join(options.output, outputFilename);
                await fs.writeFile(outputPath, JSON.stringify(compiledOutput, null, 2));
                spinner.succeed(`Successfully compiled ${chalk_1.default.blue(relativePath)}`);
                successCount++;
            }
            catch (error) {
                spinner.fail(`Failed to compile ${chalk_1.default.blue(relativePath)}`);
                console.error(chalk_1.default.red(error instanceof Error ? error.message : String(error)));
                failCount++;
            }
        }
        // Print summary
        console.log('\nCompilation summary:');
        console.log(`${chalk_1.default.green(`✓ ${successCount} contracts compiled successfully`)}`);
        if (failCount > 0) {
            console.log(`${chalk_1.default.red(`✗ ${failCount} contracts failed to compile`)}`);
        }
        if (failCount > 0) {
            process.exit(1);
        }
    }
    catch (error) {
        spinner.fail('Compilation failed');
        console.error('Error:', error);
        process.exit(1);
    }
}
exports.compileCommand = compileCommand;
/**
 * Finds all .gx files in the specified directory and its subdirectories
 */
async function findContractFiles(dir) {
    const files = [];
    // Read the directory
    const entries = await fs.readdir(dir, { withFileTypes: true });
    // Process each entry
    for (const entry of entries) {
        const fullPath = path.join(dir, entry.name);
        if (entry.isDirectory()) {
            // Recursively search subdirectories
            const subDirFiles = await findContractFiles(fullPath);
            files.push(...subDirFiles);
        }
        else if (entry.isFile() && entry.name.endsWith('.gx')) {
            // Add Grishex files to the list
            files.push(fullPath);
        }
    }
    return files;
}
/**
 * Compiles a single Grishex contract
 *
 * This is a placeholder for the actual compilation implementation
 */
async function compileContract(source, filePath, optimize) {
    try {
        // Lexical analysis
        const lexer = new lexer_1.Lexer(source);
        const tokens = lexer.tokenize();
        // Parsing - Generate AST
        const parser = new parser_1.Parser(tokens);
        const ast = parser.parse();
        // TODO: Type checking
        // TODO: Optimization
        // TODO: Code generation
        // For now, return a mock output
        return {
            contractName: path.basename(filePath, '.gx'),
            source: source,
            abi: [],
            bytecode: "0x",
            deployedBytecode: "0x",
            compiler: {
                name: "grishex",
                version: "1.0.0"
            },
            ast: JSON.stringify(ast),
            timestamp: new Date().toISOString()
        };
    }
    catch (error) {
        throw new Error(`Compilation error in ${filePath}: ${error instanceof Error ? error.message : String(error)}`);
    }
}
//# sourceMappingURL=compile.js.map