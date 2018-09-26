# PLAN - Engineering & Design Docs

```
         P urposeful
         L ogistics
         A rchitecture
P  L  A  N etwork

Welcome to PLAN!

PLAN is a secure, visual communications and logistics planning tool for individuals and organizations.
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


PLAN can't be empowering for community organizers if its not usable by non-technical users.  Yet, we know distributed systems, content-based
addressing, and cryptography are alien concepts to most people.  PLAN How does PLAN square this circle?

PLAN secret weapon is hidden in plain sight: instead of relying on 2D-constrained and sandboxed web/browser experience, PLAN uses the [Unity](https://unity3d.com) game engine to power the end-user experience while using [Go](https://golang.org) for its p2p node.  

For the end-user, this affords:
   - A realtime, visual, and spatially-oriented interface
   - A first-class input and display device experience
   - Full horsepower of the user's device/workstation
   - Multi-platform support

For PLAN, this offers: 
   - The power and capabilities of Go
   - A effective and robust multi-platform p2p node
   - Embedding of key technologies such as [IPFS](https://github.com/ipfs), [libp2p](https://github.com/libp2p), [protobufs](https://developers.google.com/protocol-buffers), and [gRPC](https://grpc.io).

The PLAN Unity client talks to a `pnode`, the name for PLAN's p2p client-serving node.  `pnode` is a daemon written in Go that serves PLAN clients while replicating community data across the community's swarm of pnodes.  

What defines a community?  In PLAN, a community is designed to reflect the human relationships that make up a community, weather that's a household, neighborhood watch, off-the-grid farm, maker-space, artist collective, or gaming group.  That is, each member in a community holds the community keyring (in addition to their private keys for that community).  In effect, the entire community's network traffic and infrastructure is inaccessible to all others, providing a fundamental bubble of cryptographic safety.  For a community member, their pnodes have the keys necessary to exchange traffic and data with other community members.


PLAN is a p2p community-centric node operating layer, built on top of an open append-only and content-based addressing storage API, 
accessed by a real-time graphical client.  


## Table of Contents
 [01. Synopsis](https://github.com/plan-tools/engineering-docs/01-synopsist)

---


