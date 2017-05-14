# nixy
nixy v1.0.0

# Summary

nixy makes it easy to create and manage deterministic nix packages.

# Requirements

Linux or OSX<br/>
Nix Package Manager<br/>
Python 3<br/>

# Usage and Configuration

## Configuration

### sudo (optional, not recommended)

The application currently relies on sudo to implement symlinking to the root path.

It's recommended to configure your `/etc/sudoders` file to allow `NOPASSWD` for the following commands.

```
mkdir
ln
chown
rm  # for symlinks only
```

If symlinks is `true` the application will attempt to link on the root. Use `symlinks_home` to instead link to your home folder.


### Virtualenv

While not required, `virtualenv` and `virtualenvwrapper` are recommended to easily manage Python enviornments.

nixy requires nothing outside of python 3. It's recommended to use the following command to set up your nixy environemnt.

```
mkvirtualenv --python=python3 nixy
```

### First time run

nixy will complain if you don't have your NIX_PATH properly set to include your new local channel.

```
(nixy) [m1001@wormhole]:[~/Documents/dev/git/nixy]: ./nixy.py
[nixy]: WARNING: set proper NIX_PATH in profile!
export NIX_PATH=localpkgs=/Users/m1001/.nixy/localrepo/default.nix:$NIX_PATH
```

This needs to be configured in order to function properly.

nixy will also create a local nix channel, `localpkgs`, when it's called for the first time.

```
ls -l ~/.nixy/
[m1001@wormhole]:[~]: ls -l ~/.nixy/
total 0
drwxr-xr-x  4 m1001  wheel  136 Jan 18 13:04 localrepo
```

## Usage

### Installing a package

Installs search both `localpkgs` and `nixpkgs`.

Install a package

```
./nixy.py install package
```

Install a package and configure symlinks

```
./nixy.py install package -s
```

### Uninstall a package

```
./nixy.py uninstall package
```

Note; uninstall cleans up symlinks.

### Search a package

```
./nixy.py search regex
```

### Create a package

```
./nixy.py package [directory]
```

or

``` 
./nixy.py package -p   # interactive mode
```

## Packaging

### JSON specification

In the examples/package.json, you can find a demonstration of how to specify a package.

If you'd prefer to build without the interactive prompts, simply call nixy package and specify the location of your `package.json`.

```
./nixy.py package ./examples/
```

### Interactive Mode

Interactive mode allows the user to fill in the details of a package by hand.

```
(nixy) [m1001@wormhole]:[~/Documents/dev/git/nixy]: ./nixy.py package -p
[nixy]: no nixy directory exists, creating ...
[nixy]: packaging from scratch ...
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
[nixy]: 0: echo hello world
confirm? [y/n]: y
[nixy]: creating new package hi in localrepo ...
[nixy]: done writing package content ...
[nixy]: updating localrepo registry to include new package ...
replacing old ‘hi-0.0.1’
installing ‘hi-0.0.1’
these derivations will be built:
  /nix/store/dq56lgg16yjjiyq8ixvqs6zp8w2jnyrv-hi-0.0.1.drv
building path(s) ‘/nix/store/qn6rsll7hm6j4cgw7nwqr1ijqjp4130j-hi-0.0.1’
hello world
building path(s) ‘/nix/store/40jbig1x7svx8a07hbxs9h4kqyi97xij-user-environment’
created 9 symlinks in user environment
[nixy]: fetched deriv dir /nix/store/dq56lgg16yjjiyq8ixvqs6zp8w2jnyrv-hi-0.0.1.drv for hi
[nixy]: working directory for hi is: /nix/store/qn6rsll7hm6j4cgw7nwqr1ijqjp4130j-hi-0.0.1

```

That's it! You have a ready-to-go Nix package installed in your local repository.

Let's dive a little deeper.

>  depends on? pkg,pkg:

This line allows the user to specify other Nix packages for dependencies. Since the package is built in a deterministic env and hashed, you never have to worry about it changing.

> source path or url: /package.tar.gz

Here you specify your source code. This is ususally in an archive. You can specfy a local file, or a url.

> create symlinks? [y/n]: y

If enabled, symlinks will be created for you based on the actions you take in the build's `$out` directory. 

For example ..

```
echo hi > $out/foo.txt 
```

This will end up symlinked to `/foo.txt` on your drive.

``` 
you currently have 0 build steps
(a)dd, (e)dit, (d)elete, (c)ontinue: a
enter shell command: echo hello world
source: /package.tar.gz
you currently have 1 build steps
0: echo hello world
(a)dd, (e)dit, (d)elete, (c)ontinue: c
[nixy]: 0: echo hello world
confirm? [y/n]: y
```

At the end of the build, your files are either written to your local nix path or also created as symlinks relative to your root path.

## The Builder

There are three ways to specify a package's build steps, and the builder has some caveats that you need to be aware of.

1) Your source file is represented as `$src`<br/>
2) Your output directory is `$out`, and attempting to write to anything else will cause a build failure.<br/>

You need to take these factors into accoutn when composing your build steps.

### Interactive

Using the interactive prompt, you can specify the build steps you want.

```
you currently have 0 build steps
(a)dd, (e)dit, (d)elete, (c)ontinue: a
enter shell command: echo hello world
source: /package.tar.gz
you currently have 1 build steps
0: echo $src  # this would echo back the source file
(a)dd, (e)dit, (d)elete, (c)ontinue: c
[nixy]: 0: echo $src  # this would echo back the source file
confirm? [y/n]: y
```
### JSON

In examples/package.json, we see how to add build steps.

```
{
    "depends": {
    },
    "version": "0.0.1",
    "name": "nixy",
    "src": "/package.tar.gz",
    "src_sha256": "default",
    "meta": {
        "desc": "nixy",
        "long_desc": "nixy!",
        "homepage": "default"
    },
    "bld": {
        "steps": true,
        "script": ["ls -l", "ls -l $src"],
        "fp": "./builder.sh"
    },
    "symlinks": true,
    "symlinks_home": true
}
```

This will run each build step listed in the "script" array.

### Shell script

If you wish to call a script for the build to include in your source packages, simply specify the name of the script with the path. 

```
./builder.sh
```
## Symlinks

By default, nix packages are built into a deterministic workspace. This writes to a hidden nix directory on the user's path. 

Suppose you'd like to "install" your application to `/usr/bin/local`. This is where symlinks come in handy.

A quick example follows.

```
mkdir -p $out/usr/bin/local
echo foo > $out/usr/bin/local/foo.txt
```

With symlinks enabled, this build will place foo.txt in /usr/bin/local and it will be owned by the user who launched the process.
