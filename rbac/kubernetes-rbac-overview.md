# Kubernetes RBAC

## Overview

Kubernetes RBAC Permissions are purely additive (there are no “deny” rules). (This is different from AWS IAM.) 
They can be scoped as namespace only (Role) or cluster-wide (ClusterRole). Note, ClusterRoles have some additional 
"extra-namespace" capabilities like Node permissions. These will need to be modeled asymmetrically (or perhaps
use one consistent model with some non-cluster capabilities pruned for namespace specific roles?) 

NOTE: in 1.9 ClusterRoles can be ["aggregated" or modified](https://github.com/kubernetes/community/pull/1219) 
for extensibility. This will have to be modeled but maybe can be split out into a separate effort.

Rules in Role definitions are sets of resources (APIs) and operations (verbs). Resources can be filtered by API 
name (apiGroups).

Roles are "bound" to Actors aka subjects (users, groups, or service accounts) via Cluster/RoleBindings. Subjects
are defined by the authentication plugin, so are arbitrary strings, with the [special case of system: prefixes.](https://kubernetes.io/docs/reference/access-authn-authz/rbac/#referring-to-subjects)
[As of 1.5 k8s has a concept of authenticated and unauthenticated "anonymous" users](https://github.com/kubernetes/kubernetes/pull/32386).
How will this affect modeling?

There are also some [default "user facing" cluster roles](https://kubernetes.io/docs/reference/access-authn-authz/rbac/#user-facing-roles),
["core component"](https://kubernetes.io/docs/reference/access-authn-authz/rbac/#core-component-roles) roles, 
[controller roles](https://kubernetes.io/docs/reference/access-authn-authz/rbac/#controller-roles), and 
["other" roles](https://kubernetes.io/docs/reference/access-authn-authz/rbac/#other-component-roles) that 
may need to be accounted for.

Resources are things that the k8s APIs (or extensions) can act upon, e.g. Pods, Endpoints, Secrets, logs, etc.  
Resources are referenced both by path-like snippets reflective of their API access to represent any instance of
that particular class of resource, or by name to represent a specific instance of that resource type (resourceNames).

Roles and Bindings are applied at startup and periodically refreshed based on the configuration of [auto-reconciliation](https://kubernetes.io/docs/reference/access-authn-authz/rbac/#auto-reconciliation).
How will this affect modeling?

There is a "bootstrap" process by the API controller even before the RBAC components are up (or if RBAC is not enabled) whereby
the default super user cluster-admin role must be used to add roles and role bindings to allow for other users to do stuff.

NOTE: WARNING: MUCH WOW: "If your API server runs with the insecure port enabled (--insecure-port), you can also make API calls via that 
port, which does not enforce authentication or authorization." Don't do that! :P

## RBAC Authorizer

The implementation gathers an array of rules and ["visits"](https://en.wikipedia.org/wiki/Visitor_pattern) each rule and
does the following:

* checks for valid rule (eg is it nil)
* checks if the request attributes refers to a resource (by type or specific name)
* checks the verb
* checks the API group
* checks if the rule applies to the user/subject (eg exact user match, membership in a group, or service account exact match)

If everything matches, then it is allowed. Since there is no "deny" semantics, the lack of an explicit rule means something 
is denied. AWS IAM for example [uses explicit deny policies](https://docs.aws.amazon.com/IAM/latest/UserGuide/reference_policies_evaluation-logic.html)
presumably because they combine Identity based policies with Resource based policies and hierarchical (SCP, aka OU) policies that can increase the complexity.  [Early kubernetes design discussions](https://github.com/kubernetes/kubernetes/issues/51862#issuecomment-326841219)
asserted that Deny rules cause "surprising" results and add unnecessary complexity.  
NOTE: [there is a webhook that can get around this to provide explicit deny](https://github.com/kubernetes/kubernetes/issues/51862).

### [Webhooks](https://kubernetes.io/docs/reference/access-authn-authz/webhook/)

> When faced with an authorization decision, the API Server POSTs a JSON- serialized authorization.k8s.io/v1beta1 SubjectAccessReview object describing the action. This object contains fields describing the user attempting to make the request, and either details about the resource being accessed or requests attributes.

This allows external implementations of the RBAC Authorizer.  We will probably not include this in the V1 tooling, but noted here for the roadmap for V2+.

### Historical Notes

* There was a [request for RBAC policy verification back in 2017](https://github.com/kubernetes/kubernetes/issues/47574) and [Jordan Liggitt said it would be useful](https://github.com/kubernetes/kubernetes/issues/47574#issuecomment-308897805). We should comment on that issue when we have something.

