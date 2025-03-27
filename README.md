# Grishex Language Project

![Grishex Logo](../Landing/public/images/grishex-logo.svg)

Welcome to the Grishex Language project! This repository contains the implementation of the Grishex programming language - a modern, secure, and efficient smart contract language designed specifically for the Grishinium Blockchain.

## Project Structure

This project is organized into the following components:

- **`grishex-npm/`**: The main npm package for Grishex language toolchain
  - Compiler implementation
  - CLI tools
  - Standard library
  - Developer tools

## Getting Started

### To set up the Grishex npm package for development:

1. Navigate to the npm package directory:
   ```bash
   cd grishex-npm
   ```

2. Run the setup script:
   ```bash
   ./setup.sh
   ```

   This will:
   - Install all dependencies
   - Build the package
   - Run tests
   - Link the package globally for development

3. Try out the CLI:
   ```bash
   grishex --help
   ```

### To create a new Grishex project:

```bash
grishex init my-dapp
cd my-dapp
npm install
```

### To compile Grishex contracts:

```bash
grishex compile
```

### To deploy a contract:

```bash
grishex deploy MyContract --network testnet
```

## Language Features

- ✅ **Type Safety**: Strong static typing with compile-time checking
- ✅ **HoloShard Compatible**: Built-in support for cross-shard operations
- ✅ **Memory Safety**: Automatic memory management to prevent common vulnerabilities
- ✅ **Gas Optimization**: Compiler optimizations for reduced transaction costs
- ✅ **Formal Verification**: Built-in tools for mathematical proof of contract correctness
- ✅ **Developer-Friendly**: Clean, JavaScript-inspired syntax with modern features

## Documentation

Comprehensive documentation is available in the [Grishex Documentation](../Landing/app/grishex) section of the Grishinium website.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details. 