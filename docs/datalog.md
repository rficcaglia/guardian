# Datalog

> Datalog bridges the gap between specification and implementation, i.e., a programmer specifies a problem 
  declaratively rather than describing it step-by-step, imperatively. A Datalog engine executes
  the specification for a set of input relations (also known as the extensional database) and produces an output 
  relation for a query ... Datalog engines used in program analysis are bddbddb, µZ, and LogicBlox. <sup>[[0]]</sup>

NOTE: Datalog has recursion but does not support negation.  Datalog is syntactically a subset of first-order logic;
the semantics of Datalog is based on the choice of [a specific model](/docs/definite-logic.md).

TBD: Is recursion needed for k8s rbac?

## Datalog Program Interpreter (ie Evaluation of a Goal)
* construct a set of ground atoms, called the Extensional Database (EDB) from all "body" predicates
* construct a set of rules called the Intensional database (IDB) from all "head" predicates
* derive relations from rules + EDB
  * Each IDB-predicate of the Datalog program corresponds to a variable relation
  * Each EDB-predicate of the Datalog program corresponds to a constant relation
  * Determining a solution of the system corresponds to determining the value of the variable relations 
    which satisy the system of equations
* materialize/compute relations to answer queries/goals:
  * accept single literal "goals" (constraints)
  * produce mapping from EDB facts to IDB facts (for a given goal)

### Top Down or Bottom Up?
* construct proof trees from top to bottom (ie top down, best for goals)
  * TBD: SLD resolution/backward chaining?
  * The initial goal is matched with the left-hand side of some rule.
  * generate other problems corresponding to the right-hand side predicates of that rule; 
  * this process is continued until no new problems are generated
* or, compute relations/mappings for all values from EDB (ie bottom up)
  * apply the rules in a given program to the EDB, and produce al1 the possible 
    consequences of the program, until no new fact can be deduced.
  

[0]: https://souffle-lang.github.io/pdf/cc.pdf

