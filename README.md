# PLAN - Engineering & Design Docs

```
         P urposeful
         L ogistics
         A rchitecture
P  L  A  N etwork
```
## Welcome to PLAN!

PLAN is an multi-purpose communications and logistics planning tool for individuals, organizations, and communities. Its open “pluggable” architecture integrates distributed services, encryption, and interoperable data-transport technologies — all in a realtime visual interface. PLAN is an instrument for productivity, organization, and collaboration.

PLAN is free and open-source (GPLv3). Components in PLAN are pluggable so that anyone can easily add, improve, or extend component functionality. The design principles of PLAN are focused on making information transport and delivery profoundly interoperable and extendable, similar and consistent with Tim Berners-Lee's vision for HTTP. Also to be acknowledged are the principles underpinning [multistream](https://github.com/multiformats/multistream) by [Protocol Labs](https://protocol.ai), which decisively improve how protocols, formats, and processes interoperate; `http://` becomes `/http/`.

May PLAN empower organizations and individuals with little or no resources to intuitively, securely, and reliably communicate and self-organize.

## What's in This Repo?

This repo presents and discusses the layers, abstractions, and technologies that comprise PLAN.  It is written for developer-types ready to understand and vet PLAN's architecture and design.  

## PLAN: A Synopsis

PLAN will be empowering for communities and organizers _only if_ non-technical users can use it easily. As software designers, we must accept that distributed technologies, content-based addressing, and cryptography are alien concepts to most people. How does PLAN square this circle?

Given that it’s not necessary to know exactly how encryption works in order to take advantage of the benefits it provides, similarly, it’s not particularly important to an end-user where exactly data resides in a network or how it is served. The design objective of PLAN's architecture/UI is to simplify the complex nature of trustless and distributed technologies with visual idioms that blend into the user experience as seamlessly and invisibly as possible. Instead of a 2D-constrained and sandboxed web/browser experience, the end-user experiences PLAN through the [Unity](https://unity3d.com) game engine while [Go](https://golang.org) powers its p2p node. Someday the [PLAN Foundation](http://plan.tools) would like to support development of an [Unreal](https://www.unrealengine.com) client implementation as well.

For the end-user, using a graphics engine affords:
   - A realtime, visual, and spatially-oriented interface
   - A first-class input and display device experience
   - Full horsepower of the user's device/workstation
   - Transparent end-to-end encryption
   - Multi-platform support (Android, iOS, macOS, Windows, Linux)

For PLAN, this affords: 
   - The power and capabilities of Go
   - A effective and robust multi-platform p2p node
   - An extensible & resilient development platform
   - Embedding of key stacks, namely: [IPFS](https://github.com/ipfs), [libp2p](https://github.com/libp2p), [Ethereum](https://www.ethereum.org), and [Protobufs](https://developers.google.com/protocol-buffers)+[gRPC](https://grpc.io).

The PLAN Unity client talks to a `pnode`, the name for PLAN's p2p client-serving node.  `pnode` is a Go daemon that serves PLAN clients while replicating community data across the community's swarm of pnodes.  

What defines a community? In PLAN, a community is designed to reflect the human relationships that make up a community, whether that's a household, neighborhood, first-responders unit, off-grid farm, city council, veterans network, makerspace, artist collective, emotional support network, music coalition, or gaming group. That is, each member in a community holds a copy of the community keyring (in addition to their private keys for that community). In effect, the entire community's network traffic and infrastructure is inaccessible to all others, providing a fundamental cryptographic "city wall" to ensure privacy and security.  

Inside a PLAN community's cryptographic city wall, residing on each community `pnode`, lives an IRC-inspired channel infrastructure. Each PLAN channel entry is composed of content data and an accompanying header that serves like HTTP headers. When a PLAN channel is created, it's assigned a protocol identifier. A channel's protocol implies the _kind_ of entries that are expected to appear that channel and _how_ they are interpreted. For example, an entry consisting of a geographical position could appear in a channel of type `/plan/channel/chat`, or in a channel of type `/plan/channel/geospace`, and the UI can handle the entry differently. In the PLAN graphical client, each channel protocol identifier maps to a particular "channel UI driver", allowing the client to select from any available drivers. So instead of people requiring a web browser, PLAN is an open platform that offers users the ability to select or add channel UI drivers that suit their interests, taste, or needs.

In addition to the entry protocol a channel is assigned, a PLAN channel is _also_ assigned an owning access control list (ACL) that specifies channel permissions, limits, and behavior. A channel's controlling ACL, like all channels, cites its own controlling ACL, and so on -- up to the community's root ACL. A community's root ACL channel, is one of several "hard wired" channels that serve core community functions and can only be altered by community admins. Another such channel, for example, is the community registry channel, containing the member ID and public keys of each community member. Functions such as community member key recovery (i.e. a member "epoch" change) and other forms of private key exchange are carried out through community channels explicitly reserved for these purposes.

Like IRC, channels can be public ("public" only to members in that community in this case), or they can be private where entry content is encrypted. Only community members that have explicitly been given the channel's key have the ability to decrypt channel content.  Also, although channels are fundamentally append-only, channels can be set so that new entry content can replace past content, allowing past entries to be edited (though past entries will naturally remain). The flexibility of a channel's protocol identifier plus the open/pluggable nature of PLAN's entry headers forms a powerful _superset_ of HTTP -- all designed to be represented and interacted with via a local, graphical, high-performance interface.

Moment to moment, each `pnode` in a given community:
   - Merges newly appearing community channel entries from the storage layer into the community repo layer
   - Serves connected Unity clients, serving client channel queries and decrypting content on the fly

The permissions and rules of merge conflict resolution are deterministic so that strong eventual consistency (SEC) is preserved. This means that although a given pnode's data state may not be equal to other community pnodes state (due to network constraints), each pnode is guaranteed to converge and to a monotonic state.

PLAN has two persistent pluggable storage layers, one characterized by append-only operations, and the other characterized by content-based loading and storing. The former, dubbed the Persistent Data Interface (PDI) is used to host a community's channel data and is intentionally designed to be compatible with the append-only nature of blockchain storage. The latter, dubbed the Cloud File Interface (CFI), is used to serve a community's high capacity data needs and off-chain storage requirements, while PLAN's channel protocols and GUI hide and manage hashnames that no one wants to see or interact with. For example, a channel of type `/plan/channel/file/cfi/video` is used as a container channel with entries that are CFI pathnames to each successive rev of that file (e.g. `/plan/cfi/ipfs/QmYwAPJv5C...`). Note that this schema allows PLAN to specify which community "cloud" files are in use ("pinned") and which can be dropped. In the client UI, a channel's faux file protocol identifier would cause it to be presented as a single opqaue object; a request for use of the video would cuase the latest rev to be fetched. This allows users to enjoy and easily access community content while not having to have any understanding about what's happening under the hood.

In sum, PLAN is a p2p community-centric node operating system, built on top of an open append-only and content-based addressing storage API, accessed by a real-time graphical client -- all in transparent cryptographic layers of privacy. Its intentional channel, ACL, and crypto sub-systems provision for flexible, defensible, and first-class human access. In PLAN, communities arise from community organizers that value owning their own data, having a formidable crypto city wall, and the ability to continue operation in the face of Internet disruptions.  


EOF
