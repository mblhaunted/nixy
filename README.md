# pmpm
Poor Man's Package Manager
v0.0.1alpha

# Summary

PMPM let's you package anything, quickly.

PMPM is a set of tools around the nix package manager designed to make packaging simple and reliable. 

By taking advantage of Nix's deterministic package building, we can set dependencies with confidence.


# Requirements

Linux or OSX
Nix Package Manager
Python 3

# Usage

## Installing a package

```
./pmpm.py install package
```

## Uninstall a package
```
./pmpm.py uninstall package
```

Note; uninstall cleans up symlinks.

## Search a package
```
./pmpm.py search regex
```

### Interactive Mode

Interactive mode allows the user to fill in the details of their package by hand. This is useful for experimenting with builds before hand.

```
(pmpm) [m1001@wormhole]:[~/Documents/dev/git/pmpm]: ./pmpm.py package -p
[pmpm]: no pmpm directory exists, creating ...
[pmpm]: packaging from scratch ...
depends on? pkg,pkg:
package name: hi
package version: 0.0.1
source path or url: /package.tar.gz
short description: hi
long description: hi!
project url:
create symlinks? [y/n]: y
build steps? [y/n]: y
source: /package.tar.gz
you currently have 0 build steps
(a)dd, (e)dit, (d)elete, (c)ontinue: a
enter shell command: echo hello world
source: /package.tar.gz
you currently have 1 build steps
0: echo hello world
(a)dd, (e)dit, (d)elete, (c)ontinue: c
[pmpm]: 0: echo hello world
confirm? [y/n]: y
[pmpm]: creating new package hi in localrepo ...
[pmpm]: done writing package content ...
[pmpm]: updating localrepo registry to include new package ...
replacing old ‘hi-0.0.1’
installing ‘hi-0.0.1’
these derivations will be built:
  /nix/store/dq56lgg16yjjiyq8ixvqs6zp8w2jnyrv-hi-0.0.1.drv
building path(s) ‘/nix/store/qn6rsll7hm6j4cgw7nwqr1ijqjp4130j-hi-0.0.1’
hello world
building path(s) ‘/nix/store/40jbig1x7svx8a07hbxs9h4kqyi97xij-user-environment’
created 9 symlinks in user environment
warning: you did not specify ‘--add-root’; the result might be removed by the garbage collector
[pmpm]: fetched deriv dir /nix/store/dq56lgg16yjjiyq8ixvqs6zp8w2jnyrv-hi-0.0.1.drv for hi
[pmpm]: working directory for hi is: /nix/store/qn6rsll7hm6j4cgw7nwqr1ijqjp4130j-hi-0.0.1

```

That's it! You have a ready-to-go Nix package installed in your local repository.

Let's dive a little deeper.

>  depends on? pkg,pkg:

This line allows the user to specify other Nix packages for dependencies. Since the package is built in a deterministic env and hashed, you never have to worry about it changing.

> source path or url: /package.tar.gz

Here you specify your source code. This is ususally in an archive. You can specfy a local file, or a url.

> create symlinks? [y/n]: y

If enabled, symlinks will be created for you based on the actions you take in the build's "$out/" directory. 

For example ..

```
echo hi > $out/foo.txt 
```

This will end up symlinked to /foo.txt on your drive.

``` 
you currently have 0 build steps
(a)dd, (e)dit, (d)elete, (c)ontinue: a
enter shell command: echo hello world
source: /package.tar.gz
you currently have 1 build steps
0: echo hello world
(a)dd, (e)dit, (d)elete, (c)ontinue: c
[pmpm]: 0: echo hello world
confirm? [y/n]: y
```

The builder is where the magic happens. Note, you have a variable here that is "$out" which is your workspace. 

At the end of the build, your files are either written to your local nix path or also created as symlinks relative to your root path.

More on the builder later.

## JSON specification

In the examples/package.json, you can find a demonstration of how to specify a package. Currently, this is unsupprorted and interactive mode is recommended.
