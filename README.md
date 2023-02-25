# Gallery

## File structure

The main `data_file` Will have the information about:
- Each file name
- Date it was changed
- Size in bytes
- MD5 hash
- Associated tags

Example:
```json
{
    "~/Photos/photo1.jpg": {
        "st_size": 2759512,
        "st_mtime": 1217577012,
        "tags": [],
        "md5": "938c2cc0dcc05f2b68c4287040cfcf71",
    },
},
```

## Versioning
We cannot use git to store and version datafiles because we don't want to store customer data in a public git repo. We will keep files backups instead.

When the new version of `data_file` is saved, we are going to save a new `data_file_{n}.backup` where `n` is the maximum number of existing backup.

## Commit

Before actually writing date in the `data_file` we will collect it in the `Cache` object. `Cache` object will have `data_file` section which must be the exact copy of what we're about to write to the disk.

## Scan

The scan process is:
- If file within a folder ending with `_ignore` suffix we ignore it
- If we don't have file extension in `file_extensions.json` file we ignore it
- If the file is not in the database - then add it to the `new` section of the `Cache`
- If the file is already in database, we need to check:
  - If the file has the same `st_size` and `st_mtime` then we just skip it, but mark as `seen` in `Cache`
  - If not, we're adding it to `modified` section of `Cache`
