# CesiumProject

Solution to Mount St. Helens surface distance problem solved using python. No external libraries are used for simplicity of solution and execution. 

# Run

Navigate to root directory of project and in command line enter:
`python main.py`

# Solution
Using simple slope equations `y = mx + b`, intersections of input path with triangle geometry are found in three passes. 
A horizontal line pass, vertical line pass, and diagonal line pass. This exploits the fact that all the traingles of the 'mesh' are oriented the same way. 
The below diagram illustrates this part does not take the actual heightmap or real distances into account.

<img src="https://github.com/theZiggurat/CesiumProject/blob/master/intersections.JPG?raw=false" width="700" height="400">

After intersections are determined, path lengths between intersections are determined using the heightmap and given spatial parameters. 
To do this we need the real 3D coordinates of each intersection. This is done in four cases. 
* Corner intersection - Easiest case as the z value will just be the height sampled at the heightmap at that point.
* Vertical/Horizontal intersection - These two cases are identical, using linear interpolation to determine what the height would be between two samples of the heightmap.
* Diagonal intersection - Similar to the last case, but linear interpolation is used along the hypotnuse of the triangle.

After scaling is applied using spatial parameters, the distances can be summed for all neighboring intersections, giving our resulting distance along the surface. 
