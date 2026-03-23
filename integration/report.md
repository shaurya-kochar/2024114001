# Integration Testing Report: StreetRace Manager

## System Architecture

The StreetRace Manager system is designed as a modular racing simulator.
It focuses on crew management, resource management (inventory/cash), race encounters, and special missions.

The underlying base modules implemented are:
1. **Registration**: Manages driver and crew records.
2. **CrewManagement**: Enhances registration with role verification, skills, and constraints for mission capabilities.
3. **Inventory**: Manages cars (healthy vs damaged state), garage items, and bankroll.
4. **Results**: Simulates race successes based on RNG and flags cars for damage.
5. **RaceManagement**: Evaluates car and driver requirements from the pool, then calls results and routes consequences to inventory.
6. **MissionPlanning**: Dedicated subsystem for complex "heists" or "rescue" operations, demanding specific crew composition and specific asset states (e.g. damaged vehicles for a repair mission).
7. **Shop**: Acts as an interface to drain cash in exchange for single-use parts like `nitrous`.
8. **PowerUps**: Plugs into inventory to use purchased single-use items dynamically.

The system scales efficiently by using a central controller (`GameManager`) which wraps these isolated sub-modules. The `GameManager` performs dependency injection of shared references into each module during `__init__`.

## Call Flow Mapping

As demonstrated in `integration/diagrams/call_graph_summary.md`, calling a simplified facade method on `GameManager` (such as `handle_run_race`) propagates state changes down the graph.
Races query `Registration` to ensure a driver role exists, `Inventory` to ensure a non-damaged car is chosen, then trigger `Results`. Any resultant damages or payouts are safely committed back into `Inventory`.

Missions represent complex intersections. For example, `assign_mission("repair")` touches `CrewManagement` to ensure a `mechanic` is on deck and checks `Inventory` for any `damaged_cars` before successfully reinstating a damaged asset back into play.

## Integration Strategies & Pytest

A total of 15+ tests cover multiple intersections.
By instantiating a fresh `GameManager(config)` in the Pytest fixture, each test executes high-level flows that mutate multiple objects:

*   **Test 1: Full registration to repair flow:** Tests that `GameManager` correctly registers a member, fails a rescue because a second member is needed, successfully completes a repair mission by requiring a mechanic, and mutates inventory.
*   **Test 2: Racing economy and Powerup consumption:** Buying `nitrous` checks shop validation, removes cash from `Inventory`, and unlocks `PowerUps.use_power_up()`.

Our testing methodology emphasized "chaining" calls across different modules. No mocks are utilized. Every transaction ensures that all inter-object communication happens in an integrated test environment mimicking actual user execution.
