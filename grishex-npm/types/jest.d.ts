declare global {
  function describe(name: string, fn: () => void): void;
  function test(name: string, fn: () => void): void;
  function expect(value: any): {
    toBe(expected: any): void;
    toEqual(expected: any): void;
    toBeTruthy(): void;
    toBeFalsy(): void;
    toContain(expected: any): void;
    toHaveLength(expected: number): void;
  };
}

export {}; 