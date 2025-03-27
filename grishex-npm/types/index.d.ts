// Тип-заглушки для модулей, у которых нет встроенных типов

declare module 'ora' {
  interface OraInstance {
    start(text?: string): OraInstance;
    stop(): OraInstance;
    succeed(text?: string): OraInstance;
    fail(text?: string): OraInstance;
    warn(text?: string): OraInstance;
    info(text?: string): OraInstance;
    text: string;
  }
  
  interface OraOptions {
    text?: string;
    color?: string;
    spinner?: string | { frames: string[] };
  }
  
  function ora(options?: string | OraOptions): OraInstance;
  
  export = ora;
}

declare module 'chalk' {
  type ChalkFunction = (text: string) => string;
  
  interface ChalkConstructor {
    (text: string): string;
    red: ChalkFunction;
    green: ChalkFunction;
    blue: ChalkFunction;
    yellow: ChalkFunction;
    cyan: ChalkFunction;
    magenta: ChalkFunction;
    white: ChalkFunction;
    black: ChalkFunction;
    gray: ChalkFunction;
    grey: ChalkFunction;
    bold: ChalkFunction;
    italic: ChalkFunction;
    underline: ChalkFunction;
    inverse: ChalkFunction;
    strikethrough: ChalkFunction;
    bgRed: ChalkFunction;
    bgGreen: ChalkFunction;
    bgBlue: ChalkFunction;
    bgYellow: ChalkFunction;
    bgCyan: ChalkFunction;
    bgMagenta: ChalkFunction;
    bgWhite: ChalkFunction;
    bgBlack: ChalkFunction;
  }
  
  const chalk: ChalkConstructor;
  
  export = chalk;
} 