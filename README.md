# VTK plot script for ERT data

The code contains some funcitons to plot 3D resistivity distribtuions from vtk files.
So far, I could not get to work the funtions using the ```if __name__ == "__main__":``` because of some errors in the vtk wrapping; therefore the file cannot be used as module, copy-paste the function instead.

The file runs with 2 positional arguments from command-line:
* name of the vtk file (e.g., inversionResult.vtk)
* name of the scalar to plot (e.g., rho)




