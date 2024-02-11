# gDrive Docs

Official documentation of the gDrive library.

[Basic guide](#basic-guide) should be enough for most of the library usages but there are also [Detailed guides](#detailed-guides) for the edge cases.

## Basic guide

Before starting the guide make sure to get [OAuth client ID credentials](https://developers.google.com/workspace/guides/create-credentials) and save the file as `credentials.json` inside the directory of the script using `gCredentials`. Okay, let's begin.

The most important thing to have in mind when working with this library is that every API call is **`lazy`**. Because of that some library usages have to be carefully programmed. For example when we are listing files(`files.list`) we can make as many API calls as we want because listing doesn't change the state of the drive, but the same isn't true for creating files(`files.create`).

There is a special method called `getFields` which allows us to get multiple data fields with only one API call thereby preventing multiple changes of state. This method is only to be used when we are working with a sensitive API call and want to get multiple data fields.

Let's take for example adding a file `myfile.mp4` from the current directory to the drive root directory.

```python
from gDrive import gDrive, gCredentials, Scopes
from gDrive.data import File

c = gCredentials([Scopes.Drive]).oauth2()
with gDrive(c) as drive:
    file_metadata_1 = File(
        name="video.mp4", description="This is the description of the video file"
    )
    # OR
    file_metadata_2 = File(
        (File.name, "video.mp4"),
        (File.description, "This is the description of the video file"),
    )
    file = drive.files.create("./myfile.mp4", file_metadata_2)
    print(file.id)
```

There is quite a bit of code there but the biggest focus should be on the last two lines. Because `files.create` changes drive state we had to be very careful when trying to get the fields of the response. Here we only needed the field `id` of the response file metadata so we could just write `file.id` and the library would make the API call `files.create` with the requested field `id`. If we required more, let's say the field `createdTime` we can't write `file.createdTime` because that would mean another API call which would attempt to add another file to the drive. In situations like these we use the method `getFields`.

The code also tries to demonstrate the two ways of creating gDrive.data entities(here the entity being `File`) which is why it is so verbose. First way is more concise but also more error prone because it requires the user to remember field names. In the second way if the entity's data structure ever changes the code will become invalid to the type checker which will make the debugging experience much less painful.

```python
from gDrive import gDrive, gCredentials, Scopes
from gDrive.data import File

c = gCredentials([Scopes.Drive]).oauth2()
with gDrive(c) as drive:
    file = drive.files.create(
        "./myfile.mp4",
        File(name="video.mp4", description="This is the description of the video file"),
    ).getFields(File.id, File.createdTime)
    print(file.id)
    print(file.createdTime)
```

The important takeaway here is that when we are using API calls that change state we should either get only a single field like `file.id` or call `getFields` with required fields but also only _ONCE_.

Below we will show a few more examples of using `getFields` to get a feel for the different types of usages. To avoid writing the imports and `gDrive` construction the code will only be partial, that is, it won't be executable.

1) Get all fields from `file`.

```python
file = drive.files.create("./myfile.mp4", File(name="video.mp4"))
file.getFields()
print(file.id, file.name, file.driveId, ...)
```

2) Get field from object inside `file`, object like `file.capabilities`.

```python
file = drive.files.create("./myfile.mp4", File(name="video.mp4"))
print(file.capabilities.canCopy)
```

3) Get all fields from object inside `file`.

```python
file = drive.files.create("./myfile.mp4", File(name="video.mp4"))
file.capabilities.getFields()
print(file.capabilities.canCopy, file.capabilities.canComment, ...)
```

4) Get multiple fields from object inside `file`.

```python
file = drive.files.create("./myfile.mp4", File(name="video.mp4"))
file.capabilities.getFields(File.Capabilities.canCopy, File.Capabilities.canDelete)
print(file.capabilities.canCopy, file.capabilities.canDelete)
```

5) Get fields from different parts of `file`.

```python
file = drive.files.create("./myfile.mp4", File(name="video.mp4"))
file.getFields(File.name, File.driveId, File.Capabilities(File.Capabilities.canDelete))
print(file.name, file.driveId, file.capabilities.canDelete)
```

6) Don't get any fields just execute the API call.

```python
from gDrive import execute

execute(drive.files.create("./myfile.mp4", File(name="video.mp4")))
```

7) Don't get any fields just execute the API call. There is a second simpler way but the static checker will complain.

```python
drive.files.create("./myfile.mp4", File(name="video.mp4")).execute()
```

To hammer the point home we will take an example of listing file in the root directory of the drive. Because we are using an API call that doesn't change the state of the drive we don't have to be careful about how we get fields. Of course if we wanted faster execution with less bandwidth usage then we should still try to minimize the amount of API calls.

The first example will have 3 API calls in total first requesting all files with just the `id` fields, then all files with just `name` fields and lastly all files with just `fileExtension` fields. Even though every API call fetches only one field, all previously requested fields are memorized inside the object so only the first access attempt will result in an API call.

```python
from gDrive import gDrive, gCredentials, Scopes, fq

c = gCredentials([Scopes.DriveReadonly]).oauth2()
with gDrive(c) as drive:
    for file in drive.files.list(q=fq().parents.Include("root"), orderBy=['name']).files:
        print(file.id)
        print(file.name)
        print(file.fileExtension)
        print(file.id)
```

The second example uses the `getFields` method which is why we will have only a single API call requesting all files with fields `id`, `name` and `fileExtension`. The speed will scale with the amount of fields requested, also you will save a lot of usage quota.

```python
from gDrive import gDrive, gCredentials, Scopes, fq

c = gCredentials([Scopes.DriveReadonly]).oauth2()
with gDrive(c) as drive:
    for file in drive.files.list(q=fq().parents.Include("root"), orderBy=['name']).files.getFields(File.id, File.name, File.fileExtension):
        print(file.id)
        print(file.name)
        print(file.fileExtension)
```

Finally, those with a keen eye will have observed that we are using an unknown class `fq`. The class helpes create file queries with the help of the type system. `files.list`'s method parameter `q` also accept a string as an argument so instead of using the `fq` class we could've written the same as "'root' in parents". For more information about queries check the [Detailed guides](#detailed-guides).


## Detailed guides

- API
    - [About](about.md)
    - [Changes](changes.md)
    - [Channels](channels.md)
    - [Comments](comments.md)
    - [Drives](drives.md)
    - [Files](files.md)
    - [Permissions](permissions.md)
    - [Replies](replies.md)
    - [Revisions](revisions.md)
    - [query](query.md)
- [Credentials](credentials.md)
- [CipherIO](cipherio.md)
- [Making your own service](gservice.md)
