/**
 * Init command - Creates a new Grishex project
 */

import * as fs from 'fs-extra';
import * as path from 'path';
import chalk from 'chalk';
import ora from 'ora';

interface InitOptions {
  template: string;
}

/**
 * Creates a new Grishex project with the specified name and options
 */
export async function initCommand(projectName: string, options: InitOptions): Promise<void> {
  console.log(`\n${chalk.cyan('Creating a new Grishex project:')} ${chalk.green(projectName)}\n`);
  
  const spinner = ora('Setting up project structure...').start();
  
  try {
    // Create project directory
    await fs.mkdir(projectName);
    
    // Create project structure
    await fs.mkdir(path.join(projectName, 'contracts'));
    await fs.mkdir(path.join(projectName, 'tests'));
    await fs.mkdir(path.join(projectName, 'scripts'));
    await fs.mkdir(path.join(projectName, 'build'));
    
    // Create configuration file
    const configContent = {
      compiler: {
        version: "1.0.0",
        optimize: true
      },
      networks: {
        testnet: {
          url: "https://testnet.grishinium.com",
          chainId: 1337
        },
        mainnet: {
          url: "https://mainnet.grishinium.com",
          chainId: 1
        }
      }
    };
    
    await fs.writeFile(
      path.join(projectName, 'grishex.config.json'),
      JSON.stringify(configContent, null, 2)
    );
    
    // Create sample contract based on template
    await createSampleContract(projectName, options.template);
    
    // Create package.json
    const packageJsonContent = {
      name: projectName,
      version: "0.1.0",
      description: "Grishex smart contract project",
      scripts: {
        "compile": "grishex compile",
        "test": "grishex test",
        "deploy": "grishex deploy"
      },
      dependencies: {
        "grishex-cli": "^1.0.0"
      }
    };
    
    await fs.writeFile(
      path.join(projectName, 'package.json'),
      JSON.stringify(packageJsonContent, null, 2)
    );
    
    // Create README.md
    const readmeContent = `# ${projectName}

A smart contract project built with Grishex for the Grishinium blockchain.

## Getting Started

\`\`\`bash
# Install dependencies
npm install

# Compile contracts
npm run compile

# Run tests
npm run test

# Deploy contracts
npm run deploy
\`\`\`
`;
    
    await fs.writeFile(
      path.join(projectName, 'README.md'),
      readmeContent
    );
    
    spinner.succeed('Project structure created successfully');
    
    // Print success message and next steps
    console.log(`\n${chalk.green('Success!')} Created ${projectName} at ${path.resolve(projectName)}`);
    console.log('\nWe suggest that you begin by typing:\n');
    console.log(`${chalk.cyan('  cd')} ${projectName}`);
    console.log(`${chalk.cyan('  npm install')}`);
    console.log(`${chalk.cyan('  npm run compile')}\n`);
  } catch (error) {
    spinner.fail('Failed to create project');
    console.error('Error:', error);
    process.exit(1);
  }
}

/**
 * Creates a sample contract based on the selected template
 */
