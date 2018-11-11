 # Proof of Correctness for PLAN

```
         P urposeful
         L ogistics
         A rchitecture
P  L  A  N etwork
```

## UNDER CONSTRUCTION

Please note that this document is currently **under construction** and is incomplete.  Rough draft is expected by November 9th, 2018.



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

#### Integrity Assurance
- The members of **C** are confident and can rest assured that members in positions of authority are:
    - **accountable**, in that any exercise of their authority or privileges is community-public information and cannot be concealed, _and_
    - **bound**, in that they cannot circumvent **C**'s preestablished decision-making structure.

#### Membership Fluidity
- New members can be invited to and join **C** at any time (given that **C** policies and permissions are met).
- A member can be deactivated from **C** such that they become equivalent to an actor that has never been a member of **C** (aside that deactivated members can retain their copies of **𝓡** before the community entered this new security "epoch").

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
- ...then **C** can elect to "hard fork" **𝓛<sub>C</sub>** to an earlier time state, where specified members are struck from the member registry and others are granted admin permission.

#### Storage Portability
- **C**, led by a coordinated admin effort, always has the ability to swap out CRDT technologies. 
- For example, **𝓛<sub>C</sub>** may automatically halt under suspicious network conditions or insufficient peer connectivity, but earlier in its history when it had to be more agile, **C** used a CRDT that favored "liveness" over safety).


---

# Proposed System of Operation

The members of **C** present the following system of operation...

## System Synopsis

