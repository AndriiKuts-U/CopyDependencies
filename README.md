# CopyDependencies
This simple program is used to copy all #indlude files in .c, .cpp, .h and ,hpp files into different folder. 
The program works recursively. After finding the #include in the file, the program will be executed again with the found library. In this way, it will be possible to copy the dependencies of a certain file and the dependencies of its dependencies.  The program also saves the structure of the includes, so that later compilation errors do not occur, for example after finding the #include "folder1\folder2\file.xxx" the program will find the "file.xxx" and copy it in a similar structure in the destination path.

The program can be useful for people working on large projects with a large number of modules and a complex structure. 




