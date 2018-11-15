


https://magnetikonline.github.io/markdown-toc-generate/



(Liveness vs safety)
        - Also, the probability of an entry entering into a state of ambiguous conflict collapses to zero past **t<sub>b</sub>**.

(channel entey validaiton)

    - Otherwise, if for whatever reason **e** cannot complete validation (or **e** depends on an unresolved [ambiguous conflict](#Ambiguous-conflict-resolution)), then **e** is placed into "deferred" status.

        5. If **e** will introduce an ambiguous or contradictory conflict, then perform [ambiguous conflict resolution](#ambiguous-conflict-resolution). 



(Proof of Permissions Assurance)

        - What if Alice is granted moderator privileges for channel 𝘾𝒉 at the same moment she is granted a _different_ set of privileges for 𝘾𝒉 by another?  In this and other cases of where there is an "ambiguous conflict", then deterministic [Ambiguous Conflict Resolution](#ambiguous-conflict-resolution) ("ACR") is invoked. 
            - Because ACR must be compatible with [Strong Eventual Consistency](#Strong-Eventual-Consistency) it must be time and state symmetric.  
            - Although natural ambiguous conflicts are rare, it is assumed that an adversary would induce ambiguous conflicts in an attempt to circumvent access controls in **C** (and take this to be the more limiting analysis). 
            - Let **ψ** be two or more entries that cross a threshold that places them into "ambiguous conflict" status.
            - We observe that the scope of possibilities implied by **ψ** grows with the specific scope of the conflict.  
                - In the above example with Alice, although there is uncertainty around _Alice's permissions in 𝘾𝒉_, there _isn't_ uncertainty around Bob's permissions in 𝘾𝒉 or Alice's permissions in a separate channel. 
                - Likewise, an ambiguous conflict about Charlie's member status in **C** means there is uncertainty around the liveness of _every entry_ he authored following the the timestamp of the conflict.  This example represents cascading dependencies on **ψ**.
            - ⇒ the superposition of all possible states of **𝓡** _only_ depends on states entangled with **ψ**.
            - We consider adversary **O** in possession of one or more member active private keyrings, wishing to attack **C**.
                1. **O** can only induce ambiguous conflicts commensurate with the access level of the keys controlled.
                    - For example, if **O** _only_ had basic member permissions within **C**, then **O** _wouldn't even have the potential_ to induce an ambiguous conflict since **O**'s sphere of access control isn't large enough to be in contention with another member. 
                2. Since ACR is time and state symmetric, **O** is limited to what resembles denial of service.  
                   - Given the vanishingly low probability of repeated naturally occurring ambiguous conflicts, a protective watchdog service in **C** could raise an alert upon clear tripwires, or could auto-initiate a [Member Halt](#member-halt) on the keyring(s) clearly inducing unnatural rates of conflict.           
            






### UNDER CONSTRUCTION




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
    - The obvious objective for an adversary to induce ambiguous conflicts would be to disrupt **C** by crafting entries designed to invalidate "high value" root entries that would cause a cascade of entry invalidations to occur.  For example, suppose member **m** is granted the permission level of super-moderator in an ACC used for 
    
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

    - In the case that **α** has gained possession of the _latest_ community key for whatever reason, this reflects that the members of **C** are _unaware_ of a security breach (otherwise a member or authority in **C** would have initiated a [Member Halt](#member-halt) or [started a new community epoch](#issuing-a-new-Community-Epoch)).  
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

