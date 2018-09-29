###Features

http://plan.tools


Let **UUID** represent a fixed-length pseudo-randomly generated ID that ensures no human-reasonable chance of collision (typically 20 to 32 bytes).

Let **σ** be the average time period it takes for replicated network messages to reach 2/3 of the network's nodes.  This lets us set a reasonable upper-bound on how long permissions changes in **C** take to propigate.  If we were to wait 100 or 1000 times **σ**, it would be safe to assume that any nodes able to receive a replicated message would have recieved it (if it was possible).  We thus express a time delay ceiling of permissions propigation as **kσ**.  Above this time, we assume there it is not beneficial to wait and hope that a newly arrived message will resolve a confict.  We therefore must establish a determinisitc set of rules to resolve all possible **CRS** conflicts.  For a network of 10,000 nodes in the internet of 2018, a reasonable value for **kσ** could be 3-12 hours.  After this point, nodes not yet reached can effecvtively regarded as being offline.


in an information network where it would be "unusual" for a replicated network message to have not been replicated across the network.  In other words, i

A founding set of community organizers ("admins") wish to form **C**, a digital community.  **C** is characterized by a set of community members, one or more positioned to administer member permissions. On each community node, the members of **C** agree to employ **L**, an append-only [CRDT](https://en.wikipedia.org/wiki/Conflict-free_replicated_data_type) whose data transactions are to be considered "in the clear" to potential adversaries.  Network nodes in **C**  

The members of **C** wish to assert that:
   1. All communication within and between members of **C** is:
        a) informationally maximally opaque, and
        b) secure from all other actors *not* in **C**.
   2. Adding new members to **C** incurs no significant additional security liabilty on the infrastructure.
   3. Within **C**, each node's "community repo state" (**CRS**) converges to a stable/monotonic state as network connectivity "catches up", for any set of network traffic delivery conditions (natural or adversarial).
   4. Members can be exiled from **C** such they no longer have access to the **CRS** after **kσ** amount of time.

The members of **C** devise the following infrastructure:
   - Each member is in possession of a copy of **KR<sup>superscript</sup>** the "community keyring"
   - the community's data repo is an append-only CRDT whose data is to be considered "in the clear"
   - **C**'s "member registry channel" is defined as a log containing each member's UUID and current crypto "epoch"
   - **C**'s root "access control channel" (ACC) is a log containing access grants to member ID

An actor is said to have access to "in" **C** if and only if she possesses the communit  
Their intention is to assert that:
   1. All communication between members in **C** is informationally opaque and secure from all actors *not* in **C**.
   2. Additional new members can be invited into **C** at any time
   3. The community's data store replicates across members of **C** such that 
        a.  bl
        b.  ggf 



```
// EpochInfo implies a linked list of epochs extending from the past to the present
type EpochInfo struct {
	EpochStart            timestamp
	EpochID               UUID
	PrevEpochID           UUID
	EpochTransitionSecs   int
}
// MemberEpoch represents a public "rev" of a community member's crypto
type MemberEpoch struct {
	EpochInfo             EpochInfo
	PubSigningKey         []byte
	PubCryptoKey          []byte
}
// ChannelEpoch represents a "rev" of Channel's most sensitive properties
type ChannelEpoch struct {
	EpochInfo             EpochInfo
	ChannelProtocol       string        // If access control channel: "/chType/ACC", else: "/chType/client/*"
	ChannelID             UUID          // Immutable; set at channel genesis
	AccessChannelID       UUID          // This channel's ACC (and conforms to an ACC) 
}
type CommunityMember struct {
    CommunityID           UUID          // Assigned 
	MemberID              UUID                     // Issued when member joins C
	type KeyRepo struct {
		CommunityKeyring  []KeyEntry
		PersonalKeyring   []KeyEntry
	}
}
```
Let **St** be an append-only p2p replicating data store, where new data blobs can be appended and subsequently retrieved (via a transaction ID).  A node's particualar state of **St**

Let 

Let **Ac** be one or more members of **C** that are designated admins and are charged with moderating and orgranizing community dats 


type CommunityMember := `


**Table of Contents**

[TOCM]

[TOC]

#H1 header
##H2 header
###H3 header
####H4 header
#####H5 header
######H6 header
#Heading 1 link [Heading link](https://github.com/pandao/editor.md "Heading link")
##Heading 2 link [Heading link](https://github.com/pandao/editor.md "Heading link")
###Heading 3 link [Heading link](https://github.com/pandao/editor.md "Heading link")
####Heading 4 link [Heading link](https://github.com/pandao/editor.md "Heading link") Heading link [Heading link](https://github.com/pandao/editor.md "Heading link")
#####Heading 5 link [Heading link](https://github.com/pandao/editor.md "Heading link")
######Heading 6 link [Heading link](https://github.com/pandao/editor.md "Heading link")

##Headers (Underline)

H1 Header (Underline)
=============

H2 Header (Underline)
-------------

###Characters
                
----

