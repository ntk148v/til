# DBMS architecture

Source: <https://www.javatpoint.com/dbms-architecture>

- The DBMS design depends upon its architecture. The basic client/server architecture is used to deal with a large number of PCs, web servers, database servers and other components that are connected with networks.
- The client/server architecture consists of many PCs and a workstation which are connected via the network.
- DBMS architecture depends upon how users are connected to the database to get their request done.

## 1. Types of DBMS Architecture

![](https://static.javatpoint.com/dbms/images/dbms-architecture.png)

## 1.1. 1-Tier Architecture

- The database is directly available to the user. It means the user can direclty sit on the DBMS and uses it.
- Development of the local application.

## 1.2. 2-Tier Architecture

- Applications on the client end can directly communicate with the database at the server side. For this interaction, API's like: ODBC, JDBC are used.
- The user interfaces and application programs are run on the client-side.
- The server side is responsible to provide the functionalities like: query processing and transaction management.
- To communicate with the DBMS, client-side application establishes a connection with the server side.

![](https://static.javatpoint.com/dbms/images/dbms-2-tier-architecture.png)

## 1.3. 3-Tier Architecture

- Contains another layer between the client and server. In this architecture, client can't directly communicate with the server.
- The application on the client and interacts with an application server which further communicates with the database system.
- End user has no idea about the existence of the database beyond the application server. The database also has no idea about any other user beyond the application.
- The 3-Tier architecture is used in case of large web application.
