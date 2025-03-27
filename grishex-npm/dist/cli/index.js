#!/usr/bin/env node
"use strict";
/**
 * Grishex CLI - Command Line Interface for the Grishex Programming Language
 *
 * This is the main entry point for the CLI tool.
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
Object.defineProperty(exports, "__esModule", { value: true });
const commander_1 = require("commander");
const fs = __importStar(require("fs-extra"));
const path = __importStar(require("path"));
// Import commands
const init_1 = require("./commands/init");
const compile_1 = require("./commands/compile");
const deploy_1 = require("./commands/deploy");
// Get version from package.json
const packageJsonPath = path.join(__dirname, '../../package.json');
const packageJson = JSON.parse(fs.readFileSync(packageJsonPath, 'utf8'));
const version = packageJson.version;
// Create CLI program
const program = new commander_1.Command();
program
    .name('grishex')
    .description('Grishex Smart Contract Language CLI')
    .version(version);
// Initialize command
program
    .command('init')
    .description('Create a new Grishex project')
    .argument('<project-name>', 'name of the project')
    .option('-t, --template <template>', 'template to use', 'default')
    .action(init_1.initCommand);
// Compile command
program
    .command('compile')
    .description('Compile Grishex contracts')
    .option('-o, --output <dir>', 'output directory', './build')
    .option('--optimize', 'apply optimization', false)
    .option('-p, --path <path>', 'path to contract files', './contracts')
    .action(compile_1.compileCommand);
// Deploy command
program
    .command('deploy')
    .description('Deploy contract to Grishinium blockchain')
    .argument('<contract>', 'contract to deploy')
    .option('-n, --network <network>', 'target network', 'testnet')
    .option('--private-key <key>', 'private key file')
    .option('--gas-limit <limit>', 'gas limit for transaction', '3000000')
    .option('--gas-price <price>', 'gas price in wei', '1000000000')
    .action(deploy_1.deployCommand);
// Add more commands here...
// Parse command line arguments
program.parse(process.argv);
// If no arguments, show help
if (process.argv.length === 2) {
    program.help();
}
//# sourceMappingURL=index.js.map