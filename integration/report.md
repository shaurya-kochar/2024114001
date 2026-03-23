# Integration Testing Report

## Overview
This report details the integration testing methodology, structure, and execution for the MoneyPoly application. Rather than isolating individual units of code with full isolation techniques, integration testing validates that combined components behave correctly when working in tandem. 

## Integration Approach
An OOP game like MoneyPoly demands interaction between a central controller and multiple state-managing nodes. The integration tests initialize a fully featured `Game` loop connecting the `Board`, `Bank`, `Dice`, and `Player` components, mirroring a standard execution sequence.

Only purely unpredictable interfaces (like `random.randint` from `Dice.roll` or `builtins.input` via `ui`) were lightly patched using `unittest.mock.patch` to allow the test suite to progress synchronously, predictably, and autonomously without hanging on `stdin`.

### Modules Inter-Connected

- **Game ↔ Board ↔ Player**: Simulated rolling logic evaluates how the current player fetches the correct board tile array, executes exact coordinates, and applies contextual rules (like checking `Property` purchase bounds or triggering Go To Jail transitions).
- **Game ↔ Property ↔ Player**: Validates property interactions, namely `mortgage_property()` and `unmortgage_property()`. Also evaluates complex algorithms like `pay_rent()` combined with the `FULL_GROUP_MULTIPLIER` rules mapped in `PropertyGroup`.
- **Game ↔ Bank ↔ Player**: Verifies monetary transactions representing standard purchases, auction allocations, and bankruptcy routines cleaning up internal arrays smoothly.
- **Game ↔ UI**: By mocking `safe_int_input` and `confirm`, integration tests efficiently proved that terminal navigation yields identical backend model alterations. 

## Coverage Provided
The repository's `/integration` setup provides 18 explicit functional cases mapped to test the following systemic interactions:
1. **Initial Setup State Check** (Initialization connections).
2. **Move Board Dynamics** (Dice → Game → Player state shift).
3. **Turn Progression Rules** (Salary additions on passing GO).
4. **Property Trades and Purchases** (Transfers mapped between components).
5. **Jail Routines** (Bail payments dropping correct balances or forcing roll attempts).
6. **Card Resolvers** (Chance cards triggering absolute or relative modifiers on a player tracking object).
7. **Economy Limits** (Auction parsing and bankruptcy checks returning assets to Bank).

## Result Summary
All functional paths successfully compile, communicate, and update states exactly as predicted. No disconnected interactions or improper attribute references occur when simulating user behaviour natively via the test environment.
