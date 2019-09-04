# A Set Model for Kubernetes RBAC

## Overview

This model is based on the OASIS XACML-inspired model <sup>[[0]]</sup>.

The basic sets:

  * S : set of all subjects
  * R : set of all roles
  * A : set of all actions (verbs)
  * &Omega; : set of all role-subject bindings (or rolebindings for short)
  * E : set of all environmental constraints
  * __R__<sub>s</sub> : set of all resources managed by the control plane services

A user is a human-being interacting with a computer system. Each user interaction takes place 
after an authentication which establishes a subject. In most situations the act of authentication identifies a particular user,
and an audit trail can connect a user session s ∈ S to its human originator.

The kubernetes orchestration system is composed of a collection of services/resources, which may
be managed via the kubernetes API. A role is a named function that is bound with
some subject; a role is specific to a set of objects/resources. 

Definition: A role r ∈ R is a tuple (i, v, n) ∈ __R__<sub>s</sub> × A × N , where i ∈ __R__<sub>s</sub> is a resource type,
v ∈ A is a verb, n ∈ N is the name of the role.

The name of a role is unique within the scope of its defining service. Note that in practice you can create a single role
associating 1..x resources to 1..y verbs with "cardinality" x × y.  We will simplify here to assume each role associates 
exactly 1 resource to 1 verb, ie cardinality = 1. 
It is trivial to see that one could expand "macro" roles to individual "micro" roles, for a role named n, 
e.g. (n<sub>i</sub>, n<sub>i+1</sub>, ..., n<sub>i+x</sub>) X (n<sub>j</sub>, n<sub>j+1</sub>, ..., n<sub>j+y</sub>) = **&sum;** n<sub>ij</sub>

A verb (or action) is a right to perform some operation on a particular object. Kubernetes verbs include: 
"get", "list", "watch", "create", "update", "patch", "delete".

A RoleBinding pair (r, s) ∈ &Omega; binds a role r ∈ R to a subject s ∈ S. 
Subjects can be groups, users or service accounts in Kubernetes. 
Again ignoring cardinality > 1 and assume that all reasoning here implies enumerating the "micro" bindings 
from all the syntactical "macro" binding definitions.

We consider each environmental constraint e ∈ E as an atomic proposition about the system activated outside the control plane, 
eg. node host IP address range, or a lookup in an external database/LDAP. The environmental constraint may need to be re-evaluated over time due to changes in the external data, but for simplicity we initially assume a snapshot is avaialbe and remains consistent (TODO: add temporal logic).

## Policies

Let's consider __P__ : set of all policies.

Definition: A policy p ∈ __P__ is a pair of functions (&rho;, &chi;) 

&rho; ∈ &Rho; where &rho; : &Omega; &rarr; 2<sup>__R__<sub>s</sub></sup>, and 

&chi; ∈ &Chi; where &chi; : &Omega; &rarr; 2<sup>E</sup>

where as noted above &Omega; is the set of all Bindings

In other words a function &rho; maps the role bindings to &#8484;<sub>2</sub> over all resources, 
and a function &chi; maps the environmental constraints to &#8484;<sub>2</sub>.

## Resource Requests and Policy Evaluation

Definition: A resource request x is a tuple (s, a, r) where s ∈ S, a ∈ A, and r ∈ __R__<sub>s</sub>.

In order to evaluate whether a resource request should be allowed or denied, 
we query whether the policy or policies applicable to the request is satisfied based on the roles and role bindings. 

As defined above, a policy p ∈ P is evaluated as functions, and produces an ordered set (sequent):

(x<sub>1</sub>, x<sub>2</sub>, ... , x<sub>n</sub> &#8866; &#8484;<sub>2</sub>), 

where x<sub>j</sub> for 1 ≤ j ≤ n is a bit string mapped to the universe X = R ∪ &Omega; ∪ E producing a policy decision of at least {0} or {1}. 

We say that each x<sub>j</sub> for 1 ≤ j ≤ n is a ?query/fact/clause? in the policy p.

The sequent notation is conjunctive: In order to determine the result of policy p through
a resource request, each fact/query (x<sub>1</sub>, x<sub>2</sub>, ... , x<sub>n</sub>), must be satisfied.

Also sequents are sequences of logical formulas, not sets<sup>[[1]]</sup>. Therefore both the number and order of occurrences of formulas are significant.

### Example 
As an example, let's assume a subject "alice" in role "r1" is requesting access "get" to a resource assigned to role binding "ω1". 
A policy "p1" specifies that the resource request must have x<sub>1</sub> corresponding to:

* a role fact requiring request.subject is contained in ω1,
* a role fact requiring request.verb is contained in r1,
* a role fact requiring that request.resource is contained in r1 
* an additonal environmental constraint fact, that the request.resource IP address is in a range e1. 

where (1,1,1,1) &rarr; {1}
and all other bit strings, eg (0,1,1,1), (1,0,1,1), ..., (0,0,0,0) &rarr; {0}

Evaluating p1 = concat(&rho;<sub>p1</sub>(ω1), &chi;<sub>p1</sub>(ω1)) = (1,1,1,1) yields {1} and the request is allowed.

## Horn Clauses

### Roles

RoleName(args) ← p ∧ q ∧ ... ∧ t ∧ [P(args) ∧ [Q(args) [∧ ...]]]

The args are variables that are instantiated at runtime from information in the request and possibly lookup in external systems.

Example:

> role pod-reader --verb=get --resource=pods 

is expressed<sup>[[2]],[[3]]</sup> as:

PodReader(resource, verb) <= (resource=='pod') & (verb=='GET')


[0]: http://citeseerx.ist.psu.edu/viewdoc/download?doi=10.1.1.459.8327
[1]: https://en.wikipedia.org/wiki/Sequent
[2]: https://sites.google.com/site/pydatalog/Online-datalog-tutorial
[3]: https://sites.google.com/site/pydatalog/roadmap-and-change/documentation-of-version-81
