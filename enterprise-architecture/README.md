# Enterprise Architecture (EA)

- [Enterprise Architecture (EA)](#enterprise-architecture-ea)
  - [1. Introduction](#1-introduction)
  - [2. Enterprise Architecture Framework (EA Framework)](#2-enterprise-architecture-framework-ea-framework)
    - [2.1. Overview](#21-overview)
    - [2.2. EA framework topics](#22-ea-framework-topics)
    - [2.3. Type](#23-type)
      - [2.3.1. The Open Group Architecture Framework](#231-the-open-group-architecture-framework)
      - [2.3.2. The Zachman Framework](#232-the-zachman-framework)
      - [2.3.3. Federal Enterprise Architectural Framework](#233-federal-enterprise-architectural-framework)
      - [2.3.4. Gartner](#234-gartner)

Sources:

- <https://en.wikipedia.org/wiki/Enterprise_architecture>
- <https://en.wikipedia.org/wiki/Enterprise_architecture_framework>
- <https://advisedskills.com/about/news/145-the-four-types-of-enterprise-architecture-framework-which-is-the-best-type-for-you-2>
- <https://www.redhat.com/architect/togaf>
- <https://pubs.opengroup.org/architecture/togaf9-doc/arch/>
- <https://www.visual-paradigm.com/guide/enterprise-architecture/what-is-zachman-framework/>
- <https://www.zachman.com/about-the-zachman-framework>
- <https://en.wikipedia.org/wiki/Zachman_Framework>
- <https://pdfs.semanticscholar.org/04a8/c5d8535fc58e5ad55dd3f9288bc78567d0c4.pdf>
- <https://www.terrafirma.com.au/our-thinking/top-10-enterprise-architecture-frameworks/>
- <https://www.youtube.com/watch?v=WiNeuRZaaZs>

## 1. Introduction

- Accoring to [Gartner](https://www.gartner.com/en/information-technology/glossary/enterprise-architecture-ea), Enterprise Architecture (EA) is a discipline for proactively and holistically leading enterprise responses to disruptive forces by identifying and analyzing the execution of change toward desired business vision and outcomes.
  - Defines, organises, standardizes, and documents the whole architecture and all important elements of the respective organisation, covering relevant domains such as business, digital, physical , or organisational.
  - The relations and interactions between elements that belong to those domains, such as porocesses, functions, applications events, data, or technologies.
- According to the standard [ISO/IEC/IEEE 42010](https://en.wikipedia.org/wiki/ISO/IEC_42010), the product used to describe the architecture of a system is called an *architectural description*.
- A methodology for developing and using architecture to guide the transformation of a business from a baseline state to a target state, sometimes through several transition states, is usually known as an *enterprise architecture framework*.

## 2. Enterprise Architecture Framework (EA Framework)

![](https://upload.wikimedia.org/wikipedia/commons/thumb/5/58/Enterprise_Architecture_frameworks_utilized_2011.jpg/240px-Enterprise_Architecture_frameworks_utilized_2011.jpg)

### 2.1. Overview

- Defines how to create and use an EA.
- Provides principles and practices for creating and using the architecture description of a system, as well as tools and approaches that help architects abstract from the level of detail at which builders work, to bring enterprise design tasks into focus and produce valuable architecture description documentation.
- The components of EA framework:
  - Description of architecture.
  - Methods for desigining architecture.
  - Organization of architects.

### 2.2. EA framework topics

![](https://upload.wikimedia.org/wikipedia/commons/thumb/3/3f/Layers_of_the_Enterprise_Architecture.jpg/320px-Layers_of_the_Enterprise_Architecture.jpg)

- Architecture domains ([Enterprise Architecture Planning](https://en.wikipedia.org/wiki/Enterprise_Architecture_Planning)):
  - Business architecture
  - Data architecture
  - Applications architecture
  - Technology architecture
- Layers of the EA: The view of architecture domains as layers.
  - Environment
  - Business Layer
  - Data Layer
  - Information System Layer
  - Technology Layer

### 2.3. Type

- EA frameworks typically fall into the following categories/ types:
  - Developed by consortiums and industry standards bodies (TOGAF, ArchiMate, BIAN, Zachman)
  - Those intended for defense use (DoDAF, MoDAF, DAF)
  - Those intended for wider government use (FEAF, AGA, NIST, FDIC)
  - Developed by private companies or universities (IBM, Gartner, Avolution)

![](https://www.avolutionsoftware.com/uploads/webp-express/webp-images/doc-root/wp-content/uploads/2019/07/Enterprise-Architecture-Framework-Comparison-1.jpg.webp)

#### 2.3.1. The Open Group Architecture Framework

- [TOGAF](https://www.opengroup.org/togaf) is the mosted used and proven EA methodology and framework (2020).
- Today, 80% of Global 50 companies use TOGAF.
- The first version of TOGAF was published by the Open Group in 1995. The current version of TOGAF as of this writing is version 9.2.
- TOGAF puts satisfying business needs as the central concern of all design activities.
- The four architectural domains of TOGAF.

<table style="width: 658px;" cellspacing="1" cellpadding="1" border="1">
    <thead>
        <tr>
            <th scope="col" style="width: 130px;">Architectural Domain</th>
            <th scope="col" style="width: 527px;">Description</th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td style="width: 130px;">Business</td>
            <td style="width: 527px;">Formulates key business processes, governance guidelines, organization structure,
                and business strategy into a well-defined, well-understood, unified whole. Describes how the current
                business processes work and how they should work to meet the intended business goals according to the
                [Architectural Vision](https://pubs.opengroup.org/architecture/togaf92-doc/arch/) document. The purpose
                of the [Architectural Vision](https://pubs.opengroup.org/architecture/togaf92-doc/arch/) document is to
                "develop a high-level aspirational vision of the capabilities and business value to be delivered as a
                result of the proposed Enterprise Architecture."</td>
        </tr>
        <tr>
            <td style="width: 130px;">Application</td>
            <td style="width: 527px;">Provides a blueprint of the application(s) that need to be developed to support
                the business goals defined within the [Architectural
                Vision](https://pubs.opengroup.org/architecture/togaf92-doc/arch/) document. The intended blueprint
                describes the logical service definitions of the application(s) to be created or refactored as well as a
                description of the interfaces that represent the given service.</td>
        </tr>
        <tr>
            <td style="width: 130px;">Data</td>
            <td style="width: 527px;">The architectural domain under which logical and physical data models are
                developed. Activities include developing new data modes and refactoring existing ones. Identifies data
                management tools and technologies.</td>
        </tr>
        <tr>
            <td style="width: 130px;">Technical</td>
            <td style="width: 527px;">Defines the hardware resources required to realize the intended architecture. This
                includes computing, network, and storage resources.</td>
        </tr>
    </tbody>
</table>

- TOGAF Architecture developement model (ADM):
  - The framework specifies how the architecture is to be created. This specification is called the ADM.
  - An 8-phase, sequential process.

  ![](https://www.opengroup.org/sites/default/files/adm_tog-r2.png)

  - Architecture Integration.

  ![](https://pubs.opengroup.org/architecture/togaf9-doc/arch/Figures/05_admintro2.png)

  - More details [here](https://pubs.opengroup.org/architecture/togaf9-doc/arch/).

- Limitations:
  - TOGAF is good for implementing *very big systems in very big companies*.
  - It's designed for companies that are *hierarchical and departmentalized*.
  - It *takes a lot of time* to learn the specification's details.

#### 2.3.2. The Zachman Framework

- Zachman Framework uses the method of taxonomy to organize a massive variety of documents and materials into categories that suit them.
- Structure:
  - A two dimensional classification scheme for descriptive representations of an Enterprise that is structured as a matrix containing 36 cells, each of them focusing on one dimension or perspective of the enterprise. Rows are often presented as different viewpoints involved in the systems development process, while columns represent different perspectives of the stakeholders involved in the organization.

  ![](https://cdn-images.visual-paradigm.com/guide/enterprise-architecture/what-is-zachman-framework/01-zachman-framework.png)

  - Columns represent the interrogatives or questions that are asked of the enterprise.
    - What (data)
    - How (function)
    - Where (network)
    - Who (people)
    - When (time)
    - Why (motivation)
  - Each row represents distinct view of the organisation, from the perspective of different stakeholders.
    - Planner's View (Scope Contexts)
    - Owner's View (Business Concepts)
    - Designer's View (System Logic)
    - Implementer's View (Technology Physics)
    - Sub-Constructor's View (Component Assembles)
    - User's View (Operation Classes)
- Rules.
  - Each cell in the Zachman Framework must be aligned with the cells immediately above and below it.
  - All the cells in each row also must be aligned with each other.
  - Each cell is unique.
  - Combining the cells in one row forms a complete description of the enterprise from that view.
- At the present moment, it would arguably be fair to say that the broad interest in the Zachman Framework has already faded away and within the next few years it is likely to be forgotten by the EA community due to its inexplicable practical utility

#### 2.3.3. Federal Enterprise Architectural Framework

- Federal Enterprise Architectural Framework (FEAF) is the U.S. reference enterprise architecture of a federal government. It provides a common approach for the integration of strategic, business and technology management as part of organization design and performance improvement.
- The FEA combines the best of both the Zachman Framework and TOGAF.
- The FEA has five reference models. They cover business, service, components, technical, and data. These five points combine with a segment model to create a perspective on how best to install enterprise architecture.
- FEA was the foundation for a massive restructuring of a high-end government. As such, the framework is a strong core to follow when building a strong foundation for a future company.

#### 2.3.4. Gartner
