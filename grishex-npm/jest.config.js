module.exports = {
  preset: 'ts-jest',
  testEnvironment: 'node',
  collectCoverage: true,
  coverageDirectory: 'coverage',
  testMatch: [
    "**/test/**/*.test.ts"
  ],
  coveragePathIgnorePatterns: [
    "/node_modules/",
    "/dist/"
  ],
  globals: {
    'ts-jest': {
      tsconfig: 'tsconfig.json'
    }
  }
}; 