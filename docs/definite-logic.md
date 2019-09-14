# Definite Logic Preliminaries

## Definition

A definite logic program is a set of clauses of the form

A ← A<sub>1</sub>, . . . , A<sub>n</sub> (n ≥ 0)

where A and A<sub>1</sub>, . . . , A<sub>n</sub> are all atoms, i.e., no negation.

This is in contrast to "normal logic programs", i.e., where there can be occurrences
of [negation-as-failure](https://en.wikipedia.org/wiki/Negation_as_failure) in the body of a clause.

## Interpretations and Models

An interpretation for a set P of first-order formulas is:

* A domain D.
* A mapping from ground terms of P to the elements of D 
* The extension of every predicate of P, ie which ground atoms of P are true and which are false.

A model of P is an interpretation of P *in which every formula of P is true*.

Formula α is a logical consequence of P

P |= α

when α is true in every model of P.

ASIDE: NOTE: P = IDB ∪ EDB

## [Hebrand Interpretation](https://en.wikipedia.org/wiki/Herbrand_interpretation)<sup>[[0]]</sup>

### [Example](https://en.wikipedia.org/wiki/Herbrand_structure)

## Least Hebrand Interpretation


[0]: https://www.doc.ic.ac.uk/~mjs/teaching/KnowledgeRep491/Fixpoint_Definite_491-2x1.pdf
[1]: https://books.google.com/books?id=LcOLqodW28EC&pg=PA231#v=onepage&q&f=false
