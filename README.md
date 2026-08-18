# Orbital Lab

## Overview
This is a project exploring the physics behind orbital mechanics.

## Numerical Method
This simulator uses semi-implicit Euler integration, reducing numerical drift in specific orbital energy after the tested simulation duration.

## Validation
A circular orbit with a radius of 7,000 km was simulated for 9,000 seconds using different timestep sizes. Both specific orbital energy and specific angular momentum were measured. Semi-implicit Euler produced substantially less energy drift than forward Euler. Specific angular momentum remained conserved to approximately floating-point precision.

## Results
| Integrator          |   Δt | Energy change |
| ------------------- | ---: | ------------: |
| Forward Euler       |  1 s |         2.01% |
| Forward Euler       | 30 s |        29.71% |
| Semi-implicit Euler |  1 s |     0.000114% |
| Semi-implicit Euler | 30 s |       0.1005% |

## Current Limitations
- Multi-body simulation not supported

## Requirements
- Python installed on your device.
- matplotlib library installed on your device.
- Memory requirement depends on simulation demands.

## Running the simulation
1. Download `Main.py`
2. Either run the program via command line or through your supported IDE of choice.