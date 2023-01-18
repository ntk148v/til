# Web services

Source: <https://www.guru99.com/webservice-testing-beginner-guide.html>

Web services can be implemented in different ways, but the following two are the popular implementations approaches:

- SOAP
- REST

## SOAP (Simple Object Access Protocol)

SOAP is a standard protocol defined by the W3C Standard for sending and receiving web service requests and responses.

SOAP uses the XML format to send and receive the request and hence the data is platform independent data. SOAP messages are exchanged between the provider applications and receiving application within the SOAP envelops.

As SOAP uses the simple http transport protocol, its messages are not got blocked by the firewalls.

![](https://www.researchgate.net/publication/327054573/figure/fig1/AS:660230866231298@1534422713647/SOAP-protocol-SOAP-is-the-master-leader-in-communications-Its-main-purpose-is-to-send.png)

## REST (Representational State Transfer architecture)

REST is an architecture that generally runs over HTTP. The REST style emphasizes the interactions between clients and services, which are enhanced by having a limited number of operations. REST is an alternative to SOAP (Simple Object Access Protocol) and instead of using XML for request REST uses simple URL in some cases. Unlike SOAP, RESTFUL applications uses HTTP build in headers to carry meta-information.

Rest API supports both XML and JSON format.

## WSDL (Web Services Description Language)

WSDL is an XML based language which will used to describe the services offered by a web service.

WSDL describes all the operations offered by the particular web service in the XML format. It also defines how the services can be called, i.e what input value we have to provide and what will be the format of the response it is going to generate for each kind of service.
