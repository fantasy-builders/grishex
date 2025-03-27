/**
 * Compile command - Compiles Grishex contracts to bytecode
 */

import * as fs from 'fs-extra';
import * as path from 'path';
import chalk from 'chalk';
import ora from 'ora';
import { Lexer } from '../../compiler/lexer';
import { Parser } from '../../compiler/parser';

interface CompileOptions {
  output: string;
  optimize: boolean;
  path: string;
}

/**
 * Compiles Grishex contracts in the specified directory
 */
export async function compileCommand(options: CompileOptions): Promise<void> {
  console.log(chalk.cyan('\nCompiling Grishex contracts...\n'));
  
  const spinner = ora('Finding contract files...').start();
  
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
      const spinner = ora(`Compiling ${chalk.blue(relativePath)}...`).start();
      
      try {
        // Read the contract source
        const source = await fs.readFile(file, 'utf8');
        
        // TODO: Implement actual compilation
        const compiledOutput = await compileContract(source, file, options.optimize);
        
        // Write the output to the build directory
        const outputFilename = path.basename(file, '.gx') + '.json';
        const outputPath = path.join(options.output, outputFilename);
        
        await fs.writeFile(outputPath, JSON.stringify(compiledOutput, null, 2));
        
        spinner.succeed(`Successfully compiled ${chalk.blue(relativePath)}`);
        successCount++;
      } catch (error) {
        spinner.fail(`Failed to compile ${chalk.blue(relativePath)}`);
        console.error(chalk.red(error instanceof Error ? error.message : String(error)));
        failCount++;
      }
    }
    
    // Print summary
    console.log('\nCompilation summary:');
    console.log(`${chalk.green(`✓ ${successCount} contracts compiled successfully`)}`);
    if (failCount > 0) {
      console.log(`${chalk.red(`✗ ${failCount} contracts failed to compile`)}`);
    }
    
    if (failCount > 0) {
      process.exit(1);
    }
  } catch (error) {
    spinner.fail('Compilation failed');
    console.error('Error:', error);
    process.exit(1);
  }
}

/**
 * Finds all .gx files in the specified directory and its subdirectories
 */
async function findContractFiles(dir: string): Promise<string[]> {
  const files: string[] = [];
  
  // Read the directory
  const entries = await fs.readdir(dir, { withFileTypes: true });
  
  // Process each entry
  for (const entry of entries) {
    const fullPath = path.join(dir, entry.name);
    
    if (entry.isDirectory()) {
      // Recursively search subdirectories
      const subDirFiles = await findContractFiles(fullPath);
      files.push(...subDirFiles);
    } else if (entry.isFile() && entry.name.endsWith('.gx')) {
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
async function compileContract(source: string, filePath: string, optimize: boolean): Promise<any> {
  try {
    // Lexical analysis
    const lexer = new Lexer(source);
    const tokens = lexer.tokenize();
    
    // Parsing - Generate AST
    const parser = new Parser(tokens);
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
  } catch (error) {
    throw new Error(`Compilation error in ${filePath}: ${error instanceof Error ? error.message : String(error)}`);
  }
} 