async function createSampleContract(projectName: string, template: string): Promise<void> {
  let contractContent: string;
  
  switch (template) {
    case 'token':
      contractContent = `contract Token {
  string public name = "MyToken";
  string public symbol = "MTK";
  uint public decimals = 18;
  uint public totalSupply = 0;
  
  mapping(address => uint) public balances;
  
  event Transfer(address indexed from, address indexed to, uint amount);
  
  constructor(string memory _name, string memory _symbol) {
    name = _name;
    symbol = _symbol;
  }
  
  function mint(address to, uint amount) public {
    totalSupply += amount;
    balances[to] += amount;
    emit Transfer(address(0), to, amount);
  }
  
  function transfer(address to, uint amount) public returns (bool) {
    if (balances[msg.sender] < amount) {
      revert InsufficientBalance(msg.sender, amount, balances[msg.sender]);
    }
    
    balances[msg.sender] -= amount;
    balances[to] += amount;
    emit Transfer(msg.sender, to, amount);
    return true;
  }
}`;
      break;
      
    case 'nft':
      contractContent = `contract NFT {
  // Token data structure
  struct Token {
    uint id;
    string uri;
    address owner;
  }
  
  // All tokens in this collection
  Token[] public tokens;
  
  // Mapping from token ID to owner
  mapping(uint => address) public owners;
  
  // Event for token transfers
  event Transfer(address from, address to, uint tokenId);
  
  // Mint a new token
  function mint(string memory uri) public returns (uint) {
    uint tokenId = tokens.length;
    tokens.push(Token(tokenId, uri, msg.sender));
    owners[tokenId] = msg.sender;
    
    emit Transfer(address(0), msg.sender, tokenId);
    return tokenId;
  }
  
  // Transfer token
  function transfer(address to, uint tokenId) public {
    // Must be owner
    assert(owners[tokenId] == msg.sender);
    
    // Update ownership
    owners[tokenId] = to;
    tokens[tokenId].owner = to;
    
    emit Transfer(msg.sender, to, tokenId);
  }
}`;
      break;
      
    case 'dex':
      contractContent = `contract DEX {
  // Token pair for this DEX
  struct Pair {
    address tokenA;
    address tokenB;
    uint reserveA;
    uint reserveB;
  }
  
  // The active trading pair
  Pair public pair;
  
  // Total liquidity tokens
  uint public totalLiquidity;
  
  // Liquidity balances
  mapping(address => uint) public liquidity;
  
  // Events
  event LiquidityAdded(address provider, uint amountA, uint amountB);
  event Swap(address user, uint amountIn, uint amountOut, bool aToB);
  
  // Add liquidity to the pool
  function addLiquidity(uint amountA, uint amountB) public returns (uint) {
    // Transfer tokens to contract
    ERC20(pair.tokenA).transferFrom(msg.sender, address(this), amountA);
    ERC20(pair.tokenB).transferFrom(msg.sender, address(this), amountB);
    
    // Calculate liquidity tokens to mint
    uint liquidityMinted;
    if (totalLiquidity == 0) {
      liquidityMinted = sqrt(amountA * amountB);
      totalLiquidity = liquidityMinted;
    } else {
      liquidityMinted = min(
        (amountA * totalLiquidity) / pair.reserveA,
        (amountB * totalLiquidity) / pair.reserveB
      );
    }
    
    // Update reserves
    pair.reserveA += amountA;
    pair.reserveB += amountB;
    
    // Mint liquidity tokens
    liquidity[msg.sender] += liquidityMinted;
    
    emit LiquidityAdded(msg.sender, amountA, amountB);
    return liquidityMinted;
  }
  
  // Swap tokens
  function swap(uint amountIn, bool aToB) public returns (uint) {
    // Calculate amount out based on constant product formula
    uint amountOut;
    if (aToB) {
      amountOut = getAmountOut(amountIn, pair.reserveA, pair.reserveB);
      ERC20(pair.tokenA).transferFrom(msg.sender, address(this), amountIn);
      ERC20(pair.tokenB).transfer(msg.sender, amountOut);
      pair.reserveA += amountIn;
      pair.reserveB -= amountOut;
    } else {
      amountOut = getAmountOut(amountIn, pair.reserveB, pair.reserveA);
      ERC20(pair.tokenB).transferFrom(msg.sender, address(this), amountIn);
      ERC20(pair.tokenA).transfer(msg.sender, amountOut);
      pair.reserveB += amountIn;
      pair.reserveA -= amountOut;
    }
    
    emit Swap(msg.sender, amountIn, amountOut, aToB);
    return amountOut;
  }
  
  // Helper: Calculate output amount
  function getAmountOut(uint amountIn, uint reserveIn, uint reserveOut) 
    internal pure returns (uint) {
    uint amountInWithFee = amountIn * 997; // 0.3% fee
    uint numerator = amountInWithFee * reserveOut;
    uint denominator = (reserveIn * 1000) + amountInWithFee;
    return numerator / denominator;
  }
}`;
      break;
      
    default: // default template
      contractContent = `contract HelloWorld {
  // A simple Hello World contract
  string public message;
  
  event MessageUpdated(string oldMessage, string newMessage);
  
  constructor(string memory initialMessage) {
    message = initialMessage;
  }
  
  function updateMessage(string memory newMessage) public {
    string memory oldMessage = message;
    message = newMessage;
    emit MessageUpdated(oldMessage, newMessage);
  }
  
  function getMessage() public view returns (string memory) {
    return message;
  }
}`;
      break;
  }
  
  // Write the contract to file
  const contractFileName = template === 'default' ? 'HelloWorld.gx' : 
                          (template === 'token' ? 'Token.gx' : 
                          (template === 'nft' ? 'NFT.gx' : 'DEX.gx'));
  
  await fs.writeFile(
    path.join(projectName, 'contracts', contractFileName),
    contractContent
  );
} 