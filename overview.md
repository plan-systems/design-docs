# PLAN - Engineering Overview

```
         P urposeful
         L ogistics
         A rchitecture
P  L  A  N etwork
```

## Tenets & Objectives

PLAN will be useful to communities and organizers _only if_ non-technical users can use it easily. As software designers, we must acknowledge that distributed technologies, content-based addressing, and cryptography are alien concepts to most people. What does PLAN do about this?

It’s not particularly important to an end-user where exactly data resides, how it's served, or how the encryption works — but that it is reliable and secure.  The primary objective of PLAN's architecture and user interface is to simplify the complex nature of "trustless" and distributed technologies with visual idioms that blend into the user experience as seamlessly and invisibly as possible. Instead of a 2D-constrained and sandboxed web/browser experience, the end-user experiences PLAN through the [Unity](https://unity3d.com) 3D engine while [Go](https://golang.org) powers its p2p node.  The [PLAN Foundation](http://plan.tools) fully supports groups interested in developing a PLAN client in alternative environments, such as [Unreal](https://www.unrealengine.com) or [Electron](https://electronjs.org/).

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

Each member of a (self-hosted and -organized) community running the PLAN client software has copy of the community keyring, giving them the ability to decrypt community data.  Anyone _without_ this keyring — anyone _not_ in the community — is _outside_ the community's cryptographic city wall. Inside a community's city wall, residing on each community `pnode`, lives an IRC-inspired channel infrastructure. Each PLAN channel entry is composed of content data and an accompanying header that serves like HTTP headers. When a PLAN channel is created, it's assigned a protocol identifier. A [channel's protocol](#channel-protocols) implies the _kind_ of entries that are expected to appear that channel and _how_ they are interpreted. For example, an entry consisting of a geographical position could appear in a channel of type `/plan/channel/chat`, or in a channel of type `/plan/channel/geospace`, and the UI can handle the entry differently. In the PLAN graphical client, each channel protocol identifier maps to a particular "channel UI driver", allowing the client to select from any available drivers. So instead of people requiring a web browser, PLAN is an open platform that offers users the ability to select or add channel UI drivers that suit their interests, taste, or needs.

In addition to the entry protocol a channel is assigned, a PLAN channel is _also_ assigned an owning access control channel (ACC) that specifies channel permissions, limits, and behavior. A channel's controlling ACC, like all channels, also cites its own controlling ACC, and so on — up to the community's root ACC. A community's root ACC, is one of several "hard&nbsp;wired" channels that serve core community functions and can only be altered by community admins. Another such channel, for example, is the community registry channel, containing the member ID and public keys of each community member. Functions such as community member key recovery (i.e. a member "epoch" change) and other forms of private key exchange are carried out through community channels explicitly reserved for these purposes.

Like IRC, channels can be public ("public" only to members in that community in this case since all of PLAN's community traffic is encrypted), or they can be private where entry content is encrypted. Only community members that have explicitly been given the channel's key have the ability to decrypt channel content. Also, although channels are fundamentally append-only, channels can be set so that new entry content can replace past content, allowing past entries to be edited (though past entries will naturally remain). The flexibility of a channel's protocol identifier plus the open/pluggable nature of PLAN's entry headers forms a powerful _superset_ of HTTP — all designed to be represented and interacted with via a local, graphical, high-performance interface.

Moment to moment, each `pnode` in a given community:
   - Merges newly appearing community channel entries from the storage layer into the community repo layer
   - Serves connected Unity clients, serving client channel queries and decrypting content on the fly
   - Serves as a public HTTP gateway for community content designated to be publicly served (e.g. a public-facing web page containing a p2p-served promo video)

The permissions and rules of merge conflict resolution are deterministic so that strong eventual consistency (SEC) is preserved. This means that although a given pnode's data state may not be equal to other community pnodes state (due to network constraints), each pnode is guaranteed to converge to a monotonic state.

PLAN has two persistent pluggable storage layers, one characterized by append-only operations, and the other characterized by content-based addressing. The former, dubbed the Persistent Data Interface (PDI) is used to host a community's channel data and is intentionally designed to be compatible with the append-only nature of blockchain storage. The latter, dubbed the Cloud File Interface (CFI), is used to serve a community's high capacity data needs and off-PDI storage requirements, while PLAN's channel protocols and GUI wrap hashnames and other implementation details that no one wants to see or interact with. For example, a channel of type `/plan/channel/file/cfi/video` is used as a wrapper whose entries are CFI pathnames to each successive revision of that file (e.g. `/plan/cfi/ipfs/QmYwAP...`). This schema affords:
   - PLAN's deterministic infrastructure to know which CFI items are in use ("pinned") and which can be unpinned/deallocated.
   - Seamless UI integration and interactivity.  In the client UI, a channel's wrapper identifier causes it to be presented as a single opaque object (like a traditional file), where its activation causes the latest revision to be fetched and consumed. This allows users to easily access community content while not having to have any understanding about what's happening under the hood (or having to interact with hashnames).

PLAN is a p2p community-centric operating system, built on pluggable append-only and pluggable content-based addressing storage.  Community content accessible via a _real-time_ visually intuitive interface — all within cryptographic layers of privacy. Its open-ended channel and ACC sub-systems provision for flexible, defensible, and first-class human access.

Using PLAN, communities arise from community organizers who value owning their own data, having a formidable crypto-city wall, and the ability to continue operating in the face of Internet disruptions.  

---

# Applying PLAN

A technology is only as interesting as how it can be harnessed and applied in our world.  

## Community Public Access 

A community using PLAN will inevitably be interested in making some of its parts accessible to the global public.  A PLAN node allows publicly accessible services to serve community content and scale (as a distributed system) alongside traditional web or internet services.  For example:
- A musical artist uses PLAN to serve past show recordings and official track releases 
- A documentary production uses PLAN to serve the film's trailer and the full film itself to users bearing a "paid" token.
- A PLAN daemon periodically renders out an image of a map with spatial annotations from a community geo-space channel, served as a web page.
- A PLAN email gateway daemon bridges access to the members of a PLAN community and the outside world.  Unlike email, however, each incoming email contains an access token that the recipient previously issued the sender, effectively eliminating unsolicited messages/spam.  Further, a sender who abuses their privileges (or loses or resells their token to a spammer), can be blocked without any concern of messages from other senders being inadvertently filtered/blocked.

## Interoperable Data Structures

- PLAN's standard unit of information storage and transport is `plan.Block`:

    ```
    // A portable, compact, self-describing, nestable information container inspired from HTTP.
    type Block struct {

        // An optional, name/label for this Block (i.e. a field-name).
        // A Block's label conforms to the context/protocol it's being used with (as applicable).
        Label      string

        // Like a MIME type, this descriptor self-describes the data format of Block.Content.
        // Anyone handed this Block uses this field to accurately process/deserialize its content.
        // This is a "multicodec path" -- see: https://github.com/multiformats/multistream
        Codec      string

        // This is a reserved integer alternative to Block.Codec.
        // See: https://github.com/multiformats/multicodec/blob/master/table.csv
        CodecCode  uint32
        
        // Payload data, serialized in accordance with the accompanying codec descriptors (above).
        Content    []byte 

        // A Block can optionally contain nested "sub" blocks.  A Block's sub-blocks
        //    can be interpreted or employed any way a client or protocol sees fit.
        Subs       []*Block
    }
    ```
- Importantly, each `plan.Block` instance is [self-describing](https://multiformats.io/) and can contain sub-blocks. Because each element is accompanied by a label, codec descriptor, or additional sub-blocks, `plan.Block` has the _simplicity and flexibility_ of JSON but the _efficiency and compactness_ of binary serialization.  This means any hierarchy of information or content can be structured dynamically, and each element contains enough meta information for it to be safely analyzed and processed further.
- Like other foundational data structures in PLAN, `plan.Block` is specified using [Protobufs](https://developers.google.com/protocol-buffers).  This means boilerplate serialization and network handling code can be [trivially generated](https://github.com/plan-tools/plan-protobufs) for most major languages and environments, including C, C++, Objective-C, Swift, C#, Go, Java, JavaScript, Python, and Ruby.  Not bad!
    - A protobuf struct ("message") can be composed of primitive data types or user-defined messages.
    - Fields of a protobuf message are explicitly and strongly typed.
    - Revisions to a protobuf message are backward-compatible with previous revisions.
    - Protobufs are faster, simpler, safer, more compact, and more efficient than JSON and XML.
    - Protobufs pair well with [gRPC](https://grpc.io), opening up broad multi-language and multi-platform network support.
    - An entire `plan.Block` hierarchy can be serialized or deserialized using a single line of code — _in every major language and environment_.

- PLAN's Protobuf-based data structures:

    | Protobuf File      | Purpose                                         |
    |--------------------|-------------------------------------------------|
    | [go-plan/plan/plan.proto](http://github.com/plan-tools/go-plan/blob/master/plan/plan.proto)                  | PLAN-wide general purpose data structures       |
    | [go-plan/pdi/pdi.proto](http://github.com/plan-tools/go-plan/blob/master/pdi/pdi.proto)                      | Persistent Data Interface (PDI) data structures |
    | [go-plan/ski/ski.proto](http://github.com/plan-tools/go-plan/blob/master/ski/ski.proto)                      | Secure Key Interface (SKI) data structures      |
    | [go-plan/pservice/pservice.proto](http://github.com/plan-tools/go-plan/blob/master/pservice/pservice.proto)  | GRPC network services and data structures       |

---

## Channel Protocols

PLAN's general purpose channels are its workhorse and _raison d'être_.  Like files in a conventional operating system, users and productivity workflows in PLAN create new channels and new channel types all the time.  However, as a PLAN client UI interacts with a given channel, it does not use filename extensions, content-embedded markers, or blindly assume that content is in a particular form.   Both PLAN channel "epochs" and channel entries each embed a `plan.Block`, making each a flexible self-describing container for content and information.  _This offers profound interoperability in the way that HTTP headers also self-describe content for a HTTP response._

| Example Channel Descriptor | Expected Channel Entry Content Codecs | Example Client UI Experience  |
|----------------------|:--------------------:|--------------------------------------|
| `/plan/ch/talk`      |          `txt`\|`rtf`\|`image`      | A familiar "vertical scroller" where new entries appear in colored ovals at the bottom and previous entries vertically scroll upward to make room. |
| `/plan/ch/geoplot`   |         `cords + (txt`\|`image)`    | A map displays text and image annotations at each given geo-coordinate entry.  Clicking/Tapping on an annotation causes a box to appear displaying who made the entry and when. |
| `/plan/ch/file/pdf`  |            `ipfs`\|`binary`         | The client UI represents this channel as a single monolithic object. Tapping on it causes the most recent channel entry (interpreted as the latest revision) to be fetched and opened locally on the client using a PDF viewing application.  Power users can learn to open previous revisions of this "file". |
| `/plan/ch/file/audio`| `ipfs`\|`mpg`\|`aac`\|`ogg`\|`flac` | Like other PLAN "file" channels, this client UI displays this channel as a single object, where opening/activating it causes the most recent entry to be fetched and played using the default media player app or using PLAN's integrated AV player.  |  
| `/plan/ch/feed/rss`  |                 `xml`               | This channel is used to publish a sequence of text, audio, or video items with accompanying meta elements (e.g. title, link, thumbnail, and description).  This channel's epoch content `Block` houses [RSS](https://en.wikipedia.org/wiki/RSS) channel information while PLAN channel entries correspond to familiar RSS `item` elements in xml.  |
| `/plan/ch/feed/atom` |                 `xml`               | Similar to `feed/rss`, but PLAN channel entries instead conform to [Atom](https://en.wikipedia.org/wiki/Atom_(Web_standard)) xml. |
| `/plan/ch/calendar`  |          `text/ifb`\|`text/ics`     | The client UI presents a familiar visual calendar idiom containing events (entries) that are graphically rendered on the appropriate days and times. The user interacts with channel UI in real-time, scrolling from week to week, to day to day as the user zooms in "closer". |

---

## Milestones

| Milestone |  Timeframe  | Description                                 |
|:---------:|:-----------:|---------------------------------------------|
|   Newton  |   2018 Q2   | Permissions model [proof of concept](https://github.com/plan-tools/permissions-model) |
|  Babbage  |   2018 Q3   | [Proof of correctness](proof-of-correctness.md) complete |
|   Morse   |   2018 Q4   | [go-plan](https://github.com/plan-tools/go-plan) command line proof of concept demo  |
|   Kepler  |   2019 Q1   | [plan-unity](https://github.com/plan-tools/plan-unity) client p proof of concept demo  |
| Fessenden |   2019 Q2   | Ethereum, DFINITY, Holochain, or another established DLT used for next PDI implementation |
|  Lovelace |   2019 Q2   | Installer and GUI setup experience for macOS  |
|   Turing  |   2019 Q3   | go-plan support and QA for Linux | 
|  Galileo  |   2019 Q3   | PLAN Foundation internally replaces Slack with PLAN  |
| Hollerith |   2019 Q4   | Installer and GUI setup experience for Windows  | 
|   Barton  |   2020 Q1   | PLAN helps support [Art Community Builders](http://artcommunitybuilders.org/) |
|     -     |    2020+    | PLAN helps support other volunteer-run events  |



# FAQ

#### Q: Why PLAN? Aren't there enough blockchain and DLTs already?
- Indeed, there are dozens of advanced DLT projects available.  _However, PLAN at its heart is not a distributed ledger technology._  The lower-level of PLAN is an information organizational and permissions system that is _built on top of an existing distributed technology_. Consider: _PLAN is to blockchain as Linux is to harddrive._

#### Q: But PLAN doesn't do X, fulfill need Y, or address use case Z.  How will PLAN address this?
- PLAN is not meant to be _all_ things to _all_ people.  PLAN first intends to target the small and micro-sized organizations that currently have _no_ choices when it comes to a multi-platform, secure, real-time, and free integrated operations platform.  PLAN is about offering a reliable and easy-to-use logistics and planning tool for organizations with little or no resources.

#### Q: Does a PLAN community admin wield all the power and control?
- Not unless you want it that way.  The phrase "community admin" is used in these docs to refer to an agent acting in accordance with community policies and bylaws on behalf of the community's already-established leadership.  This means that a community can operate as strictly or as loosely as the founding members want, but those agreements are visible to the entire community.  
- For example, community **C** could be founded such that a majority vote persistent, member-appointed "elders" are required to disperse funds.  This would be enforced by a smart contract wired into **C**'s storage layer.   See PLAN's [Proof of Integrity Assurance](proof-of-correctness.md#Proof-of-Integrity-Assurance) for more detail.


#### Q: How is PLAN's Persistent Data Interface (PDI) implemented?
- PLAN's append-only storage layer, named "**𝓛<sub>C</sub>**" in PLAN's [Proof of Correctness](proof-of-correctness.md), can be implemented by a range of storage approaches.  Since each implementation must make tradeoffs in its design, one particular implementation may be a great fit one community's needs but would be a poor fit for another community's needs. See [Liveness vs Safety](proof-of-correctness.md#Liveness-vs-Safety) for more.



EOF