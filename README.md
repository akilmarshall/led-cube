# LED Cube

A library to control a class of led cubes of my own design.
Using ws2811 led's connected serially.

big thanks to iyassou's [matrix multiplication library](https://github.com/iyassou/umatrix) for micropython

## Theory

## Build Instructions

First use the horizontal form and solder together "sticks" of leds connecting the ground and power pins forming rails.
Then chain the din and dout pins of each led in the stick linearly connecting them.
For a 3x3x3 led cube one will assemble 9 led sticks.

Then use the vertical form to assemble led sticks into "walls", soldering together the ground and power rails.
For a 3x3x3 leds one will use 3 sticks and assemble 1 of 3 walls.

solder together the walls connecting the ground and power connections between them.

finally linearly solder the sticks together (din -> dout)

## API

The color of each led is tracked in Cube._state

```
Cube.set((x, y, z), (g, r, b))
```
the set method modifies Cube._state.

```
Cube.update()
```
the update method uses the information withing Cube._state and writes to the cube. 

```
Cube.fill((g, r, b))
```
writes the color (g, r, b) to each led in the cube.
Cube._state is not modified.

```
Cube.clear()
```
Shorthand for Cube.fill((0, 0, 0))

```
Cube.rotate_x()
Cube.rotate_y()
Cube.rotate_z()
```
Rotates Cube._state pi/2 counterclockwise about the specified central axis.
Computes the new positions using [homogenous coordinate transforms](https://www.cs.brandeis.edu/~cs155/Lecture_07_6.pdf).

```
Cube._map_update(A)
# A is a 4x4 homogenous matrix
```
A helper method to update each position using the matrix A.  
