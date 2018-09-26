# PLAN - Engineering & Design Docs

```
         P urposeful
         L ogistics
         A rchitecture
P  L  A  N etwork

Welcome to PLAN!

PLAN is a secure, visual communications and logistics planning tool for individuals and communities.
It is intended to be an instrument of productivity, organization, and self-reliance.

PLAN is free and open-source (GPLv3), and each component and layer is "pluggable" an is offered as
an embodiment of an open-protocol.  The design principles of PLAN are similar and consistent with
Tim Berners-Lee's intention and design of http.

May PLAN empower organizations and individuals with little or no resources to communicate and self-organize 
intuitively and reliably.

```

## What's in This Repo?

This repo presents and discusses the layers, abstractions, and technologies that comprise PLAN. 
It is written for developer-types ready to understand and vet PLAN's architecture and design.  


## PLAN: A Synopsis


PLAN can't be empowering for community organizers if its not usable by non-technical users.  
Yet, we know distributed systems, content-based addressing, and cryptography are alien concepts to most people.  
PLAN How does PLAN square this circle?

PLAN secret weapon is hidden in plain sight: instead of relying on a 2D-constrained and sandboxed web/browser experience, PLAN uses the [Unity](https://unity3d.com) game engine to power the end-user's experience while using [Go](https://golang.org) for its p2p node.  

For the end-user, this affords:
   - A realtime, visual, and spatially-oriented interface
   - A first-class input and display device experience
   - Full horsepower of the user's device/workstation
   - Transparent end-to-end encryption
   - Multi-platform support

For PLAN, this affords: 
   - The power and capabilities of Go
   - A effective and robust multi-platform p2p node
   - Embedding of key technologies such as [IPFS](https://github.com/ipfs), [libp2p](https://github.com/libp2p), [protobufs](https://developers.google.com/protocol-buffers), and [gRPC](https://grpc.io).

The PLAN Unity client talks to a `pnode`, the name for PLAN's p2p client-serving node.  `pnode` is a Go daemon that serves PLAN clients while replicating community data across the community's swarm of pnodes.  

What defines a community?  In PLAN, a community is designed to reflect the human relationships that make up a community, whether that's a household, neighborhood, off-the-grid farm, maker-space, artist collective, or gaming group.  That is, each member in a community holds a copy of the community keyring (in addition to their private keys for that community).  In effect, the entire community's network traffic and infrastructure is inaccessible to all others, providing a fundamental cryptographic "city wall" of safety.  

Inside a PLAN community's cryptographic city wall, residing on each community pnode, lives an IRC-inspired channel infrastructure.  Each PLAN channel entry is composed of content data and an accompanying header that serves like http headers.  When a PLAN channel is created, it's assigned a protocol identifier.  A channel's protocol implies the _kind_ of entries that are expected to appear that channel and _how_ they are interpreted.  For example, an entry containing a geographical position could appear in a channel of type `/plan/channel/chat` or in a channel of type `/plan/channel/event` but the UI would present them differently.  In the PLAN graphical client, each channel protocol identifier maps to a particular "channel UI driver", allowing the client to select from any available drivers.  So instead of people using a web browser of their choice, PLAN is an open platform that offers users the ability to select or add channel UI drivers that suit their interests, taste, or needs.   

In addition to the entry protocol a channel is assigned, a PLAN channel is _also_ assigned an owning access control list (ACL) that specifies channel permissions, limits, and behavior. A channel's controlling ACL, like all channels, cites its own controlling ACL, and so on -- up to the community's root ACL.   A community's root ACL channel, is one of several "hard wired" channels that serve core community functions and can only be altered by community admins.  Another such channel, for example, is the community registry channel, containing the member ID and public keys of each community member.  Functions such as community member key recovery (i.e. a member "epoch" change) and other forms of private key exchange are carried out through community channels explicitly reserved for these purposes.  

Like IRC, channels can be public ("public" only to members in that community in this case), or they can be private where entry content is encrypted.  Only community members that have explicitly been given the channel's key have the ability to decrypt channel content.  Also, although channels are fundamentally  append-only, channels can be set so that new entry content can replace past content, allowing past entries to be edited (though past the entries will naturally remain).   The flexibility of a channel's protocol identifier plus the open/pluggable nature of PLAN's entry headers forms a powerful _superset_ of http -- all designed to be represented an interacted via a local, graphical, high-performance interface. 

Moment to moment, each `pnode` in a given community:
   - merges newly appearing community channel entries from the storage layer into the community repo layer.
   - serves connected Unity clients, serving client channel queries and decrypting content on the fly.

The permissions and rules of merge conflict resolution are deterministic so that strong eventual consistency (SEC) is preserved.  This means that although a given pnode's data state may not be equal to other community pnodes state (due to network constraints), each pnode is guaranteed to converge and to a monotonic state.

PLAN has two persistent pluggable storage layers, one characterized by append-only operations, and the other characterized by content-based loading and storing.  The former, dubbed the Persistent Data Interface (PDI) is used to host a community's channel data and is intentionally designed to be compatible with the append-only nature of blockchain storage.  The latter, dubbed the Cloud File Interface (CFI) is used to serve a community's hungry data needs while PLAN's channel and GUI hide hashnames that no one want's to see or interact with.  For example, a channel of type `/plan/channel/file/cfi/video` is used as a container channel who entries are CFI pathnames to each successive rev of that file (e.g. `/plan/cfi/ipfs/QmYwAPJv5C...`).  Note that this schema allows PLAN which community "cloud" files are in use and which can be dropped.    

In sum, PLAN is a p2p community-centric node operating layer, built on top of an open append-only and content-based addressing storage API, 
accessed by a real-time graphical client.  Its intentional channel, ACL, and crypto sub-system provision for flexible, defensible, and human-intractable access.  In PLAN, communities arise from community organizers that value owning their own data, having a formidable crypto city wall, and the ability to continue operation in the face of Internet disruptions.  


EOF
