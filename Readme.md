
# massren

massren is a tool that allows you to rename multiple files using your text editor. Everybody needs batch renaming at some point and there're loads of external tools available out there, but all of them have interfaces that you need to understand.

With massren, you just use your text editor (and all it's amazing features) for doing the renaming.

The tool works by creating a file that contains the filenames of the target directory, and opening this file in your text editor. You can then modify the filenames as you like. Once done, save the text file and your files will be renamed.

<!-- ![Massren usage animation](https://raw.github.com/laurent22/massren/animation/animation.gif "Massren usage animation") -->

## Future features

* Recursive folder listsings
    - With max depth: `massren -d1R`

* Functionality
    - Everything that massren does
    - Handle Conflicts

* Show Relative Path

* Order files by
    - -o
    - recently modified `-om`

* Re-open text file on conflicts

* Amazing Demo GIF

## features (others)

- [ ] Undo renames
- [ ] send2trash
- [ ] Configuration file
- [ ] Prompt before executing each action?
    - `rm -i` style
- [ ] Unit tests?

## Prior Art

> Imitation is the sincerest form of flattery - Oscar Wilde

* This is heavily inspired (read: copied feature-by-feature) from [laurent22/massren](https://github.com/laurent22/massren/) which is written in Golang. I'd been using it for an year now, and contributed a [small feature](https://github.com/laurent22/massren/commit/d87946ceae6bb1d080379855fa0c80e276831337) to it, but now I wanted [some](https://github.com/laurent22/massren/issues/30) [more](https://github.com/laurent22/massren/issues/28) things and tried adding those features, but Go really isn't my thing.

* There's also atleast 2 perl scripts: [vidir](https://github.com/trapd00r/vidir) & [movedit](http://www-wjp.cs.uni-sb.de/leute/private_homepages/mah/Homepage/MoveEdit.html) that do similar things.
