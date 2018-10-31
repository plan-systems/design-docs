# PLAN - Design & Engineering Docs

```
         P urposeful
         L ogistics
         A rchitecture
P  L  A  N etwork
```

## Welcome to PLAN!

[PLAN](http://plan.tools) is a multi-purpose communications and logistics planning tool for organizations and communities. PLAN is built on a “pluggable” architecture that integrates distributed services, encryption, and interoperable data-transport technologies — all inside a realtime visual interface. PLAN is an instrument for productivity, organization, and collaboration.

PLAN is free and open-source (GPLv3). The purpose of components in PLAN being pluggable is to allow anyone to easily add, improve, or extend component functionality. The design principles of PLAN are focused on making information transport and delivery openly interoperable and extensible, similar to how Tim Berners-Lee's HTTP sought to make information browsing interoperable.

We also wish to acknowledge the principles surrounding [multistream](https://github.com/multiformats/multistream) by [Protocol Labs](https://protocol.ai), which subtly but decisively improves how protocols, paths, and formats can be expressed as to invite interoperability; `http://` becomes `/http/`.

May PLAN empower organizations and individuals with little or no resources to intuitively, securely, and reliably communicate and self-organize.

## What's in This Repo?

This repo presents and discusses the layers, abstractions, and technologies that comprise PLAN.  It is written for technical-types ready to understand and vet PLAN's architecture and design.  A formal [proof of correctness](proof-of-correctness.md) for PLAN is also available for review.


## PLAN: A Synopsis

PLAN will be useful to communities and organizers _only if_ non-technical users can use it easily. As software designers, we must acknowledge that distributed technologies, content-based addressing, and cryptography are alien concepts to most people. What does PLAN do about this?

It’s not particularly important to an end-user where exactly data resides, how it's served, or how the encryption works — just that it's reliable and secure.  The primary objective of PLAN's architecture and user interface is to simplify the complex nature of trustless and distributed technologies with visual idioms that blend into the user experience as seamlessly and invisibly as possible. Instead of a 2D-constrained and sandboxed web/browser experience, the end-user experiences PLAN through the [Unity](https://unity3d.com) 3D engine while [Go](https://golang.org) powers its p2p node.  The [PLAN Foundation](http://plan.tools) fully supports groups interested in developing a PLAN client in alternative environments, such as [Unreal](https://www.unrealengine.com) or [Electron](https://electronjs.org/).

For the end-user, using a graphics engine affords:
   - A realtime, visual, and spatially-oriented interface
   - A first-class input and display device experience
   - Full horsepower of the user's device/workstation
   - Transparent end-to-end encryption
   - Multi-platform support (Android, iOS, macOS, Windows, Linux)

For PLAN, this affords:
   - The power and capabilities of Go
   - An effective and robust multi-platform p2p node
   - An extensible & resilient development platform
   - Embedding of key stacks, namely: [IPFS](https://github.com/ipfs), [libp2p](https://github.com/libp2p), [Ethereum](https://www.ethereum.org), and [Protobufs](https://developers.google.com/protocol-buffers)+[gRPC](https://grpc.io).

The PLAN Unity client talks to a `pnode`, the name for PLAN's p2p client-serving node.  `pnode` is a Go daemon that serves PLAN clients while replicating community data across the community's swarm of pnodes.   So, to summerize, PLAN has a realtime 3D/visual frontend with a p2p backend written in Go that can use almost any blockchain/DLT as the storage layer.  

What defines a community? In PLAN, a community is designed to reflect the human relationships that make up a community, whether that's a household, neighborhood, first-responders unit, off-grid farm, city council, media production, veterans network, makerspace, artist collective, emotional support network, small business, or gaming group. That is, each member in a community holds a copy of the community keyring (in addition to their private keys for that community). In effect, the entire community's network traffic and infrastructure is inaccessible to all others, providing a fundamental cryptographic "city wall" to ensure privacy and security.  

Each member of a (self-hosted and -organized) community running the PLAN client software has copy of the community keyring, giving them the abilty to decrypt community data.  Anyone _without_ this keyring — anyone _not_ in the community — is _outside_ the community's cryptographic city wall. Inside a community's city wall, residing on each community `pnode`, lives an IRC-inspired channel infrastructure. Each PLAN channel entry is composed of content data and an accompanying header that serves like HTTP headers. When a PLAN channel is created, it's assigned a protocol identifier. A channel's protocol implies the _kind_ of entries that are expected to appear that channel and _how_ they are interpreted. For example, an entry consisting of a geographical position could appear in a channel of type `/plan/channel/chat`, or in a channel of type `/plan/channel/geospace`, and the UI can handle the entry differently. In the PLAN graphical client, each channel protocol identifier maps to a particular "channel UI driver", allowing the client to select from any available drivers. So instead of people requiring a web browser, PLAN is an open platform that offers users the ability to select or add channel UI drivers that suit their interests, taste, or needs.

In addition to the entry protocol a channel is assigned, a PLAN channel is _also_ assigned an owning access control channel (ACC) that specifies channel permissions, limits, and behavior. A channel's controlling ACC, like all channels, also cites its own controlling ACC, and so on — up to the community's root ACC. A community's root ACC, is one of several "hard&nbsp;wired" channels that serve core community functions and can only be altered by community admins. Another such channel, for example, is the community registry channel, containing the member ID and public keys of each community member. Functions such as community member key recovery (i.e. a member "epoch" change) and other forms of private key exchange are carried out through community channels explicitly reserved for these purposes.

Like IRC, channels can be public ("public" only to members in that community in this case since all of PLAN's community traffic is encrypted), or they can be private where entry content is encrypted. Only community members that have explicitly been given the channel's key have the ability to decrypt channel content. Also, although channels are fundamentally append-only, channels can be set so that new entry content can replace past content, allowing past entries to be edited (though past entries will naturally remain). The flexibility of a channel's protocol identifier plus the open/pluggable nature of PLAN's entry headers forms a powerful _superset_ of HTTP — all designed to be represented and interacted with via a local, graphical, high-performance interface.

Moment to moment, each `pnode` in a given community:
   - Merges newly appearing community channel entries from the storage layer into the community repo layer
   - Serves connected Unity clients, serving client channel queries and decrypting content on the fly
   - Serves as a public HTTP gateway for community content designated to be publicly served (e.g. a public-facing web page containing a p2p-served promo video)

The permissions and rules of merge conflict resolution are deterministic so that strong eventual consistency (SEC) is preserved. This means that although a given pnode's data state may not be equal to other community pnodes state (due to network constraints), each pnode is guaranteed to converge to a monotonic state.

PLAN has two persistent pluggable storage layers, one characterized by append-only operations, and the other characterized by content-based addressing. The former, dubbed the Persistent Data Interface (PDI) is used to host a community's channel data and is intentionally designed to be compatible with the append-only nature of blockchain storage. The latter, dubbed the Cloud File Interface (CFI), is used to serve a community's high capacity data needs and off-PDI storage requirements, while PLAN's channel protocols and GUI wrap hashnames and other implementation details that no one wants to see or interact with. For example, a channel of type `/plan/channel/file/cfi/video` is used as a wrapper whose entries are CFI pathnames to each successive revision of that file (e.g. `/plan/cfi/ipfs/QmYwAPJv5C...`). This schema affords:
   - PLAN's deterministic infrastructure to know which CFI items are in use ("pinned") and which can be unpinned/deallocated.
   - Seamless UI integration and interactivity.  In the client UI, a channel's wrapper identifier causes it to be presented as a single opaque object (like a traditional file), where its activation causes the latest revision to be fetched and consumed. This allows users to easily access community content while not having to have any understanding about what's happening under the hood (or having to interact with hashnames).

PLAN is a p2p community-centric operating system, built on pluggable append-only and pluggable content-based addressing storage.  Community content accessible via a _real-time_ visually intuitive interface — all within cryptographic layers of privacy. Its open-ended channel and ACC sub-systems provision for flexible, defensible, and first-class human access.

Using PLAN, communities arise from community organizers who value owning their own data, having a formidable crypto-city wall, and the ability to continue operating in the face of Internet disruptions.  

### Channel Protocol Examples

| Channel Descriptor | Valid Entry Content-Type | Example Client UI Experience                                                                                                                                                       |
|---------------------|----------------------|--------------------------------------|
| `/plan/ch/talk`     | `txt`\|`rtf`\|`image`      | Conventional vertical "chat scroller" where entries appear in stroked colored ovals                       |
| `/plan/ch/geo-plot` | `cords+(txt`\|`image)`  | A map displays text and image annotations at each given geo-space coordinate entry.                             |
| `/plan/ch/file/pdf`| `ipfs`\|`binary`    | The client UI represents the channel as a single icon. Tapping on it causes the most recent channel entry (interpreted as the latest revision) to be fetched and opened as a PDF locally on the client. |


## Milestones

| Milestone |  Status  | Description                                 |
|:---------:|:--------:|---------------------------------------------|
|   Newton  | 2018 Q2 | Permissions model [proof of concept](https://github.com/plan-tools/permissions-model) |
|  Babbage  | 2018 Q3 | [Proof of correctness](proof-of-correctness.md)  |
|   Morse   | 2018 Q4 | [go-plan](https://github.com/plan-tools/go-plan) command line prototype & demo  |
|   Kepler  | 2019 Q1 | [plan-unity](https://github.com/plan-tools/plan-unity) client prototype & demo  |
| Fessenden | 2019 Q2 | Ethereum or DFINITY used for first PDI implementation |
|  Lovelace | 2019 Q2 | Installer and GUI setup experience for macOS  |
|   Turing  | 2019 Q3 | go-plan support and QA for Linux | 
|  Galileo  | 2019 Q3 | PLAN Foundation internally replaces Slack with PLAN  |
| Hollerith | 2019 Q4 | Installer and GUI setup experience for Windows  | 
|   Barton  | 2020 Q1 | PLAN helps support [Art Community Builders](http://artcommunitybuilders.org/) |
|     -     |  2020+  | PLAN helps support other volunteer-run events  |



