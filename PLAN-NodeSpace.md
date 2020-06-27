# PLAN NodeSpace Data Structure

```
         P.rivacy
         L.ogistics
         A.ccessibility
P  L  A  N.etworks
```

## What is a NodeSpace?

A NodeSpace a PLAN channel data schema that reflects a collection of abstract objects ("nodes") in relation to each other and nodes in other NodeSpaces.  Each node has a set of associated fields/parameters, including spatial coordinates and references ("links") to other nodes.  

## Channel Data Structure

The following tree structure defines the key/value storage schema for a NodeSpace channel.  Each `NodeID` and `LayerID` is presumed to be unique from other nodes and layers in the channel they reside in.  

```

NodeSpace Channel
|
|
/-- n/<NodeID>/<LayerID>/name               => user-specified node name
|   |                /uri[.<ident>]         => [[<uri>/n/]|.]<NodeID>/[<LayerID>|.]
|   |                /x[0-0xFF]             => positional/cord value
|   |                /id                    => seed/id/uuid/token
|   |                /sig                   => hash(id).sign(keypair[0-0xFF])
|   |                /.<user_field>         => user-specified string/value (UTF8)
|   |                /...
|   |
|   n/<NodeID>/<LayerID>/...
|   |                   /...
|   |
|   n/...
|
/-- l/<LayerID>/name                        => user-specified layer name
|              /cord_space                  => cord space type
|              /cord_unit                   => cord unit type
|              /color                       => layer color ("RRGGBB")
|              /index                       => layer index value (0, 1, 2..)
|
l/<LayerID>/...
|          /...
|
l/...

```
## Node Linking

Each `uri` field allows a node to link to any other node.  The linked node can reside in the same NodeSpace or an external NodeSpace specified by its channel URI.  A node may contain any number of links, allowing most network graphs to be represented.  The PLAN user interface offers node automated relationship visualization, offering users the ability to discern important information that may not otherwise be visible.


## Layers & Linking

A NodeSpace contains a set of node layers, each identified by a `LayerID`.  The default ("primary") node layer has an `index` value of 0 and is the implied layer when a node links to another node and no layer is specified.  By convention, the primary node layer defines each node's `name`, default target `uri`, and a coordinate position as applicable.  Additional node layers typically represent other contexts or representations of nodes (or node subsets).  

## Example NodeSpace

Consider a shared creative maker-space. A NodeSpace channel could be used for each equipment/work station.  The primary node layer could contain top-level information and contain a uri to a NodeSpace that presents a rich scene of information and links:

```
/l/11/name            => "Shop 101 Equipment Stations"
     /cord_space      => "cartesian/xy" 
     /cord_unit       => "length/meters"
     /index           => 0

/l/42/name            => "Training Coordinators"
     /index           => 1

/l/55/name            => "Power Distribution"
     /index           => 2

/n/73l6/11/name       => "2HP Drill Press"
          /uri        => "shop101/2hp-drill-welcome"
          /x0         => 33.0
          /x1         => 20.0
       /42/uri        => "shrugs-faculty/n/424323/."
       /55/uri        => "./8801/."

/n/8801/11/name       => "CrossFire Plasma Table"
          /uri        => "shop101/cf-plasma-welcome"
          /x0         => 10.0
          /x1         => 18.5
       /42/uri.0      => "shrugs-faculty/n/424323/."
          /uri.1      => "shrugs-TAs/n/12456/."
       /55/uri        => "shrugs-hall/n/NE-breaker-21-02"

/n/7110/11/name       => "Miller Plasma Cutter"
          /uri        => "shop101/miller-cutter-welcome"
          /x0         => 10.0
          /x1         => 30.0
       /42/uri        => "shrugs-faculty/n/12331/."
       /55/uri        => "./8801/."

```
