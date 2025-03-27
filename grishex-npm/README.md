# Grishex Language

Grishex is a next-generation smart contract programming language designed specifically for the Grishinium Blockchain. It combines the simplicity of JavaScript with rigorous type safety and security features to create secure, efficient, and scalable decentralized applications.

## Features

- ✅ **Type Safety**: Strong static typing with compile-time checking
- ✅ **HoloShard Compatible**: Built-in support for cross-shard operations
- ✅ **Memory Safety**: Automatic memory management to prevent common vulnerabilities
- ✅ **Gas Optimization**: Compiler optimizations for reduced transaction costs
- ✅ **Formal Verification**: Built-in tools for mathematical proof of contract correctness
- ✅ **Developer-Friendly**: Clean, JavaScript-inspired syntax with modern features

## Installation

```bash
npm install -g grishex-cli
```

## Quick Start

Create a new Grishex project:

```bash
grishex init my-dapp
cd my-dapp
npm install
```

Compile your contracts:

```bash
grishex compile
```

Deploy to the Grishinium blockchain:

```bash
grishex deploy --network testnet
```

## Documentation

Comprehensive documentation is available at [docs.grishinium.com/grishex](https://docs.grishinium.com/grishex).

## Example Contract

```javascript
contract TokenSwap {
  // Token balances for each address
  mapping(address => uint) public balances;
  
  // Event emitted on successful swap
  event Swap(
    address indexed sender,
    uint amount,
    address tokenAddress
  );
  
  // Swap tokens between users
  function swap(address recipient, uint amount) public {
    // Check if the sender has enough tokens
    if (balances[msg.sender] < amount) {
      revert InsufficientBalance();
    }
    
    // Update balances
    balances[msg.sender] -= amount;
    balances[recipient] += amount;
    
    // Emit swap event
    emit Swap(msg.sender, amount, address(this));
  }
}
```

## License

MIT 