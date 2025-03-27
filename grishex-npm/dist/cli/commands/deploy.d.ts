/**
 * Deploy command - Deploys compiled Grishex contracts to the Grishinium blockchain
 */
interface DeployOptions {
    network: string;
    privateKey?: string;
    gasLimit: string;
    gasPrice: string;
}
/**
 * Deploys a compiled contract to the Grishinium blockchain
 */
export declare function deployCommand(contract: string, options: DeployOptions): Promise<void>;
export {};
