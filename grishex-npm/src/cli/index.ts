#!/usr/bin/env node

/**
 * Grishex CLI - Command Line Interface for the Grishex Programming Language
 * 
 * This is the main entry point for the CLI tool.
 */

import { Command } from 'commander';
import * as fs from 'fs-extra';
import * as path from 'path';
import chalk from 'chalk';

// Import commands
import { initCommand } from './commands/init';
import { compileCommand } from './commands/compile';
import { deployCommand } from './commands/deploy';

// Get version from package.json
const packageJsonPath = path.join(__dirname, '../../package.json');
const packageJson = JSON.parse(fs.readFileSync(packageJsonPath, 'utf8'));
const version = packageJson.version;

// Create CLI program
const program = new Command();

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
  .action(initCommand);

// Compile command
program
  .command('compile')
  .description('Compile Grishex contracts')
  .option('-o, --output <dir>', 'output directory', './build')
  .option('--optimize', 'apply optimization', false)
  .option('-p, --path <path>', 'path to contract files', './contracts')
  .action(compileCommand);

// Deploy command
program
  .command('deploy')
  .description('Deploy contract to Grishinium blockchain')
  .argument('<contract>', 'contract to deploy')
  .option('-n, --network <network>', 'target network', 'testnet')
  .option('--private-key <key>', 'private key file')
  .option('--gas-limit <limit>', 'gas limit for transaction', '3000000')
  .option('--gas-price <price>', 'gas price in wei', '1000000000')
  .action(deployCommand);

// Add more commands here...

// Parse command line arguments
program.parse(process.argv);

// If no arguments, show help
if (process.argv.length === 2) {
  program.help();
} 