# PLAN Design & Engineering Docs

```
         P urposeful
         L ogistics
         A rchitecture
P  L  A  N etwork
```

## Welcome to PLAN!

[PLAN](http://plan.tools) is a multi-purpose communications and logistics planning tool for organizations and community organizers. PLAN is built on a “pluggable” architecture that integrates distributed services, encryption, and interoperable data-transport technologies — all inside a realtime visual interface. PLAN is intended to be an instrument for productivity, organization, and collaboration. 

PLAN is free and open-source (GPLv3). The purpose of components in PLAN being pluggable is to allow anyone to easily add, improve, or extend component functionality. The design principles of PLAN are focused on making information transport and delivery openly interoperable and extensible, similar to how Tim Berners-Lee's HTTP sought to make information browsing interoperable.

We wish to acknowledge the principles surrounding [multistream](https://github.com/multiformats/multistream) by [Protocol Labs](https://protocol.ai), which subtly but decisively improves how protocols, paths, and formats can be expressed as to invite interoperability; `http://` becomes `/http/`.

 May PLAN empower organizations and individuals with little or no resources to self-organize.

## What's in This Repo?

This repo presents and discusses the layers, abstractions, and technologies that comprise PLAN.  It is written for a technical audience ready to understand and vet PLAN's architecture and design.  We recommend that visitors read this document and then consider exploring our other supporting documents:
1. [PLAN Appiled](PLAN-Applied.md)
2. [PLAN Proof of Correctness](PLAN-Proof-of-Correctness.md)

## Goals & Objectives

PLAN can only be useful to organizations and community organizers if non-technical users can use it easily. As software designers, we must acknowledge that distributed technologies, content-based addressing, and cryptography are alien concepts to most people. How does PLAN address this?

The primary objective of PLAN's architecture and user interface is to simplify the complex nature of "trustless" and distributed technologies with visual idioms that blend into the user experience as seamlessly and invisibly as possible. In most cases, it’s not particularly important to an end-user where exactly data resides, how it's served, or how the encryption works — but that it is intuitive, reliable, and secure. Instead of a 2D-constrained and sandboxed web/browser experience, the end-user experiences PLAN through the [Unity](https://unity3d.com) 3D engine while [Go](https://golang.org) powers its p2p node. The [PLAN Foundation](http://plan.tools) fully supports groups interested in developing a PLAN client in alternative environments, such as [Unreal](https://www.unrealengine.com) or [Electron](https://electronjs.org/).

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

## Architecture Synopsis

The PLAN Unity client talks to a `pnode`, the name for PLAN's p2p client-serving node.  `pnode` is a Go daemon that serves PLAN clients while replicating community data across the community's swarm of pnodes.   So, to summarize, PLAN has a realtime 3D/visual frontend with a p2p backend written in Go that can use almost any blockchain/DLT as the storage layer.  

What defines a community? In PLAN, a community is designed to reflect the human relationships that make up a community, whether that's a household, neighborhood, first-responders unit, off-grid farm, city council, media production, veterans network, maker-space, artist collective, emotional support network, small business, or gaming group. That is, each member in a community holds a copy of the community keyring (in addition to their private keys for that community). In effect, the entire community's network traffic and infrastructure is inaccessible to all others, providing a fundamental cryptographic "city wall" to ensure privacy and security.  

Each member of a (self-hosted and -organized) community running the PLAN client software has copy of the community keyring, giving them the ability to decrypt community data. Anyone _without_ this keyring — anyone _not_ in the community — is _outside_ the community's cryptographic city wall. Inside a community's city wall, residing on each community `pnode`, lives an IRC-inspired channel infrastructure. Each PLAN channel entry is composed of content data and an accompanying header that serves like HTTP headers. When a PLAN channel is created, it is assigned a protocol identifier. A [channel's protocol](#channel-protocols) implies the _kind_ of entries that are expected to appear that channel and _how_ they are interpreted. For example, an entry consisting of a geographical position could appear in a channel of type `/plan/channel/chat`, or in a channel of type `/plan/channel/geospace`; the UI is able to flexibly handle the entry differently. In the PLAN graphical client, each channel protocol identifier maps to a particular "channel UI driver", allowing the client to select from any of the available drivers. So instead of people requiring a web browser, PLAN is an open platform that offers users the ability to select or add channel UI drivers that suit their interests, taste, or needs.

In addition to the entry protocol a channel is assigned, a PLAN channel is _also_ assigned an owning access control channel (ACC) that specifies channel permissions, limits, and behaviors. A channel's controlling ACC, like all channels, also cites its own controlling ACC, and so on — up to the community's root ACC. A community's root ACC, is one of several "hard&nbsp;wired" channels that serve core community functions and can only be altered by community admins. Another such channel, for example, is the community registry channel, containing the member ID and public keys of each community member. Functions such as community member key recovery (i.e. a member "epoch" change) and other forms of private key exchange are carried out through community channels explicitly reserved for these purposes.

Like IRC, channels can be public (since all of PLAN's community traffic is encrypted to non-community members), or they can be private where entry content is compartmented in an additional layer of encryption. Only community members that have explicitly been given the channel's key have the ability to decrypt channel content. Also, although channels are fundamentally append-only, channels can be set so that new entry content can replace past content, allowing past entries to be edited (though past entries will naturally remain). The flexibility of a channel's protocol identifier plus the open/pluggable nature of PLAN's entry headers forms a powerful _superset_ of HTTP — all designed to be represented and interacted with via a local, graphical, high-performance interface.

Moment to moment, each `pnode` in a given community:
   - Merges newly appearing community channel entries from the storage layer into the community repo layer
   - Hosts connected Unity clients, serving client channel queries and decrypting content on the fly
   - Serves as a public HTTP gateway for community content designated to be publicly served (e.g. a public-facing web page containing a p2p-served promo video)

The permissions and rules of merge conflict resolution are deterministic so that strong eventual consistency (SEC) is preserved. This means that although a given pnode's data state may not be equal to other community pnodes state (due to network constraints), each pnode is guaranteed to converge to a monotonic state.

PLAN has two persistent pluggable storage layers, one characterized by append-only operations, and the other characterized by content-based addressing. The former, dubbed the Persistent Data Interface (PDI) is used to host a community's channel data and is intentionally designed to be compatible with the append-only nature of blockchain storage. The latter, dubbed the Cloud File Interface (CFI), is used to serve a community's high capacity data needs and off-PDI storage requirements, while PLAN's channel protocols and GUI wrap hashnames and other implementation details that no one wants to see or interact with. For example, a channel of type `/plan/channel/file/cfi/video` is used as a wrapper whose entries are CFI pathnames to each successive revision of that file (e.g. `/plan/cfi/ipfs/QmYwAP...`). This schema affords:
   - PLAN's deterministic infrastructure to know which CFI items are in use ("pinned") and which can be unpinned/deallocated.
   - Seamless UI integration and interactivity.  In the client UI, a channel's wrapper identifier causes it to be presented as a single opaque object (like a traditional file), where its activation causes the latest revision to be fetched and consumed. This allows users to easily access community content while not having to have any understanding about what's happening under the hood (or having to interact with hashnames).

PLAN is a p2p community-centric operating system, built on pluggable append-only and pluggable content-based addressing storage.  Community content is accessible via a _real-time_ visually intuitive interface — all within cryptographic layers of privacy. Its open-ended channel and ACC sub-systems provision for flexible, defensible, and first-class human access.

Using PLAN, communities arise from organizers and members who value owning their own data, having a formidable crypto-city wall, and the ability to continue operating in the face of Internet disruptions.  

---


# FAQ

#### Q: Why PLAN? Aren't there enough blockchain and DLTs already?
- Indeed, there are dozens of advanced DLT projects available and new ones on the way.  _However, PLAN at its heart is not a distributed ledger technology._  The lower-level of PLAN is an information organization and permissions system that is _built on top of an existing distributed technology_. Consider: _PLAN is to blockchain as Linux is to a harddrive._  When a new more capable DLT arrives, PLAN's [Proof of Storage Portability](PLAN-Proof-of-Correctness.md#Proof-of-Storage-Portability) demonstrates how a community can in effect upgrade their storage technology.

#### Q: But PLAN doesn't do X, fulfill need Y, or address use case Z.  How will PLAN address this?
- PLAN is not meant to be _all_ things to _all_ people.  PLAN first intends to target the small and micro-sized organizations that currently have _no_ choices when it comes to a multi-platform, secure, real-time, free, and integrated operations platform. PLAN is all about offering a reliable and easy-to-use logistics and planning tool for organizations with little or no resources.

#### Q: Does a PLAN community admin wield all the power and control?
- Not unless you want it that way.  The phrase "community admin" is used in these docs to refer to an agent acting in accordance with community policies and bylaws on behalf of the community's already-established leadership. This means that a community can operate as strictly or as loosely as the founding members want, but those agreements are visible to the entire community.  
- For example, community **C** could be founded such that a majority vote from a persistent, member-appointed "designee" are required to add a new member to the community. This would be enforced by a smart contract wired in to **C**'s storage layer. See PLAN's [Proof of Integrity Assurance](PLAN-Proof-of-Correctness.md#Proof-of-Integrity-Assurance) for more detail.

#### Q: How is PLAN's Persistent Data Interface (PDI) implemented?
- PLAN's append-only storage layerr ("**𝓛<sub>C</sub>**") described in PLAN's [Proof of Correctness](PLAN-Proof-of-Correctness.md), can be implemented by a range of storage approaches. Since each implementation must make tradeoffs in its design, one particular implementation may be a great fit for one community's needs but would be a poor fit for another community's needs. See [Liveness vs Safety](PLAN-Proof-of-Correctness.md#Liveness-vs-Safety) for more information.




---
---
