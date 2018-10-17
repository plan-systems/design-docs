 # Proof of Correctness for PLAN

```
         P urposeful
         L ogistics
         A rchitecture
P  L  A  N etwork
```

## What is this?

In computer science, a "proof of [correctness](https://en.wikipedia.org/wiki/Correctness_(computer_science))" refers to a formal walk-though and demonstration that a proposed method and/or design rigorously satisfies a given set of specifications or claims.  The intention is to remove _all doubt_ that there exists a set of conditions such that the proposed method would _not_ meet all the specifications.

Below, we express the [scenario](#scenario), a [set of specifications](#Specifications-&-Requirements), and a [proposed system of operation](#Proposed-System-of-Operation).  We then proceed to demonstrate [correctness for each specification](#Proof-of-Requirements-&-Claims), citing how the system and its prescribed operation satisfies that specification.  

Please note that the data structures listed below are intended to convey understanding and model correctness more than they are intended to be performant.  [go-plan](https://github.com/plan-tools/go-plan) is intended to be the latter.

---


# Scenario

A founding set of community organizers ("admins") wish to form **C**, a secure distributed storage network comprised of computers with varying capabilities, each running a common peer-to-peer software daemon ("node"). **C** is characterized by a set of individual members for any given point in time, with one or more members charged with administering member status, member permissions, and community-global rules/policies.  

On their nodes, the members of **C** agree to employ **𝓛**, an _append-only_ [CRDT](https://en.wikipedia.org/wiki/Conflict-free_replicated_data_type).  Data entries appended to **𝓛** ("transactions") are characterized by an arbitrary payload buffer, a signing public key, and a signature authenticating the transaction.  Transactions on any given **𝓛** are considered to be "in the clear" (i.e. neither "wire" privacy _nor_ storage privacy is assumed).

Let **𝓛<sub>C</sub>** be a CRDT whose genesis is under exclusive control of the admins of **C**.  **𝓛<sub>C</sub>** is assumed to either contain (or have access to) a verification system such that a transaction submitted to **𝓛<sub>C</sub>** is acceptable _only if_ the transaction's author (signer) has explicit _𝓛-append permission_ ("postage").  At first this may appear to be a strong requirement, but it reflects the _transference_ of security liability of the key(s) specified during the genesis of **𝓛<sub>C</sub>** to an _external_ set of authorities.

For example, a customized "private distro" of the [Ethereum](https://en.wikipedia.org/wiki/Ethereum) blockchain ("**⧫**") could be used to implement **𝓛** since:
- The admins of **C**, on creating **⧫<sub>C</sub>**, would issue themselves large some bulk amount _C-Ether_ ("postage").
- The admins of **C** would periodically distribute portions of _C-Ether_ to members of **C** (serving as a postage quota).  
- On **C**'s nodes, **⧫<sub>C</sub>**:
    - Large client payload buffers would be split into 32k segments (Ethereum's transaction size limit) and _then_ committed.
    - Transactions that do not "burn" an amount of postage commensurate with the byte size of the payload would be rejected/dropped.
    - Transactions that transfer postage from non-designated identities would be rejected/dropped.

For context, consider watching the distinguished [George Glider](https://en.wikipedia.org/wiki/George_Gilder) in this [video clip](https://www.youtube.com/watch?v=cidZRD3NzHg&t=1214s) speak about blockchain as an empowering distributed security and information technology.

---

## On Digital Security

We acknowledge that even the most advanced secure systems are vulnerable to private key theft, socially engineered deception, or physical coercion.  That is, an adversary in possession of another's private keys without their knowledge, or an adversary manipulating or coercing others is difficult (or impossible) to prevent.  Biometric authentication systems can mitigate _some_ of these threats, but they also introduce additional surfaces that could be exploited (e.g. spoofing a biometric device or exploiting an engineering oversight).

The system of operation discussed here features swift auto-countermeasures _once it becomes known_ that private keys have been compromised or unauthorized access has occurred.

---

## On Network Latency

When a chain of events is descibed in this system, replcated data transactions and messages are assumed to potentially take significant lengths of time to propigate across the network.  It is also assumed that some nodes may be offline for indefinite periods of time.

Given the nodes of **C**, let **Δ<sub>C</sub>** be the time period needed for there to be at least a 99% chance that all _reachable_ nodes in **C** have received a given replicated message.   For a network of 10,000 reachable nodes in 2018, **Δ<sub>C</sub>** is in the neighborhood of 1-10 minutes, depending on how **𝓛** implements transaction replication.

---

# Specifications & Requirements

The members of **C** wish to assert...

#### Signal Opacity
- For all actors _not_ in **C**, all transactions sent to, read from, and residing on **𝓛<sub>C</sub>** are informationally opaque to the maximum extent possible.

#### Access Exclusivity
- _Only_ members of **C** effectively have read and append access to **𝓛<sub>C</sub>**.
- Alternatively, parts of **C** can be set up for "public access" where non-members of **C** have read access to select community content.

#### Permissions Assurance
- There is a hierarchy of member admin policies and permissions that asserts itself in order to arrive at successive states (and cannot be circumvented).
- Consider the case where a number of members are (or become) covert adversaries of **C** (or are otherwise coerced).  Even if working in concert, it must still be impossible to: impersonate other members, insert unauthorized permission or privilege changes, gain access to others' private keys or information, or alter **𝓛<sub>C</sub>** in any way that poisons or destroys community content.

#### Membership Fluidity
- New members can be invited to and join **C** at any time (given that **C** policies and permissions are met).
- A member can be "delisted" from **C** such that they become equivalent to an actor that has never been a member of **C** (aside that delisted members can retain their copies of **𝓡** before the community entered this new security "epoch").

#### Strong Eventual Consistency
- For each node **n<sub>i</sub>** in **C**, it's local replica state ("**𝓡<sub>i</sub>**"), converges to a stable/monotonic state as **𝓛<sub>C</sub>** message traffic eventually "catches up", for any set of network traffic delivery conditions (natural or adversarial). That is, **𝓡<sub>1</sub>**...**𝓡<sub>N</sub>** mutate such that strong eventual consistency (SEC) is guaranteed.  

#### Practical Security Provisioning
- If/When it is discovered that a member's private keys are known to be either lost or possibly comprised, a "[keyring halt](#keyring-halt)" can be immediately initiated such that any actor in possession of said keys will have no further read or write access to **C**.
- Actors that can initiate a keyring halt include:
   - the afflicted member, _or_
   - a member peer (depending on community-global settings), _or even_
   - an automated watchdog system on **C** (responding to abnormal or malicious activity)
- Following a keyring halt, the afflicted member's security state enters new "epoch" and incurs no additional security liability.  That is, there are no potential "gotchas" sometime down the road if an adversary gains access to previously compromised keys.

#### Independence Assurance
- In the event that:
    - an adversary gains covert access to admin/root private keys, _or_
    - one or more admins becomes adversarial towards **C**, _or_ 
    - **𝓛<sub>C</sub>** is otherwise corrupted or vandalized, 
- ...then **C** can elect to "hard fork" **𝓛<sub>C</sub>** to an earlier time state, where specified members are delisted from the member registry and others are granted admin permission.

#### Storage Portability
- **C**, led by a coordinated admin effort, always has the ability to swap out CRDT technologies. 
- For example, **𝓛<sub>C</sub>** may automatically halt under suspicious network conditions or insufficient peer connectivity, but earlier in its history when it had to be more agile, **C** used a CRDT that favored "liveness" over safety).


---

# Proposed System of Operation

The members of **C** present the following system of infrastructure...

## System Synopsis

- The system proposed is "IRC-inspired" in that community and member information is organized into an infinitely large virtual channel addressing space.  However, instead of entries entered into channels just being rebroadcast to connected clients (as on an IRC server), entries _persist_ by being stored as replicated transactions on **𝓛<sub>C</sub>**.    
- When a channel is created, it is assigned a `ChannelProtocol` string, specifying the _kind_ of entries that are expected to appear that channel and _how_ UI clients should interpret them.  This, plus the ability for _any_ channel entry to include arbitrary HTTP-style headers, affords graphical client interfaces rich and wide-open possibilites.
- Also like IRC, each channel has its own permissions settings.  Every channel is controlled by an "access control" channel ("ACC"), a channel that conforms to a protocol designed to specify channel permissions.  Like other channels, each ACC designates a parent ACC, all the way up to **C**'s root-level ACC.  
- Members, channels, and **C** itself uses security "epochs" to demarcate security events and provide [permissions assurance](#permissions-assurance).
- Each community node (**n<sub>i</sub>**) iteratively mutates its local replica (**𝓡<sub>i</sub>**) by "replaying" newly arriving entries from **𝓛<sub>C</sub>**, possibly rejecting entries or deferring entries for later processing as appropriate.
- Hence, the entry processing pipeline forms a securely contained processing center system of operation above and outside **C**'s channel data space.


## System Security


- Let `UUID` represent a constant-length independently generated identifier that ensures no reasonable chance of peer collision. Athough it is difficult to express [collision odds](http://preshing.com/20110504/hash-collision-probabilities/) in meaningful human terms (even for "modest" probability spaces such as 1 in 2<sup>160</sup>), 20 to 32 pseudo-randomly generated bytes is more than sufficient to implement `UUID`.
- Each member, **m**, in **C** securely maintains custody of two "keyrings":
   1. **[]K<sub>m</sub>**, the member's _personal keyring_, used to:
       - decrypt/encrypt information "sent" to/from that member
       - create signatures that authenticate information authored by that member
   2. **[]K<sub>C</sub>**, the _community keyring_, used to encrypt/decrypt "community public" data (i.e. the cryptographic bridge between **𝓛<sub>C</sub>** and **𝓡<sub>i</sub>**) 
- When **m** signs or encrypts data, **m** always uses the latest published ("live") keys, denoted by **[0]K<sub>m</sub>** and **[0]K<sub>C</sub>** (as newly issued keys are inserted on the "left" side of a list).
- When **m** is accessing **C**, it is given that **m**'s local client effectively has access to these keyrings (though they can be implmented in ways that further comparmentalize security, such as using a hardware dongle or a key server).


## System Data Structures

- Each transaction residing in **𝓛<sub>C</sub>** contains a one or more serializations of:
```
type EntryCrypt struct {
    CommunityKeyID    UUID     // Identifies the community key used to encrypt .HeaderCrypt
    HeaderCrypt       []byte   // := Encrypt(<EntryHeader>.Marshal(), <EntryCrypt>.CommunityKeyID)
    ContentCrypt      []byte   // := Encrypt(<Content>.Marshal(), e->hdr.ContentKeyID)
    Sig               []byte   // Authenticates this entry; generated by e->hdr.AuthorMemberID
}
```
- `.HeaderCrypt` is decrypted using **[]K<sub>C</sub>** into an `EntryHeader`:
```
type EntryHeader struct {
    EntryOp           int32    // Op code specifying how to interpret this entry. Typically, POST_CONTENT
    TimeAuthored      int64    // Unix timestamp of when this header was encrypted and signed
    ChannelID         UUID     // Channel that this entry is posted to (or operates on)
    ChannelEpochID    UUID     // Cites the latest epoch of the channel in effect when this entry was authored
    AuthorMemberID    UUID     // Creator of this entry (and signer of EntryCrypt.Sig)
    AuthorMemberEpoch UUID     // Epoch of the author's identity when this entry was authored
    ContentKeyID      UUID     // Identifies any key used to encrypt EntryCrypt.ContentCrypt
}
```
- Each entry therefore specifies a destination `ChannelID` in **C**'s _virtual_ channel space to be merged into.  
- On each community node **n<sub>i</sub>**, newly arriving entries from **𝓛<sub>C</sub>** are validated and merged into the node's local community "repo" ("**𝓡<sub>i</sub>**") using the [Channel Entry Validation](#Channel-Entry-Validation) procedure. 

```
// A node's community replica/repo/𝓡i
type CommunityRepo struct {
   Channels          map[ChannelID]ChannelStore
}

// Stores channel entries and provides rapid access to them
type ChannelStore struct {
   ChannelID         ChannelID
   Epochs            []ChannelEpoch  // The latest element is this channel's current epoch
   ValidUpTo         int64           // Time index indicating what entry validity checked up to
   LiveTable         []Entry         // Entries indexed by TimeAuthored
   RetryPool         []Entry         // Contains entries that were soft rejected
}

// Represents a "rev" of this channel's security properties
type ChannelEpoch struct {
   EpochInfo         EpochInfo
   ChannelProtocol   string          // If access control channel: "/chType/ACC"; else: "/chType/client/*"
   AccessChannelID   UUID            // This channel's parent ACC, conforms to an ACC, cannot form circuit
}

// Specifies general epoch parameters and info
type EpochInfo struct {
   TimeStarted       timestamp
   EpochID           UUID
   EpochIDPrev       UUID
   TransitionSecs    int             // Epoch transition param, etc
}
```

6. Entries that do not conform to channel properties or permissions are placed in a `RetryPool` within **𝓡<sub>i</sub>**. The node periodically reattempts to merge these entries with the understanding that later-arriving entries may alter **𝓡<sub>i</sub>** such that previously rejected entries now conform. Entries that are rejected on the basis of an validation failure (e.g. invalid signature) are permanently rejected. These rejections are cause for concern and could logged to discern bad actor patterns.
7. Members of **C** maintain their copy of the community keyring, **[]K<sub>C</sub>**, where:
    1. **[]K<sub>C</sub>** encrypts/decrypts `EntryCrypt` traffic to/from **𝓛<sub>C</sub>**
    2. A newly generated community key is distributed to **C**'s members via a persistent data channel using asymmetric encryption (the community admin that issues a new community key separately "sends" the key to each member in **C**'s member registry channel, encrypting the new key with the recipient members's latest public key, which is also available in the member registry channel)
8. **C**'s "member registry channel" is defined as a log containing each member's UUID and current crypto "epoch":
```
// Represents a public "rev" of a community member's crypto
type MemberEpoch struct {
   MemberID          UUID
   EpochInfo         EpochInfo
   PubSigningKey     []byte
   PubCryptoKey      []byte
   HomeChannel       UUID
   ExInfo            plan.Block
}
```
7. **C**'s root "access control channel" (ACC) is a log containing access grants to member ID

8.  If/When a member, **m**, becomes aware their keyrings may have been lost or in possession of another, **m** (or a peer of **m**) would initiate a _keyring halt procedure_,
  

```
type MemberGenesis struct {
   MemberID          UUID       // Member ID
   FirstEpochID      UUID       // References a MemberEpoch in the community registry channel
}
```


## Reserved Channels
- A small number of channel `UUID`s are hardcoded ("reserved") and are used to specify root-level information and permissions, namely admin and member status.  The number, purpose, and use of these channels can be expanded to meet future needs.  These channels are special in that entries must meet additonal security checks/requirements.


#### Root Access Channel
- This is **C**'s root channel, effectively specifying which members are admins.
- Automated machinery in **C** could optionally be geared to use smart contracts on **𝓛<sub>C</sub>** to add entries to this channel.
    - .e.g. a majority vote of admins could be required in order to add a new admin to the root access channel. 

#### Member Registry Channel
- community-public read-only (only admins can write), where entries contain one or more `MemberGenesis` records, referencing an initial `MemberEpoch` record in the resereved _Member Epoch Channel_ (below).  

#### Member Epoch Channel
- a special community-public channel where members (or designated memebrs/admin specified by the parent ACC) publish new revisions to their `MemberEpoch` record.  
- A `MemberEpoch` record specifies essential information about a member, such as their public encryption and signining keys.
- Entries in this channel must meet the additional requirements that ensure a `MemberEpoch` can only be updated by it's owner (or a member delegated to do so).




## Standard Procedures

#### Keyring Halt
- Given member **m**'s private keys ("**[]K<sub>m</sub>**"), a _keyring halt_ is a special transaction submitted to **𝓛<sub>C</sub>**, immediately "burning" the abilty of **m** (or any possessor of **[]K<sub>m</sub>**) to post transactions to **𝓛<sub>C</sub>**.
    - Any transactions signed by **[]K<sub>m</sub>** and subsequently posted to **𝓛<sub>C</sub>** will be rejected because **[]K<sub>m</sub>** no longer has post permission on **𝓛<sub>C</sub>**.
    - For example, in **⧫<sub>C</sub>**, the transaction would send all **m**'s _C-Ether_ to address `x0`.
- In the case that an adversary in possesion of **[]K<sub>m</sub>** transfers their postage (their 𝓛-append priviledges) to another identity _before_ a keyring halt is posted for **m**, entries using postage descendent from the "tainted" postage would be rejected.
- In the case that an a adversary in possession of **[]K<sub>m</sub>** [starts a new member epoch](#Starting-a-New-Member-Epoch), an admin or member delegate in relationship with **m** would issue new entries that replace/rescind entries as necessary.  With any malicious entries in the [Member Epoch Channel](#Member-Epoch-Channel) rescinded, any 



#### Starting a New Member Epoch

- Given member **m** in **C** (defined by **m**'s member `UUID` and history of `MemberEpoch`s validly appearing in **C**'s reserved _member registry channel_.
- When **m** wishes to replace their currently published ("live") `MemberEpoch` with a new revision (often, when **m** wishes to _rekey_)
    - **m** creates an updated `MemberEpoch`, **𝓔**, retaining the newly generated private keys in **[]K<sub>personal</sub>**
    - **m** packages **𝓔** into a new entry ("**e<sub>𝓔</sub>**"), signs it, and posts it to **C**'s reserved _member epoch channel_.
        - In the  _member epoch channel_, in order for an entry to be considered live, it must have the appropriate member signatures, or it must be authored by a member bestowed with an elevated access level (i.e. one or more members or admins designated to assist members if they are locked out of **C** as a result of a [keyring halt](#keyring-halt)
- Once each node **n<sub>i</sub>** merges **e<sub>𝓔</sub>**, subsequent entries authored by **m** that are _not_ signed by **m**'s _latest_ signing key are rejected.  



#### Adding A New Member to C

- When **C** wants to bestow member status to actor **a**:
    - Given the permissions and authority needed on **C**, the root authority on **C** generates a new entry in the community registry channel containing:
        - a newly generated `MemberID` for **a**
        - 
    - A member of **C** ("**m<sub>a</sub>**") is designated as the "authority of admittance" for **a**
    - With this authority, **m<sub>a</sub>**'s node creates a token **τ**, containing:
        - a newly generated `MemberID` for **a**
        - a copy of the community keyring
        - a secret **s<sub>a</sub>** later used by **a** to register a new set of public keys under the given `MemberID`
        - network addresses and other boostrapping information that allows **a** to gain connectivity to **𝓛<sub>C</sub>**
        - a token that bestows its bearer postage on **𝓛<sub>C</sub>**
    - **τ**, secured with a symmetrical key, is given to **a** via any unsecured means (e.g. email, USB, OS file sharing)
    - Via face-to-face communication, direct contact, or via other secure means, **m<sub>a</sub>** gives **a** the key to access **τ**.
    - On a newly created "blank" node, **n<sub>a</sub>** (or an existing node of **C** in a logged-out state)
        - **a** passes **τ** to the client
        - the client prompts **a** for the key that decrypts **τ**
        - the client opens **τ** and, if applicable:
            - bootstraps **𝓛<sub>C</sub>**
            - builds **𝓡<sub>a</sub>** using normal [channel entry validation](#Channel-Entry-Validation)
        - when **𝓡<sub>a</sub>** is current, **n<sub>a</sub>**:
            - generates a new set of private keys to be published.  
            - posts a new `MemberEpoch` to **𝓛<sub>C</sub>**, also signed by **s<sub>a</sub>**, authenticating the new member epoch. 
    - The nodes of **C**, verifying this, now regard the public keys in `MemberEpoch` as **a**'s latest public keys.
        - Entries that are authored and signed by **a** any earlier than **Δ<sub>C</sub>** are rejected.

#### Delisting A Member from C
- When **C** or admins of **C** decide that member **m** is to be "delisted", they want to immediately strip **m**'s abilty to read and write to **C**.  
    - read **C** content
    - author content in **C** 


#### Loss of Keys
- Given **m** in **C**, a _keyring halt_ refers to the prompt execution of the following steps:
- If/When a member **m** becomes aware their community or personal keys have been lost or compromised ("**[]K<sub>lost</sub>**"), the possessor of **[]K<sub>lost</sub>** naturally would be able to:
    - author entries in **m**'s name
    - read community-public data on **C**
- In such an event, a _keyring halt_ is issued, referring to a special transaction issued by **m** (or on behalf of **m**) and submitted to **𝓛<sub>C</sub>**, immediately "burning" **m**'s ability to post any further transactions across **𝓛<sub>C</sub>**.  
    - In effect, this removes the ability of any actor in possession of **[]K<sub>lost</sub>** to author (and post) any further entries to **𝓛<sub>C</sub>**.  
- An admin, peers of **m**, a quorum of **C**, or an automated system would:
    - [initiate a new community epoch](#Starting-a-New-Community-Epoch) for **C**.
        - In effect, all subsequent community-public data in **C** uses a newly generated community key that is not in **[]K<sub>lost</sub>**.
        - [start a new member epoch](#Starting-a-New-Member-Epoch) for **m**.
    3. In effect, all subsequent transactions on **𝓛<sub>C</sub>** will be unreadable to any holder of the compromised keyring
            - a secure token that would be transferred to **m** via a secure channel (or in person).  This token, when opened, would allow a new `MemberEpoch` to be accepted for **m**, allowing **m** to resume normal access to **𝓛<sub>C</sub>**.
     In effect, all subsequent transactions on **𝓛<sub>C</sub>** will be unreadable to any holder of the compromised keyring is not is possession of any key that would gain them access to the newly issued community key or **m** newly issued keys.  **m** would regain
Note that the given adversary would only have access to community public data (with **[]K<sub>C</sub>**) and **m**'s particular dats
- In the case that an adversary issues their own **e<sub>𝓔</sub>** _before_ **m** is able to initiate a _keyring halt_, **m** could work with an admin of **C** to:
    - issue an entry that would rescind any entries in the _member epoch channel_ not authored by **m**

#### Channel Entry Validation
- Given node **n<sub>i</sub>** in **C**, let **𝓡<sub>i</sub>** denote the local replica state of **𝓛<sub>C</sub>** on **n<sub>i</sub>** at a given time.
- "Channel Entry Validation" is the process of merging incoming entries from **𝓛<sub>C</sub>** into **𝓡<sub>i</sub>** such that all "live" entries and channels of **𝓡<sub>i</sub>** are compliant and are in integrity with each author and admin's intent and security/privacy expectations. 
- When an entry is "deferred":
    - Since entries can arrive in a semi-arbitrary order at **n<sub>i</sub>**, an entry may arrive whose successful processing may depend on other entries that have _yet_ to arrive (or finish processing).
    - This means that as **n<sub>i</sub>** attempts to merge entries from **𝓛<sub>C</sub>** into **𝓡<sub>i</sub>**, it will sometimes encounter an incoming entry **e** that it cannot yet assuredly merge or reject.  In this situation, **e** is moved into an appropriate `RetryPool` such that  **n<sub>i</sub>** will retry merging it at a later time (we say "**e** is deferred").
- When an entry is "rejected":
    - As **n<sub>i</sub>** processes entries from **𝓛<sub>C</sub>**, there are specific conditions that, if not met, will cause **n<sub>i</sub>** to "hard" reject an entry.
    - If a "hard" requirement is not met, such as an entry having an authentic signature, then the entry is considered to be permanently rejected/discarded (we say "**e** is rejected"). 
- For each new entry **e** arriving from **𝓛<sub>C</sub>** (or is locally authored and also submitted to **𝓛<sub>C</sub>**):
    - Authenticate **e**:
        1. **e<sub>digest</sub>** ⇐  ComputeDigest(**e**`.CommunityKeyID`,   **e**`.HeaderCrypt`,  **e**.`ContentCrypt`)
        2. **e<sub>hdr</sub>** ⇐ `EntryHeader` ⇐ Decrypt(**e**`.HeaderCrypt`,  **𝓡<sub>i</sub>**.LookupKey(**e**`.CommunityKeyID`))
            - if the specified community key is not found, **e** is deferred.
        3. **𝓔<sub>auth</sub>** ⇐ **𝓡<sub>i</sub>**.LookupMemberEpoch(**e<sub>hdr</sub>**.`AuthorMemberID`, **e<sub>hdr</sub>**`.AuthorMemberEpoch`)
            - if **𝓔<sub>auth</sub>** = `nil`, then **e** is deferred. 
            - if **e<sub>hdr</sub>**`.TimeAuthored` is after **𝓔<sub>auth</sub>**`.TimeClosed`, then **e** is deferred.
        3. **e<sub>authPubKey</sub>** ⇐ **𝓡<sub>i</sub>**.LookupKeyFor(**e<sub>hdr</sub>**.`AuthorMemberID`, **e<sub>hdr</sub>**`.AuthorMemberEpoch`)
            - if **e<sub>authPubKey</sub>** = `nil`, then **e** is deferred. 
        4. ValidateSig(**e<sub>digest</sub>**, **e**`.Sig`, **e<sub>authPubKey</sub>**)
            - if **e**`.Sig` is invalid, then **e** is rejected.
    - "Channel-Validate" **e**:
        1. **𝘾𝒉<sub>dst</sub>** ⇐ **𝓡<sub>i</sub>**.GetChannelStore( **e<sub>hdr</sub>**.`ChannelID` )
            - if **𝘾𝒉<sub>dst</sub>** = `nil`, then **e** is deferred.
        2. Validate the `ChannelEpoch` cited by **e**:
            - **𝓔<sub>cited</sub>** ⇐ **𝘾𝒉<sub>dst</sub>**.LookupEpoch( **e<sub>hdr</sub>**.`ChannelEpochID` )
                - if **𝓔<sub>cited</sub>** = `nil`, then **e** is deferred.
            - if **𝓔<sub>cited</sub>**.CanAccept(**e<sub>hdr</sub>**`.TimeAuthored`), then proceed, else **e** is rejected.
                - this ensures that authors aren't risking security by using an excessively old `ChannelEpoch` 
        3. **𝘾𝒉<sub>acc</sub>** ⇐ **𝓡<sub>i</sub>**.GetChannelStore(  **𝓔<sub>cited</sub>**.`AccessChannelID` )
        4. **ℓ<sub>auth</sub>** ⇐ **𝘾𝒉<sub>acc</sub>**.LookupAccessLevelFor( **e<sub>hdr</sub>**.`AuthorMemberID` )
            - if  **ℓ<sub>auth</sub>** does not permit **e<sub>hdr</sub>**`.EntryOp`, then **e** is deferred.
    - Merge **e** into **𝓡<sub>i</sub>**:
        - if inserting **e** introduces an "ambiguous conflict", then perform [ambiguous conflict resolution](#ambiguous-conflict-resolution). 
        - if **𝘾𝒉<sub>dst</sub>** is an ACC and will be _more_ restrictive with **e**, then [initiate a new channel epoch](Initiating-a-New-Channel-Epoch) for **𝘾𝒉<sub>dst</sub>**
        - **𝘾𝒉<sub>dst</sub>**.InsertEntry(**e**)
    - Propagate the mutation of **𝘾𝒉<sub>dst</sub>** ("revalidation"):
        - if  **𝘾𝒉<sub>dst</sub>** is now _equally_ or _less_ restrictive, then `return` since no changes would possibly precipitate.
        - if  **𝘾𝒉<sub>dst</sub>** is now _more_ restrictive, then revalidate dependent channels:
            - Let **t<sub>rev</sub>** ⇐ **e<sub>hdr</sub>**`.TimeAuthored`
            - **[]𝘾𝒉<sub>dep</sub>** ⇐ **𝘾𝒉<sub>dst</sub>**.GetDependentChannels(**t<sub>rev</sub>**)
                - Note: only ACCs have dependencies
            - for each **𝘾𝒉<sub>j</sub>** in **[]𝘾𝒉<sub>dep</sub>**:
                - Scanning forward from **t<sub>rev</sub>** in  **𝘾𝒉<sub>j</sub>**, for each entry **e<sub>k</sub>**:
                    - [re]validate **e<sub>k</sub>** (steps 1-4 above)
                    - if **e<sub>k</sub>** is now deferred:
                        - **𝘾𝒉<sub>j</sub>**.RemoveEntry(**e<sub>k</sub>**)
                        - Defer **e<sub>k</sub>** normally
                        - Propagate the mutation of **𝘾𝒉<sub>j</sub>**
        - Although there are edge cases where change propagation _could_ result in a cascading workload, in almost all cases the amount of work is either n/a or negligible.  This is because:
            - Revalidation is only needed if:
                - the channel is an ACC (since only ACCs have dependencies), _and_
                - the entry mutation makes an ACC _more_ restrictive 
            - Most activity in **C** is presumably content, not access-control related.  (e.g. compare the number of ACL-related files stored on a workstation to the _total_ number of files)
            - Mutations to a channel tend to occur close to the present time (⇒ only O(1) of all entry history is affected)
            - Revalidation can be strategically scheduled, allowing multiple ACC mutations to require only a single revalidation pass.


#### Access Privileges

- Each channel in **C** must specify a special type channel called an access control channel ("ACC"), including ACCs themselves.
- An ACC specifies an access permission level for all possible members of **C** by storing:
    - a default 

 permissions for one or more other channels are called access control channels ("ACC")
/*
There are two sources of access control information, both stored in a channel's owning access channel.
   (1)  Default ChannelAccess levels, and
   (2)  ChannelAccess grants given to explicit community members. 

Note that even access channels follow the same plumbing, offering a powerful but compact hierarchal permissions schema.

Any channel (or access channel) can either be community-public or private.
    (a) community-public -- entry body encrypted with a community key and the owning access channel specifies
                            what permissions are and what users have grants outside of that (e.g. default READ_ACCESS,
                            users Alice and Bob have READWRITE_ACCESS access, Charlie is set for NO_ACCESS, and Daisy has MODERATOR_ACCESS.
    (b) private          -- entry body encrypted with the channel key "sent" to users via the channel's access channel.  Like with (a), 
                            members are granted explicit access levels (listed in ChannelAccess)

*/



#### Ambiguous Conflict Resolution

- The consensus properties of **C** are effectively called into action here.  By default, entries in conflict with each other are each given a score based on the seniority of each member and the time delta of the entries.  There is either deterministic "winner" or "tie". In a tie, both entries in conflict are nullified.  
    - Implementation note: nullified entries, although effectively rejected, remain 
    - and that occur within a given time window are rejected.  
- In accessing ambiguous conflict resolution, we separate them into to categories:
   - Legitimate/Natural
       - In this case, we assume the intention and timestamp on the entries are accurate and well intentioned. 
   - Adversary-Induced
       - In this case, we assume one or more of the entries in conflict have forged `TimeAuthored` and are mal-intentioned.
- Ideally, we want to devise a resolution scheme that produces the most favorable outcomes for natural conflicts but is resilient against adversary-induced conflicts. 
    
#### Starting a New Community Epoch 
- "Starting a New Epoch for a Community"?



When a community admin initiates a community-key "rekey event", the newly generated community key is securely and individually
"sent" to each community member via the community's public key transfer channel. The new community key is encrypted using each member's public key.
When a pnode is processing an entry that it does not have a community key for, it will check the community's public key channel
for an entry for the current client's public key, it will send the client the encrypted community key.  The client uses its SKI
to decrypt the payload into the new community key.  This key is added to the user's SKI keychain and is sent back to pnode.

 - a secure token that would be transferred to **m** via a secure channel (or in person).  This token, when opened, would allow a new `MemberEpoch` to be accepted for **m**, allowing **m** to resume normal access to **𝓛<sub>C</sub>**.
     In effect, all subsequent transactions on **𝓛<sub>C</sub>** will be unreadable to any holder of the compromised keyring is not is possession of any key that would gain them access to the newly issued community key or **m** newly issued keys.  **m** would regain

#### Issuing a New Private Channel Key
#### Starting a New Channel Epoch 
 

---

## Proof of Requirements & Claims

_Each item here corresponds to each item in the [Specifications & Requirements](#Specifications-&-Requirements) section_.


#### Proof of Signal Opacity

- Given that each `EntryCrypt` of **C** residing within transactions stored on **𝓛<sub>C</sub>** and considered to be "in the clear", what information is being made available or is discernible to an actors who are _not_ members of **C**?
- An actor _not_ a member of **C** by definition does not possess the community keyring, **[]K<sub>C</sub>**, containing the latest community keys.  Thus, the _only_ information available to actors outside of **C** is the `UUID` of the community key used to encrypt a given `EntryCrypt` stored on **𝓛<sub>C</sub>**. This implies:
    - Only members of **C** effectively have read-access to **C**'s content.
    - Information opacity is maximized since all other information resides within `HeaderCrypt` or `ContentCrypt`, _with the exception that_  adversaries snooping **𝓛<sub>C</sub>** could discern _when_ a new community security epoch began (by noting the appearance of new `UUID`).  However, this is weak information since such an event could correspond to any number of circumstances.
    - If actor **a** is formerly a member of **C** (or gained access to a member's keys), then **a**'s access is limited to read-access up to until the time when a new community security epoch was initiated.   In order for **a** to receive the latest community key, **a** must possess the _latest_ private key of a member currently in **C** (see [Starting a New Community Epoch](#Starting-a-New-Community-Epoch)). 
        - In the case that **a**'s copy of the keys matches the current **C** security epoch, this represents the members of **C** are _unaware_ of the security breach (otherwise a member would have initiated a [keyring halt](#keyring-halt) or at least [started a new community security epoch](#Starting-a-New-Community-Epoch)).  

#### Proof of Access Exclusivity

- _Read-Access Exclusivity_
    - Only an actor is possession of **[]K<sub>C</sub>** has the ability to read the encrypted content residing on **𝓛<sub>C</sub>**.  Also see the above section.
- _Append-Access Exclusivity_
    - Given **𝓛<sub>C</sub>**, in order for a storage transaction **txn<sub>C</sub>** to be accepted by **𝓛<sub>C</sub>**, by definition it must:
        - contain a valid signature that proves the data and author borne by **txn<sub>C</sub>** is authentic, _and_
        - specify an author that **𝓛<sub>C</sub>** recognizes as having permission to post a transaction of that size.
    - Given that each member **m** of **C** is in sole possession of their personal keyring, it follows that _only_ **m** can author and sign transactions that **𝓛<sub>C</sub>** will accept.  
    - In the case where **m**'s private keys are lost or compromised, **m** would immediately initiate a [keyring halt](#keyring-halt), leaving any actor in possession of **m**'s keys unable to post a transaction to **𝓛<sub>C</sub>**.

#### Proof of Permissions Assurance

- All "live" entries in a node's local replica ("**𝓡<sub>i</sub>**") must pass [Channel Entry Validation](#Channel-Entry-Validation).  This implies each successive state of **𝓡<sub>i</sub>** is, exclusively, a valid mutation of its previous state.  
- However, transactions arriving from **𝓛<sub>C</sub>** ("entries") will naturally arrive somewhat out of order — or they could be intentionally modified, reordered, or withheld by an adversary.   
- First, we rule out the corruption/alteration of entries since any entry with an invalid signature is immediately and permanently rejected.
    - The case where an adversary covertly has possession of a member's private keys is addressed later on.
 - So, could the reordering, blocking, or withholding of entries from **𝓛<sub>C</sub>** ("withholding") cause **𝓡<sub>i</sub>** to pass through a state such that one of the access controls or grants established by members of **C** could be circumvented or exploited?  We consider two categories of failures:
    1. **Unauthorized key, channel, or content access**
        - These scenarios are characterized by gaining unauthorized access to a key that in turn allows access to encrypted contents on **𝓡<sub>i</sub>**.
        - Since any withholding of entries couldn't result in any _additional_  generation/grant of permissions, the remaining possibility is that withholding entries would somehow result in  **𝓡<sub>i</sub>** not mutating in a way where privileged data remains accessible.  However, this is precluded since any ACC mutation that is restrictive in nature automatically [starts a new channel security epoch](#Starting-a-New-Channel-Epoch), where _only_ members listed for access are each explicitly sent the new private channel key (using each recipient's public key).  This summarizes how member access is "removed" in an append-only system: the delisted member isn't issued the  key for the new security epoch.    
    2. **Access control violation**
        - This implies, there exists a way for member **m** (or an adversary covertly in possession of **m**'s keys) to author one or more channel entries such that one or more channel permissions can be altered in an unauthorized way or otherwise circumvented.
        - This can be expressed as an entry being validated, and thus merged, into a channel when it should instead be rejected.  How could an entry ever be merged in a channel whose ACC denies access?  [Channel Entry Validation](#Channel-Entry-Validation) ensures that entries that do not validate under their host channel's ACC will never be "live".
        - An adversary in possession of **m**'s keys could forge an entry to a community-public channel that **m** does not have write access to, but [Channel Entry Validation](#Channel-Entry-Validation) running on others' nodes would reject this entry.  
        - In cases where there is an "ambiguous conflict" (e.g. an admin grants Alice moderator access to channel 𝘾𝒉 at the same exact time a different admin grants Alice standard access to 𝘾𝒉) then deterministic [ambiguous conflict resolution](#ambiguous-conflict-resolution) occurs. 
            - Although ambiguous conflicts are rare, we assume here that an adversary would induce ambiguous conflicts in an attempt to circumvent access controls on **C**.  
            - The scope of uncertainty around an ambiguous conflict ("**ψ**") is proportional to the specific scope of the conflict (e.g. the contended status of who moderates **C**'s lost and found channel does not affect other areas of **C**).  In other words, given ambiguous conflict **ψ**, the superposition of all possible states of **𝓡** in **C** only depends on states entangled with **ψ**.
            - Given this, and that ambiguous conflicts are [deterministically resolved](#ambiguous-conflict-resolution) in a symmetrical, access-neutral) way, adversary **O** is _at most_ limited to denial of service.  Further, **O** could only do so in proportion to **O**'s level of access within **C**.  For example, if **O** only has standard member permissions in **C**, then **O** couldn't even create an entry able to be in ambiguous conflict since **O**'s sphere of access control is not even large enough to contend with another member. 
            - Given the low probability of repeated naturally occurring ambiguous conflicts, a protective watchdog service for **C** could raise an admin alert under certain conditions — or  auto-initiate a [keyring halt](#keyring-halt).

#### Proof of Membership Fluidity

- Both [adding a new member](#adding-A-New-Member) and [delisting a member](#delisting-a-member) are implemented using standard entries in **C**'s channel system entries undergo normal [channel entry validation](#Channel-Entry-Validation).
- This implies that all the properties, assurances, and security afforded by channel entry validation extend to all apsects of membership fluidity.  In other words, membership fluidity is just a specialized form of [permissions assurance](#Permissions-Assurance).

#### Proof of Strong Eventual Consistency

- For each node **n<sub>i</sub>** in **C**, it's local replica state ("**𝓡<sub>i</sub>**") at a given moment in time is dependent on:
    - The set and order of entries that have arrived from **𝓛<sub>C</sub>**
    - The set and order of entries that have been authored locally (and have then been submitted to **𝓛<sub>C</sub>**)
    - [Channel entry validation](#Channel-Entry-Validation) continuously occuring on **n<sub>i</sub>** (and presumed to be running on other nodes of **C**). 
- Natural or adversarial network conditions could effectively cause entries to and from **𝓛<sub>C</sub>** to be delayed (or withheld). However, given sufficient time and network connectivity, when _all_ of replicated entries across **𝓛<sub>C</sub>** _eventually_ arrive at **n<sub>1</sub>**...**n<sub>N</sub>**, are **𝓡<sub>1</sub>**...**𝓡<sub>N</sub>** each in an equivalent ("consistent") state?  
- In short, we start with this systems's [proof of permissions assurance](#proof-of-Permissions-Assurance) and then demonstrate that it is commutative, implying that the eventual state of **𝓡<sub>i</sub>** is _independent_ of the order of arrivial of entries from **𝓛<sub>C</sub>**.
- It should be noted that if **𝓛<sub>C</sub>** favors safety over liveness (e.g. DFINITY, Hashgraph), then there is ceiling time window for transactions to clear.  This implies there is a ceiling to the superposition of possibile states of any given **𝓡<sub>i</sub>**.  In other words, after a known time period, **𝓡<sub>i</sub>** can rule out any late-arriving etries.  


#### Proof of Practical Security Provisioning

- Initiating a [keyring halt] and [starting a New Member Epoch] speak for themsekves.


#### Proof of Independence Assurance

- Suppose a set of members of **C** decide, for whatever reason, that they are better off in their own community **C′** with an alternative pact of goverenance or leadership.  They desire **C′** to be equivalent to a **C** where at time **t<sub>C′</sub>**, the admins of **C** ("**[]a**") are demoted to standard member status and a new set of members ("**[]a′**")  are endowed with admin status.  
    - It is assumed that the members of **C′** do not have unauthorized access or the privte keys of others in **C**.
- Since **𝓛<sub>C</sub>** is append-only CRDT, each transaction is assumed to have a timestamp and identifying UUID, implying **𝓛<sub>C</sub>** is characterized as a sequence of sealed data transactions that can be paritioned at any arbitrary time index.  
- The new admins of **C′** construct the following:
    1. Create a new CRDT ("**𝓛<sub>C′</sub>**") and allocate bulk postage identically to **𝓛<sub>C</sub>**'s genesis _in addition to_ allocating bulk postage for **[]a′**
    2. Copy the parameters from **C**'s genesis _in addition to_ granting admin status for **[]a′**.
    3. Transfer entries from **𝓛<sub>C</sub>** to **𝓛<sub>C′</sub>** upto time **t<sub>C′</sub>** (omitting entries as desired)
    4. Use the credentials of **[]a′** to demote/delist **[]a** and any other desired members.
        - For each member demoted or delisted, reduce/burn their postage permissions on **𝓛<sub>C′</sub>** as appropriate.

#### Proof of Storage Portability

- Suppose **C** wishes to switch to an alternative CRDT techology.
- Using a weaker form of the steps listed in [proof of independence assurance](#proof-of-independence-assurance), **C** can coordinate a switch to a new CRDT medium almost transparently.  
- Using steps similar to the steps in the [proof of independence assurance](#proof-of-independence-assurance), the admins of **C** can coordinate a switch to a new CRDT medium almost transparently.  
- This is to say that **𝓛** is to **C** as a hard drive is to a workstation.  **C**'s "hard drive" can be replaced:
    - with the same exact model
    - with a different "brand"
    - with a different storage technology all together
- Alernatively a repo **𝓡** could be ported and run under a different processing system implementation.

     

### further



note: although TimeAuthored is used to index entries, some Lc implementations may optionally provide a time index value that converges to within
a fixed provable accuracy of when the network witnessed it sent (as it travels further into the past).  TimeConsensus (Dfinity, Hashgraph).  For a given transaction **t**, let **t<sub>t </sub>**


### Version History



| Version |   Date   | Description of Changes |
|:-------:|:--------:|------------------------|
|   0.1   | Oct 2018 | Under construction     |
|         |          |                        |
|         |          |                        |


### scrap/work area

In this operating system

 
      This is because **a**, unlike members of **C**, would not have a key needed to decrypt the newly community keys. 
       be  not possess the newly issued key  Thus, all **C** entries authored in the new community key epoch will be unreadable by **a**. 



Let **St** be an append-only p2p replicating data store, where new data blobs can be appended and subsequently retrieved (via a transaction ID). A node's particular state of **St**

Let
   , where the afflicted member's keys are regenerated (originating from a token generated from a community admin).  


8. **C**'s technology provisions for a "hard fork", where admins and members elect which fork to place themselves in.  

Let **σ<sub>C</sub>** be the average time period it takes for replicated network messages to reach 2/3 of the network's nodes.  This lets us set a reasonable upper-bound on how long permissions changes in **C** take to propagate.  If we were to wait 10 or 100 times **σ**, it would be safe to assume that any nodes able to receive a replicated message would have received it (if it was possible).  We thus express a time delay ceiling of permissions propagation as **kσ**.  Above this time, we assume there it is not beneficial to wait and hope that a newly arrived message will resolve a conflict.  We therefore must establish a deterministic set of rules to resolve all possible **CRS** conflicts.  For a network of 10,000 nodes in the internet of 2018, a reasonable value for **kσ** could be 3-12 hours.


And since a new channel security epoch entails sending each member a newly generated   This means if the entry that removes Oscar's access from the private channel is withheld, then ._ he idea is that if the entry that removed Oscar's access has yet to be merged into **𝓡<sub>i</sub>**, then Oscar   This case is somewhat of a trick question and reveals the nature of this operating system: "private channels" are really just a matter of whom has been securely sent the keys.  Hence, in this system, any time an ACC is mutated in the _more restrictive_ direction,  o read all   Hence,    _provided that an ACC mutation also initiates a new channel security epoch_.  This means that 
        enters a state where  **Trudy**  How could an absence of transactions ("entries") from **𝓛<sub>C</sub>** result in 




A community KeyID identifies a specific shared "community-global" symmetric key.
When a PLAN client starts a session with a pnode, the client sends the pnode her community-public keys.
PDIEntryCrypt.CommunityKeyID specifies which community key was used to encrypt PDIEntryCrypt.Header.
If/when an admin of a community issues a new community key,  each member is securely sent this new key via
the community key channel (where is key is asymmetrically sent to each member still "in" the community. 


/*



// A channel access control list (PDIEntry.accessCtrlRef)
//     - Effectively allows a composite user and group access control mapping be built (in effect specifying users and groups that have read, write, ownership permission).
//     - Maps to a keyring entry in each user's SKI containing the corresponding master key to encrypt/decrypt channel entries when that ACL was in effect
//     - Any community user can be...
//          ...issued the channel msg master key (read access)
//              - Entries contain the user's pubkey and their "verify" pubkey (allowing signatures to be authenticated)
//              - These users are issued new master keys if/when a channel moves to newly generated access control list
//          ...placed on the channel's write list (write access)
//              - Although a user could hack their client so that they're on this write list, other nodes will not have this alteration and will reject the entry.
//          ...placed on a ban list.  Similar to the a write access hack, a banned user's entry will be rejected by other swarm nodes.
//              - This allows a channel to be offer community-public write access, except for explicitly named user or group id.



*/




// Every Channel keeps the following files:
//    a) channel data tome (unstructured binary file)
//        - the data body of incoming channel entries is first appended to this file
//        - read+append access to this file is used to optimize performance and caching (since data is never altered, only appended)
//    b) channel entry index (sqlite db)
//        - for each channel entry: timestamp_secs (int64, ascending-indexed),  entry hashname (TINYTEXT), tome_file_pos, tome_entry_len
//    c) list of the access control list history and when each one went into effect -- so it knows what to reject
//        - when a user is "added" to the channel, the owner must grant master key acces for each rev of the control list into the past (or as far as the owner wants to go)




https://github.com/protocol/research-RFPs/blob/master/RFPs/rfp-4-CRDT-ACL.md


https://github.com/protocol/research-RFPs/blob/master/RFPs/rfp-5-optimized-CmRDT.md

https://github.com/protocol/research/blob/master/README.md

https://github.com/protocol/research-RFPs/blob/master/RFP-application-instructions.md

https://github.com/ipfs/research-CRDT/tree/master/research

https://github.com/ipfs/research-CRDT

https://github.com/protocol/research/issues/8


https://github.com/protocol/research-RFPs/blob/master/RFP-application-instructions.md

