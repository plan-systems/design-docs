# Proof of Correctness for PLAN

```
         P urposeful
         L ogistics
         A rchitecture
P  L  A  N etwork
```

### What is this?

In computer science, a "proof of [correctness](https://en.wikipedia.org/wiki/Correctness_(computer_science))" refers to a formal walk-though and demonstration that a proposed method and/or design rigorously satisfies a given set of specifications or claims.  The intention is to remove _all doubt_ that there exists a set of conditions such that the proposed method would _not_ meet all the specifications.

Below, we first express the scenario, a set of specifications, and a digital infrastructure schema.  We then proceed to demonstrate correctness for each specification, citing how the schema and its prescribed operation satisfies that specification.  

Please note that the data structures listed below are intended to convey understanding and model correctness more than they are intended to be performant.  [go-plan](https://github.com/plan-tools/go-plan) embodies is this latter implementation.

---

### Scenario

A founding set of community organizers ("admins") wish to form **C**, a secure distributed storage network comprised of computers with varying capabilities, each running a common peer-to-peer software daemon ("node"). **C** is characterized by a set of individual members for any given point in time, with one or more members charged with administering member status, member permissions, and community-global rules/policies.  

On their nodes, the members of **C** agree to employ **𝓛**, an _append-only_ [CRDT](https://en.wikipedia.org/wiki/Conflict-free_replicated_data_type).  Data entries appended to **𝓛** ("transactions") are characterized by an arbitrary payload buffer, a signing public key, and a signature of a cryptographic digest of the transaction.  Transactions on **𝓛** are considered to be "in the clear" to adversaries (i.e. neither "wire" privacy _nor_ storage privacy is assumed).

For a given **C**, **𝓛<sub>C</sub>** is assumed to either contain (or have access to) a verification system such that a transaction submitted to **𝓛<sub>C</sub>** is acceptable _only if_ the transaction's author (signer) has permission.  This may appear to be a strong requirement, but instead only reflects the _transference_ of all security liability to the key(s) specified during the genesis of **𝓛<sub>C</sub>** to an _external_ set authorities.

For example, a customized "private distro" of the [Ethereum](https://en.wikipedia.org/wiki/Ethereum) blockchain ("**Eth<sub>C</sub>**") could be used to implement **𝓛<sub>C</sub>** since:
   - The admins, upon creating **Eth<sub>C</sub>**, would issue themselves some large bulk amount _"C-Ether"_.
   - The admins of **C** would periodically distribute portions of _C-Ether_ to members of **C** (quotas).  
   - Large client payload buffers would be split into 32k segments (Ethereum's transaction size limit) and _then_ committed to **Eth<sub>C</sub>**.
   - On **C**'s nodes, **Eth<sub>C</sub>** transactions that do not "burn" an amount of _C-Ether_ commensurate with the byte size of the payload would be rejected/ignored.

---


### Specifications & Requirements

The members of **C** wish to assert that:
1. _Only_ members of **C** have append access to **𝓛<sub>C</sub>**.
2. For all actors _not_ in **C**, all transactions sent to, read from, and residing on **𝓛<sub>C</sub>** are informationally opaque to the maximum extent possible.
3. New members can be added to **C** at any time (given that **C** policies and permissions are met).
4. There is a hierarchy of member admin policies and permissions that asserts itself in order to arrive at successive states (and cannot be circumvented).
5. Assume a minority number of members are (or become) covert adversaries of **C**. Even if working in concert, it must be impossible for them to: impersonate other members, insert unauthorized permission or privilege changes, gain access to others' private keys or information, or alter **𝓛<sub>C</sub>** in any way that poisons or destroys community content.
5. In the event an admin becomes an adversary of **C**, an adversary gains access to an admin's private keys, or **𝓛<sub>C</sub>** is otherwise corrupted or vandalized, **C** can elect to "hard fork" **𝓛<sub>C</sub>** to an earlier time state.
6. Member admins can "delist" members from **C** such that they become equivalent to an actor that has never been a member of **C** (aside that delisted members can retain their copies of **R** before the community entered this new security "epoch").
7. For each node **i** in **C**, it's local replica state ("**R<sub>i</sub>**"), converges to a stable/monotonic state as **𝓛<sub>C</sub>** message traffic "catches up", for any set of network traffic delivery conditions (natural or adversarial). That is, **R<sub>1</sub>**...**R<sub>n</sub>** update such that strong eventual consistency (SEC) is guaranteed.  
8. If/When it is discovered that a member's personal or community keys are known to be either comprised or lost, an admin (or members previously designated by the afflicted member) initiate a new security epoch such that:
   - an adversary in possession of said keys will have no further access to **C**
   - the afflicted member's resulting security state is unaffected
9. **C**, led by a coordinated admin effort, can swap out CRDT technologies (e.g. **C** may use a CRDT that automatically halts under suspicious network conditions or insufficient peer connectivity, but earlier in its history when it had to be more agile, **C** used a CRDT that favored "liveness" over safety).


---


### Proposal

The members of **C** propose the following infrastructure:
1. Let `UUID` represent a constant-length independently unique ID that ensures no reasonable chance of collision (typically 20 to 32 pseudo-randomly generated bytes).
2. Each member of **C** securely maintains two "keyrings":
  1. **[]K<sub>personal</sub>**, the member's _personal keyring_, used to:
       - decrypt/encrypt information "sent" to/from that member
       - create signatures that authenticate information claimed to be authored by that member
  2. **[]K<sub>C</sub>**, the _community keyring_, used to encrypt/decrypt "community public" data (i.e. the cryptographic bridge between **𝓛<sub>C</sub>** and **R<sub>L</sub>**)
3. Each transaction residing on **𝓛<sub>C</sub>** is a serialization of:
```
type EntryCrypt struct {
   CommunityKeyID    UUID     // Identifies the community key used to encrypt .HeaderCrypt
   HeaderCrypt       []byte   // := Encrypt(<EntryHeader>.Marshal(), <EntryCrypt>.CommunityKeyID)
   ContentCrypt      []byte   // := Encrypt(<Body>.Marshal(), <EntryHeader>.ContentKeyID)
   Sig               []byte   // := MakeSig(<EntryCrypt>.Marshal(), KeyFor(<EntryHeader>.AuthorMemberID,
                              //                                           <EntryHeader>.AuthorMemberEpoch))
}
```
4. Each `EntryCrypt.HeaderCrypt` is encrypted using **[]K<sub>C</sub>** and specifies a persistent `ChannelID` that it operates on **C**'s _virtual_ channel space:
```
type EntryHeader struct {
   EntryOp           int32    // Op code specifying how to interpret this entry. Typically, POST_CONTENT
   TimeSealed        int64    // Unix timestamp of when this header was encrypted and signed ("sealed")
   ChannelID         UUID     // Channel that this entry is posted to (or operates on)
   ChannelEpochID    UUID     // Epoch of the channel in effect when this entry was sealed
   AuthorMemberID    UUID     // Creator of this entry (and signer of EntryCrypt.Sig)
   AuthorMemberEpoch UUID     // Epoch of the author's identity when this entry was sealed
   ContentKeyID      UUID     // Identifies *any* key used to encrypt EntryCrypt.ContentCrypt
}
```
5. For every `EntryCrypt` **e** authored by members of **C** and posted to **𝓛<sub>C</sub>**, **e**`.Sig` is generated from on a hash digest of all other fields using the private signing key associated with the author's member ID and their current member epoch.  The key used to encrypt **e<sub>header</sub>**
5. On a community node **i**, let **e** be an `EntryCrypt` newly arriving from **𝓛<sub>C</sub>**.  
  1. Let **e<sub>header</sub>** be the `EntryHeader` resulting from decrypting e.`HeaderCrypt` using the key in **[]K<sub>C</sub>** indexed by `e.CommunityKeyID`.
  2. `e.Sig` is validated by retrieving the public signing key listed for (**e<sub>header</sub>**`.AuthorMemberID`, `.AuthorMemberEpoch`) within **R<sub>i</sub>**.
If either of the keys listed above are not found, it is possible that **R<sub>i</sub>** has not been updated with entries that have yet to arrive.  Thus, **e** is placed into the node's "holding tank" for delayed processing since  If the keys are found by steps (1) or (2) fail to check, the entry is considered "hard" rejected and not considered further.
6. Assuming , verified, and deterministically merged into the node's local community "repo", **R<sub>i</sub>**:

```
// A node's community replica/repo/Ri
type CommunityRepo struct {
   Channels          map[ChannelID]ChannelStore
}

// Stores and provides rapid access to entries in a channel
type ChannelStore struct {
   ChannelID         ChannelID
   Epochs            []ChannelEpoch  // The latest element is this channel's current epoch
   EntryTable        []Entry         // Contains EntryHeader info and points to ContentCrypt blob
}

// Represents a "rev" of this channel's security properties
type ChannelEpoch struct {
   EpochInfo         EpochInfo
   ChannelProtocol   string          // If access control channel: "/chType/ACC"; else: "/chType/client/*"
   ChannelID         UUID            // Immutable; generated during channel genesis
   AccessChannelID   UUID            // This channel's owning ACC (and conforms to an ACC)
}

// Specifies general epoch parameters and info
type EpochInfo struct {
   EpochStart        timestamp
   EpochID           UUID
   EpochIDPrev       UUID            // Forms a linked list extending from the past
   TransitionSecs    int             // Custom-epoch transition rules, etc
}
```

6. Entries that do not conform to channel properties or permissions are placed in a "holding tank" within **R<sub>i</sub>**. The node periodically reattempts to merge these entries with the understanding that later-arriving entries may alter **R<sub>i</sub>** such that previously rejected entries now conform. Entries that are rejected on the basis of an validation failure (e.g. signature validation failure) are dropped. These rejections are cause for concern and could logged to discern bad actor patterns.
7. Members of **C** maintain their copy of the community keyring, **[]K<sub>C</sub>**, where:
    1. **[]K<sub>C</sub>** encrypts/decrypts `EntryCrypt` traffic to/from **𝓛<sub>C</sub>**
    2. A newly generated community key is distributed to **C**'s members via a persistent data channel using asymmetric encryption (the community admin that issues a new community key separately "sends" the key to each member in **C**'s member registry channel, encrypting the new key with the recipient members's latest public key, which is also available in the member registry channel)
8. **C**'s "member registry channel" is defined as a log containing each member's UUID and current crypto "epoch":
```
// MemberEpoch represents a public "rev" of a community member's crypto
type MemberEpoch struct {
   EpochInfo             EpochInfo
   PubSigningKey         []byte
   PubCryptoKey          []byte
}
```
7. **C**'s root "access control channel" (ACC) is a log containing access grants to member ID

8.  If/When a member, **m**, becomes aware their keyrings has been lost or compromised, **m** (or a peer of **m**) can immediately initiate a _keyring halt procedure_, where:
     1.  A special transaction by **m** (or on behalf of **m**) is submitted to **𝓛<sub>C</sub>** immediately "burning" **m**'s ability to post any further transactions to **𝓛<sub>C</sub>**.  This removes the ability of an adversary in possession of _any_ of **m**'s keyrings to author further entries on **𝓛<sub>C</sub>**.  
     2.  An admin, or a quorum of **C**, or an automated system initiates:
        - a new community key epoch for **C**, _and_
        - a secure token that would be transferred to **m** via a secure channel (or in person).  This token, when opened, would allow a new `MemberEpoch` to be accepted for **m**, allowing **m** to resume normal access to **𝓛<sub>C</sub>**.
     In effect, all subsequent transactions on **𝓛<sub>C</sub>** will be unreadable to any holder of the compromised keyring is not is possession of any key that would gain them access to the newly issued community key or **m** newly issued keys.  **m** would regain
Note that the given adversary would only have access to community public data (with **[]K<sub>C</sub>**) and **m**'s particualar dats

```

type CommunityMember struct {
    CommunityID               UUID          // Assigned
    MemberID                  UUID          // Issued when member joins C
    type KeyRepo struct {
        CommunityKeyring []KeyEntry
    PersonalKeyring  []KeyEntry
    }
}
```


---

### Proof of Requirements & Claims

 1.  In order for a data storage transaction, **t**, to be accepted into **𝓛<sub>C</sub>**, it must (by definition):
    - contain a valid signature that proves the data and author borne by **t** is authentic, _and_
    - specify an author that **𝓛<sub>C</sub>** recognizes as having permission to post a transaction of that size.

 Given that each member **m** of **C** is in sole possession of their personal keyring, it follows that only **m** can author and sign transactions that **𝓛<sub>C</sub>** will regard as authentic.  If/When **m** becomes aware their personal keys are lost or compromised, **m** can immediately initiate a _keyring halt procedure_.  

  **𝓛<sub>C</sub>** (and )
 A **C** node in **C** running a daemon hosting **𝓛<sub>C</sub>** is hosting a replicating append-only CRDT database by definition.  Using any implementation available, it is endowed with authentication mechanism such that any client wishing to submit a transaction to be appended, must either provide a transaction signature that  


### further






### scrap/work area

In this operating system



Let **St** be an append-only p2p replicating data store, where new data blobs can be appended and subsequently retrieved (via a transaction ID). A node's particular state of **St**

Let
   , where the afflicted member's keys are regenerated (originating from a token generated from a community admin).  


8. **C**'s technology provisions for a "hard fork", where admins and members elect which fork to place themselves in.  

Let **σ<sub>C</sub>** be the average time period it takes for replicated network messages to reach 2/3 of the network's nodes.  This lets us set a reasonable upper-bound on how long permissions changes in **C** take to propagate.  If we were to wait 10 or 100 times **σ**, it would be safe to assume that any nodes able to receive a replicated message would have received it (if it was possible).  We thus express a time delay ceiling of permissions propagation as **kσ**.  Above this time, we assume there it is not beneficial to wait and hope that a newly arrived message will resolve a conflict.  We therefore must establish a deterministic set of rules to resolve all possible **CRS** conflicts.  For a network of 10,000 nodes in the internet of 2018, a reasonable value for **kσ** could be 3-12 hours.



https://github.com/protocol/research-RFPs/blob/master/RFPs/rfp-4-CRDT-ACL.md


https://github.com/protocol/research-RFPs/blob/master/RFPs/rfp-5-optimized-CmRDT.md

https://github.com/protocol/research/blob/master/README.md

https://github.com/protocol/research-RFPs/blob/master/RFP-application-instructions.md

https://github.com/ipfs/research-CRDT/tree/master/research

https://github.com/ipfs/research-CRDT

https://github.com/protocol/research/issues/8


https://github.com/protocol/research-RFPs/blob/master/RFP-application-instructions.md
