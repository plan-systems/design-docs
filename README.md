# PLAN Design & Engineering Docs

```
         P urposeful
         L ogistics
         A rchitecture
P  L  A  N etwork
```

## Welcome to PLAN!

PLAN is open-source collaboration software for groups to securely communicate and coordinate activities, featuring:
- Channels specialized for chat, file sharing, interactive maps, tasking, scheduling, and inventory management
- End-to-end security, complete data ownership, and mission-critical reliability
- A highly visual interface where channels, file, and links are found in virtual spaces
- Optional storage decentralization for risk mitigation and offline operation
- Built-in collaboration tools for teams to organize and manage operations
- Relationship and organization management and visualization
- A “[pluggable](PLAN-API-Documentation.md#Primary-Interfaces)” architecture designed to support modification and flexibility.
	
PLAN’s architecture brings all these parts together into a unified, _integrated_, visual interface. The design principles of PLAN center around making information highly interoperable and extensible, inspired by how HTTP originated as a step towards interoperability and compatibility.  PLAN is freely available through the GNU General Public License ([GPL3](https://www.gnu.org/licenses/gpl-3.0.en.html)). 

PLAN is designed and intended for:
- Community organizations
- Crisis management teams
- Educators and researchers
- Civic institutions
- Businesses and sales teams
- Clubs and gaming groups
- Support groups

## What's in This Repo?

This repo presents and discusses the layers, abstractions, and technologies that comprise PLAN.  It is written for a technical audience ready to understand and vet PLAN's architecture and design.  We recommend that visitors read this document and then explore our other supporting documents:
1. [FAQ](#FAQ)
2. [API Documentation](PLAN-API-Documentation.md)
3. [Data Model Proof of Correctness](PLAN-Proof-of-Correctness.md)

## Why PLAN?

Distributed technologies offer astonishing potential, but they lack a consistent and accessible graphical user experience. Distributed ledgers and other “serverless” technologies are ripe to be integrated into a _unified_ visual interface that prioritizes human usability and convenience.  Such a system must be resistant to mass-messaging/spam, outside interference, and malicious actors.  As an information visualizer, PLAN allows teams to communicate and conduct logistics planning efficiently, reliability, and privately. PLAN offers assurance that the information we store and depend on will be available not only during times of prosperity, but also during natural disaster, political crisis, or economic drought. 

## PLAN Systems

[PLAN Systems](http://plan-systems.org) is a non-profit public charity, developing and providing publicly available systems that foster robust digital self-reliance for low resource communities, while also reducing the burden on local, state, and federal agencies.  

May PLAN empower organizations and individuals, and may it be an instrument of productivity and self-organization.

## Architecture Objectives

The primary objective of PLAN's architecture and user interface is to simplify the complex nature of digital privacy and distributed systems using interactive visual idioms that blend into the user experience as seamlessly as possible. In most cases, it’s not particularly important to an end-user where exactly data resides, how it's served, or how encryption works — _but that it's intuitive and reliable_.

Instead of a 2D-constrained and sandboxed web browser experience, a PLAN user experiences their organization's structure and content through the [Unity](https://unity3d.com) graphics engine as it renders channels of information into virtual space.  The client is served by a "community" node that uses a storage abstraction compatible with many existing [distributed ledgers](https://en.wikipedia.org/wiki/Distributed_ledger).

Design goals:
- Multiplatform: _Android, iOS, Linux, macOS, Windows_
- User experience is 2D/orthographic, first person, isometric, AR, VR
- Peer-to-peer [persistent storage abstraction](PLAN-API-Documentation.md#persistent-data-interface) compatible with distributed ledgers
- Peer-to-peer [cloud storage abstraction](PLAN-API-Documentation.md#cloud-file-interface) compatible with distributed storage systems
- Pluggable content handling and rendering via [channel GUI adapters](PLAN-API-Documentation.md#channel-gui-adapters)
- “Offline first” to allow work when only part of the network reachable
- Access controls for groups as a whole or for individual channels or members
- Allow a community to peer-host select content for external consumption

PLAN users get:
- A responsive, engaging, animated, and intuitive experience
- A first-class input and display device experience
- Full horsepower of the device/workstation
- Complete data ownership and control

How is PLAN implemented?
- User client written in [Unity](https://unity3d.com) 3D engine (C# and .NET Core)
- Peer-to-peer backend daemon ("node") written in [Go](https://golang.org)
- Channels are identified and interpreted via self-describing metadata
- Access control implemented using channels; each channel is a child of some other channel, up to a root.
- Local file system caching and partial network resilience to enable offline work


## Architecture Synopsis

PLAN has a 3D/visual frontend with a peer-to-peer backend that uses one or more secure distributed storage providers.  The PLAN client, written in [Unity](https://unity3d.com), connects to a "community" peer-to-peer PLAN node, a daemon written in [Go](https://golang.org).  These nodes serve PLAN clients while replicating shared community data across the community's federation of nodes. 

What defines a community? In PLAN, a community is designed to reflect the human relationships that make up the community, whether that's a household, neighborhood, first-responders unit, off-grid farm, city council, media production, veterans network, maker-space, artist collective, emotional support network, small business, or gaming group. The entire community's network traffic and infrastructure is inaccessible to all others, forming a cryptographic _city wall_ of privacy and security.  

A PLAN community is formed when one or more founders/organizers gather and together use the community genesis tool that codifies initial governance and administration.  In that process, they also decide which of the available [StorageProviders](PLAN-API-Documentation.md#persistent-data-interface) implementaitons are best for their needs.  After that, the founders and subsequent members of the community maintain a copy of the "community keyring", giving members the ability to access the community's shared data repository. Anyone _without_ this keyring — anyone _not_ in the community — is _outside_ the community's crypto city wall.  

Inside this outer layer of security, residing on each community node, lives an IRC-inspired channel infrastructure. Each PLAN channel entry contains content and metadata that works like HTTP headers, allowing content to be richly interpreted.  But a channel's "protocol identifier" also contributes to describing how entry content should be interpreted.  

When a PLAN channel is created, it is assigned a protocol identifier string (e.g. `/plan/channel/chat`). This [channel protocol](PLAN-API-Documentation.md#channel-protocols) implies the _kind_ of entries that are expected to appear in a channel and _how_ they should be interpreted and presented within the PLAN client. In the client, each channel type string maps to a channel GUI adapter or "driver" that is invoked when the user opens/views a channel, like when an OS opens a specific application to handle a given file type.  A power user can set their client to invoke alternative channel adapters that may be more appropriate for their situation, client device, or personal taste.  This leaves exciting possibilities for custom channel design and development.  As PLAN grows into its core mission and vision, primary development is going towards channels that:
- facilitate group communication and workflows
- track tasks and task status
- build interactive maps, charts, floor plans, and virtual spaces
- track inventory and supplies
- integrate files and media sharing
- tally and track community polls and voting
- coordinate and visualize calendars and scheduling
- accept and filter custom-designed forms

In addition to the entry protocol a channel is assigned, a PLAN channel is _also_ assigned an owning access control channel (ACC) that specifies channel permissions, limits, and behaviors. A channel's controlling ACC, like all channels, also cites its own controlling ACC, and so on — up to the community's root ACC. A community's root ACC, is one of several "hard&nbsp;wired" channels that serve core community functions and can only be altered by community admins. Another such channel, for example, is the community registry channel, containing the member ID and public keys of each community member. Functions such as member key regeneration and key exchange are carried out through community channels explicitly reserved for these purposes.

Akin to IRC, PLAN channels are either "community-public" (readable only to members in the community), or they are private where entry content is encrypted such that only channel members have access. Only community members that have explicitly been given a private channel's key have the ability to decrypt its content. And although channels are fundamentally append-only, channels can be set so that new entry content can replace past content, allowing past entries to be edited (though past entries will naturally remain). The flexibility of a channel's protocol identifier plus the rich and flexible nature of PLAN's [interoperable data structures](PLAN-API-Documentation.md#Interoperable-Data-Structures) make PLAN's channel system dynamic and extensible — designed to be represented and interacted with via a local, graphical, high-performance interface.

At any given time, each community node:
   - Merges newly appearing community channel entries from the storage layer into the community repo layer
   - Hosts connected Unity clients, serving client channel queries and decrypting content on the fly
   - Serves as a public HTTP gateway for community content designated to be publicly served (e.g. a public-facing web page containing a peer-served promo video)

The permissions and rules of merge conflict resolution are deterministic so that strong eventual consistency (SEC) is preserved. This means that although a given node's data state may not be equal to other community nodes state (due to network constraints), each node is guaranteed to converge to a monotonic state.

PLAN has two persistent pluggable storage layers, one characterized by append-only operations and the other characterized by content-based addressing. The former, the Persistent Data Interface (PDI) is used to host a community's channel data and is intentionally designed to be compatible with the append-only nature of blockchain storage. The latter, the [Cloud File Interface](PLAN-API-Documentation.md#cloud-file-interface) (CFI), is used to support a community's bulk data storage needs, while PLAN's channel protocols and GUI wrap hashnames and other implementation details that no one wants to see or interact with. For example, a channel of type `/plan/channel/file/cfi/video` is used as a wrapper whose entries are CFI pathnames to each successive revision of that file. This schema affords:
   - PLAN's deterministic infrastructure to know which CFI items are in use ("pinned") and which can be unpinned/deallocated.
   - Seamless UI integration and interactivity.  In the client UI, a channel's wrapper identifier causes it to be presented as a single opaque object (like a traditional file), where its activation causes the latest revision to be fetched and consumed. This allows users to easily access community content while not having to have any understanding about what's happening under the hood (or having to interact with hashnames).

## Summary

PLAN is a peer-to-peer community-first tool, built on append-only and pluggable content-based addressing storage.  Community content is accessible via a _real-time_ visually intuitive interface protected inside cryptographic layers of privacy. Its open-ended channel sub-systems form a level foundation that supports flexible, defensible, and first-class human access.

Using PLAN, communities arise from organizers and members who value owning their own data, having a formidable cryptographic-city wall, and the ability to continue operating in the face of Internet disruptions.  

---



## Project Milestones

| Milestone |  Timeframe  | Description                                                                               |
|:---------:|:-----------:|-------------------------------------------------------------------------------------------|
|   [Newton](https://en.wikipedia.org/wiki/Isaac_Newton)  |   2018 Q2   | Permissions model [proof of concept](https://github.com/plan-systems/permissions-model)     |
|  [Babbage](https://en.wikipedia.org/wiki/Charles_Babbage)  |   2018 Q3   | PLAN [Proof of Correctness](PLAN-Proof-of-Correctness.md) complete                        |
|   [Morse](https://en.wikipedia.org/wiki/Samuel_Morse)   |   2019 Q1   | [plan-core](https://github.com/plan-systems/plan-core) command line proof of concept demo       |
|   [Kepler](https://en.wikipedia.org/wiki/Johannes_Kepler)  |   2019 Q2   |  [CFI](PLAN-API-Documentation.md#cloud-file-interface) ([IPFS](https://ipfs.io/)) integration   |
|  [Mercator](https://en.wikipedia.org/wiki/Gerardus_Mercator) |   2019 Q2   | [plan-client-unity](https://github.com/plan-systems/plan-client-unity) preliminary proof of concept |                                       |
| [Fessenden](https://en.wikipedia.org/wiki/Reginald_Fessenden) |   2019 Q3   | Ethereum, DFINITY, Holochain, or other DLT used for first p2p [PDI](PLAN-API-Documentation.md#Persistent-Data-Interface) implementation |
|   [Turing](https://en.wikipedia.org/wiki/Alan_Turing)  |   2019 Q3   | Support and QA for Linux                                                          | 
|  [Lovelace](https://en.wikipedia.org/wiki/Ada_Lovelace) |   2019 Q3   | Installer and GUI setup experience for macOS                                              |
|  [Galileo](https://en.wikipedia.org/wiki/Galileo_Galilei)  |   2019 Q4   | PLAN Systems internally switches from Slack to PLAN                                       |
| [Hollerith](https://en.wikipedia.org/wiki/Herman_Hollerith) |   2019 Q4   | Installer and GUI setup experience for Windows                                            | 
|   [Barton](https://en.wikipedia.org/wiki/Clara_Barton)  |   2020 Q1   | PLAN helps support [Art Community Builders](http://artcommunitybuilders.org/)             |
|     -     |    2020+    | PLAN expands support for other volunteer-run events                                       |



---


# FAQ


#### Q: Why PLAN? Aren't there enough blockchain and distributed ledgers already?
- Indeed, there are many advanced distributed ledger projects available and new ones on the way.  However, _PLAN is not a distributed ledger_.  PLAN is an information organization and access control system that _resides atop a storage system_. 
- Consider: _PLAN is to distributed ledger as operating system is to harddrive_.  If a more capable or suitable storage technology appears, PLAN's [Proof of Storage Portability](PLAN-Proof-of-Correctness.md#Proof-of-Storage-Portability) demonstrates how a community can switch storage technologies.

#### Q: What are the ways PLAN is pluggable or can be otherwise be extended?
- PLAN features an architecture intended for modularity, flexibility, and specialization. PLAN's [Primary Interfaces](PLAN-API-Documentation.md#Primary-Interfaces) span from storage layers, to PLAN GUI plugins called Channel Adapters that allow a channel to be experienced differently.

#### Q: Where is a community data stored and who ultimately controls it?
- The [Persistent Data Interface](PLAN-API-Documentation.md#Persistent-Data-Interface) is intended for _permanent_ community storage and should be regarded at the community's channel repository. 
- The [Cloud File Interface](PLAN-API-Documentation.md#cloud-file-interface) is an abstraction that exposes a distributed storage system, used for bulk data storage. It pairs well with the PDI since a channel entry can reference a CFI item using only a short string.  
- In both cases, _the community stores and controls its own data_.  By design, a PLAN community is not dependent on storage or infrastructure outside the community (other than whatever third-party telecommunications infrastructure is needed) 

#### Q: But PLAN doesn't do X, fulfill need Y, or address use case Z.  How will PLAN address this?
- PLAN is not meant to be _all_ things to _all_ people. PLAN is intended for micro-sized to medium-sized organizations and groups that have few or no options when it comes to a multi-platform, secure, and integrated operations platform. PLAN is all about offering a reliable and easy-to-use logistics and planning tool for ad-hoc groups or under-resourced organizations. 

#### Q: Does a PLAN community admin wield all the power and control?
- Not unless you want it that way.  The phrase "community admin" is used in these docs to refer to an agent acting in accordance with community policies and bylaws on behalf of the community's already-established leadership. This means that a community can operate as strictly or as loosely as the founding members want, but those agreements are visible to the entire community.  
- For example, community **C** could be founded such that a majority vote from a member-appointed set of "board" members are required in order to add a new member to the community. This would be enforced by a smart contract wired into **C**'s storage layer. See PLAN's [Proof of Accountability Assurance](PLAN-Proof-of-Correctness.md#Proof-of-Accountability-Assurance) for more.

#### Q: Is PLAN is locked into Unity?
- Although [PLAN&nbsp;Systems](http://plan-systems.org) is making the primary PLAN client with [Unity](https://unity3d.com/), we would fully support development of a client made with [Unreal](https://www.unrealengine.com), [CRYENGINE](https://www.cryengine.com/), [Godot](https://godotengine.org/) or any other established 3D framework.

#### Q: Can multiple PLAN communities interact or federate?
- There are many interesting areas of research and future development related to how independent PLAN communities can interact and be allies.  Open research areas include:
    - Peer Federations — a community's leadership grants privileges to another community's members en masse. 
    - Hierarchical Federations — a community originates as subordinate in some way to parent community.
    - Commerce Federations — multiple communities maintain shared identity or marketplace federation infrastructure, facilitating trade and commerce. 

#### Q: How can I try PLAN or support its development?
- Check out the [PLAN website](http://plan-systems.org) and fill out our contact form.  This will allow you hear about announcements and upcoming releases.

---
---
