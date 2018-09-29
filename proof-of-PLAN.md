###Features

http://plan.tools


Let **UUID** represent a fixed-length pseudo-randomly generated ID that ensures no human-reasonable chance of collision (typically 20 to 32 bytes).

Let **σ** be the average time period it takes for replicated network messages to reach 2/3 of the network's nodes.  This lets us set a reasonable upper-bound on how long permissions changes in **C** take to propigate.  If we were to wait 100 or 1000 times **σ**, it would be safe to assume that any nodes able to receive a replicated message would have recieved it (if it was possible).  We thus express a time delay ceiling of permissions propigation as **kσ**.  Above this time, we assume there it is not beneficial to wait and hope that a newly arrived message will resolve a confict.  We therefore must establish a determinisitc set of rules to resolve all possible **CRS** conflicts.  For a network of 10,000 nodes in the internet of 2018, a reasonable value for **kσ** could be 3-12 hours.  After this point, nodes not yet reached can effecvtively regarded as being offline.


in an information network where it would be "unusual" for a replicated network message to have not been replicated across the network.  In other words, i

A founding set of community organizers ("admins") wish to form **C**, a digital community.  **C** is characterized by a set of community members, one or more positioned to administer member permissions. On each community node, the members of **C** agree to employ **L<sub>C</sub>**, an append-only [CRDT](https://en.wikipedia.org/wiki/Conflict-free_replicated_data_type) whose data transactions are to be considered "in the clear" to potential adversaries.  Network nodes in **C**  

The members of **C** wish to assert that:
   1. All communication within and between members of **C** is:
        a) informationally maximally opaque, and
        b) secure from all other actors *not* in **C**.
   2. Adding new members to **C** incurs no significant additional security liabilty on the infrastructure.
   3. Within **C**, each node's "community repo state" (**CRS**) converges to a stable/monotonic state as network connectivity "catches up", for any set of network traffic delivery conditions (natural or adversarial).
   4. Members can be de-listed from **C** such they no longer have access to the **CRS** after **kσ** amount of time.


The members of **C** devise the following infrastructure:
   - All data entries on **L<sub>C</sub>** are encrypted using keys located on **[K]<sub>C</sub>**, the "community keyring"
   - Encrypted, entries on **L<sub>C</sub>** are serialized from:
```
   type EntryCrypt struct {
       CommunityKeyID   UUID        // Community key used to encrypt .HeaderCrypt
       HeaderCrypt      []byte      // := Encrypt(<EntryHdr>.Marshal(), <EntryCrypt>.CommunityKeyID)
       ContentCrypt     []byte      // := Encrypt(<Body>.Marshal(), <EntryHdr>.ContentKeyID)
       Sig              []byte      // := CalcSig(<EntryCrypt>.Marshal(), GetKey(<EntryHdr>.AuthorMemberID,
                                    //                                           <EntryHdr>.AuthorMemberEpoch))
   }
```
   - Decrypted, each entry is specified to be appended to a virtual channel:
    ```
    type EntryHeader struct {
        EntryOp             EntryOp // Specifies how to interepret this entry.  Typically POST_CONTENT
        TimeSealed          int64   // Unix timestamp of when this header was encrypted and signed.
        ChannelID           UUID    // "Channel" that this entry is posted to.
        ChannelEpoch        UUID    // Epoch of this channel in effect when this entry was sealed
        AuthorMemberID      UUID    // Creator of this entry (and signer of EntryCrypt.Sig)
        AuthorMemberEpoch   UUID    // Epoch of the author's identity when this entry was sealed
        ContentKeyID        UUID    // Specifies key used to encrypt EntryCrypt.BodyCrypt
    }
    ```
   - Each member of **C** maintains possession of the community keyring **[K]<sub>C</sub>**, such that:
        - **[K]<sub>C</sub>** is set of keys that encrypts and decrypts **C**'s message traffic to/from **L**
        - A newly generated community key is distributed to **C**'s members via a persistent data channel using asymmetric encryption (a community admin )
   - **C**'s "member registry channel" is defined as a log containing each member's UUID and current crypto "epoch"
   - **C**'s root "access control channel" (ACC) is a log containing access grants to member ID

An actor is said to have access to "in" **C** if and only if she possesses the communit  
Their intention is to assert that:
   1. All communication between members in **C** is informationally opaque and secure from all actors *not* in **C**.
   2. Additional new members can be invited into **C** at any time
   3. The community's data store replicates across members of **C** such that 
        a.  bl
        b.  ggf 



