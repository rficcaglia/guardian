from z3 import *

fp = Fixedpoint()

roleSort = BitVecSort(3)
resourceSort = BitVecSort(3)
userSort = BitVecSort(3)

access = Function('access', roleSort, resourceSort, BoolSort()) # create an edge from resource to role
bind = Function('bind', roleSort, userSort, BoolSort()) # create an edge from role to binding
grant = Function('grant', userSort, resourceSort, BoolSort()) # created edge from binding to user

fp.register_relation(bind, access)
fp.register_relation(grant, bind)

aRole = Const('aRole',roleSort)
aRes = Const('aRes',resourceSort)
aUser = Const('aUser', userSort)

fp.declare_var(aRes,aRole,aUser)

fp.rule(bind(aRole,aRes), access(aRole,aRes))
fp.rule(bind(aRole,aUser), [access(aRole, aRes),access(aUser, aRole)]) # bind a role to a resource
fp.rule(grant(aUser,aRes), [bind(aRole,aUser), bind(aRole,aRes)]) # add a user to a binding

acmeAdmins = BitVecVal(1,roleSort)
aPod = BitVecVal(2,resourceSort)
alice = BitVecVal(3,userSort)
bob = BitVecVal(3,userSort)
bPod = BitVecVal(4,resourceSort)

# edge facts, ie access facts
# fact() - shorthand for fp.rule(c,True)
fp.fact(access(acmeAdmins,aPod))
fp.fact(access(alice,acmeAdmins))
fp.fact(access(bob,bPod))
print "current set of rules", fp

fp.set(engine='datalog') #, generate_proof_trace=True)
fp.set('datalog.generate_explanations', True)

print fp.query(bind(acmeAdmins,alice)), "Alice is an acmeAdmin" 
print fp.query(grant(alice,aPod)), "Alice has access to aPod"
print fp.query(access(bob,aPod)), "Bob has access to aPod"
