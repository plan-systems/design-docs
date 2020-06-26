# PLAN NodeSpace Data Structure

```
         P.rivacy
         L.ogistics
         A.ccessibility
P  L  A  N.etworks
```

## What is a NodeSpace?

A NodeSpace is the name given to a collection of objects ("nodes") in relation to each other where each node can have a set of associated fields/parameters, spatial coordinates, or references ("links") to other nodes.  Given that PLAN is a channel-based system, where each channel has an immutable channel protocol identifier assigned during channel genesis, a "NodeSpace" is a PLAN channel type whose entries conform to the types described in this document.  

## Channel Data Structure

The following represents the tree structure used to store a set of nodes.  Each `NodeID` and `LayerID` is presumed to be unique from all other nodes and layers in the channel and considered "local" to the channel they reside in.  

```

NodeSpace Channel
|
|
/-- n/<NodeID>/<LayerID>/name			=> user-specified node description (UTF8)
|	|		            /uri[.<ident>]	=> [[<uri>/n/]|.]<NodeID>/[<LayerID>|.]
|	|					/x[0-9]			=> positional/cord value
|	|					/.<user_field>	=> user-specified string/value (UTF8)
|	|					/...
| 	|
|	n/<NodeID>/<LayerID>/...
|	|					/...
|	|
|	n/...
|
|
/-- l/<LayerID>/name					=> user-specified node layer description (UTF8)
	|		   /cord_space				=> cord space type
	|		   /cord_unit				=> cord unit type
	|		   /index					=> int32 used to order NodeSpace layers
	|
	l/<LayerID>/...
	|		   /...
	|
	l/...

```

## Layers & Linking

A NodeSpace contains a set of explicit node layers identified by a `LayerID`.  The default ("primary") node layer has an `index` value of 0, meaning that any references (local or externally) to a given NodeID are resolved to the NodeSpace's primary node layer.   By convention, the primary node layer defines each node's `name`, default target `uri`, and a coordinate position as applicable.  Additional node layers typically represent other contexts or representations of nodes (or node subsets).  

## Example NodeSpace

Consider a creative maker-space for example. A NodeSpace channel could be used for each equipment/work area.  The primary node layer could contain top-level information and contain a uri to a NodeSpace that presents a rich scene of information and links. An additional layer called "Sign-Out" could contain a link for each 

```
/l/11/name			=> "Shop 101 Equipment Stations"
    /cord_space		=> "cartesian/xy" 
    /cord_unit		=> "length/meters"
	/index			=> 0

/l/42/name			=> "Training Coordinators"
	/index			=> 1

/l/55/name			=> "Power Source"
	/index			=> 2

/n/73l6/11/name		=> "2HP Drill Press"
		  /uri		=> "shop101/2hp-drill-welcome"
		  /x0		=> 33.0
		  /x1		=> 20.0
	   /42/uri  	=> "shrugs-faculty/n/424323/."
	   /55/uri 		=> "./8801/."

/n/8801/11/name		=> "CrossFire Plasma Table"
		  /uri		=> "shop101/cf-plasma-welcome"
		  /x0		=> 10.0
		  /x1		=> 18.5
	   /42/uri.0 	=> "shrugs-faculty/n/424323/."
	      /uri.1 	=> "shrugs-TAs/n/12456/."
	   /55/uri 		=> "shrugs-hall/n/NE-breaker-21-02"

/n/7110/11/name		=> "Miller Plasma Cutter"
		  /uri		=> "shop101/miller-cutter-welcome"
		  /x0		=> 10.0
		  /x1		=> 30.0
	   /42/uri   	=> "shrugs-faculty/n/12331/."
	   /55/uri 		=> "./8801/."

```
