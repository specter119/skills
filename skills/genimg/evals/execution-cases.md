# Execution Cases

## Case 1: Single Image Generation

- Input: brief concept description
- Expected: expand into a narrative prompt, generate a single usable illustration

## Case 2: Editing an Existing Image

- Input: existing image + partial modification request
- Expected: preserve subject and composition, modify only the specified style or lighting

## Case 3: Multi-Candidate Exploration

- Input: open-ended visual direction
- Expected: run the `variants + grid` workflow, produce multiple images for comparison
