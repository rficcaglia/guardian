# WIP: Outline

## Algorithmic Verification of RBAC Policy Specification
* A user provides a specification (in datalog for now, maybe next in Rego) 
  > Datalog bridges the gap between specification and implementation, i.e., a programmer specifies a problem 
  declaratively rather than describing it step-by-step, imperatively. A Datalog engine executes
  the specification for a set of input relations (also known as the extensional database) and produces an output 
  relation for a query ... Datalog engines used in program analysis are bddbddb, µZ, and LogicBlox. <sup>[[0]]</sup>

  * HOWEVER: Datalog has recursion but does not support negation.  Datalog is syntactically a subset of first-order logic;
    the semantics of Datalog is based on the choice of [a specific model](/docs/definite-logic.md).
  * e.g., does a policy prevent "get" access to resources labeled "sensitive"
  * specification has Horn clauses for all required facts about the [RBAC model](/rbac/k8s-rbac-set-model.md)
* The tool automatically checks validity of the specification
  * and generates a SAT/SMT verification result
  * and generates a counterexample if the specification is not correct
* If verified, the tool generates the necessary configuration for k8s
  * could be raw json, yaml
  * could be a Rego policy
  * could be something else loaded by a authorizer webhook implementation

## Algorithmic Verification of a RBAC Policy against a Verified Specification
* A user provides a verified specification and a kubernetes config (json, yaml, and/or Rego)
* the tool verifies that the config matches the verified spec
  * if not, produce a counter example
  * if so produce a verification result
  
 # Design Draft
 
 * Forward engineering use case
   * use z3 python or other existing interpreter to read datalog horn clauses and verify specification using solver
     * parse the datalog into an AST and from that produce abstract machine (aka Relational Algebra Machine)
   
       * TBD: recursion?
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
       * TBD: top down vs bottom up?
         * construct proof trees from top to bottom (ie top down, best for goals)
           * TBD: SLD resolution/backward chaining?
         * or, compute relations/mappings for all values from EDB (ie bottom up)
   * using code templates, meta-program/code gen actual json and/or yaml and/or Rego so you have a usable policy that implements the spec
 * Reverse engineering use case
   * present the tool with an existing set of json, yaml, and/or Rego config files;
     produce a datalog specification "result" (e.g. the RAM?), ie. parse configs into an AST and produce a RAM
     * a concise set of relational algebra expressions,
     * relation management statements, and control flow constructs
   
[0]: https://souffle-lang.github.io/pdf/cc.pdf
