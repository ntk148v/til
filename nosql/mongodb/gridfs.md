# GridFS

Source: <https://www.mongodb.com/docs/manual/core/gridfs/>

- GridFS is a specification for storing and retrieveing files that exceed the BSON-document size limit of 16MB.
- GridFS divides the file into parts, or chunks, and stores each chunk as a separate document. Default chunk size: 255kB.
- GridFS uses 2 collections to store files:
  - 1 collection stores the file chunks
  - 1 other stores file metadata.

![](https://www.mongodb.com/docs/drivers/node/current/includes/figures/GridFS-upload.png)

- When to use GridFS
  - Store files larger than 16MB.
  - If your filesystem limits the number of files in a directory, you can use GridFS to store as many files as needed.
  - When you want to access information from portions of large files without having to load whole files into memory, you can use GridFS to recall sections of files without reading the entire file into memory.
  - When you want to keep your files and metadata automatically synced and deployed across a number of systems of facilities, you can use GridFS.
- When not to use GridFS
  - If you need to update the content of the entire file atomically -> Store multiple versions of each file and specify the current version of the file in the metadata.
  - If your files are all smaller than the 16MB BSON Document Size limit -> store each file in a single document instead of using  GridFS.
