 # Proof of Correctness for PLAN

```
         P urposeful
         L ogistics
         A rchitecture
P  L  A  N etwork
```

## UNDER CONSTRUCTION

Please note that this document is currently **under construction** and is incomplete.  Rough draft is expected by November 1st, 2018.



## What is this?

In computer science, a "proof of [correctness](https://en.wikipedia.org/wiki/Correctness_(computer_science))" refers to a formal walk-though and demonstration that a proposed method and/or design rigorously satisfies a given set of specifications or claims.  The intention is to remove _all doubt_ that there exists a set of conditions such that the proposed method would _not_ meet all the specifications.

Below, we express a [scenario](#scenario), list a [set of specifications](#Specifications-&-Requirements), and propose [a system of operation](#Proposed-System-of-Operation) intended to address the scenario and specifications.  We then proceed to demonstrate [correctness for each specification](#Proof-of-Requirements-&-Claims), citing how the system and its prescribed operation satisfies that specification.  

Please note that the data structures listed below are intended to convey understanding and model correctness more than they are intended to be performant.  [go-plan](https://github.com/plan-tools/go-plan) is intended to be the latter.

---


# Scenario

A founding set of community organizers ("admins") wish to form **C**, a secure distributed storage network comprised of computers with varying capabilities, each running a common peer-to-peer software daemon ("node"). **C** is characterized by a set of individual members for any given point in time, with one or more members charged with administering member status, member permissions, and community-global rules/policies.  

On their nodes, the members of **C** agree to employ **𝓛**, an _append-only_ [CRDT](https://en.wikipedia.org/wiki/Conflict-free_replicated_data_type).  Data entries appended to **𝓛** ("transactions") are characterized by an arbitrary payload buffer, a signing public key, and a signature authenticating the transaction.  Transactions on any given **𝓛** are considered to be "in the clear" (i.e. neither "wire" privacy _nor_ storage privacy is assumed).

Let **𝓛<sub>C</sub>** be a CRDT whose genesis is under exclusive control of the admins of **C**.  **𝓛<sub>C</sub>** is assumed to either contain (or have access to) a verification system such that a transaction submitted to **𝓛<sub>C</sub>** is acceptable _only if_ the transaction's author (signer) has explicit _𝓛-append permission_ ("postage").  At first this may appear to be a strong requirement, but it reflects the _transference_ of security liability of the key(s) specified during the genesis of **𝓛<sub>C</sub>** to an _external_ set of authorities.


For example, a customized "private distro" of the [Ethereum](https://en.wikipedia.org/wiki/Ethereum) blockchain ("**⧫**") could be used to implement **𝓛** since:
- The admins of **C**, on creating **⧫<sub>C</sub>**, would issue themselves some large bulk amount _C-Ether_ (postage)
- The admins of **C** would periodically distribute portions of _C-Ether_ to members of **C** (a postage quota).  
- On **C**'s nodes, **⧫<sub>C</sub>**:
    - Large payload buffers would be split into 32k segments (Ethereum's transaction size limit) and _then_ committed.
    - Any transaction that does not "burn" an amount of postage commensurate with the byte size of the payload would be dropped/rejected.
    - Any transaction that attempts to transfer postage from a non-designated identities would be dropped/rejected.

For context, consider watching the distinguished [George Glider](https://en.wikipedia.org/wiki/George_Gilder) in this [video clip](https://www.youtube.com/watch?v=cidZRD3NzHg&t=1214s) speak about blockchain as an empowering distributed security and information technology.

---

## On Digital Security

We acknowledge that even the most advanced and secure systems are vulnerable to private key loss or theft, socially engineered deception, and physical coercion.  That is, an adversary in possession of another's private keys without their knowledge, or an adversary manipulating or coercing others is difficult (or impossible) to prevent.  Biometric authentication systems can mitigate _some_ of these threats, but they also introduce additional surfaces that could be exploited (e.g. spoofing a biometric device or exploiting an engineering oversight).

Security frameworks often don't analyze or provision for the loss of private keys since the implications are typically catastrophic, effectively making the issue someone else's intractable problem. Any system lacking such analysis and provisioning can only be considered incomplete for every-day use. The system of operation discussed here features swift countermeasures and recovery _once it becomes known_ that private keys have been compromised (or suspect activity has been witnessed). 

---

## On Network Connectivity

In any system, replicated data transactions and messages take non-trivial periods of time to traverse and propagate across the network.  Also, any number of nodes could be offline for indefinite periods of time. 

No assumptions are made about network connectivity or reachability in this proof, and propagation times are expressed as "**Δ<sub>C</sub>**":
- Let **Δ<sub>C</sub>** be the time period needed for there to be at least a 99.9% chance that all _reachable_ nodes in **C** have received a given replicated transaction over **𝓛<sub>C</sub>**.
- For example, given a swarm of reachable nodes on a WAN, **Δ<sub>C</sub>** is in the neighborhood of 1-10 minutes, depending on how **𝓛<sub>C</sub>** implements transaction replication (even swarms larger than 10<sup>7</sup>).

Like the way an operating system is _only_ as swift as its host storage system, the latency and liveness of the system presented below is solely dependent on **𝓛**.  This means that the tradeoffs  **𝓛<sub>C</sub>** makes, in terms of connectivity, safety, and liveness, determine **C**'s overall network properties and behavior. 

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
- For each node **n<sub>i</sub>** in **C**, it's local replica state ("**𝓡<sub>i</sub>**"), converges to a stable/monotonic state as **𝓛<sub>C</sub>** message traffic eventually "catches up", for any set of network traffic delivery conditions (natural or adversarial). That is, **𝓡<sub>1</sub>**...**𝓡<sub>N</sub>** mutate such that strong eventual consistency ("SEC") is guaranteed.  

#### Practical Security Provisioning
- If/When it is discovered that a member's private keys are known to be either lost or possibly comprised, a [member halt](#member-halt) can be immediately initiated such that any actor in possession of said keys will have no further read or write access to **C**.
- Actors that can initiate a member halt include:
   - the afflicted member, _or_
   - a member peer (depending on community-global settings), _or even_
   - an automated watchdog system on **C** (responding to abnormal or malicious activity)
- Following a member halt, the afflicted member's security state enters new "epoch" and incurs no additional security liability.  That is, there are no potential "gotchas" sometime down the road if an adversary gains access to previously compromised keys.

#### Independence Assurance
- In the event that:
    - an adversary gains access to admin/root private keys and hijacks **C**, _or_
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

- The system proposed embraces a multi-tier security model, where each community member possess a community-common keyring in addition to their personal keyring.  In effect, this places the entire system's infrastructure and transaction traffic inside a cryptographic "city wall".
- The system's data model is IRC-inspired in that community data entries are written sequentially to channels within a virtual channel addressing space.  However, instead of channel entries just being rebroadcast to other connected clients (as on an IRC server), entries _persist_ as replicated transactions across **𝓛<sub>C</sub>**.  
- When a channel is created, it is assigned a protocol descriptor string, specifying the _kind_ of entries that are expected to appear that channel and _how_ UI clients should interpret them (functionally comparible to MIME types).  This, plus the ability for _any_ channel entry to include arbitrary HTTP-style headers, affords viusally-oriented client interfaces rich and wide-open possibilities.
- Also inspired from IRC, each channel has its own permissions settings. Every channel is controlled by a access control channel ("ACC"), a channel that conforms to a protocol explicitly designed to specify channel permissions. Like other channels, each ACC designates a parent ACC, and so on, all the way up to **C**'s root-level ACC.  
- Member, channel, and community security and key distribution uses "epochs" to demarcate security events, in effect furnishing [permissions assurance](#permissions-assurance).
- In a flow known as [channel entry validation](#channel-entry-validation), each community node (**n<sub>i</sub>**) iteratively mutates its local replica (**𝓡<sub>i</sub>**) by attempting to merge newly arriving entries from **𝓛<sub>C</sub>** into **𝓡<sub>i</sub>**.  During validation, if **𝓡<sub>i</sub>** is not yet in a state to fully validate an incoming entry **e**,, then **e** is deferred for later processing.
- In effect, the system presented here forms a secure and compartmentalized core outside **C**'s channel data space, like how a traditional OS carefully maintains internal pipelines and hierarchies of operations and permissions to serve and protect user processes.


## System Security

- Let `UUID` represent a constant-length independently generated identifier that ensures no reasonable chance of peer collision. Although it is difficult to express [collision odds](http://preshing.com/20110504/hash-collision-probabilities/) in meaningful human terms (even for "modest" probability spaces such as 1 in 2<sup>160</sup>), 20 to 32 pseudo-randomly generated bytes is [more than sufficient](hash-collision-odds.py).  
- Each member **m** in **C** securely maintains custody of two "keyrings":
   1. **[]K<sub>m</sub>**: **m**'s _personal keyring_, used to:
       - decrypt/encrypt information "sent" to/from **m**, _and_
       - create signatures that authenticate all information authored by **m**.
   2. **[]K<sub>C</sub>**: the _community keyring_, used to protect all "community public" data.
       - Each entry authored by **m** is encrypted by **m**'s local client using the latest community encryption key on **[]K<sub>C</sub>**.
        - That is, **[]K<sub>C</sub>** encrypts/decrypts `EntryCrypt` traffic to/from **𝓛<sub>C</sub>** and **𝓡<sub>i</sub>** 
        - Newly [issued community keys](#Issuing-a-New-Community-Epoch) are securely distributed to members via the [community epoch channel](#Community-Epoch-Channel).
- As **m** accesses **C**, it is presumed  that **m**'s local client has access to these keyrings (though they can be implemented in ways that further compartmentalize security, such as using a hardware dongle or a key server). 



## Channel Overview
Channels are intended to be used for any purpose and serve members as containers for persistent [channel entries](#channel-entries) (through channel "drivers" running on member clients).  The system itself collectively uses specialized "reserved" channels to carry out critical member and community security controls.  

1. **Reserved channels** are specialized channels used by the system intenrally to carry out critical security controls. 
    - Reserved channels specify root-level information and permissions, namely admin and member records and community key distribution. 
    - These channels are special in that entries must meet additional security/signing requirements and used internally for explicit purposes.  
    - Because reserved channels have their own strict access control behavior, they are the _only_ channels that don't solely rely on ACCs for access control.
    - The number, purpose, and use of these channels can be expanded to meet future needs. 
2. **General purpose channels** are the principal purpose of the entire system.
    - Members create channels of various types (`.ChannelProtocol`), directing client UIs to consistently interpret and present entries as appropriate. 
    - Every channel specifies a governing access control channel ("parent ACC").  A channel's parent ACC effectively specifies a permission level for any given member `UUID`, allowing each node in **C** to carry out [channel entry validation](#channel-entry-validation).
    - General purpose channels can either be:
        - **community-public**, where channel entry content is encrypted with a community key, _or_
        - **private**, where entry content is encrypted with the specified by **e<sub>hdr</sub>**`.ContentKeyID`.  
            - Key mechanics for private channels are similar to [starting a new community epoch](#issuing-a-new-Community-Epoch), except the channel owner updating the `ChannelEpoch` performs key generation and distribution.  
            - Only members that have at least read-access are "sent" the keys needed in order to decrypt private channel entries.
                - Even community admins _do not_ have the authority or means to gain access to a private channel's key.   
                - This ensures that _only the members that have been explicitly given access_ are the ones who could possibly have access to the private channel's key.
3. **Access Control Channels** are specialized channels used to express permissions for all other channels, including other ACCs.
    - An ACC can be regarded as an access authority that specifies:
        - channel permissions for a given member `UUID`, _and_
        - default permissions for members not otherwise specified
    - Like general purpose channels, each ACC must designate a parent ACC, and so on, all the way up to the _reserved_ [root ACC](#Root-Access-Control-Channel).
    
        

### Reserved Channels


#### Root Access Control Channel
- This is **C**'s root access channel, effectively specifying which members are admins.
- All other channels, including channels that are access control channels (channels purposed to specify permissions
- Automated machinery in **C** could optionally be geared to use smart contracts on **𝓛<sub>C</sub>** to add entries to this channel.
    - e.g. a majority vote of admins could be required in order to add a new admin to the root access channel. 
        

#### Member Epoch Channel
- This is a special channel where members post revisions to their published member "epoch" record.  
    - A `MemberEpoch` contains essential information about a specific member, such as their most recently published public keys and their "home" channel `UUID`
        ```
        // MemberEpoch contains a member's community-public info
        type MemberEpoch struct {
            MemberID          UUID
            EpochInfo         EpochInfo
            PubSigningKey     []byte
            PubEncryptKey     []byte
            HomeChannel       UUID
            ExInfo            plan.Block
        }
        ```
- Each entry is this channel embeds a `MemberEpoch`, **𝓔**, and is only considered valid if:
    - the member who signed the entry is either the `MemberID` that appears in **𝓔** or an authorized member delegated to do so, _and_
    - the predecessor ("parent") epoch (**𝓔**`.ParentEpochID`) is evaluated to be eligible to be succeeded.
- Since a `MemberEpoch` specifies a member's public keys, each node in **C** maintains a database from the entries in this channel to:
    - authenticate signatures on each `EntryCrypt`
    - encrypt entry content exclusively for a given member (e.g. key exchange)
- Only a community admin (or certified delegate) is permitted to post a `MemberEpoch` for members _other than themselves_. This provides the means for:
    - [adding new members](#Adding-A-New-Member) to **C**,
    - [delisting members](#Delisting-A-Member) from **C**, _and_
    - restoring a member's access to **C** following a [member halt](#member-halt).
- When a [member halt](#member-halt) has been issued for **m**, an special `MemberEpoch` entry is posted to this channel.
    - Once this entry is live in **𝓡<sub>i</sub>**'s member epoch channel, all subsequent entries with **m**'s signature are deferred during [channel entry validation](#Channel-Entry-Validation).
    - When the cause for concern is addresssed, a community authority would [issue a new member epoch](#Issuing-a-New-member-Epoch) for **m**.

#### Community Epoch Channel
- This channel is where a community admin (or authorized agent) posts an entry that, in effect, replaces the current community key with a newly issued symmetric key. 
- This channel contains a succession of entries that embed:
    - an `EpochInfo` containing parameters associated with the new community epoch, _and_
    - the newly generated community key _for each_ member **m** in **C**, encrypted using **m**'s public latest encryption key published in the [member epoch channel](#Member-Epoch-Channel).

using asymmetric encryption (the community admin that issues a new community key separately "sends" the key to each member in **C**'s member registry channel, encrypting the new key with the recipient members's latest public key, which is also available in the member registry channel)



## Channel Entries

- Each transaction residing in **𝓛<sub>C</sub>** contains a serialization of an `EntryCrypt`:
    ```
    type EntryCrypt struct {
        CommunityKeyID    UUID     // The community key used to encrypt .HeaderCrypt
        HeaderCrypt       []byte   // An EntryHeader, encrypted with .CommunityKeyID
        ContentCrypt      []byte   // Channel content, encrypted with EntryHeader.ContentKeyID
        Sig               []byte   // Authenticates this entry; signed by EntryHeader.AuthorMemberID
    }
    ```
- Given entry **e** arriving from **𝓛<sub>C</sub>**, **e**`.HeaderCrypt` is decrypted into an `EntryHeader` ("**e<sub>hdr</sub>**") using **[]K<sub>C</sub>** :
    ```
    type EntryHeader struct {
        EntryOp           int32    // Entry opcode. Typically, POST_CONTENT
        TimeAuthored      int64    // When this header was sealed/signed
        ChannelID         UUID     // Channel that this entry is posted to (or operates on)
        ChannelEpochID    UUID     // Epoch of the channel in effect when entry was authored
        AuthorMemberID    UUID     // Creator of this entry (and signer of EntryCrypt.Sig)
        AuthorMemberEpoch UUID     // Epoch of the author's identity when entry was authored
        ContentKeyID      UUID     // Identifies the key used to encrypt EntryCrypt.ContentCrypt
    }
    ```
- Every entry specifies a destination `ChannelID` within **C**'s channel space to be merged into. 
- During [channel entry validation](#Channel-Entry-Validation) on each community node, newly arriving entries from **𝓛<sub>C</sub>** are validated and merged into the node's locally stored `CommunityRepo` ("**𝓡<sub>i</sub>**") 
- **𝓡<sub>i</sub>** consists of:
    - a datastore for each channel `UUID` that makes an appearance in **C** 
    - bookkeeping needed to resume sessions with **𝓛<sub>C</sub>**
    - a queue of entries to be merged in accordance with [channel entry validation](#Channel-Entry-Validation).
    - infrastructure for "deferred" entries to be retried periodically
    ```
    // CommunityRepo is a node's replica/repo/𝓡i
    type CommunityRepo struct {
        ChannelsByID      map[UUID]ChannelStore
    }

    // ChannelStore stores entries for a given channel and provides rapid access to them
    type ChannelStore struct {
        ChannelID         UUID
        EpochHistory      []ChannelEpoch  // Record of all past channel epochs
        EntryTable        []EntryIndex    // Entry info indexed by TimeAuthored and hashname
        ContentTome       ContentTome     // Entry content store
    }

    // EntryIndex packages the the essential parts of an entry, plus status information.
    type EntryIndex struct {
        EntryHeader      EntryHeader
        EntryStatus      EntryStatus      // Status of entry (e.g. LIVE, DEFERRED)
        ContentPos       uint64           // Byte offset into ..ContentTome
        ContentLen       uint32           // SByte length at .ContentPos in ..ContentTome
    }
    ```
- The epoch mechanism is how access controls can arise in an append-only storage environment.  When the owner of a channel posts a new `ChannelEpoch` to that channel, is to assign a parent ACC for a given 

```
// Specifies general epoch parameters and info
type EpochInfo struct {
    TimeStarted       timestamp
    TimeClosed        timestamp
    EpochID           UUID
    ParentEpochID     UUID            // 0 if this is the first epoch.
    TransitionSecs    int             // Epoch transition params, etc
    ...
}

// ChannelEpoch represents a "rev" of a given channel's security properties.
type ChannelEpoch struct {
    EpochInfo         EpochInfo
    ChannelProtocol   string          // If access control channel: "/chtype/ACC", else: "/chtype/client/*"
    AccessChannelID   UUID            // This is channel's parent ACC; cannot form circuit
}

```



## Standard Procedures

#### Member Halt
- Given: member **m** (or their private keyring) is potentially under the control or influence of an adversary.
- A "member halt" refers to an automated sequence of actions performed on **m**'s behalf once it's believed that their personal keyring ("**[]K<sub>m</sub>**") is under the influence of another.  
- The conditions/requisites needed in order to initiate a member halt on others' behalf can be arbitrarily based on security needs and situational circumstances.  
- A member halt for **m** could be inititated by:
    - **m**, delivers a message under address to a trusted peer. duress signal?
    - **m**, upon discovering that another actor has gained access to **[]K<sub>m</sub>**, _or_
    - a community admin (or automated agent), noticing damning or malicious activity originating from the holder of **[]K<sub>m</sub>**, _or_
    - a peer of **m** (previously designated by **m**), who is personally contacted by **m** and asked to do so (in a situation where **m** does not have connectivity to **𝓛<sub>C</sub>**)
- When a member halt is initiated:
    1. A special entry is posted to the [member epoch channel](#member-epoch-channel), signaling the nodes in **C** to defer all further entries signed by **[]K<sub>m</sub>**.  
        - In effect, this halts any actor in possession of **[]K<sub>m</sub>** from posting _any_ entries in _any_ channel on **C**.
        - The [member epoch channel](#Member-Epoch-Channel) allows a grace period for older (predecessor) member signining keys to be used.  This provisions against an adversary in possession of **[]K<sub>m</sub>** from "locking out" **m** by [issuing a new member epoch](#Issuing-a-New-Member-Epoch).
    2. A special transaction is submitted to **𝓛<sub>C</sub>**, immediately "burning" the ability of **m** (or any actor in possession of **[]K<sub>m</sub>**) to post transactions.
        - As this propagates across **𝓛<sub>C</sub>**, subsequent transactions signed by **[]K<sub>m</sub>** will be rejected because post permission on **𝓛<sub>C</sub>** will no longer exist for **[]K<sub>m</sub>**.
        - This removes an adversary's ability to vandalize **𝓛<sub>C</sub>** by filling it with junk data.   
        - For example, for **⧫<sub>C</sub>**, the transaction would send all **m**'s _C-Ether_ to address `x0`.
    3. An admin, automated agent, or delegated member(s) would [issue a new community epoch](#issuing-a-new-Community-Epoch) for **C**.
        - Since newly issued community keys _aren't_ set to halted members, anyone in possession of **[]K<sub>m</sub>** would lose all further read access to **𝓛<sub>C</sub>**.



#### Member Halt Recovery
- Given: a [member halt](#member-halt) was issued for **m**
- Some time later, admin(s) or delegated members can review the situation:
    - When appropriate, **m** access is restored via a simplified variation of [adding a new member](#Adding-A-New-Member).
    - In the case that an adversary in possession of **[]K<sub>m</sub>** transfers their postage (their privileges on **𝓛<sub>C</sub>**) to another identity _before_ a member halt is posted for **m**, entries using postage from the illicit postage could be identified and rejected.
    - In the case that an a adversary in possession of **[]K<sub>m</sub>** [issued a new member epoch](#issuing-a-new-Member-Epoch) (impersonating **m**), then an admin in communication with **m** would issue new entries that rescind the earlier entries as appropriate.  As normal [channel entry validation](#Channel-Entry-Validation) proceeds, this will automatically result in any dependent (adversary-authored) entries to be removed from "live" status.


#### Issuing a New Member Epoch

- Given: member **m** wishes to replace their currently published `MemberEpoch` with a new revision:
    - **m** generates new encryption and signing key pairs and places the private keys into their personal keyring, **[]K<sub>m</sub>**.
    - **m** creates an newly updated `MemberEpoch`, **𝓔′**, and places the newly generated public keys into **𝓔′**.
    - **m** packages **𝓔′** into a new entry ("**e<sub>𝓔′</sub>**"), signs it, and posts it to **C**'s [Member Epoch Channel](#Member-Epoch-Channel).
    - As **e<sub>𝓔′</sub>** propagates across **𝓛<sub>C</sub>** (and goes live on **n<sub>i</sub>**):
        - [Channel Entry Validation](#Channel-Entry-Validation) requires that entries by **m** must use the most recently published signing key.
        - Members posting entry content to **m** securely use **m**'s latest public encryption key.
- If a [member halt](#member-halt) has been ordered on **m**, then a community admin (or delegate) intervention is required in order for **m** 


#### Issuing a New Community Epoch
- Given: an admin, delegated member, or an automated agent wants to initiate a community-key "rekey" event, also known as _starting a new community epoch_.
- The purpose of starting this new "community epoch" is so that an actor with unauthorized possession of the community keyring will no longer have access to community data.  In other words, the purpose is to deprecate the current community key and issue a successor.
- A new community epoch follows a member [member halt](#member-halt) or the [delisting of a member](#Delisting-A-member) since it's important to ensure that the current community key (and any actor in possession of it) will no longer be useful.  This is made so because once a new community key epoch is issued, all entries are expected to be encrypted with it. 
- The admin, member, or agent starting a new community epoch:
    - Generates a new symmetrical key
    - For each open/active `MemberEpoch` ("**𝓔<sub>m</sub>**") in the _Member Epoch Channel_ (i.e. for each current member of **C**)
        - Encrypt the community key using **𝓔<sub>m</sub>**`.PubEncryptKey`
        - Place the encrypted community key in a new entry and post it to **𝓔<sub>m</sub>**`.KeyInboxChannel`
- Each member's client, upon seeing a new entry in their `KeyInboxChannel`:
    - Decrypts the payload using the member's personal keyring.
    - Adds the new key to the member's community keyring.
    - Uses the community key to encrypt all subsequent entries for **C**
- Within **Δ<sub>C</sub>**, newly authored transactions are _only_ readable by the registered members of **C**.
    - An actor in possession of a halted keyring or any keys from old member epochs would be unable to decrypt the new community key.
    - If **𝓛<sub>C</sub>** favors safety, then **C** could additionally be configured to reject entries encrypted with a community key older than **Δ<sub>C</sub>** since offline nodes effectively remain in a halted state until they regain access to a critical threshold of central validators.  


#### Adding A New Member

- Given the permissions and prerequisites are met on **C** are met to bestow member status to actor **α**:
    1. A root authority of **C** generates and posts a special `MemberEpoch`, **𝓔<sub>α0</sub>**, in the [Member Epoch Channel](#Member-Epoch-Channel), containing:
        - a newly generated `MemberID` for **α**.
        - the public half of newly generated keys. 
        - any additional information useful in tracking or documentation (e.g. signatures proving that the authority to invite **α** was granted by the appropriate collective authority of **C**).
    2. Also created is token **τ**, containing:
        - a copy of **𝓔<sub>a0</sub>**
        - a copy of the community keyring, **[]K<sub>C</sub>**
        - the private half of the newly generated keys in **𝓔<sub>a0</sub>**
        - network addresses and other bootstrapping information that allows **α** to gain connectivity to **𝓛<sub>C</sub>**
        - a token that bestows its bearer postage on **𝓛<sub>C</sub>**
    3. **τ** is encrypted with a passphrase, and is passed to **α** via any non-secure means (USB device, email, file sharing)
    4. Using face-to-face communication, direct contact, or other secure means, **α** is passed the passphrase to **τ**.
    5. On a newly created "blank" node, **n<sub>α</sub>** (or an existing node of **C** in a logged-out state)
        - **α** passes **τ** to the client
        - the client prompts for the passphrase that decrypts **τ**
        - the client opens **τ**, and if applicable:
            - bootstraps **𝓛<sub>C</sub>**
            - builds **𝓡<sub>α</sub>** normally
        - Once that **𝓡<sub>α</sub>** is up to date (i.e. with **𝓔<sub>α0</sub>** live in the _Member Epoch Channel_), **α** immediately posts a successor `MemberEpoch`, just as they would when [starting a new member epoch](#issuing-a-new-Member-Epoch).  

#### Delisting A Member
- Situation: **C** or admins of **C** decide that member **m** is to be "delisted", they want to immediately strip **m**'s ability to read and write to **C**.  
    - read **C** content
    - author content in **C** 




- Entries that are malformed (e.g. an invalid signature) are permanently rejected. These rejections are cause for concern and could be logged to discern bad actor patterns.

#### Channel Entry Validation
- Given node **n<sub>i</sub>** in **C**, let **𝓡<sub>i</sub>** denote the local replica state of **𝓛<sub>C</sub>** on **n<sub>i</sub>** at a given time.
- "Channel Entry Validation" is the process of merging incoming entries from **𝓛<sub>C</sub>** into **𝓡<sub>i</sub>** such that all "live" entries and channels of **𝓡<sub>i</sub>** are compliant and are in integrity with each author and admin's intent and security/privacy expectations. 
- Entries that do not conform to channel properties or governing access controls are placed in a "deferred" state within **𝓡<sub>i</sub>** and do not go live.  A node periodically reattempts to merge deferred entries as later-arriving entries may alter **𝓡<sub>i</sub>** such that previously deferred or rejected entries now fully validate. 
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
            - if **e<sub>hdr</sub>**`.TimeAuthored` is after **𝓔<sub>auth</sub>**`.EpochInfo.TimeClosed`, then **e** is deferred.
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
    

#### Issuing a New Channel Epoch 
 
#### Key Petittioning

---

## Proof of Requirements & Claims

_Each item here corresponds to each item in the [Specifications & Requirements](#Specifications-&-Requirements) section_.


#### Proof of Signal Opacity

- Given that each `EntryCrypt` of **C** residing within transactions stored on **𝓛<sub>C</sub>** and considered to be "in the clear", what information is being made available or is discernible to an actors who are _not_ members of **C**?
- An actor _not_ a member of **C** by definition does not possess the community keyring, **[]K<sub>C</sub>**, containing the latest community keys.  Thus, the _only_ information available to actors outside of **C** is the `UUID` of the community key used to encrypt a given `EntryCrypt` stored on **𝓛<sub>C</sub>**. This implies:
    - Only members of **C** effectively have read-access to **C**'s content.
    - Information opacity is maximized since all other information resides within `HeaderCrypt` or `ContentCrypt`, _with the exception that_  adversaries snooping **𝓛<sub>C</sub>** could discern _when_ a new community security epoch began (by noting the appearance of new `UUID`).  However, this is weak information since such an event could correspond to any number of circumstances.
    - If actor **a** is formerly a member of **C** (or gained access to a member's keys), then **a**'s access is limited to read-access up to until the time when a new community security epoch was initiated.   In order for **a** to receive the latest community key, **a** must possess the _latest_ private key of a member currently in **C** (see [Starting a New Community Epoch](#issuing-a-new-Community-Epoch)). 
        - In the case that **a**'s copy of the keys matches the current **C** security epoch, this represents the members of **C** are _unaware_ of the security breach (otherwise a member would have initiated a [member halt](#member-halt) or at least [started a new community security epoch](#issuing-a-new-Community-Epoch)).  

#### Proof of Access Exclusivity

- _Read-Access Exclusivity_
    - Only an actor is possession of **[]K<sub>C</sub>** has the ability to read the encrypted content residing on **𝓛<sub>C</sub>**.  See [Proof of Signal Opacity](#proof-of-signal-opacity).
- _Append-Access Exclusivity_
    - Given **𝓛<sub>C</sub>**, in order for a storage transaction **txn<sub>C</sub>** to be accepted by **𝓛<sub>C</sub>**, by definition it must:
        - contain a valid signature that proves the data and author borne by **txn<sub>C</sub>** is authentic, _and_
        - specify an author that **𝓛<sub>C</sub>** recognizes as having permission to post a transaction of that size.
    - Given that each member **m** of **C** is in sole possession of their personal keyring, it follows that _only_ **m** can author and sign transactions that **𝓛<sub>C</sub>** will accept.  
    - In the case where **m**'s private keys are lost or compromised, **m** would immediately initiate a [member member halt](#member-halt), leaving any actor in possession of **m**'s keys unable to post a transaction to **𝓛<sub>C</sub>**.

#### Proof of Permissions Assurance

- All "live" entries in a node's local replica ("**𝓡<sub>i</sub>**") must pass [Channel Entry Validation](#Channel-Entry-Validation).  This implies each successive state of **𝓡<sub>i</sub>** is, exclusively, a valid mutation of its previous state.  
- However, transactions arriving from **𝓛<sub>C</sub>** ("entries") will naturally arrive somewhat out of order — or they could be intentionally modified, reordered, or withheld by an adversary.   
- First, we rule out the corruption/alteration of entries since any entry with an invalid signature is immediately and permanently rejected.
    - The case where an adversary covertly has possession of a member's private keys is addressed later on.
 - So, could the reordering, blocking, or withholding of entries from **𝓛<sub>C</sub>** ("withholding") cause **𝓡<sub>i</sub>** to pass through a state such that one of the access controls or grants established by members of **C** could be circumvented or exploited?  We consider two categories of failures:
    1. **Unauthorized key, channel, or content access**
        - These scenarios are characterized by gaining unauthorized access to a key that in turn allows access to encrypted contents on **𝓡<sub>i</sub>**.
        - Since any withholding of entries couldn't result in any _additional_  generation/grant of permissions, the remaining possibility is that withholding entries would somehow result in  **𝓡<sub>i</sub>** not mutating in a way where privileged data remains accessible.  However, this is precluded since any ACC mutation that is restrictive in nature automatically [starts a new channel security epoch](#issuing-a-new-Channel-Epoch), where _only_ members listed for access are each explicitly sent the new private channel key (using each recipient's public key).  This summarizes how member access is "removed" in an append-only system: the delisted member isn't issued the  key for the new security epoch.    
    2. **Access control violation**
        - This implies, there exists a way for member **m** (or an adversary covertly in possession of **m**'s keys) to author one or more channel entries such that one or more channel permissions can be altered in an unauthorized way or otherwise circumvented.
        - This can be expressed as an entry being validated, and thus merged, into a channel when it should instead be rejected.  How could an entry ever be merged in a channel whose ACC denies access?  [Channel Entry Validation](#Channel-Entry-Validation) ensures that entries that do not validate under their host channel's ACC will never be "live".
        - An adversary in possession of **m**'s keys could forge an entry to a community-public channel that **m** does not have write access to, but [Channel Entry Validation](#Channel-Entry-Validation) running on others' nodes would reject this entry.  
        - In cases where there is an "ambiguous conflict" (e.g. an admin grants Alice moderator access to channel 𝘾𝒉 at the same exact time a different admin grants Alice standard access to 𝘾𝒉) then deterministic [ambiguous conflict resolution](#ambiguous-conflict-resolution) occurs. 
            - Although ambiguous conflicts are rare, we assume here that an adversary would induce ambiguous conflicts in an attempt to circumvent access controls on **C**.  
            - The scope of uncertainty around an ambiguous conflict ("**ψ**") is proportional to the specific scope of the conflict (e.g. the contended status of who moderates **C**'s lost and found channel does not affect other areas of **C**).  In other words, given ambiguous conflict **ψ**, the superposition of all possible states of **𝓡** in **C** only depends on states entangled with **ψ**.
            - Given this, and that ambiguous conflicts are [deterministically resolved](#ambiguous-conflict-resolution) in a symmetrical, access-neutral) way, adversary **O** is _at most_ limited to denial of service.  Further, **O** could only do so in proportion to **O**'s level of access within **C**.  For example, if **O** only has standard member permissions in **C**, then **O** couldn't even create an entry able to be in ambiguous conflict since **O**'s sphere of access control is not even large enough to contend with another member. 
            - Given the low probability of repeated naturally occurring ambiguous conflicts, a protective watchdog service for **C** could raise an admin alert under certain conditions — or  auto-initiate a [member member halt](#member-halt).

#### Proof of Membership Fluidity

- Both [adding a new member](#adding-A-New-Member) and [delisting a member](#delisting-a-member) are implemented using standard entries in **C**'s channel system entries undergo normal [channel entry validation](#Channel-Entry-Validation).
- This implies that all the properties, assurances, and security afforded by channel entry validation extend to all aspects of membership fluidity.  In other words, membership fluidity is just a specialized form of [permissions assurance](#Permissions-Assurance).

#### Proof of Strong Eventual Consistency

- For each node **n<sub>i</sub>** in **C**, it's local replica state ("**𝓡<sub>i</sub>**") at a given moment in time is dependent on:
    - The set and order of entries that have arrived from **𝓛<sub>C</sub>**
    - The set and order of entries that have been authored locally (and have then been submitted to **𝓛<sub>C</sub>**)
    - [Channel entry validation](#Channel-Entry-Validation) continuously occurring on **n<sub>i</sub>** (and presumed to be running on other nodes of **C**). 
- Natural or adversarial network conditions could effectively cause entries to and from **𝓛<sub>C</sub>** to be delayed (or withheld). However, given sufficient time and network connectivity, when _all_ of replicated entries across **𝓛<sub>C</sub>** _eventually_ arrive at **n<sub>1</sub>**...**n<sub>N</sub>**, are **𝓡<sub>1</sub>**...**𝓡<sub>N</sub>** each in an equivalent ("consistent") state?  
- In short, we start with this systems's [proof of permissions assurance](#proof-of-Permissions-Assurance) and then demonstrate that it is commutative, implying that the eventual state of **𝓡<sub>i</sub>** is _independent_ of the order of arrival of entries from **𝓛<sub>C</sub>**.
- It should be noted that if **𝓛<sub>C</sub>** favors safety over liveness (e.g. DFINITY, Hashgraph), then there is ceiling time window for transactions to clear.  This implies there is a ceiling to the superposition of possible states of any given **𝓡<sub>i</sub>**.  In other words, after a known time period, **𝓡<sub>i</sub>** can rule out any late-arriving entries.  


#### Proof of Practical Security Provisioning

- Given member **m** in **C**, we wish to show that this system provisions for even the worst security scenarios: 
    1. Scenario: **m** loses their private keyring ("**[]K<sub>lost</sub>**")
        - A community admin (or delegated member) would use a procedure similar to [adding a new member](#Adding-A-New-Member), resulting in a successor `MemberEpoch` to be issued for **m**.
        - Even if an adversary were to recover _and_ extract keys from a locked **[]K<sub>lost</sub>**, they would, at most, have read-access up to when the new `MemberEpoch` was published.
        - Although **m** would importantly be able to retain and resume their identity within **C**, **m** would be unable to decrypt some entries from the past (since **m**'s new keyring would lack the keys).
        - Fortunately, for each private channel **𝘾𝒉<sub>p</sub>** that **m** had belonged to, **m** would be able to regain access if _at least_ one other member had _at least_ read-access to **𝘾𝒉<sub>p</sub>** (since that would **m** could be petition for the channel's keyring). 
        - If **m** every recovers **[]K<sub>lost</sub>**, access to past data would be restored with no additional action. 
    2. Scenario: an adversary ("**O**") gains access to **m**'s private keyrings ("**[]K<sub>m</sub>**") through deception, coercion, or covert access to **m**'s client device.
        - **O** would naturally be able to:
            - read community-public data on **C**
            - author entries impersonating **m**
            - read content intended to be private for **m**
        - When **m**, a peer of **m**, an admin, or an automated notices something is amiss, they would initiate a [member halt](#member-halt) on **m**, resulting in:
            - **O** losing append/post access to **C** (twofold: no postage _and_ **m**'s `MemberEpoch` suspended), _and_
            - **O** losing further read access to **𝓛<sub>C</sub>** once a new community epoch is issued.
        - In the case that **O** [issues a new member epoch](#issuing-a-new-Member-Epoch) (as **m**) _before_ a member halt is issued:
            - **m** would _still_ be able to issue a member halt (see [member halt](#member-halt)), _and_
            - an admin of **C**, in communication with **m**, would later rescind any entries in the [member epoch channel](#member-epoch-channel) not authored by **m**.
    3. Scenario: admin ("**O**") on **C** covertly wishes to snoop on **m**.
        - At no point would **O** ever have access to **[]K<sub>m</sub>** since it never leaves **m**'s local client space (in any form).  This implies that **O** has _no_ abilty to gain access to content encrypted for **m** _or_  the keys to any private channels that **m** has access to.  
        - In the event an admin posts a new `MemberEpoch` for **m** without permission, **m** would immediately be aware since **m**'s client would see the epoch issued (but not have the keys).   Note that hijacking another's identity as in this case would not allow the perpetrator to gain access to any of **m**'s private data since only **m** has possession of **[]K<sub>m</sub>**.
        Note that the given adversary would only have access to community public data (with **[]K<sub>C</sub>**) and **m**'s particular data

    4. Scenario: multiple adversaries infiltrate **C** 
        - Plan A: denial of service by abusing [member halt](#member-halt)
            - Since a member halt only suspends a member's access to **C**, its liabily (as a mechanism) is limited to a one-time denial of service.    
            - An adversarial member halt could be easily undone by an admin, and the offending member's integrity would immediately move under a spotlight.  
            - Limitations could be added to the [member halt procedure](#member-halt) that would guard against adversarial behavior (e.g. a member is limited to ordering one halt per day).
    

#### Proof of Independence Assurance

- Suppose a set of members of **C** decide, for whatever reason, that they are better off in their own community **C′** with an alternative pact of governance or leadership.  They desire **C′** to be equivalent to a **C** where at time **t<sub>C′</sub>**, the admins of **C** ("**[]a**") are demoted to standard member status and a new set of members ("**[]a′**")  are endowed with admin status.  
    - It is assumed that the members of **C′** do not have unauthorized access or the private keys of others in **C**.
- Since **𝓛<sub>C</sub>** is append-only CRDT, each transaction is assumed to have a timestamp and identifying UUID, implying **𝓛<sub>C</sub>** is characterized as a sequence of sealed data transactions that can be partitioned at any arbitrary time index.  
- The new admins of **C′** construct the following:
    1. Create a new CRDT ("**𝓛<sub>C′</sub>**") and allocate bulk postage identically to **𝓛<sub>C</sub>**'s genesis _in addition to_ allocating bulk postage for **[]a′**
    2. Copy the parameters from **C**'s genesis _in addition to_ granting admin status for **[]a′**.
    3. Transfer entries from **𝓛<sub>C</sub>** to **𝓛<sub>C′</sub>** up to time **t<sub>C′</sub>** (omitting entries as desired)
    4. Use the credentials of **[]a′** to demote/delist **[]a** and any other desired members.
        - For each member demoted or delisted, reduce/burn their postage permissions on **𝓛<sub>C′</sub>** as appropriate.

#### Proof of Storage Portability

- Suppose **C** wishes to switch to an alternative CRDT technology.
- Using a weaker form of the steps listed in [proof of independence assurance](#proof-of-independence-assurance), **C** can coordinate a switch to a new CRDT medium almost transparently.  
- Using steps similar to the steps in the [proof of independence assurance](#proof-of-independence-assurance), the admins of **C** can coordinate a switch to a new CRDT medium almost transparently.  
- This is to say that **𝓛** is to **C** as a hard drive is to a workstation.  **C**'s "hard drive" can be replaced:
    - with the same exact model
    - with a different "brand"
    - with a different storage technology all together
- Alternatively a repo **𝓡** could be ported and run under a different processing system implementation.

     

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
//        - when a user is "added" to the channel, the owner must grant master key access for each rev of the control list into the past (or as far as the owner wants to go)




https://github.com/protocol/research-RFPs/blob/master/RFPs/rfp-4-CRDT-ACL.md


https://github.com/protocol/research-RFPs/blob/master/RFPs/rfp-5-optimized-CmRDT.md

https://github.com/protocol/research/blob/master/README.md

https://github.com/protocol/research-RFPs/blob/master/RFP-application-instructions.md

https://github.com/ipfs/research-CRDT/tree/master/research

https://github.com/ipfs/research-CRDT

https://github.com/protocol/research/issues/8


https://github.com/protocol/research-RFPs/blob/master/RFP-application-instructions.md

