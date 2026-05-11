# Execution Cases

## Scenario 1: Create an Exploration Notebook from Scratch

- Input: dataset, analysis goal, minimal constraints
- Expected: static analysis first, then decide whether to add lightweight UI

## Scenario 2: Clean Up an Out-of-Control Notebook

- Input: existing marimo notebook with scattered UI and complex cell dependencies
- Expected: consolidate cell cohesion, reduce exposed names, propose module extraction recommendations

## Scenario 3: Decide Whether to Extract a Module

- Input: a repeated piece of UI / chart / helper logic
- Expected: give a clear verdict of "keep in the notebook" or "extract to a module"
