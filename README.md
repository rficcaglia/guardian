# guardian
Formal Verification of Cloud Native Components

> “The heaviest penalty for declining to rule is to be ruled by someone inferior to yourself.” 

― Plato, The Republic

# Introduction
Guardian is an omnibus repository for tooling to formally verify components of a cloud native system. As each component is fleshed out, it might become its own standalone project, or Guardian could become just a Swiss Army Knife of useful verification tools. TBD. Suggestions are welcome!

# Guiding Principles
For any Guardian project the main idea is that Guardian provides a framework for formal expression and verification of the relationship between the intent of a program and program logic such that:

P |= φ <sup>[[0]]</sup>

or “P satisfies φ”, where P is a program, ie a computational process, and φ is a logic (a set of properties). 

The "formal" activities in scope for Guardian projects in terms of this relation:
• Guardian tooling MUST enable program verification - the task of proving that P |= φ.
• Guardian tooling SHOULD assist with specification - the task of defining (a list of) properties φ to be satisfied by the program.
• Guardian tooling MAY assist with program synthesis, ie the task of finding P given (a list of) φ.

The general framework provided by Guardian consists of finding:

* A metalanguage comprising
  * types, or data domains, or universes of discourse for various computational situations.
  * and the syntax for specifying parameterized specifications .
* An intepreter for the metalanguage, providing the theorems to be proven from the specification. This gives a "program logic".

## Further Considerations

* incorporating concurrency and λ-calculus <sup>[[1]]</sup>

# Current Sub-Projects Under Active Investigation

* [Kubernetes RBAC Policy Verification](https://github.com/cncf/sig-security/pull/242)
* Kubernetes NetworkPolicy Verification
* Kubernetes Admission Control Verfication <sup> [example](https://docs.google.com/document/d/1ihFfEfgViKlUMbY2NKxaJzBkgHh-Phk5hqKTzK-NEEs/edit#bookmark=id.mdmvg9pwqh31) </sup>

## Ideas for Future Sub-Project Work

* Certificate (Lifecycle) Management Verification
* Supply Chain Management Verification
* Verification of "Defense in Depth", e.g. CVE Impact Model

[0]: https://arxiv.org/pdf/1112.0347.pdf
[1]: http://www.nyu.edu/projects/barker/Lambda/barendregt.94.pdf
