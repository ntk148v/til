# Everything is a file

"Everything is a file" is an approach to interface design in Unix derivatives. While this turn of phrase does not as such figure as a Unix design principle or philosophy, it is a common way to analyse designs, and informs the design of new interfaces in a way that prefers, in rough order of import:

1. representing objects as file descriptors instead of alternatives like abstract handles or names,
2. operating on the objects with standard input/output operations, returning byte streams to be interpreted by applications (rather than explicitly structured data), and
3. allowing the usage or creation of objects by opening or creating files in the global filesystem name space.

The lines between the common interpretations of "file" and "file descriptor" are often blurred when analysing Unix, and nameability of files is the least important part of this principle; thus, it is sometimes described as "Everything is a file descriptor".
