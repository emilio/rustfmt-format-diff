# `rustfmt-format-diff`

This is a small python script, in the spirit of
[`clang-format-diff`][clang-format-diff], that takes care of reading a diff, and
running `rustfmt` with the `--file-lines` option appropriately.

This is intended to allow projects to incrementally adopt rustfmt, without
massive patches.

## Usage

To format your last git commit, for example:

```
$ git diff HEAD~ | python rustfmt-format-diff.py -p 1
```

## Known issues

Right now this is pretty much as fine-grained as it could be, but rustfmt isn't
(see <https://github.com/rust-lang-nursery/rustfmt/issues/1835>).

With that fixed, the idea is to use it in bindgen, and then ideally Servo, to
get consistent formatting across the board without much disruption. Ideally even
as a commit hook.

[clang-format-diff]: https://clang.llvm.org/docs/ClangFormat.html#script-for-patch-reformatting
