# Keyword Registry Server (KRS)

Keyword Registry Server is the backend for the Keyword Registry Platform (KRP)

# Table of Contents

1. [Table of Contents](#table-of-contents)
2. [Background](#background)
3. [Installation](#installation)
4. [Entity](#entities)
5. [API](#apis)

## Background

### Problem

In documentations, it is common to have one of the following characteristics in writing:

1. Assumptions on the pre-requisite knowledge of readers
2. The use of words that require context for understanding

These characteristics hinder the ability of readers to understand the topic.

### Proposed solution

For avoidance of doubt, the goal is to allow maintainers to define `keywords`.

`Keywords` are any of \[acryonym | word | phrase\]
that require some pre-requisite knowledge or context for understanding.

## Installation

### Local development

1. On a terminal, run `make local-compose`
2. On another terminal, run `make install` followed by `make dev`

### Updating dependencies

1. Add the new dependency via `pip install <your dependency>`
2. Run `make pipreqs` to update `requirements.txt`

## Entity

### User

A `User` is a user of Keyword Registry Platform (KRP).

```
User {
    ID: string!
    Username: string!
    Password: string!
    IsVerified: boolean!
    CreatedAt: string!
    UpdatedAt: string
    DeletedAt: string
}
```

### Project

A `Project` is used to group a set of `Keywords`

> One `User` can own have `Project`s (one-to-many)

```
Project {
    ID: string
    Name: string
    OwnerID: string
    CreatedAt: string
    UpdatedAt: string
    DeletedAt: string
}
```

### Keyword

A `Keyword` is a user's definition of a \[acryonym | word | phrase\]

> One `Project` can have many `Keyword`s (one-to-many)

```
Keyword {
    ID: string
    ProjectID: string
    Keyword: string
    Definition: string
    Context: string
    Links: string
    State: 'pending' | 'approved'
}
```

### Vote

A `Vote` can be an upvote or downvote of a `Keyword`

> One `Keyword` can have many `Vote`s (one-to-many)

> One `User` can have many `Vote`s (one-to-many)

```
Vote {
    ID: string
    UserID: string
    KeywordID: string
    Direction: 0 | 1
}
```

## API

WIP
