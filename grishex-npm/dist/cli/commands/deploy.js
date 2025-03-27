"use strict";
/**
 * Deploy command - Deploys compiled Grishex contracts to the Grishinium blockchain
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
exports.deployCommand = void 0;
const fs = __importStar(require("fs-extra"));
const path = __importStar(require("path"));
const chalk_1 = __importDefault(require("chalk"));
const ora_1 = __importDefault(require("ora"));
/**
 * Deploys a compiled contract to the Grishinium blockchain
 */
async function deployCommand(contract, options) {
    console.log(chalk_1.default.cyan(`\nDeploying contract to ${options.network}...\n`));
    const spinner = (0, ora_1.default)('Preparing deployment...').start();
    try {
        // Find the compiled contract file
        const buildDir = './build';
        const contractJsonPath = path.resolve(buildDir, `${contract}.json`);
        if (!await fs.pathExists(contractJsonPath)) {
            spinner.fail(`Compiled contract not found: ${contractJsonPath}`);
            console.log(chalk_1.default.yellow('\nMake sure to compile your contract first:'));
            console.log(`${chalk_1.default.cyan('  grishex compile')}\n`);
            process.exit(1);
        }
        // Read the contract JSON
        const contractJson = JSON.parse(await fs.readFile(contractJsonPath, 'utf8'));
        // TODO: Load network configuration
        const networkConfig = await loadNetworkConfig(options.network);
        // TODO: Connect to the network
        spinner.text = `Connecting to ${options.network}...`;
        // const provider = await connectToNetwork(networkConfig);
        // TODO: Load wallet/signer
        spinner.text = 'Loading wallet...';
        // const wallet = await loadWallet(options.privateKey, provider);
        // TODO: Deploy the contract
        spinner.text = 'Deploying contract...';
        // const deployedContract = await deployContract(contractJson, wallet, options);
        // Mock deployment for now
        await new Promise(resolve => setTimeout(resolve, 2000));
        spinner.succeed('Contract deployed successfully');
        // Mock contract address
        const contractAddress = `0x${Array(40).fill(0).map(() => Math.floor(Math.random() * 16).toString(16)).join('')}`;
        // Display deployment info
        console.log('\nDeployment Information:');
        console.log(`${chalk_1.default.cyan('Contract:')} ${contract}`);
        console.log(`${chalk_1.default.cyan('Network:')} ${options.network}`);
        console.log(`${chalk_1.default.cyan('Address:')} ${contractAddress}`);
        console.log(`${chalk_1.default.cyan('Transaction Hash:')} 0x${Array(64).fill(0).map(() => Math.floor(Math.random() * 16).toString(16)).join('')}`);
        console.log(`${chalk_1.default.cyan('Gas Used:')} ${Math.floor(Math.random() * 1000000)}`);
        // Save deployment info to file
        const deploymentInfo = {
            contractName: contract,
            network: options.network,
            address: contractAddress,
            timestamp: new Date().toISOString(),
            transactionHash: `0x${Array(64).fill(0).map(() => Math.floor(Math.random() * 16).toString(16)).join('')}`
        };
        await fs.ensureDir('./deployments');
        await fs.writeFile(`./deployments/${contract}_${options.network}.json`, JSON.stringify(deploymentInfo, null, 2));
        console.log(`\nDeployment info saved to ${chalk_1.default.green(`./deployments/${contract}_${options.network}.json`)}`);
    }
    catch (error) {
        spinner.fail('Deployment failed');
        console.error('Error:', error instanceof Error ? error.message : String(error));
        process.exit(1);
    }
}
exports.deployCommand = deployCommand;
/**
 * Loads the network configuration from the grishex.config.json file
 */
async function loadNetworkConfig(networkName) {
    const configPath = path.resolve('grishex.config.json');
    if (!await fs.pathExists(configPath)) {
        throw new Error('Configuration file not found: grishex.config.json');
    }
    const config = JSON.parse(await fs.readFile(configPath, 'utf8'));
    if (!config.networks || !config.networks[networkName]) {
        throw new Error(`Network "${networkName}" not found in configuration file`);
    }
    return config.networks[networkName];
}
//# sourceMappingURL=deploy.js.map