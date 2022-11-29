# Deep packet inspection (DPI)

Source:

- <https://www.okta.com/identity-101/deep-packet-inspection/>
- <https://en.wikipedia.org/wiki/Deep_packet_inspection>

## 1. Introduction

- DPI is a type of data processing that inspects in detail the data being sent over a computer network, and may take actions such as alerting, blocking, re-routing, or logging it accordingly.

![](https://www.okta.com/sites/default/files/media/image/2022-08/DEEPPACKETINSPECTION_GRAPHIC_1.png)

## 2. How does DPI work?

- DPI grows [more and more common](https://www.techrepublic.com/article/deep-packet-inspection-the-smart-persons-guide/).
- Common approaches:
  - Pattern matching: Every attack comes with a repeatable signature.
  - Deny by default: Programmers describe this approach as restricting traffic to only what is necessary. The system denies everything else, even if it's possibly valid.
  - System default: Firewall provider may have present DPI network rules. Leave them as they are, and you'll allow the company to protect you.

## 3. How DPI can help & harm you?

- Advantages: DPI gets the credit for stopping things like:
  - Malware.
  - Spam.
  - Theft.
  - Noncompliance.
  - Training.

![](https://www.okta.com/sites/default/files/media/image/2022-08/DEEPPACKETINSPECTION_GRAPHIC_2.png)

- Disadvantages:
  - Irritation: Lock down the rules too tightly, and your staff may not able to communicate freely. Your customers may not be able to reach you either.
  - Complication: Must program your DPI tools, in most cases.
  - Speed: Your system needs time to look through each packet, and while your end users may not notice the lag in standard communication (like email), they may see the shift in other media (like video).