- The system embraces a multi-tier security model, where each community member possesses a community-common keyring as well as their private keyring.  In effect, this places the entire system's infrastructure and transaction traffic inside a cryptographic "city wall".
- The system's data model is IRC-inspired in that member interaction takes the form of data entries written sequentially to channels within the a virtual channel addressing space.  However, instead of channel entries just being rebroadcast to other connected clients (as on an IRC server), entries _persist_ as transactions replicated across **𝓛<sub>C</sub>**.  
- When a channel is created, it is assigned a protocol descriptor string, specifying the _kind_ of entries that are expected to appear that channel and _how_ UI clients should interpret them (functionally comparible to MIME types).  This, plus the ability for _any_ channel entry to include arbitrary HTTP-style headers, creates many possibilities for visually-oriented client interfaces.
- Also inspired from IRC, each channel has its own permissions settings. Each channel designates an access control channel ("ACC") to be used as an oracle for channel permissions.  An ACC is a special channel type that additionally conforms to a protocol designed to specify channel permissions. Like other channels, each ACC also designates a parent ACC, and so on, all the way up to **C**'s root-level ACC.  
- Member, channel, and community security and key distribution uses "epochs" to demarcate security events, in effect furnishing [permissions assurance](#permissions-assurance).
- In a flow known as [channel entry validation](#channel-entry-validation), each community node ("**n<sub>i</sub>**") iteratively mutates its local replica ("**𝓡<sub>i</sub>**") by attempting to merge newly arriving entries from **𝓛<sub>C</sub>** into **𝓡<sub>i</sub>**.  During validation, if **𝓡<sub>i</sub>** is not yet in a state to fully validate an incoming entry **e**, then **e** is said to be "deferred" for later processing.
- This system, in effect, forms a secure and operational core outside **C**'s channel data space, comparable to how a traditional OS maintains internal pipelines and hierarchies of operations and permissions, designed to serve and protect user processes.

---

## System Security

- Let `UUID` represent a constant-length independently generated identifier that ensures no reasonable chance of peer collision. Although it is difficult to express [collision odds](http://preshing.com/20110504/hash-collision-probabilities/) in meaningful human terms (even for "modest" probability spaces such as 1 in 2<sup>160</sup>), 20 to 32 pseudo-randomly generated bytes is [more than sufficient](hash-collision-odds.py).  
- Each member **m** in **C** securely maintains custody of two "keyrings":
   1. **[]k<sub>m</sub>**: **m**'s _personal keyring_, which:
       - decrypts/encrypts information "sent" to/from **m**, _and_
       - creates signatures that authenticate information authored by **m**.
   2. **[]k<sub>C</sub>**: the _community keyring_, which ensures **C**'s "community-public" data is only readable by members of **C**.
        - Each entry authored by **m** is encrypted by **m**'s local client using the latest community key on **[]k<sub>C</sub>**.
        - That is, **[]k<sub>C</sub>** encrypts/decrypts `EntryCrypt` traffic to/from **𝓛<sub>C</sub>** and **𝓡<sub>i</sub>** 
        - Newly [issued community keys](#Issuing-a-New-Community-Epoch) are securely distributed to members via the [Community Epoch Channel](#Community-Epoch-Channel).


---

## Channel Entries

- Transactions residing in **𝓛<sub>C</sub>** are storage containers for `EntryCrypt`:
    ```
    type EntryCrypt struct {
        CommunityKeyID    UUID     // The community key used to encrypt .HeaderCrypt
        HeaderCrypt       []byte   // EntryHeader encrypted with .CommunityKeyID
        ContentCrypt      []byte   // Channel content, encrypted with EntryHeader.ContentKeyID
        Sig               []byte   // Authenticates this entry; signed by EntryHeader.AuthorMemberID
    }
    ```
- Given entry **e** arriving from **𝓛<sub>C</sub>** and access to  **[]k<sub>C</sub>**, node **n<sub>i</sub>** decrypts **e**`.HeaderCrypt` into an `EntryHeader` ("**e<sub>hdr</sub>**"):
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
- During [channel entry validation](#Channel-Entry-Validation), newly arriving entries from **𝓛<sub>C</sub>** are validated and merged into node **n<sub>i</sub>**'s locally stored `CommunityRepo` ("**𝓡<sub>i</sub>**").
- **𝓡<sub>i</sub>** consists of:
    - a datastore for each channel `UUID` that makes an appearance in **C** 
    - bookkeeping needed to resume sessions with **𝓛<sub>C</sub>**
    - a queue of entries to be merged in accordance with [channel entry validation](#Channel-Entry-Validation).
    - a mechanism for "deferred" entries to be retried periodically
    ```
    // CommunityRepo is a node's replica/repo/𝓡i
    type CommunityRepo struct {
        ChannelsByID      map[UUID]ChannelStore
    }

    // ChannelStore stores entries for a given channel and provides rapid access to them
    type ChannelStore struct {
        ChannelID         UUID
        ChannelProtocol   string          // "/chType/ACC" or "/chType/desc/<protocol-desc>"
        EpochHistory      []ChannelEpoch  // Record of all past channel epochs
        EntryTable        []EntryIndex    // Entry info indexed by TimeAuthored and hashname
        ContentTome       ContentTome     // Entry content store/db for channel
    }

    // EntryIndex packages the the essential parts of an entry, plus status information.
    type EntryIndex struct {
        EntryHeader      EntryHeader
        EntryStatus      EntryStatus      // Status of entry (e.g. LIVE, DEFERRED)
        ContentPos       uint64           // Byte offset into ..ContentTome
        ContentLen       uint32           // Byte length at .ContentPos in ..ContentTome
    }
    ```

---

## Channel Epochs

Under an append-only storage model, the mechanism that gives rise to mutable permissions and access controls is centered around `ChannelEpoch`. 
- In a procedure known as [issuing a new channel epoch](#Issuing-a-New-Channel-Epoch), an owner of channel **𝘾𝒉** posts a new revision to **𝘾𝒉**'s current `ChannelEpoch` to:
    - edit properties specific to **𝘾𝒉**, _or_
    - designate a different parent ACC for **𝘾𝒉**.
- Naturally, part of [channel entry validation](#channel-entry-validation) is to reject entries from members that lack the appropriate permissions to issue a new `ChannelEpoch` for a given channel. 
    ```
    // Specifies general epoch parameters and info
    type EpochInfo struct {
        TimeStarted       timestamp
        TimeClosed        timestamp
        EpochID           UUID
        ParentEpochID     UUID            // 0 if this is the first epoch.
        TransitionSecs    int             // How long before previous epochs "expire"
        ...                               // Other epoch transition parameters
    }

    // ChannelEpoch represents a "rev" to a channel's security properties.
    type ChannelEpoch struct {
        EpochInfo         EpochInfo
        AccessChannelID   UUID            // This is channel's parent ACC; cannot form circuit
        MemberGrants      AccessGrants    // Permissions for explicitly specified members   
        DefaultGrants     AccessGrants    // Permissions for members not otherwise specified  
    }
    ```

---

## Channels
Channels are intended as general-purpose containers for [channel entries](#channel-entries) of all forms.  This system uses channels internally for administration and permissions controls.


1. **Access Control Channels** (ACCs) are specialized channels used to express permissions for all other channels, including other ACCs.
    - An ACC serves as an access authority that specifies:
        - channel permissions for a given member `UUID`, _and_
        - default permissions for members not otherwise specified.
    - Like general purpose channels, each ACC must designate a parent ACC, and so on, all the way up to the _reserved_ [root ACC](#Root-Access-Control-Channel).
    - Multiple channels can name the _same_ ACC as their parent ACC, allowing a single ACC to conveniently manage permissions for any number of channels.
    - ACCs also are the vehicle for key distribution, where a channel owner "sends" a newly issued private channel to each member with access, using their public key.
2. **Reserved channels** are specialized channels used by the system to internally carry out community governance and member administration.
    - Reserved channels specify root-level information and permissions, namely admin and member records.
    - Entries in these channels must meet additional security/signing requirements and serve prescribed purposes.  
    - Because reserved channels have nuanced specifications, they do not solely rely on ACCs for access controls.
    - The number, purpose, and use of these channels can be expanded to meet future needs. 
3. **General purpose channels**, alas, are the system's primary service deliverable, comprising most channels in **C**.
    - When a new channel is created, the creator (and hence owner) specifies a "protocol descriptor", a string directing client UIs to consistently interpret, handle, and present channel entries in accordance with the expectations associated with the channel's protocol.  
    - Each channel also names a governing access control channel ("parent ACC").  A channel's parent ACC is charged with returning a permission level for any given member `UUID`, allowing  nodes in **C** to independently carry out [channel entry validation](#channel-entry-validation).
    - General purpose channels are either:
        - **community-public**, where channel entry content is encrypted with the latest community key, _or_
        - **private**, where entry content is encrypted with the key identified by **e<sub>hdr</sub>**`.ContentKeyID`.  
            - Key mechanics for private channels are similar to [starting a new community epoch](#issuing-a-new-Community-Epoch), except the channel owner updating the `ChannelEpoch` performs key generation and distribution.  
            - Only members that have at least read-access are "sent" the keys needed in order to decrypt private channel entries.
                - By default, community admins _do not_ have the authority/means to gain access to a private channel's key.   
                - This ensures that _only the members that have been explicitly given channel access_ could possibly have access to the channel's key.

## Reserved Channels


#### Root Access Control Channel
- This is **C**'s root access channel, effectively specifying which members are recognized as community authorities ("admins").
- All community-public channels, including ACCs, implicitly are under authority of this channel.
- When a new community is formed ("community genesis"), the initial entries this channel are auto-generated in accordance with the parameters and policies provided.
- Automated machinery in **C** can optionally be geared to use smart contracts on **𝓛<sub>C</sub>** to manage, monitor, or validate entries in this channel.
    - E.g. a majority vote of existing admins could be required in order to add a new admin to the root access channel. 
        

#### Member Epoch Channel
- This is a special channel where members post revisions to their currently published `MemberEpoch`.
    - `MemberEpoch` contains essential information about a specific member, such as their most recently published public keys and their "home" channel `UUID`
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
    - the member who signed the entry matches the `MemberID` that appears in **𝓔** (or is an authorized member delegated to do so), _and_
    - the predecessor ("parent") epoch of **𝓔** is eligible to be succeeded.
- `MemberEpoch` importantly publishes a member's public keys to the rest of the community, allowing each node in **C** to maintain a database used to:
    - authenticate signatures on each `EntryCrypt`
    - encrypt entry content exclusively for a given member (used for key distribution)
- Only a community admin (or certified delegate) is permitted to post a `MemberEpoch` for members _other than themselves_. This provides the means for:
    - [adding new members](#Adding-A-New-Member) to **C**,
    - [deactivating members](#deactivating-A-Member) from **C**, _and_
    - restoring a member's access to **C** following a [member halt](#member-halt).
- When a [member halt](#member-halt) has been issued on **m**, an special `MemberEpoch` entry is posted to this channel.
    - Once this entry is live on **𝓡<sub>i</sub>**, all subsequent entries with **m**'s signature are deferred during [channel entry validation](#Channel-Entry-Validation).
    - When the cause for concern is addressed, a community authority [issues a new member epoch](#Issuing-a-New-member-Epoch) for **m**.

#### Community Epoch Channel
- This channel is where a community admin (or authorized agent) posts an entry that, in effect, replaces the current community key with a newly issued key. 
- This channel contains a succession of entries that embed:
    - an `EpochInfo` containing parameters associated with the new community epoch, _and_
    - a newly generated symmetric key _for each_ member **m** in **C**, encrypted using **m**'s latest public key published in **C**'s [Member Epoch Channel](#Member-Epoch-Channel):
        ```
        // KeyIssue is the vessel used to securely pass a ski.KeyEntry to another member
        type KeyIssue struct {
            MemberID          UUID      // Specifies the recipient 
            MemberEpochID     UUID      // Implies which key was used to encrypt .KeyEntryCrypt
            KeyEntryCrypt     []byte    // Encrypted ski.KeyEntry
        }
        ```

---

## Standard Procedures


#### Issuing a New Member Epoch

- Given: member **m** wishes to replace their currently published `MemberEpoch` with a new revision:
    - **m** generates new encryption and signing key pairs and places the private keys into their personal keyring, **[]k<sub>m</sub>**.
    - **m** prepares a replacement `MemberEpoch`, **𝓔′**, placing the newly generated public keys into **𝓔′**.
    - **m** packages **𝓔′** into a new entry ("**e<sub>𝓔′</sub>**"), signs it, and posts it to **C**'s [member epoch channel](#Member-Epoch-Channel).
    - As **e<sub>𝓔′</sub>** propagates across **𝓛<sub>C</sub>** (and goes live on **𝓡<sub>i</sub>**):
        - [Channel entry validation](#Channel-Entry-Validation) now requires that entries authored by **m** must use the newly published signing key.
        - Other member clients intending to securely pass keys or content to **m** would use **m**'s updated public encryption key.
- If a [member halt](#member-halt) has been ordered on **m**, then admin (or community authority) intervention is required before **m** is permitted to post a new `MemberEpoch`.


#### Issuing a New Community Epoch
- Given: an admin, delegated member, or an automated agent wants to issue a new/replacement community key and deprecate the previously issued communuty key.
- The purpose of starting this new "community epoch" is so that an actor in possession of the community keyring ("**[]k<sub>C</sub>**") will no longer be able to decrypt community-public data on **C** _unless they are currently a member of **C**_.  This typically applies after a [member halt](#member-halt) or after [deactivating a member](#deactivating-A-member) since it's important that the currently active community key (and an actor in possession of it) is longer used to encrypted community traffic.  
- As the newly posted community key epoch goes live across the nodes of **C**, all new `EntryCrypt` on **𝓛<sub>C</sub>** are encrypted using it. 
- The admin or permissioned member or agent does the following:
    1. Generates a new symmetrical key to serve as the next community key ("**k<sub>C</sub>**").
    2. Prepares a new entry containing an `EpochInfo` ("**𝓔<sub>C</sub>**").
    3. For each open/active `MemberEpoch` ("**𝓔<sub>m</sub>**") in the [Member Epoch Channel](#Member-Epoch-Channel) (for each member  **m** in **C**):
        - Creates a new `KeyIssue` (intended for **m**), encrypting **k<sub>C</sub>** using **𝓔<sub>m</sub>**`.PubEncryptKey`, 
        - Appends the `KeyIssue` key to **𝓔<sub>C</sub>**'s content body.
    4. Posts **𝓔<sub>C</sub>** to the [Community Epoch Channel](#Community-Epoch-Channel).
- Member **m**'s client, upon seeing **𝓔<sub>C</sub>** go live:
    1. Searches the content body of **𝓔<sub>C</sub>** for a `KeyIssue` matching **m**'s member ID.
    2. Recovers **k<sub>C</sub>** from the `KeyIssue` using the member's private keyring.
    3. Adds **k<sub>C</sub>** to **m**'s own community keyring.
    4. Uses **k<sub>C</sub>** to encrypt all subsequent authored entries bound for **𝓛<sub>C</sub>**
- Within **Δ<sub>C</sub>**, newly authored transactions are _strictly only_ readable by the current members of **C**.
    - An actor in possession of a halted keyring or any keys past member epochs will not have any of the keys needed to extract **k<sub>C</sub>**.
    - If **𝓛<sub>C</sub>** favors safety, then **C** could additionally be configured to reject entries encrypted with a community key older than **Δ<sub>C</sub>** since offline nodes effectively remain in a halted state until they regain access to a critical threshold of central validators.  

#### Issuing a New Channel Epoch 
- Given: an owner of channel **𝘾𝒉** decides to alter permissions on **𝘾𝒉**, such as:
    - editing **𝘾𝒉**'s default access permissions to be more restrictive, _or_
    - removing access permissions for explicitly named members, _or_
    - making **𝘾𝒉** private and granting access to only specifically listed members of **C**.
- Similar to [issuing a new member epoch](#Issuing-a-New-Member-Epoch), **𝘾𝒉**'s owner posts an entry to **𝘾𝒉** intended to revise the current `ChannelEpoch`.
- If **𝘾𝒉** is private, a procedure similar to [issuing a new community epoch](#issuing-a-new-Community-Epoch) distributes **𝘾𝒉**'s latest access key to members that have at least read-only access to **𝘾𝒉**.

#### Member Halt
- Given: member **m** (or their private keyring) is potentially under the control or influence of an another.
- A "member halt" refers to an automated sequence of actions performed on **m**'s behalf once it's believed that their personal keyring ("**[]k<sub>m</sub>**") is under the influence of another.  
- The conditions/requisites needed in order to initiate a Member Halt on another's behalf can be arbitrarily based on security needs and situational circumstances.  
- A Member Halt on **m** could be initiated by:
    - **m**, upon discovering that another actor has gained access to **[]k<sub>m</sub>**, _or_
    - a peer of **m** (previously designated by **m**), upon receiving an email, phone call, text message, or signal of duress from **m**, _or_
    - a community admin or automated agent, noticing damning or malicious activity originating from a holder of **[]k<sub>m</sub>**.
- Once a Member Halt is initiated on **m**:
    1. A special entry is posted to the [Member Epoch Channel](#member-epoch-channel), signaling to all nodes in **C** to defer all further entries signed by **[]k<sub>m</sub>**.  
        - In effect, this halts any actor in possession of **[]k<sub>m</sub>** from posting _any_ entries to _any_ channel on **C**.
        - The [Member Epoch Channel](#Member-Epoch-Channel) has a grace period for older (predecessor) member keys to be used to authorize a Member Halt.  This provisions against an adversary in possession of **[]k<sub>m</sub>** from "locking out" **m** by [issuing a new member epoch](#Issuing-a-New-Member-Epoch).
    2. A special transaction is submitted to **𝓛<sub>C</sub>**, immediately "burning" the ability of **m** (or any actor in possession of **[]k<sub>m</sub>**) to post further transactions.
        - As this propagates across **𝓛<sub>C</sub>**, subsequent transactions signed by **[]k<sub>m</sub>** will be rejected because post permission on **𝓛<sub>C</sub>** will no longer exist for **[]k<sub>m</sub>**.
        - This removes an adversary's ability to vandalize **𝓛<sub>C</sub>** (e.g filling it with junk data).
        - For example, for **⧫<sub>C</sub>**, the transaction would send all **m**'s _C-Ether_ to address `x0`.
    3. An admin, automated agent, or delegated member(s) would [issue a new community epoch](#issuing-a-new-Community-Epoch) for **C**.
        - Since newly issued community keys _aren't_ posted for halted members, any agent(s) in possession of **[]k<sub>m</sub>** would lose all further read access to **𝓛<sub>C</sub>** since they would not have a key to extract the newly issued community key for **C**.



#### Member Halt Recovery
- Given: a [member halt](#member-halt) was issued on **m**.
- Some time later, admin(s) or delegated members can review the situation:
    - When appropriate, **m**'s access is restored and new keys issued using a variant of [adding a new member](#Adding-A-New-Member).
    - In the case that an adversary in possession of **[]k<sub>m</sub>** transfers their postage (their privileges on **𝓛<sub>C</sub>**) to another identity _before_ a Member Halt is issued on **m**, entries using postage from the illicit postage could be identified and rejected.
    - In the case that an a adversary in possession of **[]k<sub>m</sub>** [issued a new member epoch](#issuing-a-new-Member-Epoch) (impersonating **m**), then an admin in communication with **m** would issue new entries that rescind the earlier entries as appropriate.  As normal [channel entry validation](#Channel-Entry-Validation) proceeds, this will automatically result in any dependent (adversary-authored) entries to be removed from "live" status.



#### Adding A New Member

- Given: the permissions/prerequisites on **C** are met to bestow member status to actor **α**:
    1. A designated authority of **C** generates and posts a special `MemberEpoch`, **𝓔<sub>α0</sub>**, in the [Member Epoch Channel](#Member-Epoch-Channel), containing:
        - a newly generated `MemberID` for **α**.
        - newly generated public keys. 
        - information on **α**'s invitation, such as:
            - documentation of which authorities in **C** were connected to **α**'s invitation.
            - proof that **α**'s invitation was granted by the collective authority of **C**.
    2. Also created is token **τ**, containing:
        - a copy of **𝓔<sub>a0</sub>**, _and_
        - a copy of the community keyring, **[]k<sub>C</sub>**, _and_
        - the private half of public keys in **𝓔<sub>a0</sub>**, _and_
        - network addresses and other bootstrapping information needed in order to connect to **𝓛<sub>C</sub>**, _and_
        - a token that bestows its bearer postage on **𝓛<sub>C</sub>**.
    3. **τ** is encrypted with a passphrase, and is passed to **α** via any non-secure means (USB device, email, file sharing).
    4. Using face-to-face communication, direct contact, or other secure means, **α** is passed the passphrase to **τ**.
    5. On a newly created "blank" node, **n<sub>α</sub>** (or an existing node of **C** in a logged-out state):
        1. **α** passes **τ** to the client
        2. the client prompts for the passphrase that decrypts **τ**
        3. the client opens **τ**, and as applicable:
            - bootstraps **𝓛<sub>C</sub>**
            - builds/updates **𝓡<sub>α</sub>** normally
        4. Once that **𝓡<sub>α</sub>** is up to date (i.e. once **𝓔<sub>α0</sub>** is live in the _Member Epoch Channel_), **α** posts a successor `MemberEpoch` as they would when [starting a new member epoch](#issuing-a-new-Member-Epoch).  

#### Deactivating A Member
- Given: the admins and/or collective authority of **C** decide that member **m** is to be "deactivated", meaning that **m**'s access **C** is to be immediately rescinded.  
- The designated authority of **C** performs a procedure identical to the [Member Halt](#member-halt) procedure.  In effect:
    1. Any subsequent entries authored by **m** will be rejected, _and_
    2. **m** will be unable to post any transactions to **𝓛<sub>C</sub>**, _and_
    4. All new entries on **𝓛<sub>C</sub>** will be unreadable to **m** within **Δ<sub>C</sub>**.


#### Channel Entry Validation
- Given node **n<sub>i</sub>** in **C**, let **𝓡<sub>i</sub>** denote the local replica state of **𝓛<sub>C</sub>** on node **n<sub>i</sub>** at a given time.
- _Channel entry validation_ is the process of merging incoming entries arriving from **𝓛<sub>C</sub>** such that entries placed into "live" status (on **𝓡<sub>i</sub>**) comply and are in integrity with all relevant author and channel permissions and intent.
- Since entries can arrive at **n<sub>i</sub>** in arbitrary order from **𝓛<sub>C</sub>**, entries will arrive whose validation will depend on other entries that have not yet been processed — _on entries yet to even arrive_.
- As node **n<sub>i</sub>** processes an incoming entry **e** to be merged with **𝓡<sub>i</sub>**:
    - If **e** satisfies _all channel properties and parent ACC permissions_, then **e** is placed into "live" status.
    - Otherwise, if for whatever reason **e** cannot complete validation (or **e** depends on an unresolved [ambiguous conflict](#Ambiguous-conflict-resolution)), then **e** is placed into "deferred" status.
        - Node **n<sub>i</sub>** will periodically reattempt to validate **e** as subsequent entries mutate **𝓡<sub>i</sub>** and as any conflicts resolve.  
        - Unless **e** was crafted with malicious intent, it would be unexpected for **e** to remain indefinitely deferred.
- For each new entry **e** arriving from **𝓛<sub>C</sub>** (or is locally authored and also submitted to **𝓛<sub>C</sub>**):
    1. Authenticate **e**:
        1. **e<sub>digest</sub>** ⇐  ComputeDigest(**e**`.CommunityKeyID`,   **e**`.HeaderCrypt`,  **e**.`ContentCrypt`)
        2. **e<sub>hdr</sub>** ⇐ `EntryHeader` ⇐ Decrypt(**e**`.HeaderCrypt`,  **[]k<sub>C</sub>**.LookupKey(**e**`.CommunityKeyID`)
            - if the community key is not found, then **e** is deferred.
        3. **𝓔<sub>author</sub>** ⇐ **𝓡<sub>i</sub>**.LookupMemberEpoch(**e<sub>hdr</sub>**.`AuthorMemberID`, **e<sub>hdr</sub>**`.AuthorMemberEpoch`)
            - if **𝓔<sub>author</sub>** = `nil`, then **e** is deferred. 
            - if **e<sub>hdr</sub>**`.TimeAuthored` falls outside the scope of **𝓔<sub>author</sub>**, then **e** is deferred.
        3. **k<sub>pub</sub>** ⇐ **𝓡<sub>i</sub>**.LookupPublicKey(**e<sub>hdr</sub>**.`AuthorMemberID`, **e<sub>hdr</sub>**`.AuthorMemberEpoch`)
            - if **k<sub>pub</sub>** = `nil`, then **e** is deferred. 
        4. ValidateSig(**e<sub>digest</sub>**, **e**`.Sig`, **k<sub>pub</sub>**)
            - if **e**`.Sig` is invalid, then **e** is deferred.
    2. Validate **e** in its destination channel:
        1. **𝘾𝒉<sub>dst</sub>** ⇐ **𝓡<sub>i</sub>**.GetChannelStore(**e<sub>hdr</sub>**.`ChannelID`)
            - if **𝘾𝒉<sub>dst</sub>** = `nil`, then **e** is deferred.
        2. Check that **e** cites an agreeable `ChannelEpoch`:
            - **𝓔<sub>cited</sub>** ⇐ **𝘾𝒉<sub>dst</sub>**.LookupEpoch(**e<sub>hdr</sub>**.`ChannelEpochID`)
                - if **𝓔<sub>cited</sub>** = `nil`, then **e** is deferred.
            - if **e<sub>hdr</sub>**`.TimeAuthored` falls outside the scope of **𝓔<sub>cited</sub>**, then **e** is deferred.
            - if **𝓔<sub>cited</sub>**.CanAccept(**e<sub>hdr</sub>**), then proceed, otherwise **e** is deferred.
        3. Check that **𝘾𝒉<sub>dst</sub>**'s parent ACC permits **e**:
            - **𝘾𝒉<sub>AC</sub>** ⇐ **𝓡<sub>i</sub>**.GetChannelStore(**𝓔<sub>cited</sub>**.`AccessChannelID`)
            - **𝓅<sub>author</sub>** ⇐ **𝘾𝒉<sub>AC</sub>**.LookupPermissions(**e<sub>hdr</sub>**.`AuthorMemberID`)
            - if  **𝓅<sub>author</sub>** does not allow **e<sub>hdr</sub>**`.EntryOp`, then **e** is deferred.
        4. If **e** inserts a permissions change but does not [issue a new channel epoch](#issuing-a-New-Channel-Epoch) as required, then **e** is deferred.
        5. If **e** will introduce an ambiguous or contradictory conflict, then perform [ambiguous conflict resolution](#ambiguous-conflict-resolution). 
    3. Merge **e** into **𝓡<sub>i</sub>**:
        - **𝘾𝒉<sub>dst</sub>**.InsertEntry(**e**)
    4. Propagate the mutation of **𝘾𝒉<sub>dst</sub>** as required ("revalidation"):
        - if  **𝘾𝒉<sub>dst</sub>** is now _equally_ or _less_ restrictive, then `return` since dependencies that are live will be unaffected.
        - if  **𝘾𝒉<sub>dst</sub>** is now _more_ restrictive, then revalidate dependent channels:
            - **t<sub>rev</sub>** ⇐ **e<sub>hdr</sub>**`.TimeAuthored`
            - **[]𝘾𝒉<sub>dep</sub>** ⇐ **𝘾𝒉<sub>dst</sub>**.GetDependentChannels(**t<sub>rev</sub>**)
            - for each **𝘾𝒉<sub>j</sub>** in **[]𝘾𝒉<sub>dep</sub>**:
                - Scanning forward from **t<sub>rev</sub>** in  **𝘾𝒉<sub>j</sub>**, for each entry **e<sub>k</sub>**:
                    - [re]validate **e<sub>k</sub>** (steps 1-5 above)
                    - if **e<sub>k</sub>** is now deferred:
                        - **𝘾𝒉<sub>j</sub>**.RemoveEntry(**e<sub>k</sub>**)
                        - Defer **e<sub>k</sub>** normally
                        - Propagate the mutation of **𝘾𝒉<sub>j</sub>**
        - Although there are edge cases where change propagation could result in a cascading workload, the amount of work is generally either n/a or negligible.  This is because:
            - Most entries are content-related, not access-control related.
                - Revalidation only needs to proceed if an entry makes a channel _more_ restrictive.
                - For example, compare the number of ACL-related files stored on a conventional workstation to the _total_ number of files.
                - Only ACCs tend to have dependent channels.
            - Mutations to a channel occur close to the present time, so only O(1) of all entry history typically needs to be revalidated.
        - Revalidation can also be strategically managed, where multiple ACC mutations are scheduled such that only a single revalidation pass is needed.





---

## Proof of Requirements & Claims

_Each item here corresponds to each item in the [Specifications & Requirements](#Specifications-&-Requirements) section_.


#### Proof of Signal Opacity

- Given that (a) all community channel entries reside within transactions stored on **𝓛<sub>C</sub>**, _and_ (b) transactions are considered to be "in the clear":
    - What information is available or otherwise discernible to non-members of **C**?
- Let **α** be an actor that is _not_ a member of **C**, implying that **α** does not possess the latest community keys.  
    - ⇒ the _only_ information directly available to **α** is the `UUID` of the key used to encrypt each `EntryCrypt` stored on **𝓛<sub>C</sub>**.
        1. ⇒ information opacity is maximized in that all other information resides within an entry's `HeaderCrypt` and `ContentCrypt`.
            - Adversaries snooping **𝓛<sub>C</sub>** can only discern _when_ a new community security epoch began (by noting the appearance of a new community key `UUID`).  However, this is weak information since such an event could correspond to any number of circumstances.
        2. ⇒ _only_ members of **C** effectively have read-access to **C**'s content and member activity.
    - If **α** is a former member of **C**, then **α**'s access is limited to read-only up to when  **α** was [deactivated](#deactivating-A-Member) (when the [new community epoch was issued](#issuing-a-new-Community-Epoch) as part of deactivating a member).


#### Proof of Access Exclusivity

- _Read-Access Exclusivity_
    - Only an actor is possession of the community keyring ("**[]k<sub>C</sub>**") has the ability to read community-public content residing on **𝓛<sub>C</sub>**.  See [Proof of Signal Opacity](#proof-of-signal-opacity).
- _Write-Access Exclusivity_
    - There are _three_ layers that prevent the unauthorized mutation of **𝓛<sub>C</sub>** or a community replica/repo  ("**𝓡<sub>i</sub>**"):
        1. **𝓛<sub>C</sub> Postage**, the mechanism ensuring that **𝓛<sub>C</sub>** will only accept storage transaction **txn<sub>j</sub>** if:
            - **txn<sub>j</sub>** bears an author that **𝓛<sub>C</sub>** recognizes as having permission to post a transaction of that size, _and_
            - **txn<sub>j</sub>** bears a valid signature that proves the contents and author borne by **txn<sub>j</sub>** is authentic.
        2.  **Community Keyring Access**, referring to that _only_ community members are issued **[]k<sub>C</sub>**.  
            - So even if actor **α** is able procure postage on **𝓛<sub>C</sub>**, they must also submit an `EntryCrypt` containing an `EntryHeader` encrypted using a recent community key — otherwise **𝓡<sub>i</sub>** will reject it.
        3. **Channel Entry Validation**, referring to "deep" validation of entries arriving from **𝓛<sub>C</sub>**.  Part of this flow is verifying that:
            - the signature contained in a given `EntryCrypt` is a valid signature from the member `UUID` borne by its `EntryHeader`, _and_
            - the member is a valid/current member of **C** (based on **𝓡<sub>i</sub>**'s [Member Epoch Channel](#Member-Epoch-Channel)).
    - Given that each member **m** of **C** is in sole possession of their private keys ⇒ _only_ members of **C** can mutate **𝓛<sub>C</sub>** or **𝓡<sub>i</sub>**.
    - In the case where **m**'s private keys are possibly compromised, **m** would immediately initiate a [member halt](#member-halt), leaving any actor in possession of **m**'s keys challenged or unable to move past the above layers. 
        - For in-depth security scenario analysis, see [Proof of Practical Security Provisioning](#Proof-of-Practical-Security-Provisioning). 

#### Proof of Permissions Assurance

- In order for an entry to be "live" in a node's repo ("**𝓡<sub>i</sub>**"), it must repeatedly survive [Channel Entry Validation](#Channel-Entry-Validation).  
    - ⇒ each successive state of **𝓡<sub>i</sub>** is, exclusively, an authorized mutation from its previous state.  
- However, if an important entry is withheld from node **n<sub>i</sub>**, it is easy to imagine dependent entries piling up and **𝓡<sub>i</sub>** being at a standstill.  
- In addition to transactions arriving out of order from **𝓛<sub>C</sub>** naturally, we must consider if entries are altered, reordered, or withheld by adversaries manipulating communications signals or infrastructure.
- We can rule out corruption or alteration of entries since each `EntryCrypt` bears a signature dependent on its contents, so altered entries would be immediately rejected.
    - The case where an adversary covertly has possession of a member's private keys is discussed in [Proof of Practical Security Provisioning](#Proof-of-Practical-Security-Provisioning). 
 - So then, could the _reordering, blocking, or withholding_ ("withholding") of entries from **𝓛<sub>C</sub>** cause **𝓡<sub>i</sub>** to pass through a state such that access controls or grants established by members of **C** could be circumvented or exploited?  We separate the possibilities into two categories:
    1. **Unauthorized key, channel, or content access**
        - These scenarios are characterized by gaining unauthorized access to a privileged key that in turn allows read access to restricted content within **𝓡<sub>i</sub>**.
        - Since any withholding of entries can't result in the _additional_  generation/grant of permissions, the remaining possibility is that withholding entries somehow result in  **𝓡<sub>i</sub>** not mutating such that privileged data somehow remains accessible. This is a legitimate concern, however, [Channel Entry Validation](#Channel-Entry-Validation) requires that any mutation that is access-restrictive in nature must also [issue a new channel security epoch](#issuing-a-new-Channel-Epoch).  In this process flow, _only_ members with access privileges are (securely) issued the newly generated private channel key.   Similarly, this is why a [new community epoch is issued](#Issuing-a-New-Community-Epoch) when a member is [deactivated](#deactivating-A-Member) or a [member halt](#Member-halt) is issued (but not when a [new member is added](#adding-a-new-member)).
        - ⇒ In the case where entries are _withheld_ from **n<sub>i</sub>**, there is no possibility that subsequent entries could reveal restricted material since new peer entries would be encrypted with a newly issued member, channel or community key (after **Δ<sub>C</sub>**) .
    2. **Circumventing access controls**
        - These scenarios are characterized by posting malicously architected channel entries on **C** intended to circumvent access controls.
        - Given [Proof of Access Exclusivity](#Proof-of-Access-Exclusivity), we know that in order for **𝓡<sub>i</sub>** to be mutated (or maliciously manipulated), the perpetrating actor must possess _both_ an active member and community keyring.    
            - ⇒ this would start with **m** (or an adversary covertly in possession of **m**'s keys) authoring and submitting said entries in an attempt to somehow sidestep an aspect of the system's channel permissions enforcement.   How could an entry go live across **C** whose parent ACC denies access?  [Channel Entry Validation](#Channel-Entry-Validation)'s primary purpose is to _ensure that **only** entries that validate under the parent channel's ACC are placed into "live" status_.
        - What if **m** (or an adversary in possession of **m**'s keys) "hotwires" their node or manually crafts an entry to perform an operation not allowed by **m**?  
            - Athough **m** would be able to submit doctored entries to **𝓛<sub>C</sub>**, [Channel Entry Validation](#Channel-Entry-Validation) running on _every other_ community node would see that **m** does not have the required privileges and would indefinitely defer (reject) the entry.   
            - This is analogous to submitting a transaction on the global Bitcoin or Ethereum blockchain that transfers coinage from an ID that does ont have sufficient funds — the transaction will never validate. 
        - What if Alice is granted moderator priviledes for channel 𝘾𝒉 at the same moment she is granted a _different_ set of priviledes for 𝘾𝒉 by another?  In this and other cases of where there is an "ambiguous conflict", then deterministic [Ambiguous Conflict Resolution](#ambiguous-conflict-resolution) ("ACR") is invoked. 
            - Because ACR must be compatible with [Strong Eventual Consistency](#Strong-Eventual-Consistency) it must be time and state symmetric.  
            - Although natural ambiguous conflicts are rare, it is assumed that an adversary would induce ambiguous conflicts in an attempt to circumvent access controls in **C** (and take this to be the more limiting analysis). 
            - Let **ψ** represent two or more entries that cross a threshold that places them into "ambiguous conflict" status.
            - We observe that the scope of possibilties implied by **ψ** grows with the specific scope of the conflict.  
                - In the above example with Alice, although there is uncertainty around _Alice's permissions in 𝘾𝒉_, there _isn't_ uncertainty around Bob's permissions in 𝘾𝒉 or Alice's permissions in a separate channel. 
                - Likewise, an ambigous conflict about Charlie's member status in **C** means there is uncertainty around the liveness of _every entry_ he authored following the the timestamp of the conflict.  This example represents cascading dependencies on **ψ**.
            - ⇒ the superposition of all possible states of **𝓡** _only_ depends on states entangled with **ψ**.
            - We consider adversary **O** in possession of one or more member active private keyrings, wishing to attack **C**.
                1. **O** could only induce ACR in proportion to the access priviledges of the keyrings they control within **C**.
                    - For example, if **O** _only_ had basic member permissions within **C**, then **O** _wouldn't even have the potential_ to induce an ambiguous conflict since **O**'s sphere of access control isn't large enough to be in contention with another member. 
                2. Since ACR is time and state symmetric, **O** is limited to what resembles denial of service.  
                   - Given the vanishingly low probability of repeated naturally occurring ambiguous conflicts, a protective watchdog service in **C** could raise an alert upon clear tripwires, or could auto-initiate a [member halt](#member-halt) on the keyring(s) clearly inducing unnatural rates of conflict.           
            

#### Proof of Integrity Assurance

[Integrity Assurance](#Integrity-Assurance) specifies that members in positions of authority are accountable and remain bound to community policies and expectations.
- Every member action (mutation) on **C** is manifested as a channel entry, whether that is a routine content entry or a specially-signed entry in the [Member Epoch Channel](#Member-Epoch-Channel).
    - ⇒ every member interaction (channel entry) is replicated across **𝓛<sub>C</sub>**, an append-only storage layer, and available for review _to all other members of **C**_.
    - ⇒ any attempt of a member to conceal or rescind a previous entry will not result in the original entry being altered.
    - ⇒ all actions in community-public channels, which includes all community administrative [reserved channels](#reserved-channels), are always openly visible for peer review and scrutiny.  
- In private channels, entry content is encrypted and _only_ members granted access by the channel's owner can read the channel's content.  
    - By default, _not even community admins or authorities_ can gain access private channel content unless they have been granted access.  
    - Although the actions of a member in private channel **𝘾𝒉<sub>p</sub>** cannot be witnessed or reviewed by memebers outside of that channel, _any participant_ of **𝘾𝒉<sub>p</sub>** could be pressured by community authorities to turn over the channel's keyring (or face [deactivation](#deactivating-a-member]) or social/legal repercussions).
    - Community authorities are free to make use of private channels (just like other community members), but any action affecting reserved or community-public channels would be publicly available information and would be part of the permanent record that is **𝓛<sub>C</sub>**.
- Important channels, such as [reserved channels](#reserved-channels) or channels used to conduct community governance, could harness the dependable and predictable nature of "smart contracts" on **𝓛<sub>C</sub>**.  For example:
    - **C** has a _special_ community admin account capable of executing community propositions.  This virtual agent (and its private keys) are wired into a smart contract on **𝓛<sub>C</sub>** such that ⅔ of **C**'s "council" members are needed to sign a proposition before the contract's "threshold" signature triggers the proposition to be executed with admin permissions.
    - **C** makes use of a channel UI extension that in effect recreates a voting booth, allowing the members of **C** to vote on community propositions.  Corresponding smart contracts on **𝓛<sub>C</sub>** would be wired into these channels such that community members would have full assurance than voted propositions are executed relaibly and predictably.


#### Proof of Membership Fluidity

- Both [adding a new member](#adding-A-New-Member) and [deactivating a member](#deactivating-a-member) are implemented using standard entries in **C**'s channel system and undergo [Channel Entry Validation](#Channel-Entry-Validation) like all other standard entries _in addition to further checks and restrictions_.
- This implies that all the properties, assurances, and protection afforded by Channel Entry Validation extend to all aspects of membership fluidity.  This is to say that membership fluidity is a specialized form of [Permissions Assurance](#Permissions-Assurance) and so is thus addressed in [Proof of Permissions Assurance](#Proof-of-Permissions-Assurance).


#### Proof of Strong Eventual Consistency

- For each node **n<sub>i</sub>** in **C**, it's local replica state ("**𝓡<sub>i</sub>**") at a given moment in time is dependent on:
    - The set and order of entries that have arrived from **𝓛<sub>C</sub>**
    - The set and order of entries that have been authored locally (and have then been submitted to **𝓛<sub>C</sub>**)
    - [Channel Entry Validation](#Channel-Entry-Validation) continuously occurring on **n<sub>i</sub>** (and presumed to be running on other nodes of **C**). 
- Natural or adversarial network conditions could effectively cause entries to and from **𝓛<sub>C</sub>** to be delayed (or withheld). However, given sufficient time and network connectivity, when _all_ of replicated entries across **𝓛<sub>C</sub>** _eventually_ arrive at **n<sub>1</sub>**...**n<sub>N</sub>**, are **𝓡<sub>1</sub>**...**𝓡<sub>N</sub>** each in an equivalent ("consistent") state?  
- In short, we start with this systems's [Proof of Permissions Assurance](#proof-of-Permissions-Assurance) and then demonstrate that it is commutative, implying that the eventual state of **𝓡<sub>i</sub>** is _independent_ of the order of arrival of entries from **𝓛<sub>C</sub>**.
- It should be noted that if **𝓛<sub>C</sub>** favors safety over liveness (e.g. DFINITY, Hashgraph), then there is ceiling time window for transactions to clear.  This implies there is a ceiling to the superposition of possible states of any given **𝓡<sub>i</sub>**.  In other words, after a known time period, **𝓡<sub>i</sub>** can rule out any late-arriving entries.  


#### Proof of Practical Security Provisioning

- Given member **m** in **C**, we wish to show that this system provisions for even the worst security scenarios: 
    1. Scenario: **m** loses/erases all copies of their private keyring ("**[]k<sub>lost</sub>**").
        - A community admin (or delegated member) would use a procedure similar to [adding a new member](#Adding-A-New-Member), resulting in a successor `MemberEpoch` to be issued for **m**.
        - Even if an adversary were to recover _and_ extract keys from a locked **[]k<sub>lost</sub>**, they would, at most, have read-access up to when the new `MemberEpoch` was published.
        - Although **m** would importantly be able to retain and resume their identity within **C**, **m** would be unable to decrypt some entries from the past (since **m**'s new keyring would lack the keys).
        - Fortunately, for each private channel **𝘾𝒉<sub>p</sub>** that **m** had belonged to, **m** would be able to regain access if _at least_ one other member had _at least_ read-access to **𝘾𝒉<sub>p</sub>** (since that would **m** could be petition for the channel's keyring). 
        - If **m** every recovers **[]k<sub>lost</sub>**, access to past data would be restored with no additional action. 
    2. Scenario: an adversary ("**O**") gains access to **m**'s private keyrings ("**[]k<sub>m</sub>**") through deception, coercion, or covert access to **m**'s client device.
        - **O** would naturally be able to:
            - read community-public data on **C**
            - author entries impersonating **m**
            - read content intended to be private for **m**
        - When **m**, a peer of **m**, an admin, or an automated notices something is amiss, they would initiate a [member halt](#member-halt) on **m**, resulting in:
            - **O** losing append/post access to **C** (twofold: no postage _and_ **m**'s `MemberEpoch` suspended), _and_
            - **O** losing further read access to **𝓛<sub>C</sub>** once a new community epoch is issued.
        - In the case that **O** [issues a new member epoch](#issuing-a-new-Member-Epoch) (as **m**) _before_ a member halt is issued:
            - **m** would _still_ be able to issue a [member halt](#member-halt), _and_
            - an admin of **C**, in communication with **m**, would later rescind any entries in the [Member Epoch Channel](#member-epoch-channel) not authored by **m**.
    3. Scenario: admin ("**O**") on **C** covertly wishes to snoop on **m**.
        - At no point would **O** ever have access to **[]k<sub>m</sub>** since it never leaves **m**'s local client space (in any form).  This implies that **O** has _no_ ability to gain access to content encrypted for **m** _or_  the keys to any private channels that **m** has access to.  
        - In the event an admin posts a new `MemberEpoch` for **m** without permission, **m** would immediately be aware since **m**'s client would see the epoch issued (but not have the keys).   Note that hijacking another's identity as in this case would not allow the perpetrator to gain access to any of **m**'s private data since only **m** has possession of **[]k<sub>m</sub>**.
        Note that the given adversary would only have access to community public data (with **[]k<sub>C</sub>**) and **m**'s particular data

    4. Scenario: multiple adversaries infiltrate **C** 
        - Plan A: denial of service by abusing [member halt](#member-halt)
            - Since a member halt only suspends a member's access to **C**, its liability (as a mechanism) is limited to a one-time denial of service.    
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
    4. Use the credentials of **[]a′** to demote/deactivate **[]a** and any other desired members.
        - For each member demoted or deactivated, reduce/burn their postage permissions on **𝓛<sub>C′</sub>** as appropriate.

#### Proof of Storage Portability

- Suppose **C** wishes to switch to an alternative CRDT technology.
- Using a weaker form of the steps listed in [proof of independence assurance](#proof-of-independence-assurance), **C** can coordinate a switch to a new CRDT medium almost transparently.  
- Using steps similar to the steps in the [proof of independence assurance](#proof-of-independence-assurance), the admins of **C** can coordinate a switch to a new CRDT medium almost transparently.  
- This is to say that **𝓛** is to **C** as a hard drive is to an operating system.  **C**'s "hard drive" can be replaced:
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

**𝓡<sub>c</sub>**
**𝓡<sub>m</sub>**
**𝓛<sub>c</sub>**

**[]k<sub>c</sub>**
**[]k<sub>m</sub>**

#### Ambiguous Conflict Resolution

- Because community nodes can get transactions from **𝓛<sub>C</sub>** in an arbitrary order, it is possible for two different repos, **𝓡<sub>i</sub>** and **𝓡<sub>j</sub>**, to be in a state where members using them author conflicting entries that cannot be resolved.  
- In order to support strong eventual consistency, conflicts must always be deterministically resolved _only_ using information all nodes are guaranteed to eventually possess. 
- Given: 
    - entry **e<sub>0</sub>** is currently "live" in **𝓡<sub>i</sub>**, _and_
    - entry **e<sub>1</sub>** being processed by [channel entry validation](#Channel-Entry-Validation) and ambiguous conflicts with **e<sub>0</sub>** (i.e. either entry could be the "winner" but both can't)
- If/When node **n<sub>i</sub>** observes that **e<sub>1</sub>** is in ambiguous conflict with **e<sub>0</sub>**:
    - This means only one entry can be regarded as the "winner"
    - **n<sub>i</sub>** posts an entry in the Conflict Resolution Channels

- Note, in the case that **𝓛<sub>C</sub>** offers consensus timestamps for transactions (which is common), this alone is enough to radically 
    - For example, resolution couldn't depend on the arrival time of each entry from **𝓛<sub>C</sub>** unless 
    not depend on _when_ each entry arrived from **𝓛<sub>C</sub>**, _and_
    - 

- WE DONT HAVE SO SOLVE ALL CONFLICTS (such as in a collab doc)
    - we JUST have to cover the system ones -- we can enumerate them all:
        - always choose the grant-access direction?  (vs revoke direction)
it follows that each repo across **C** will vary .  If part of the network is recovering from a partition, it becomes more possible for two members to author entries that 
- Examples:
    - **e<sub>0</sub>**

**𝓡<sub>i</sub>**  across **C** can be in vario states


- IF the entry 
- If the entries are in separate channels
- Ambiguous conflicts can _also_ be adversary-induced, so we must analyze. 
    - The obvious objective for an adversary to induce ambiguous conflicts would be to disrupt **C** by crafting entries designed to invalidate "high value" root entries that would cause a cascade of entry invalidations to occur.  For example, suppose member **m** is granted the permission level of supermoderator in an ACC used for 
    
    posting an entry into a high-level ACC used across **C** dated a year ago causing 

two or more entries having "equal authority" conflict in that if they are live, then there is an inconsistency and/or contradiction.  
    - When two entries are back with "equal authority", the permissions levels 
- To unpack this, we consider two categories of ambiguous conflicts:
   - **Natural**, where network latency between the nodes of **C** resulted in a situation where two separate nodes authored entries 
   
   what is mildly similar to a race condition.
        - While each entry will have a globally-known author timestamp, they could arrive at a node in any order and with any delay.  
        - While there are an exponential number of permutations for how 
        
         permutations of the order entries arrive, however, seldom result in an ambiguous conflict since:
            - the entries are 
     However, in this case, each entry will me timestamped 


       - In this case, we assume the intention and timestamp on the entries are accurate and well intentioned. 
   - Adversary-Induced
       - In this case, w

- The consensus properties of **C** are effectively called into action here.  By default, entries in conflict with each other are each given a score based on the seniority of each member and the time delta of the entries.  There is either deterministic "winner" or "tie". In a tie, both entries in conflict are nullified.  
    - Implementation note: nullified entries, although effectively rejected, remain 
    - and that occur within a given time window are rejected.  
- In accessing ambiguous conflict resolution, we separate them into to categories:
   - Legitimate/Natural
       - In this case, we assume the intention and timestamp on the entries are accurate and well intentioned. 
   - Adversary-Induced
       - In this case, we assume one or more of the entries in conflict have forged `TimeAuthored` and have maliciously intentions.
- Ideally, we want to devise a resolution scheme that produces the most fair and reasonable outcomes for natural conflicts but is resilient against adversary-induced conflicts. 
    




- **m** uses a client that connects with a trusted community node (meaning a node that **m** trusts with the community keyring). 

 a client session with **𝓛<sub>C</sub>**, **m**'s local client node is presumed to have access to these keyrings (though they can be implemented in ways that further compartmentalize security, such as hardware dongles or a key server). 


And since a new channel security epoch entails sending each member a newly generated   This means if the entry that removes Oscar's access from the private channel is withheld, then ._ he idea is that if the entry that removed Oscar's access has yet to be merged into **𝓡<sub>i</sub>**, then Oscar   This case is somewhat of a trick question and reveals the nature of this operating system: "private channels" are really just a matter of whom has been securely sent the keys.  Hence, in this system, any time an ACC is mutated in the _more restrictive_ direction,  o read all   Hence,    _provided that an ACC mutation also initiates a new channel security epoch_.  This means that 
        enters a state where  **Trudy**  How could an absence of transactions ("entries") from **𝓛<sub>C</sub>** result in 




A community KeyID identifies a specific shared "community-global" symmetric key.
When a PLAN client starts a session with a pnode, the client sends the pnode her community-public keys.
PDIEntryCrypt.CommunityKeyID specifies which community key was used to encrypt PDIEntryCrypt.Header.
If/when an admin of a community issues a new community key,  each member is securely sent this new key via
the community key channel (where is key is asymmetrically sent to each member still "in" the community. 

    - In the case that **α** has gained possession of the _latest_ community key for whatever reason, this reflects that the members of **C** are _unaware_ of a security breach (otherwise a member or authority in **C** would have initiated a [member halt](#member-halt) or [started a new community epoch](#issuing-a-new-Community-Epoch)).  
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

