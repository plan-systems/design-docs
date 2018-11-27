# PLAN Applied

```
         P urposeful
         L ogistics
         A rchitecture
P  L  A  N etwork
```

A technology is only as interesting as how it can be harnessed and applied to our world.  

## Community Public Access 

A community using PLAN will inevitably be interested in making some of its parts accessible to the global public.  A PLAN node allows publicly accessible services to serve explicitly designated community content and scale (as a distributed system) alongside traditional web or internet services.  For example:
- A musical artist uses PLAN to serve show recordings and official releases. 
- A documentary production uses PLAN to serve the film's trailer and perhaps the full film itself to users bearing a "paid" token.
- A PLAN daemon periodically renders out an image of a map with spatial annotations from a community geo-space channel, served as an html page.
- A PLAN email gateway daemon bridges access to the members of a PLAN community and the outside world.  Unlike email, however, each incoming email contains an access token that the recipient previously issued the sender, effectively eliminating unsolicited messages ("spam").  Further, a sender who abuses their privileges (or loses or resells their token to a spammer), can be blocked without any concern of messages from _other_ senders being inadvertently filtered/blocked.

## Interoperable Data Structures

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
- Like other foundational data structures in PLAN, `plan.Block` is specified using [Protobufs](https://developers.google.com/protocol-buffers).  This means boilerplate serialization and network handling code can be [trivially generated](https://github.com/plan-tools/plan-protobufs) for most major languages and environments, including C, C++, Objective-C, Swift, C#, Go, Java, JavaScript, Python, and Ruby.  Not bad!
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

## Channel Protocols

- PLAN's general purpose channels are its workhorse and _raison d'être_.  Like files in a conventional operating system, users and productivity workflows in PLAN create new channels and new channel types all the time.  
- As a PLAN client UI interacts with a given channel, it does not use filename extensions, content-embedded markers, or blindly assume that content is in a particular form.   Both PLAN channel "epochs" and channel entries each embed a `plan.Block`, making each a flexible self-describing container for content and information.  _This offers profound interoperability in the way that HTTP headers also self-describe content for a HTTP response._

| Example Channel Descriptor | Expected Channel Entry Content Codecs | Example Client UI Experience  |
|----------------------|:--------------------:|--------------------------------------|
| `/plan/ch/talk`      |          `txt`\|`rtf`\|`image`      | A familiar "vertical scroller" where new entries appear in colored ovals at the bottom and previous entries vertically scroll upward to make room. |
| `/plan/ch/geoplot`   |         `cords + (txt`\|`image)`    | A map displays text and image annotations at each given geo-coordinate entry.  Clicking/Tapping on an annotation causes a box to appear displaying who made the entry and when. |
| `/plan/ch/file/pdf`  |            `ipfs`\|`binary`         | The client UI represents this file-revision channel as a single monolithic object. Tapping on it causes the most recent channel entry (interpreted as the latest revision) to be fetched and opened locally on the client using a PDF viewing application.  Power users can learn to open previous revisions of this "file". |
| `/plan/ch/file/audio`| `ipfs`\|`mpg`\|`aac`\|`ogg`\|`flac` | Like other PLAN "file" channels, this client UI displays this channel as a single object, where opening/activating it causes the most recent entry to be fetched and played using the default media player app or using PLAN's integrated AV player.  |  
| `/plan/ch/feed/rss`  |                 `xml`               | This channel is used to publish a sequence of text, audio, or video items with accompanying meta elements (e.g. title, link, thumbnail, and description).  This channel's epoch content `Block` houses [RSS](https://en.wikipedia.org/wiki/RSS) channel information while PLAN channel entries correspond to familiar RSS `item` elements in xml.  |
| `/plan/ch/feed/atom` |                 `xml`               | Similar to `feed/rss`, but PLAN channel entries instead conform to [Atom](https://en.wikipedia.org/wiki/Atom_(Web_standard)) xml. |
| `/plan/ch/calendar`  |          `text/ifb`\|`text/ics`     | The client UI presents a familiar visual calendar idiom containing events (entries) that are graphically rendered on the appropriate days and times. The user interacts with channel UI in real-time, scrolling from week to week, to day to day as the user zooms in "closer". |


## Cloud File Interface
- You are rightly unsettled if you think all the data in a PLAN community is stored on its append-only shared storage layer.  Recall that the Persistent Data Interface (PDI) abstracts the community-shared container that stores all the channels in a community.  The PDI is typically implemented using a replicated transaction log or blockchain, so entries are regarded as immutable and permanent.  However, this means it is not flexible enough to meet general-purpose client storage needs.
    - Consider a film production team using PLAN as a secure collaboration and file-sharing tool.  Suppose their post-production workflow is to render-out variations of scenes currently being edited for director review. It would be a waste to burn the community's _permanent_ shared storage to hold gigabytes of data that won't be used after a week.  Worse, a couple member nodes would be accessing this data (as _all_ data under the PDI replicates to each community node).
- So how is bulk data stored in PLAN if relying on the PDI is clearly the wrong choice?  Introducing the Cloud File Interface (CFI), whose purpose is to provide access to scalable but purgeable storage on-demand.  The CFI is an abstraction of [content-addressable storage](https://en.wikipedia.org/wiki/Content-addressable_storage), where content is referenced by hashname.  Unlike the PDI, content written to the CFI isn't necessarily intended to persist indefinitely (though it may).
- Each entry in a "file" channel represents a revision of a high-level file and is either an inline content blob or a CFI hashname.  In the latter case, each entry is _only_ a short string and doesn't consume material space on a community's permanent shared storage.  In the PLAN client, the channel appears as a single monolithic icon or animation.  When the user opens/views this object, the PLAN client hands off the most recent channel entry (a CFI pathname) to the CFI layer for retrieval.
    - Conveniently, this approach yields CFI garbage collection for "free".  For a given file channel, once an entry containing a CFI item is superseded longer than some grace period (or any other valuation calculus), the referenced item can be safely "unpinned" through the CFI.  
    - At the PLAN client level, the user is not burdened or distracted with the details and steps associated with accessing and managing the CFI.  This means the user never has to see hashnames or even understand how the PDI and CFI work together.  
- Like the PDI, the Cloud File Interface is designed to be pluggable, offer flexibility, and preserve portability.  Most organizations using PLAN will be happy with PLAN's reference CFI implementation using [IPFS](https://ipfs.io/), but others may want to choose from other possibilities, such as [Dat](https://datproject.org/).


---

## Milestones

| Milestone |  Timeframe  | Description                                                                               |
|:---------:|:-----------:|-------------------------------------------------------------------------------------------|
|   [Newton](https://en.wikipedia.org/wiki/Isaac_Newton)  |   2018 Q2   | Permissions model [proof of concept](https://github.com/plan-tools/permissions-model)     |
|  [Babbage](https://en.wikipedia.org/wiki/Charles_Babbage)  |   2018 Q3   | [PLAN Proof of Correctness](PLAN-Proof-of-Correctness.md) complete                        |
|   [Morse](https://en.wikipedia.org/wiki/Samuel_Morse)   |   2018 Q4   | [go-plan](https://github.com/plan-tools/go-plan) command line proof of concept demo       |
|  [Mercator](https://en.wikipedia.org/wiki/Gerardus_Mercator) |   2018 Q4   | PLAN architecture visualization exhibit in Unity                                          |
|   [Kepler](https://en.wikipedia.org/wiki/Johannes_Kepler)  |   2019 Q1   | [plan-unity](https://github.com/plan-tools/plan-unity) client proof of concept demo       |
| [Fessenden](https://en.wikipedia.org/wiki/Reginald_Fessenden) |   2019 Q2   | Ethereum, DFINITY, Holochain, or another established DLT used for next PDI implementation |
|  [Lovelace](https://en.wikipedia.org/wiki/Ada_Lovelace) |   2019 Q2   | Installer and GUI setup experience for macOS                                              |
|   [Turing](https://en.wikipedia.org/wiki/Alan_Turing)  |   2019 Q3   | go-plan support and QA for Linux                                                          | 
|  [Galileo](https://en.wikipedia.org/wiki/Galileo_Galilei)  |   2019 Q3   | PLAN Foundation internally replaces Slack with PLAN                                       |
| [Hollerith](https://en.wikipedia.org/wiki/Herman_Hollerith) |   2019 Q4   | Installer and GUI setup experience for Windows                                            | 
|   [Barton](https://en.wikipedia.org/wiki/Clara_Barton)  |   2020 Q1   | PLAN helps support [Art Community Builders](http://artcommunitybuilders.org/)             |
|     -     |    2020+    | PLAN expands support for other volunteer-run events                                       |


---
---


Back to [README](README.md)
