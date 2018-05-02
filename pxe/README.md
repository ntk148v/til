# PXE - Preboot Exectution Environment

## What is PXE?

- A short and simple explanation of PXE is that it allows you to boot a computer over a network without requiring a harddrive or cdrom. You can do this with as few as 2 computers (1 server, 1 client) or you can do it with as many as can get your hands on.
- PXE uses the protocols IP, TFTP and DHCP with PXE-specific extensions.

## PXE architecture:
- PXE runs on the BIOS of the NIC.
- PXE provides APIs to a boostrap program for accessing the protocols involved in PXE operation.

![PXE APIs](./imgs/PXE_APIs.png)

    - Preboot Services API: Contains several control and information functions.
    - Trivial File Transport Protocol (TFTP) API: Enables opening and closing of TFTP connections, and reading packets from and writing packets to a TFTP connection.
    - User Datagram Protocol (UDP) API: Enables opening and closing UDP connections, and reading packets from and writing packets to a UDP connection.
    - Universal Network Driver Interface (UNDI) API: Enables basic control of and I/O through the client's network interface device.

## PXE Protocol

- How it works? PXE message flow:

![PXE message flow](./imgs/PXE_message_flow.jpg)

![PXE Boot](./imgs/PXE_Boot.png)

- Step 1: The client broadcasts a DHCPDISCOVER message to the standard DHCP port (^&).
- Step 2: The DHCP or Proxy DHCP Service responds by sending a DHCPOFFER message to the client on the standard DHCP reply port (68).
- Step 3: From the DHCPOFFER(s) that it receives, the client records the following:
    - The Client IP address.
    - The Boot Server list from the Boot Server field in the PXE tags from the DHCPOFFER.
- Step 4: If the client selects an IP address offered by a DHCP Service, then it must complete the standard DHCP protocol by sending a request for the address back to the Service and then waiting for an acknowledgement from the Service.
- Step 5: The client send a DHCPREQUEST with the same information as step 1 to the selected boot server, either on broadcast UDP (67) or multicast/unicast (4011).
- Step 6: The Boot Server unicasts a DHCPACk packet back to the client on the client source port. This reply packet contains:
    - Boot file name
    - Multicast TFTP configuration parameters.
    - Any other options the NBP requires before it can be successfully executed.
- Step 7: The client downloads the executable file using either standard TFTP (69) or MTFTP.
- Step 8: The PXE client determines whether an authenticity test on the downloaded file is required. If the test is required, the client sends another DHCPREQUEST message to the boot server requesting a credentials file for the prev downloaded boot file, downloads the credentials via TFTP or MTFTP and performs the authenticity test.
- Step 9: If the authenticity test succeeded or was not required, then the PXE client initiates exection of the downloaded code.
