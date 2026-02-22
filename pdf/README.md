# PDF

Source: <https://en.wikipedia.org/wiki/PDF>

**Portable Document Format (PDF)**, standardized as ISO 32000, is a file format developed by Adobe in 1992 to present documents, including text formatting and images, in a manner independent of application software, hardware, and operating systems

PDF files may contain a variety of content besides flat text and graphics including logical structuring elements, interactive elements such as annotations and form-fields, layers, rich media (including video content), three-dimensional objects using U3D or PRC, and various other data formats. The PDF specification also provides for encryption and digital signatures, file attachments, and metadata to enable workflows requiring these features.

## Technical details

A PDF file is often a combination of vector graphics, text, and bitmap graphics. The basic types of content in a PDF are:

- Typeset text stored as content streams.
- Vector graphics for illustrations and designs that consist of shapes and lines.
- Raster graphics for photographs and other types of images.
- Multimedia objects in the document.

## File format

A PDF file is organized using ASCII character, except for certain elements that may have binary content. The file starts with a header containing a magic number (as a readable string) and the version of the format, for example `%PDF-1.7`. The format is a subset of a COS ("Carousel" Object Structure) format. A COS tree file consists primarily of objects, of which there are nine types:

- Boolean values, representing true or false
- Real numbers
- Integers
- Strings, enclosed within parentheses ((...)) or represented as hexadecimal within single angle brackets (<...>). Strings may contain 8-bit characters.
- Names, starting with a forward slash (/)
- Arrays, ordered collections of objects enclosed within square brackets ([...])
- Dictionaries, collections of objects indexed by names enclosed within double angle brackets (<<...>>)
- Streams, usually containing large amounts of optionally compressed binary data, preceded by a dictionary and enclosed between the stream and endstream keywords.
- The null object