```
// EpochInfo implies a linked list of epochs extending from the past to the present
type EpochInfo struct {
	EpochStart            timestamp
	EpochID               UUID
	PrevEpochID           UUID
	EpochTransitionSecs   int
}
// MemberEpoch represents a public "rev" of a community member's crypto
type MemberEpoch struct {
	EpochInfo             EpochInfo
	PubSigningKey         []byte
	PubCryptoKey          []byte
}
// ChannelEpoch represents a "rev" of Channel's most sensitive properties
type ChannelEpoch struct {
	EpochInfo             EpochInfo
	ChannelProtocol       string        // If access control channel: "/chType/ACC", else: "/chType/client/*"
	ChannelID             UUID          // Immutable; set at channel genesis
	AccessChannelID       UUID          // This channel's ACC (and conforms to an ACC) 
}
type CommunityMember struct {
    CommunityID           UUID          // Assigned 
	MemberID              UUID                     // Issued when member joins C
	type KeyRepo struct {
		CommunityKeyring  []KeyEntry
		PersonalKeyring   []KeyEntry
	}
}
```
Let **St** be an append-only p2p replicating data store, where new data blobs can be appended and subsequently retrieved (via a transaction ID).  A node's particualar state of **St**

Let 

Let **Ac** be one or more members of **C** that are designated admins and are charged with moderating and orgranizing community dats 


type CommunityMember := `


**Table of Contents**

[TOCM]

[TOC]

#H1 header
##H2 header
###H3 header
####H4 header
#####H5 header
######H6 header
#Heading 1 link [Heading link](https://github.com/pandao/editor.md "Heading link")
##Heading 2 link [Heading link](https://github.com/pandao/editor.md "Heading link")
###Heading 3 link [Heading link](https://github.com/pandao/editor.md "Heading link")
####Heading 4 link [Heading link](https://github.com/pandao/editor.md "Heading link") Heading link [Heading link](https://github.com/pandao/editor.md "Heading link")
#####Heading 5 link [Heading link](https://github.com/pandao/editor.md "Heading link")
######Heading 6 link [Heading link](https://github.com/pandao/editor.md "Heading link")

##Headers (Underline)

H1 Header (Underline)
=============

H2 Header (Underline)
-------------

###Characters
                
----

~~Strikethrough~~ <s>Strikethrough (when enable html tag decode.)</s>
*Italic*      _Italic_
**Emphasis**  __Emphasis__
***Emphasis Italic*** ___Emphasis Italic___

Superscript: X<sub>2</sub>，Subscript: O<sup>2</sup>

**Abbreviation(link HTML abbr tag)**

The <abbr title="Hyper Text Markup Language">HTML</abbr> specification is maintained by the <abbr title="World Wide Web Consortium">W3C</abbr>.

###Blockquotes

> Blockquotes

Paragraphs and Line Breaks
                    
> "Blockquotes Blockquotes", [Link](http://localhost/)。

###Links

[Links](http://localhost/)

[Links with title](http://localhost/ "link title")

`<link>` : <https://github.com>

[Reference link][id/name] 

[id/name]: http://link-url/

GFM a-tail link @pandao

###Code Blocks (multi-language) & highlighting

####Inline code

`$ npm install marked`

####Code Blocks (Indented style)

Indented 4 spaces, like `<pre>` (Preformatted Text).

    <?php
        echo "Hello world!";
    ?>
    
Code Blocks (Preformatted text):

    | First Header  | Second Header |
    | ------------- | ------------- |
    | Content Cell  | Content Cell  |
    | Content Cell  | Content Cell  |

####Javascript　

```javascript
function test(){
	console.log("Hello world!");
}
 
(function(){
    var box = function(){
        return box.fn.init();
    };

    box.prototype = box.fn = {
        init : function(){
            console.log('box.init()');

			return this;
        },

		add : function(str){
			alert("add", str);

			return this;
		},

		remove : function(str){
			alert("remove", str);

			return this;
		}
    };
    
    box.fn.init.prototype = box.fn;
    
    window.box =box;
})();

var testBox = box();
testBox.add("jQuery").remove("jQuery");
```

####HTML code

```html
<!DOCTYPE html>
<html>
    <head>
        <mate charest="utf-8" />
        <title>Hello world!</title>
    </head>
    <body>
        <h1>Hello world!</h1>
    </body>
