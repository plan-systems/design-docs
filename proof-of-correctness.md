 # Proof of Correctness for PLAN

```
         P urposeful
         L ogistics
         A rchitecture
P  L  A  N etwork
```

## What is this?

In computer science, a "proof of [correctness](https://en.wikipedia.org/wiki/Correctness_(computer_science))" refers to a formal walk-though and demonstration that a proposed method and/or design rigorously satisfies a given set of specifications or claims.  The intention is to remove _all doubt_ that there exists a set of conditions such that the proposed method would _not_ meet all the specifications.

Below, we express the scenario, a set of specifications, and a digital infrastructure schema.  We then proceed to demonstrate correctness for each specification, citing how the schema and its prescribed operation satisfies that specification.  

Please note that the data structures listed below are intended to convey understanding and model correctness more than they are intended to be performant.  [go-plan](https://github.com/plan-tools/go-plan) is the latter.

---

## On Digital Security

We acknowledge that even the most advanced secure systems are vulnerable to private key theft, socially engineered deception, or extreme coercion.  That is, an adversary in possession of another's private keys without their knowledge, or an adversary manipulating or coercing others is difficult or impossible to prevent.  Biometric authentication systems can mitigate _some_ of these threats, but they also introduce additional surfaces that can potentially be exploited (e.g. spoofing a biometric device or exploiting an engineering oversight).

The system of operation discussed here features swift auto-countermeasures _once it becomes known_ that private keys have been compromised or unauthorized access has occurred.

---

## Scenario

A founding set of **c**ommunity organizers ("admins") wish to form **C**, a secure distributed storage network comprised of computers with varying capabilities, each running a common peer-to-peer software daemon ("node"). **C** is characterized by a set of individual members for any given point in time, with one or more members charged with administering member status, member permissions, and community-global rules/policies.  

On their nodes, the members of **C** agree to employ **𝓛**, an _append-only_ [CRDT](https://en.wikipedia.org/wiki/Conflict-free_replicated_data_type).  Data entries appended to **𝓛** ("transactions") are characterized by an arbitrary payload buffer, a signing public key, and a signature authenticating the transaction.  Transactions on **𝓛** are considered to be "in the clear" to adversaries (i.e. neither "wire" privacy _nor_ storage privacy is assumed).

Given **C**, **𝓛<sub>C</sub>** is assumed to either contain (or have access to) a verification system such that a transaction submitted to **𝓛<sub>C</sub>** is acceptable _only if_ the transaction's author (signer) has explicit _𝓛-append permission_.  At first this may appear to be a strong requirement, but it reflects the _transference_ of security liability of the key(s) specified during the genesis of **𝓛<sub>C</sub>** to an _external_ set of authorities.

For example, a customized "private distro" of the [Ethereum](https://en.wikipedia.org/wiki/Ethereum) blockchain ("**⧫<sub>C</sub>**") could be used to implement **𝓛<sub>C</sub>** since:
   - The admins, upon creating **⧫<sub>C</sub>**, would issue themselves some large bulk amount _"C-Ether"_.
   - The admins of **C** would periodically distribute portions of _C-Ether_ to members of **C** (a quota implementation).  
   - Large client payload buffers would be split into 32k segments (Ethereum's transaction size limit) and _then_ committed to **⧫<sub>C</sub>**.
   - On **C**'s nodes, **⧫<sub>C</sub>** transactions that do not "burn" an amount of _C-Ether_ commensurate with the byte size of the payload would be rejected/ignored.

To put **𝓛** into context, consider watching the distinguished [George Glider](https://en.wikipedia.org/wiki/George_Gilder) in this [video clip](https://www.youtube.com/watch?v=cidZRD3NzHg&t=1214s) speak about blockchain as an empowering distributed security and information technology.

---


## Specifications & Requirements

The members of **C** wish to assert that:
1. _Only_ members of **C** have append-access to **𝓛<sub>C</sub>**.
2. For all actors _not_ in **C**, all transactions sent to, read from, and residing on **𝓛<sub>C</sub>** are informationally opaque to the maximum extent possible.
3. There is a hierarchy of member admin policies and permissions that asserts itself in order to arrive at successive states (and cannot be circumvented).
4. New members can be added to **C** at any time (given that **C** policies and permissions are met).
5. Assume a minority number of members are (or become) covert adversaries of **C** (or are otherwise coerced).  Even if working in concert, it must be impossible for them to: impersonate other members, insert unauthorized permission or privilege changes, gain access to others' private keys or information, or alter **𝓛<sub>C</sub>** in any way that poisons or destroys community content.
5. In the event that an adversary gains access to an admin's private keys (or an admin becomes an adversary), or **𝓛<sub>C</sub>** is otherwise corrupted or vandalized, **C** can elect to "hard fork" **𝓛<sub>C</sub>** to an earlier time state.
6. Member admins can "delist" members from **C** such that they become equivalent to an actor that has never been a member of **C** (aside that delisted members can retain their copies of **𝓡** before the community entered this new security "epoch").
7. For each node **n<sub>i</sub>** in **C**, it's local replica state ("**𝓡<sub>i</sub>**"), converges to a stable/monotonic state as **𝓛<sub>C</sub>** message traffic "catches up", for any set of network traffic delivery conditions (natural or adversarial). That is, **𝓡<sub>1</sub>**...**𝓡<sub>n</sub>** update such that strong eventual consistency (SEC) is guaranteed.  
8. If/When it is discovered that a member's personal or community keys are known to be either comprised or lost, an admin (or members previously designated by the afflicted member) initiate a new security epoch such that:
   - an adversary in possession of said keys will have no further access to **C**
   - the afflicted member's resulting security state is unaffected
9. **C**, led by a coordinated admin effort, can swap out CRDT technologies (e.g. **C** may use a CRDT that automatically halts under suspicious network conditions or insufficient peer connectivity, but earlier in its history when it had to be more agile, **C** used a CRDT that favored "liveness" over safety).


---


## System Proposal

The members of **C** propose the following infrastructure:
1. Let `UUID` represent a constant-length independently unique ID that ensures no reasonable chance of collision (typically 20 to 32 pseudo-randomly generated bytes).
2. Each member of **C** securely maintains two "keyrings":
  1. **[]K<sub>personal</sub>**, the member's _personal keyring_, used to:
       - decrypt/encrypt information "sent" to/from that member
       - create signatures that authenticate information claimed to be authored by that member
  2. **[]K<sub>C</sub>**, the _community keyring_, used to encrypt/decrypt "community public" data (i.e. the cryptographic bridge between **𝓛<sub>C</sub>** and **𝓡<sub>L</sub>**)
3. Each transaction residing on **𝓛<sub>C</sub>** is a serialization of:
```
type EntryCrypt struct {
    CommunityKeyID    UUID     // Identifies the community key used to encrypt .HeaderCrypt
    HeaderCrypt       []byte   // := Encrypt(<EntryHeader>.Marshal(), <EntryCrypt>.CommunityKeyID)
    ContentCrypt      []byte   // := Encrypt(<Body>.Marshal(), e->hdr.ContentKeyID)
    Sig               []byte   // Authenticates this EntryCrypt; signed by e->hdr.AuthorMemberID
}

```
Let:


    return 
4. Each `EntryCrypt.HeaderCrypt` is encrypted using **[]K<sub>C</sub>** and specifies a persistent `ChannelID` that it operates on **C**'s _virtual_ channel space:
```
type EntryHeader struct {
    EntryOp           int32    // Op code specifying how to interpret this entry. Typically, POST_CONTENT
    TimeAuthored      int64    // Unix timestamp of when this header was encrypted and signed ("sealed")
    ChannelID         UUID     // Channel that this entry is posted to (or operates on)
    ChannelEpochID    UUID     // Cites the latest epoch of the channel in effect when this entry was authored
    AuthorityEntryID  UUID     // Cites the entry in ChannelEpochID->ChannelID authorizing the validity of this entry
    AuthorMemberID    UUID     // Creator of this entry (and signer of EntryCrypt.Sig)
    AuthorMemberEpoch UUID     // Epoch of the author's identity when this entry was sealed
    ContentKeyID      UUID     // Identifies *any* key used to encrypt EntryCrypt.ContentCrypt
}
```
5. For every `EntryCrypt` **e** authored by members of **C** and posted to **𝓛<sub>C</sub>**, **e**`.Sig` is generated from on a hash digest of all other fields using the private signing key associated with the author's member ID and their current member epoch.  The key used to encrypt **e<sub>header</sub>**
5. On a community node **n<sub>i</sub>**, let **e** be an `EntryCrypt` newly arriving from **𝓛<sub>C</sub>**.  
  1. Let **e<sub>header</sub>** be the `EntryHeader` resulting from decrypting e.`HeaderCrypt` using the key in **[]K<sub>C</sub>** indexed by `e.CommunityKeyID`.
  2. `e.Sig` is validated by retrieving the public signing key listed for (**e<sub>header</sub>**`.AuthorMemberID`, `.AuthorMemberEpoch`) within **𝓡<sub>i</sub>**.
If either of the keys listed above are not found, it is possible that **𝓡<sub>i</sub>** has not been updated with entries that have yet to arrive.  Thus, **e** is placed into the node's "holding tank" for delayed processing since  If the keys are found by steps (1) or (2) fail to check, the entry is considered "hard" rejected and not considered further.
6. Assuming , verified, and deterministically merged into the node's local community "repo", **𝓡<sub>i</sub>**:

```
// A node's community replica/repo/𝓡i
type CommunityRepo struct {
   Channels          map[ChannelID]ChannelStore
}

// Stores and provides rapid access to entries in a channel
type ChannelStore struct {
   ChannelID         ChannelID
   Epochs            []ChannelEpoch  // The latest element is this channel's current epoch
   ValidUpTo         int64           // Time index indicating what entry validitty checked up to
   LiveTable         []Entry         // Entries indexed by TimeAuthored
   RetryPool         []Entry         // Contains entries that were soft rejected
}

// Represents a "rev" of this channel's security properties
type ChannelEpoch struct {
   EpochInfo         EpochInfo
   ChannelProtocol   string          // If access control channel: "/chType/ACC"; else: "/chType/client/*"
   ChannelID         UUID            // Immutable; generated during channel genesis
   AccessChannelID   UUID            // This channel's owning ACC, conforms to an ACC, cannot form circuit
}

// Specifies general epoch parameters and info
type EpochInfo struct {
   EpochStart        timestamp
   EpochID           UUID
   EpochIDPrev       UUID            // Forms a linked list extending from the past
   TransitionSecs    int             // Custom-epoch transition rules, etc
}
```

6. Entries that do not conform to channel properties or permissions are placed in a "holding tank" within **𝓡<sub>i</sub>**. The node periodically reattempts to merge these entries with the understanding that later-arriving entries may alter **𝓡<sub>i</sub>** such that previously rejected entries now conform. Entries that are rejected on the basis of an validation failure (e.g. signature validation failure) are dropped. These rejections are cause for concern and could logged to discern bad actor patterns.
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

8.  If/When a member, **m**, becomes aware their keyrings has been lost or compromised, **m** (or a peer of **m**) would initiate a _keyring halt procedure_, where:
     1.  A special transaction by **m** (or on behalf of **m**) is submitted to **𝓛<sub>C</sub>**, immediately "burning" **m**'s ability to post any further transactions to **𝓛<sub>C</sub>**.  In effect, this removes the ability of any actor in possession of **m**'s keyrings to author further entries on **𝓛<sub>C</sub>**.  
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

### Standard Procedures

   * [Keyring Halt](#keyring-halt-procedure)
   * [Deferring An Entry]

   * [Merging Channel Entries](#Channel-Entry-Validation)
        - Given node **n<sub>i</sub>** in **C**, let **𝓡<sub>i</sub>** denote the local replica state of **𝓛<sub>C</sub>** at a given time.
        - On "deferring" an entry:
            - Since entries can arrive in a semi-arbitrary order at **n<sub>i</sub>**, an entry may arrive whose successful processing may depend on other entries that have yet to arrive (or finish processing).
            - This means that as **n<sub>i</sub>** attempts to merge entries from **𝓛<sub>C</sub>** into **𝓡<sub>i</sub>**, it will sometimes encounter an incoming entry **e** that it cannot yet assuredly merge or reject.  In this sitaution, **e** is moved into an appropriate `RetryPool` such that  **n<sub>i</sub>** will retry merging it at a later time (we say "**e** is deferred").
        - On "rejecting" an entry:
            - As **n<sub>i</sub>** processes entries from **𝓛<sub>C</sub>**, there are specific conditions that, if not met, will cause **n<sub>i</sub>** to "hard" reject an entry.
            - If a "hard" requirement is not met, such as an entry having a valid signature, the entry is considered to be permanently rejected/discarded (we say "**e** is rejected"). 
        - For each new entry **e** arriving from **𝓛<sub>C</sub>** (or is locally authored and also submitted to **𝓛<sub>C</sub>**):
            - Validate **e**:
                1. **e<sub>digest</sub>** ⇐  DigestFor(  **e**`.CommunityKeyID`,   **e**`.HeaderCrypt`,  **e**.`ContentCrypt` )
                2. **e<sub>hdr</sub>** ⇐ `EntryHeader` ⇐ Decrypt( **e**`.HeaderCrypt`,  **𝓡<sub>i</sub>**.LookupKey(**e**`.CommunityKeyID`) )
                    - if the specified key is not found, **e** is deferred.
                3. **e<sub>authPubKey</sub>** ⇐ **𝓡<sub>i</sub>**.LookupKeyFor(**e<sub>hdr</sub>**.`AuthorMemberID`, **e<sub>hdr</sub>**`.AuthorMemberEpoch`)
                4. ValidateSig(**e<sub>digest</sub>**, **e**`.Sig`, **e<sub>authPubKey</sub>**)
                    - if **e**`.Sig` is invalid, then **e** is rejected.
            - Try to merge **e** into **𝓡<sub>i</sub>**:
                1. **𝘾𝒉<sub>store</sub>** ⇐ **𝓡<sub>i</sub>**.GetChannelStore( **e<sub>hdr</sub>**.`ChannelID` )
                2. Ensure the cited `ChannelEpoch` is acceptable:
                    - **𝓔<sub>cited</sub>** ⇐ **𝘾𝒉<sub>store</sub>**.LookupEpoch( **e<sub>hdr</sub>**.`ChannelEpochID` )
                        - if **𝓔<sub>cited</sub>** == `nil`, then **e** is deferred.
                    - **𝓔<sub>expected</sub>** ⇐ **𝘾𝒉<sub>store</sub>**.ExpectedEpoch()
                        - if **𝓔<sub>cited</sub>** ≠ **𝓔<sub>expected</sub>**, then **e** is deferred.
                    
                7. **𝘼𝘾𝘾𝒉<sub>store</sub>** ⇐ **𝓡<sub>i</sub>**.GetChannelStore( **𝘾𝒉<sub>epoch</sub>**.`ChannelID` )
                8. **ℓ<sub>auth</sub>** ⇐ **𝘼𝘾𝘾𝒉<sub>store</sub>**.LookupAccessLevelFor( **e<sub>hdr</sub>**.`AuthorMemberID` )
                    - if any unexpected conditions during steps 1-4, then **e** is rejected.
                    - if  **ℓ<sub>auth</sub>** does not permit **e<sub>hdr</sub>**`.EntryOp`, then **e** is deferred.
                        
                9. if **𝘾𝒉<sub>store</sub>**`.IsACC()` _and_ has mutated to be _more_ restricitve, then revalidate dependent channels:
                    - Let **t<sub>rev</sub>** ⇐ **e<sub>hdr</sub>**`.TimeAuthored`
                    - for each **𝘾𝒉<sub>j</sub>** in **C** where **𝘾𝒉<sub>j</sub>**`.AccessChannelID` == **𝘾𝒉<sub>store</sub>**`.ChannelID`:
                        - Scanning forward from **t<sub>rev</sub>** in  **𝘾𝒉<sub>j</sub>**, for each entry **e<sub>j</sub>**:
                            - Revalidate **e<sub>j</sub>** (steps 1-4 above)
                    - Although there are edge cases where the above _could_ result in a cascading workload, in almost all cases the amount of work is either n/a or negligable.  This is because:
                        - Revaldiation is only needed if:
                            - the channel is an ACC (i.e. only ACCs have dependencies), _and_
                            - the entry mutation makes an ACC _more_ restrictive 
                        - Most activity in **C** is presumably content, not access-control related.  (e.g. compare the number of ACL-related files stored on a workstation to the _total_ number of files)
                        - Mutations to a channel tend to occur close to the present time (⇒ only O(1) of all entry history is affected)
                        - Revalidation can be strategically deferred/scheduled, allowing multiple ACC mutations to require only a single revalidation pass.

                            
   * [Start New Community Epoch](#Initiate-a-New-Community-Epoch)
   * [Start New Member Epoch](#Initiate-a-New-Member-Epoch)
   * [Add New Member](#Add-New-Member)
   * [Delist Member](#Delisting-a-Member)
 

---

## Proof of Requirements & Claims

_Each numbered item here corresponds to the items in the Specifications & Requirements section_.

 1.  Given **𝓛<sub>C</sub>**, in order for a data storage transaction **txn<sub>C</sub>** to be accepted, by definition it must:

     - contain a valid signature that proves the data and author borne by **txn<sub>C</sub>** is authentic, _and_
     - specify an author that **𝓛<sub>C</sub>** recognizes as having permission to post a transaction of that size.

     Given that each member **m** of **C** is in sole possession of their personal keyring, it follows that _only_ **m** can author and sign transactions that **𝓛<sub>C</sub>** will accept.  In the case where **m**'s personal keys are lost or compromised, **m** would immediately initiate a [Keyring Halt](#keyring-halt) procedure, leaving any possessor of **m**'s private keys unable to post a trasnaction to **𝓛<sub>C</sub>**.


2.  Any actor _not_ a member of **C** by definition does not possess the community keyring, **[]K<sub>C</sub>**, containing the latest community keys.  Thus, the _only_ information available to actors outside of **C** is the `UUID` of the community key used to encrypt a given `EntryCrypt` stored on **𝓛<sub>C</sub>**. This implies:
    - information opacity is maximized since all other information resides within `HeaderCrypt` or `ContentCrypt`, _with the exception that_  adversaries snooping **𝓛<sub>C</sub>** could discern _when_ a new community security epoch began.  However this is weak information since such an event could correspond to any number of circumstances.
    - if actor **a** is formerly a member of **C** (or was known to have access to a member's private keys), then **a**'s access is limited to
      read-access up to until the time when a new community security epoch was initiated.   In order for **a** to receive the latest community key, **a** must possess the latest private key of a member currently in **C** (see _initiating a new community security epoch_). 
      
3. All "live" entries in a node's local replica ("**𝓡<sub>i</sub>**") must pass [Channel Entry Validation](#Channel-Entry-Validation).  This implies each successive state of **𝓡<sub>i</sub>** is a valid mutation of its previous state.  What is the possibilty that replicas on two different nodes differ such that are such that  node **n<sub>i</sub>** **nSo is there a way for  **𝓡<sub>i</sub>** and  **𝓡<sub>j</sub>** The remaining possibilty for  **𝓡<sub>i</sub>** to be  abilty for For this not to be the case, one of the following must be true:
    - Given node **n<sub>i</sub>** there exists a way to reorder (or temporarily withhold) transcations coming from **𝓛<sub>C</sub>** such that **𝓡<sub>i</sub>** passes through states that it ordinarily would not have passed through. This scenario:
        - precludes the possibility of unauthorized key or channel access since any absence of transcations couldn't result in generation/grant of _additional_ permissions, _provided that an ACC mutation also initiates a new channel security epoch_. Since all ACC references must cite the _latest_ ACC epoch (or risk rejection), an adversary witholding transactions from **n<sub>i</sub>** at worst would result in denial of service.
        - discounts **𝓛<sub>C</sub>**'s ability to auto-halt if 
    - There exists a way for a member **m** (or an adversary covertly in possession of **m**'s keys) to author a series of channel entries such that one or more channel permissions are violated or altered in an unauthorized way. This can be expressed as an entry being validated, and thus merged, into a channel when it should be rejected.  How could an entry be merged in a channel that whose ACC denies it?  Implementation oversights aside, this could only happen by a late-arriving entry retroactively changing a channel's ACC such that now some set of entries should now be rejected.  However, since [ACC Change Propigation](#) occurs for all ACC changes, any conflicting entries would be put into the channel's `RetryTable`.  In cases where there is an ambigous conflict (e.g. an admin gives  member is given moderator access to a channel while another 
        - An implementation bug 


   - if an entry **e** under consideration does not validate against its parent ACC, it is said to be "in conflict".  All entries (except those in **C**'s "root" channels) can potentially be in conflict since an entry could arrive and alter it's parent ACC such that is now in conflict.
    -if **e** is in conflict,  
 - when "in band" conflict occurs (a conflict w/in the same channel), the "winner" is chosen by a weighted compare of each authors relative senioriy weighted with the time delta
     that is, there exists no possible    It is uncondiontally moved from the `LiveTable` to the `RetryTable` (e.g. a post from an author that has now been delisted). --  i.e. any entry NOT in an ACC!
   - every entry in an ACC *could* potentially affect all other channels it controls
   - unapposed ACC change: there exists no other entry authored in the timespan **ko**  
   - an ambigous conflict (in an ACC): the merger of **e<sub>1</sub>** would potentially result in one or more _other_ entries to unambigously conflict 

Since the [Add New Member](#Add-New-Member) procedure is implemented by making standard entries that conform to [Channel Entry Validation](#Channel-Entry-Validation), the security liabilty of  

integrity of adding new members to **C** in accordance with **C** policies rests in the 


a probabiltisic proof?  if entries in the soft holding tank

     

### further



note: although TimeAuthored is used to index entries, some Lc implmentations may optionally provide a time index value that converges to within
a fixed provable accuracy of when the network witnessed it sent (as it travels further into the past).  TimeConsensus (Dfinity, Hashgraph).  For a given transaction **t**, let **t<sub>t </sub>**


### scrap/work area

In this operating system

 
      This is because **a**, unlike members of **C**, would not have a key needed to decrypt the newly community keys. 
       be  not possess the newly issued key  Thus, all **C** entries authored in the new community key epoch will be unreadable by **a**. 



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
