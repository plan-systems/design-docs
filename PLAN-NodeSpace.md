# PLAN NodeSpace Data Structure

```
         P.rivacy
         L.ogistics
         A.ccessibility
P  L  A  N.etworks
```

## What is a NodeSpace?

A NodeSpace is a PLAN channel data schema that reflects a collection of abstract objects ("nodes") in relation to each other and nodes in other NodeSpaces.  Each node has a set of associated fields/parameters, including spatial coordinates and references ("links") to other nodes.  

## Channel Data Structure

The following tree structure defines the key/value entry storage schema for a NodeSpace channel.  Each `NodeID` and `LayerID` is unique from other nodes and layers in the channel they reside in.  Other than what is required to adequately represent content structure, all key/value entries are optional.

```
l/<LayerID>/name                        => user-specified layer name
           /cord_space                  => cord space type
           /cord_unit                   => cord unit type
           /time_unit                   => time unit type
           /color                       => layer color ("RRGGBB")
           /index                       => layer index value (0, 1, 2..)
 
l/<LayerID>/...
           /...
 
...

n/<NodeID>/<LayerID>/name               => user-specified node name
                    /uri[.<ident>]      => [[<uri>/n/]|.]<NodeID>[/<LayerID>]
                    /x[0-9]             => positional cord value
                    /t                  => [start] time value
                    /t.end              => end time value
                    /.<user_field>      => user-specified value
                    /...
   
n/<NodeID>/<LayerID>/...
                    /...

...

```



## Node Linking

Each `uri` field allows a node to link to any other node.  The linked node can reside in the same NodeSpace or an external NodeSpace specified by its channel URI.  A node may contain any number of links, allowing most network graphs to be represented.  The PLAN user interface offers node automated relationship visualization, offering users the ability to discern important information that may not otherwise be visible.


## Layers & Linking

A NodeSpace contains a set of node layers, each identified by a `LayerID`.  The default ("primary") node layer has an `index` value of 0 and is the implied layer when a node links to another node and no layer is specified.  By convention, the primary node layer defines each node's `name`, default target `uri`, and a coordinate position as applicable.  Additional node layers typically represent other contexts or representations of nodes (or node subsets).  

## Example NodeSpaces

Consider a volunteer firefighter's network. A NodeSpace channel can be used to create an organizational map of personnel, positions, fire-stations, equipment maintenance, and current training status of each trainer and volunteer.  The primary node layer could contain top-level information and a uri to a NodeSpace that presents a rich scene of information and links, from the headquarters element all the way to a team responding to an on-scene emergency.  Another NodeSpace can be used to represent past fires that have been extinguished, along with detailed reports, chain of custody documentation, and lessons learned.

**NodeSpace uri `firestation7-eq`**
```
/l/11/name               => "Volunteer Fire Station 7"
     /cord_space         => "cartesian/xy" 
     /cord_unit          => "length/meters"
     /index              => 0

/l/30/name               => "Training Coordinators"
     /index              => 1

/l/55/name               => "On-site Power Distribution"
     /index              => 2

/l/60/name               => "On-Call & Ops Schedule"
     /index              => 3

/n/73l6/11/name          => "Lincoln 220 Cutter/Welder"
          /uri           => "station7/lincoln-220-welcome"
          /x0            => 33.0
          /x1            => 20.0
       /30/uri           => "station7-faculty/n/424323"
       /55/uri           => "station7-forum/n/NE-breaker-8-01"
       /60/uri           => "veterans-gallery/n/2020-1"

/n/7110/11/name          => "Emergency Dispatch"
          /uri           => "station7/dispatch"
          /x0            => 10.0
          /x1            => 30.0
       /30/uri           => "station7-operator/n/12331"
       /55/uri           => "./8801/."

/n/8801/11/name          => "Fire Engine #42 "
          /uri           => "station7/cf-plasma-welcome"
          /x0            => 10.0
          /x1            => 18.5
       /30/uri.0         => "station7-faculty/n/424323"
          /uri.1         => "station7-TAs/n/6456"
       /55/uri           => "station7-forum/n/NE-breaker-8-02"
       /60/uri           => "veterans-gallery/n/2020-2"

```

**NodeSpace uri `station7vets-gallery`**
```
/l/10/name               => "Station 7 Veterans Gallery"
     /time_unit          => "utc/seconds" 
     /index              => 0
     /.desc              => "Explore past service calls and experiences of Station 7 Veterans "

/l/30/name               => "Equipment Used"
     /index              => 1
     /.desc              => "Equipment used to respond each emergency"

/l/40/name               => "Rescue Response Map"
     /index              => 2
     /cord_space         => "earth-geospace/latlong" 
     /cord_unit          => "angle/degrees"
     /.desc              => "Experience Station 7 volunteer fire fighters working on-site"

/n/2020-1/10/name        => "Chief's Wall"
            /.desc       => "News and announcements from the Fire Chief" 
            /uri         => "firestation7/chiefs-wall-announce"
            /uri.author  => "chief-univ/n/17145"
            /t           => 1593266130
         /30/uri.0       => "firestation7-eq/n/73l6"
            /uri.1       => "firestation7-eq/n/7110"
         /40/x0          => 38.8931
            /x1          => 77.0458

/n/2020-2/30/name        => "That Others May Live"
            /.desc       => "Honoring the Veterans Fire Fighters that have come before us." 
            /uri         => "station7/history"
            /uri.author  => "station7-TAs/n/6456"
            /t           => 1592056593
         /30/uri.0       => "station7-eq/n/8801"
            /uri.1       => "station7-eq/n/73l6"
         /40/uri         => "acme-virtual-tours-321
            /x0          => 31.7683
            /x1          => -35.2137
            /t           => 1593216511
            /t.end       => 1655128530

```
