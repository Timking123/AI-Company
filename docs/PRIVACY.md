# Privacy and provenance

This is a public workflow kit. Its examples are fictional, and its operational
templates contain placeholders rather than real project records.

## What does not belong in the public kit

- Private project names, repositories, internal task registries, conversations,
  infrastructure addresses, account secrets, or absolute personal file paths.
- Working directories, local previews, caches, evaluation archives, or a copy
  of somebody's complete coding-assistant configuration.
- Private context imported from a project while adapting or testing the workflow.

The release review should inspect the files that Git will publish, reachable
history, text and binary assets, metadata, and generated archives. Checking only
the current README or running a keyword scanner is not an exhaustive privacy audit.

## What remains intentionally public

- The repository owner's public GitHub account, repository URLs, and commit
  identity. A GitHub noreply address avoids publishing a personal mailbox; it
  does not make a contribution anonymous.
- Official documentation links, fictional examples, and this project's own
  authorship and license information.
- The hero image's AI-origin information. The PNG retains C2PA content
  credentials, including generator information, timestamps, and image or
  manifest identifiers. These identify the image's provenance; they are not
  the operational task records used to run the workflow.

The hero has no conventional EXIF or PNG text chunks, but it is not a
zero-metadata image. Content credentials are retained to make its generated
origin clear. See [SOURCES.md](SOURCES.md).

## Checks have limits

`python scripts/validate.py` catches missing files, broken local references,
unsafe SVG structures, and some suspicious text patterns. It does not certify
anonymity, inspect every possible metadata field, detect steganography, or
audit a hosting platform's records. Review new material before each publication.

Keep real adoption records in the target project's approved private location.
When sharing a case study, use synthetic data or obtain the necessary consent
and sanitize the complete evidence, including image metadata and history.
