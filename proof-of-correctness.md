

http://plan.tools


A founding set of community organizers ("admins") wish to form **C**, a distributred storage and communication network. On each community node, the members of **C** agree to employ **L<sub>C</sub>**, an append-only [CRDT](https://en.wikipedia.org/wiki/Conflict-free_replicated_data_type) whose data transactions are to be considered "in the clear" to potential adversaries.   **C** is characterized by a set of community members at a given point in time, with one or more members administering member permissions on data structures encoded on **L<sub>C</sub>**.

The members of **C** wish to assert that:
   1. Only members of **C** have append access to **L<sub>C</sub>**
   1. All communication within and between members of **C** is:
      1. informationally maximally opaque, and
      2. secure from all other actors *not* in **C**.
   2. Adding new members to **C** incurs no additional security liabilty on the infrastructure.
   3. Within **C**, each node's "community repo state" (**CRS**) converges to a stable/monotonic state as network connectivity "catches up", for any set of network traffic delivery conditions (natural or adversarial).
   4. Members can be de-listed from **C** such they no longer have access to the **CRS** after **kσ** amount of time.


The members of **C** devise the following infrastructure:
   - Let `UUID` represent a fixed-length pseudo-randomly independently generated ID that ensures no reasonable chance of collision (typically 20 to 32 bytes).
   - All data entries on **L<sub>C</sub>** are encrypted using keys located on the "community keyring", **[K]<sub>C</sub>**.
   - Encrypted, entries on **L<sub>C</sub>** are a serialization of:
```
   type EntryCrypt struct {
       CommunityKeyID      UUID     // Community key used to encrypt .HeaderCrypt
       HeaderCrypt         []byte   // := Encrypt(<EntryHdr>.Marshal(), <EntryCrypt>.CommunityKeyID)
       ContentCrypt        []byte   // := Encrypt(<Body>.Marshal(), <EntryHdr>.ContentKeyID)
       Sig                 []byte   // := CalcSig(<EntryCrypt>.Marshal(), GetKey(<EntryHdr>.AuthorMemberID,
                                    //                                           <EntryHdr>.AuthorMemberEpoch))
   }
```
   - Decrypted, each entry is specified to be appended to a _virtual_ channel:
```
   type EntryHeader struct {
       EntryOp             EntryOp  // Specifies how to interepret this entry. Typically, POST_CONTENT
       TimeSealed          int64    // Unix timestamp of when this header was encrypted and signed.
       ChannelID           UUID     // "Channel" that this entry is posted to.
       ChannelEpoch        UUID     // Epoch of the channel in effect when this entry was sealed
       AuthorMemberID      UUID     // Creator of this entry (and signer of EntryCrypt.Sig)
       AuthorMemberEpoch   UUID     // Epoch of the author's identity when this entry was sealed
       ContentKeyID        UUID     // Specifies key used to encrypt EntryCrypt.ContentCrypt
   }
```
   - Each member of **C** maintains possession of the community keyring **[K]<sub>C</sub>**, such that:
        - **[K]<sub>C</sub>** is set of keys that encrypts and decrypts **C**'s message traffic to/from **L**
        - A newly generated community key is distributed to **C**'s members via a persistent data channel using asymmetric encryption (a community admin )
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




Let **σ** be the average time period it takes for replicated network messages to reach 2/3 of the network's nodes.  This lets us set a reasonable upper-bound on how long permissions changes in **C** take to propigate.  If we were to wait 100 or 1000 times **σ**, it would be safe to assume that any nodes able to receive a replicated message would have recieved it (if it was possible).  We thus express a time delay ceiling of permissions propigation as **kσ**.  Above this time, we assume there it is not beneficial to wait and hope that a newly arrived message will resolve a confict.  We therefore must establish a determinisitc set of rules to resolve all possible **CRS** conflicts.  For a network of 10,000 nodes in the internet of 2018, a reasonable value for **kσ** could be 3-12 hours. 