</html>
```

###Images

Image:

![](https://pandao.github.io/editor.md/examples/images/4.jpg)

> Follow your heart.

![](https://pandao.github.io/editor.md/examples/images/8.jpg)

> 图为：厦门白城沙滩 Xiamen

图片加链接 (Image + Link)：

[![](https://pandao.github.io/editor.md/examples/images/7.jpg)](https://pandao.github.io/editor.md/examples/images/7.jpg "李健首张专辑《似水流年》封面")

> 图为：李健首张专辑《似水流年》封面
                
----

###Lists

####Unordered list (-)

- Item A
- Item B
- Item C
     
####Unordered list (*)

* Item A
* Item B
* Item C

####Unordered list (plus sign and nested)
                
+ Item A
+ Item B
    + Item B 1
    + Item B 2
    + Item B 3
+ Item C
    * Item C 1
    * Item C 2
    * Item C 3

####Ordered list
                
1. Item A
2. Item B
3. Item C
                
----
                    
###Tables
                    
First Header  | Second Header
------------- | -------------
Content Cell  | Content Cell
Content Cell  | Content Cell 

| First Header  | Second Header |
| ------------- | ------------- |
| Content Cell  | Content Cell  |
| Content Cell  | Content Cell  |

| Function name | Description                    |
| ------------- | ------------------------------ |
| `help()`      | Display the help window.       |
| `destroy()`   | **Destroy your computer!**     |

| Item      | Value |
| --------- | -----:|
| Computer  | $1600 |
| Phone     |   $12 |
| Pipe      |    $1 |

| Left-Aligned  | Center Aligned  | Right Aligned |
| :------------ |:---------------:| -----:|
| col 3 is      | some wordy text | $1600 |
| col 2 is      | centered        |   $12 |
| zebra stripes | are neat        |    $1 |
                
----

####HTML entities

&copy; &  &uml; &trade; &iexcl; &pound;
&amp; &lt; &gt; &yen; &euro; &reg; &plusmn; &para; &sect; &brvbar; &macr; &laquo; &middot; 

X&sup2; Y&sup3; &frac34; &frac14;  &times;  &divide;   &raquo;

18&ordm;C  &quot;  &apos;

##Escaping for Special Characters

\*literal asterisks\*

##Markdown extras

###GFM task list

- [x] GFM task list 1
- [x] GFM task list 2
- [ ] GFM task list 3
    - [ ] GFM task list 3-1
    - [ ] GFM task list 3-2
    - [ ] GFM task list 3-3
- [ ] GFM task list 4
    - [ ] GFM task list 4-1
    - [ ] GFM task list 4-2

###Emoji mixed :smiley:

> Blockquotes :star:

####GFM task lists & Emoji & fontAwesome icon emoji & editormd logo emoji :editormd-logo-5x:

- [x] :smiley: @mentions, :smiley: #refs, [links](), **formatting**, and <del>tags</del> supported :editormd-logo:;
- [x] list syntax required (any unordered or ordered list supported) :editormd-logo-3x:;
- [x] [ ] :smiley: this is a complete item :smiley:;
- [ ] []this is an incomplete item [test link](#) :fa-star: @pandao; 
- [ ] [ ]this is an incomplete item :fa-star: :fa-gear:;
    - [ ] :smiley: this is an incomplete item [test link](#) :fa-star: :fa-gear:;
    - [ ] :smiley: this is  :fa-star: :fa-gear: an incomplete item [test link](#);
            
###TeX(LaTeX)
   
$$E=mc^2$$

Inline $$E=mc^2$$ Inline，Inline $$E=mc^2$$ Inline。

$$\(\sqrt{3x-1}+(1+x)^2\)$$
                    
$$\sin(\alpha)^{\theta}=\sum_{i=0}^{n}(x^i + \cos(f))$$
                
###FlowChart

```flow
st=>start: Login
op=>operation: Login operation
cond=>condition: Successful Yes or No?
e=>end: To admin

st->op->cond
cond(yes)->e
cond(no)->op
```

###Sequence Diagram
                    
```seq
Andrew->China: Says Hello 
Note right of China: China thinks\nabout it 
China-->Andrew: How are you? 
Andrew->>China: I am good thanks!
```

###End
