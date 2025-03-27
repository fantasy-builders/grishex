/**
 * Init command - Creates a new Grishex project
 */
interface InitOptions {
    template: string;
}
/**
 * Creates a new Grishex project with the specified name and options
 */
export declare function initCommand(projectName: string, options: InitOptions): Promise<void>;
export {};
