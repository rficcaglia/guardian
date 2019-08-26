# WIP: Outline

Algorithmic Verification of RBAC Policy
* A user provides a policy (in Rego for now) and a desired specification (in ?)
– e.g., policy denies all "get" access to resources labeled "sensitive"
* The tool automatically checks validity of the specification
  * and generates a verification certificate if the program is correct
  * and generates a counterexample if the program is not correct
