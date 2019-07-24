# Setup

This document describes how to set up a PLAN development environment.

* [Contributing to PLAN](#contributing-to-plan)
  * [Contributing to a PLAN component](#contributing-to-a-plan-component)
  * [Developing a new PLAN component in Go](#developing-a-new-plan-component-in-go)
* [Advanced](#advanced)
  * [Creating a Multi-Repo Workspace](#creating-a-multi-repo-workspace)
  * [Developing new server-side language bindings](#developing-new-server-side-language-bindings)


## Contributing to PLAN

PLAN uses Go modules, so you must be using Go version 1.11 or above and you must not have a `GOPATH` set. Nor should you clone PLAN repos you're working on into `~/go/src`. Each of PLAN's repos contains a Makefile to test and build.


### Contributing to a PLAN component

The easiest way to contribute to PLAN is to provide bugfixes or new features for an existing PLAN component.

First, click the "Fork" button on GitHub for the project you want to work on. Then clone your fork locally to wherever you'd like to work.

```
cd ~/src/PLAN  # or wherever you'd like to work
git clone git@github.com:<your name>/plan-pdi-local.git
```

Once you've done so, you can use Makefile targets to test, build, or cross-compile for distribution.

```
make check    # lint and test
make build    # build for your architecture
make release  # build for all supported architectures and create tarballs
```

When you're ready to contribute your changes back, open a Pull Request on the project.


### Developing a new PLAN component in Go

If you want to create a brand new PLAN component written in Go (such as a new PDI provider), you'll want to use [`plan-core`](https://github.com/plan-systems/plan-core).

Create your new repo and initialize the Go modules system:

```
git init my-component
cd my-component
go mod init
```

Then import the specific subpackages you'll need for your application:

```go
import (
	"github.com/plan-systems/plan-core/pdi"
	"github.com/plan-systems/plan-core/plan"
	"github.com/plan-systems/plan-core/tools/ctx"
)
```


## Advanced


### Creating a Multi-Repo Workspace

If you are working on a large feature that might have cross-repository concerns, you should set up a Multi-Repo Workspace. This is how the core PLAN team sets up their workspace. This workspace will have the PLAN repositories cloned side-by-side somewhere on your file system, and only use Go modules support for third-party dependencies.

```
cd ~/src/PLAN  # or wherever you'd like to work

# clone the set of repos you'd like to work with
for repo in {plan-client-phost,plan-core,plan-pdi-local,plan-pnode,plan-protobufs};
do
    git clone git@github.com:plan-systems/${repo}.git
done
```

Now we're ready to work on a specific project. Each project has a Makefile target `make hack`, which uncomments the `replace` directives in the `go.mod` file so that the cross-repo dependencies point to the repo you have on your file system instead of the one on GitHub. The Make target also tells git to ignore changes to `go.mod` and `go.sum`.

```
cd plan-pdi-local
make hack
```

When we're done, we can `make unhack` to comment-out the `replace` directives and tell git to stop ignoring changes to `go.mod` and `go.sum`.


### Developing new server-side language bindings

PLAN uses [protobufs](https://developers.google.com/protocol-buffers/) for communication between components. The protobufs are defined in the [`plan-protobufs`](https://github.com/plan-systems/plan-protobufs) repo. This allows you to write a PLAN component in any language.

Currently the PLAN team is building all server components in [Go](https://golang.org/). The core functions for PLAN in Go are defined in the [`plan-core`](https://github.com/plan-systems/plan-core) repo. If you wanted to build a component in another language, you could use the protobufs in `plan-protobufs` to create your own language bindings and implement the functionality in `plan-core` as a community project.
