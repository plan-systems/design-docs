# PLAN API Documentation

```
         P urposeful
         L ogistics
         A rchitecture
P  L  A  N etwork
```

A technology is only as interesting as how it can be harnessed and applied in our world.  

## Primary Interfaces

PLAN features 7 primary areas of extension and interoperability.  Together, they reflect PLAN's engineering mission to be modular, future-proof, and adaptable. 

|     Area of Interoperability    | Purpose                                                                                                                                     |
|:-------------------------------:|---------------------------------------------------------------------------------------------------------------------------------------------|
|  [Interoperable Data Structures](#Interoperable-Data-Structures)  | Flexible, portable, self-describing, performant data structures                                                               |
| [Persistent Data Interface](#Persistent-Data-Interface)  | Abstracts a community's permanent data store; designed to be compatible with distributed ledgers (e.g. blockchains)                    |
|        [Channel Protocols](#channel-protocols)           | Separates content streams by purpose and interpretation, not just by content type or format                                            |
|       [Channel GUI Adapters](#Channel-GUI-Adapters)      | Provides an interchangeable front-end GUI experience for a given channel type                                                          |
|       [Cloud File Interface](#Cloud-File-Interface)      | Abstracts expendable shared bulk storage; designed to be compatible with distributed content-addressable storage systems               |
|       [Secure Key Interface](#Secure-Key-Interface)      | Abstracts private key handling and crypto services; designed to integrate third-party encryption and authentication systems            |
|        [Public Services](Public-Services)                | Serves public requests for explicitly shared community content via conventional internet protocols                                     |

## Interoperable Data Structures

- PLAN features a powerful but tiny set of flexible, portable, self-describing, and performant data structures. 
- Thanks to [Protobufs](https://developers.google.com/protocol-buffers) and [gRPC](https://grpc.io), developers can access content in PLAN using every major language and over a network connection with only a few lines of code. 
- PLAN's standard unit of information storage, structure, and transport is `plan.Block`:
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
- Importantly, each `plan.Block` instance is [self-describing](https://multiformats.io/) and can contain sub-blocks. Because each `plan.Block` can be accompanied by a label, codec descriptor, or any number of sub-blocks, it has the _simplicity and flexibility_ of JSON but the _efficiency and compactness_ of binary serialization.  This means any hierarchy of information or content can be structured dynamically, and each element contains enough meta information for it to be safely analyzed and processed further.
- Like other foundational data structures in PLAN, `plan.Block` is specified using [Protobufs](https://developers.google.com/protocol-buffers).  This means boilerplate serialization and network handling code can be [trivially generated](https://github.com/plan-tools/plan-protobufs) for most major languages and environments, including C, C++, Haskell, Objective-C, Swift, C#, Go, Java, JavaScript, Python, and Ruby.  Not bad!
    - Protobufs are faster, simpler, safer, more compact, and more efficient than JSON and XML.
    - A Protobuf struct ("message") can be composed of primitive data types or user-defined messages.
    - The fields of a Protobuf message are explicitly and strongly typed.
    - Revisions to a Protobuf message are backward-compatible with earlier revisions.
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


## Persistent Data Interface
- The **Persistent Data Interface** ("PDI") is an abstraction for append-only storage shared by a PLAN community.  It stores all of a community's channel entries and is _cryptographically exclusive_ to its members.
- The PDI embraces an append-only model so that a wide range of replicating data types and distributed ledgers can be used as an implementation.  
- PDI transactions ("channel entries") are modeled as immutable and permanent (though content mutability is recreated virtually in PLAN's intermediate channel database layer).
- A conventional centralized shared database can also be used to implement the PDI, offering performance and convenience for small communities that are getting started.
- The PDI offers [portability](PLAN-Proof-of-Correctness.md#Proof-of-Storage-Portability), so a community could start with a centralized server for convenience/availability, and later migrate to a distributed ledger that scales down the road.
- In [go-plan](http://github.com/plan-tools/go-plan), the interface `StorageSession` in [StorageProvider.go](http://github.com/plan-tools/go-plan/blob/master/pdi/StorageProvider.go) is the heart of the PDI.



---

## Channel Protocols
- PLAN's general purpose channels are its workhorse and _raison d'être_.  Like files in a conventional operating system, users and productivity workflows in PLAN create new channels and new channel types all the time.  
- As a PLAN client UI interacts with a given channel, it does not use filename extensions, content-embedded markers, or blindly assume that content is in a particular form.   Both PLAN channel "epochs" and channel entries each embed a `plan.Block`, making each a flexible self-describing container for content and information.  _This offers profound interoperability in the way that HTTP headers also self-describe content for a HTTP response._

| Example Channel Descriptor | Expected Channel Entry Content Codecs | Example Client UI Experience  |
|----------------------|:--------------------:|--------------------------------------|
| `/plan/ch/chat`      |          `txt`\|`rtf`\|`image`      | A familiar "vertical scroller" where new entries appear in colored ovals at the bottom and previous entries vertically scroll upward to make room. |
| `/plan/ch/geoplot`   |         `cords+(txt`\|`image)`    | A map displays text and image annotations at each given geo-coordinate entry.  Clicking/Tapping on an annotation causes a box to appear displaying who made the entry and when. |
| `/plan/ch/file/pdf`  |            `ipfs`\|`binary`         | The client UI represents this file-revision channel as a single monolithic object. Tapping on it causes the most recent channel entry (interpreted as the latest revision) to be fetched and opened locally on the client using a PDF viewing application.  Power users can learn to open previous revisions of this "file". |
| `/plan/ch/file/audio`| `ipfs`\|`mpg`\|`aac`\|`ogg`\|`flac` | Like other PLAN "file" channels, this client UI displays this channel as a single object, where opening/activating it causes the most recent entry to be fetched and played using the default media player app or using PLAN's integrated AV player.  |  
| `/plan/ch/feed/rss`  |                 `xml`               | This channel is used to publish a sequence of text, audio, or video items with accompanying meta elements (e.g. title, link, thumbnail, and description).  This channel's epoch content `Block` houses [RSS](https://en.wikipedia.org/wiki/RSS) channel information while PLAN channel entries correspond to familiar RSS `item` elements in xml.  |
| `/plan/ch/feed/atom` |                 `xml`               | Similar to `feed/rss`, but PLAN channel entries instead conform to [Atom](https://en.wikipedia.org/wiki/Atom_(Web_standard)) xml. |
| `/plan/ch/calendar`  |          `text/ifb`\|`text/ics`     | The client UI presents a familiar visual calendar idiom containing events (entries) that are graphically rendered on the appropriate days and times. The user interacts with channel UI in real-time, scrolling from week to week, to day to day as the user zooms in "closer". |


### Custom Channel Protocols
- A community or organization may have a specific need and always has the option to design a custom channel content protocol that meets specialized needs.
    - A custom-designed channel protocol generally will need an accompanying custom channel GUI adapter so PLAN clients can interact with that channel type.
    - For example, a brewery uses sensor arrays to monitor temperatures all over a warehouse.  These sensors periodically write JSON data to a channel with a given custom channel type.  The brewery has its own channel GUI adapter "bound" to the custom channel channel type that displays the floor plan of the brewery and overlaid with color swaths visualizing the most recent temperature readings.  

---

## Channel GUI Adapters
- A channel's protocol identifier string corresponds to a matching channel GUI adapter or "driver" in the PLAN client.  Like a traditional hardware driver, a PLAN channel adapter is designed specifically to interface with a data consumer and producer having an established format and flow.
- When a user accesses/opens a channel in PLAN, the client starts a new instance of the channel module designed _for that specific type of channel_.  If multiple matching channel adapters are available, the client can choose based on user settings or can prompt the user to select one.
- A PLAN channel adapter is a C# class that lives in the Unity client. New adapter instances are passed a gRPC connection set up for a given channel `UUID`.
- A channel with type `/plan/ch/calendar`, could invoke the client's default `calendar` channel adapter _or_ instead use another that:
    - displays scheduled events on a horizontal timeline that extends from the past to the future,
    - displays scheduled events on geographically relevant map, _or_
    - overlays appointments from an outside calendar service.
- Users can choose alternate channel adapters in the way a media player offers alternate skins/UIs
- Developers that create and extend channel adapters can focus on the API or GUI, rather than infrastructure related tasks.

---

## Cloud File Interface
- The **Cloud File Interface** ("CFI") is an abstraction for [content-addressable storage](https://en.wikipedia.org/wiki/Content-addressable_storage), where files/content are referenced by hashname and are available across the community's network.  Unlike the PDI, content written to the CFI isn't necessarily intended to persist indefinitely (though it can).   
- The CFI provides scalable and expendable storage, serving a community's temporary and bulk storage needs.
- Distributed storage systems typically only replicate on-demand (e.g. BitTorrent), so CFI content tends to only consume local storage for users accessing that content.  This is in contrast to how entries posted to the PDI replicate to _every_ community node.
- "File" channels allow PLAN users to interact with files and trees in familiar ways, but under the hood each entry in the channel is a CFI pathname that points to a revision of the file or tree.  Since each revision pathname is _only_ a short string, these channels don't materially consume the community's permanent shared storage.  When a user opens/views this object, the PLAN client hands off the most recent channel entry (a CFI pathname) to the CFI layer for retrieval while the PLAN client graphically reports progress.
    - Conveniently, this helps the PLAN client manage the CFI for "free".  For a given file channel, once an entry containing a CFI item is superseded longer than some grace period (or any other expiration function), the referenced item can be safely and automatically "unpinned" (or more aggressively reclaimed).
    - At the PLAN client level, the user is not burdened or distracted with the details associated with managing the CFI.  The user never sees hashnames and requires zero knowledge about how the PDI and CFI are working together.  
- Consider a film production team using PLAN as a collaboration and file-sharing tool. Their workflow is to present scene cuts to the team for feedback and review. Instead of using the community's _permanent_ shared storage for short-term video files, the team uses a channel where posted files _appear_ in the channel and can be conveniently played.  However, under the hood, the PLAN client is posting the file to the CFI and placing a CFI pathname in the channel.  The channel is set so that files older than X days expire and are unpinned/deallocated.
- Like the PDI, the Cloud File Interface is designed to be pluggable, offer flexibility, and preserve portability.  Most organizations using PLAN will be happy with PLAN's reference CFI implementation using [IPFS](https://ipfs.io/), a capable peer-to-peer distributed storage system.  However, others may want to choose from other possibilities, such as [Dat](https://datproject.org/).  
- The CFI and PDI are architecturally disjoint, but a single storage layer could be used to implement both, provided it has the requisite capabilities.

---

## Secure Key Interface
- The SKI abstracts private key storage, private key handling, and offers support for third-party encryption and authentication systems.
- The SKI guarantees compartmentalization in PLAN, ensuring that private keys remain secure and reside "outside" of PLAN.


---

## Public Services 

A community using PLAN will inevitably be interested in making some of its parts accessible to the global public.  A PLAN node allows publicly accessible services to serve explicitly designated community content and scale (as a distributed system) alongside traditional web or internet services.  For example:
- A musical artist uses PLAN to serve show recordings and official releases. 
- A documentary production uses PLAN to serve the film's trailer and the full film to users bearing a the right token.
- A PLAN daemon periodically renders out an image of a map with spatial annotations from a community geo-space channel, served as an html page.
- A PLAN email gateway daemon bridges access to the members of a PLAN community and the outside world.  Unlike email, however, each incoming email contains an access token that the recipient previously issued the sender, effectively eliminating unsolicited messages ("spam").  Further, a sender who abuses their privileges (or loses or resells their token to a spammer), can be blocked without any concern of messages from _other_ senders being inadvertently filtered/blocked.


---

## Milestones

| Milestone |  Timeframe  | Description                                                                               |
|:---------:|:-----------:|-------------------------------------------------------------------------------------------|
|   [Newton](https://en.wikipedia.org/wiki/Isaac_Newton)  |   2018 Q2   | Permissions model [proof of concept](https://github.com/plan-tools/permissions-model)     |
|  [Babbage](https://en.wikipedia.org/wiki/Charles_Babbage)  |   2018 Q3   | PLAN [Proof of Correctness](PLAN-Proof-of-Correctness.md) complete                        |
|   [Morse](https://en.wikipedia.org/wiki/Samuel_Morse)   |   2018 Q4   | [go-plan](https://github.com/plan-tools/go-plan) command line proof of concept demo       |
|  [Mercator](https://en.wikipedia.org/wiki/Gerardus_Mercator) |   2019 Q1   | [plan-unity](https://github.com/plan-tools/plan-unity) preliminary proof of concept |                                       |
|   [Kepler](https://en.wikipedia.org/wiki/Johannes_Kepler)  |   2019 Q2   |  CFI ([IPFS](https://ipfs.io/)) integration   |
| [Fessenden](https://en.wikipedia.org/wiki/Reginald_Fessenden) |   2019 Q2   | Ethereum, DFINITY, Holochain, or other established DLT used for first PDI implementation |
|  [Lovelace](https://en.wikipedia.org/wiki/Ada_Lovelace) |   2019 Q3   | Installer and GUI setup experience for macOS                                              |
|   [Turing](https://en.wikipedia.org/wiki/Alan_Turing)  |   2019 Q3   | go-plan support and QA for Linux                                                          | 
|  [Galileo](https://en.wikipedia.org/wiki/Galileo_Galilei)  |   2019 Q4   | PLAN Systems internally replaces Slack with PLAN                                       |
| [Hollerith](https://en.wikipedia.org/wiki/Herman_Hollerith) |   2019 Q4   | Installer and GUI setup experience for Windows                                            | 
|   [Barton](https://en.wikipedia.org/wiki/Clara_Barton)  |   2020 Q1   | PLAN helps support [Art Community Builders](http://artcommunitybuilders.org/)             |
|     -     |    2020+    | PLAN expands support for other volunteer-run events                                       |


---
---


Back to [README](README.md)
