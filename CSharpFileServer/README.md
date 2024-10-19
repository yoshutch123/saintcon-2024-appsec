# C# File Server

## Function
A web application that allows users to upload/download files.

## Vulnerabilities
There are 3 severe vulnerabilities:
- C#_EASY (in the file download function)
- C#_MODERATE
- C#_HARD

## In-scope files
- `Program.cs`

## Exclusions
- Don't try to add auth for file download. Should there be auth? Probably. But using UUIDs as filenames significantly reduces risk in that respect and there are other things to focus on here. I'm not going to make you write your own auth routine here.
- CSRF. What value is there in forcing someone else to upload a file by clicking a link?

