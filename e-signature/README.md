# Electronic signature vs Digital signature

Source:

- <https://juro.com/learn/digital-signature-vs-electronic-signature>
- <https://www.docusign.com/en-au/blog/news/whats-the-difference-between-electronic-signatures-and-digital-signatures>
- <https://comodosslstore.com/blog/difference-between-electronic-signatures-and-digital-signatures.html>
- <https://www.docusign.com/how-it-works/electronic-signature/digital-signature/digital-signature-faq>

## 1. Electronic signature

- An electronic signature is a **digital markup added to a contract** to show that the parties have agreed to the contract’s terms. Electronic signatures replace wet ink signatures, which are added to physical copies of a contract.
- Use cases:
  - Electronic signatures are commonly added to business contracts to show that a signatory chooses to agree with the terms laid out by the other party. By creating an electronic signature, a signatory will demonstrate its intention to create a legally binding relationship and fulfill the obligations set out for both businesses.
- Electronic signatures can be created by contract parties in Word or PDF. They are created and added to contracts by individuals and teams signing or making the document in some way.

## 2. Digital signature

- A digital signature is a method used to **seal a document** and provide evidence of the document’s integrity and authenticity.
- In other words, tt is a specific type of electronic signature that uses a specific technical implementation to meet the needs of highly regulated industries -> more **secure** and **tamper-evident**, which **encrypts** the documents and permanently embeds the information in it if a user tries to commit any changes in the document then the digital signature will be invalidated.
- Digital signatures are often used by certification authorities or trust service providers, rather than commercial teams seeking to close a deal. These bodies will validate the digital signatures and verify the digital document.
- Digital signatures are not created by people, they are created by software and algorithms. This relies on an advanced method called **Public Key Infrastructure (PKI)**, which is a set of processes, hardware, and software that combines to ensure data is transferred securely by generating two keys - a public and private one.
  - When a signer electronic signs a document, the signature is created using the signer's private key, which is always securely kept by the signer.
  - The mathematical algorithm acts like a cipher, creating data matching the signed document, called a hash, and encrypting the data. The resulting encrypted data is the digital signature.
  - The signature is also marked with the time that the document was signed. If the document changes after signing, the digital signature is invalidated.
  - To protect the integrity of the signature, PKI requires that the keys be creted, conducted, and saved in a secure manner, and often requires the services of a reliable **Certificate Authority (CA)**.

  ![](https://www.docusign.com/static-c-assets/ds_subpage_diagram2.svg)

## 3. Is a digital signature the same thing as an electronic signature?

- Although some people use the terms digital signature and electronic signature interchangeably, they are **different features and they perform different functions**.
- Both digital signatures and electronic signatures add authenticity and integrity to documents. However, they do this in different ways.
  - Digital signatures make it possible to identify specific documents
  - eSignatures demonstrate the intent of a signatory to be legally bound by the terms within a specific document.
- Although they are not the same, **digital signature technology can be used alongside electronic signatures to make them more secure**.
