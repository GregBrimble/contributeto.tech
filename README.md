# [contributeto.tech](https://contributeto.tech/)
Built for [HackUPC](https://hackupc.com/) 2018 by [Greg Brimble](https://gregbrimble.com/) and [James O'Donnell](https://www.james-odonnell.com/).

## Inspiration
When looking to get involved with the open source community, the first challenge is finding a project to contribute to. This can be a non-trivial task:
* some old repositories get abandoned and their maintainers disappear,
* some projects aren't setup to be able to accept outside help,
* 'trending' and 'popular' repositories which are often promoted on the homepage of GitHub etc., are not generally very personalised
* these repositories are often promoted for use, rather than for contribution to, so don't consider current open issues, contribution policies and licenses etc.

## What it does
[contributeto.tech](https://contributeto.tech/) recommends both specific repositories, and their open issues, to users interested in contributing to open source. It analyses a user's history with programming languages and topics, and searches GitHub in realtime for similar repositories. By showing targeted repositories and issues, [contributeto.tech](https://contributeto.tech/) reduces the bridge to the user creating their first pull request.

## How we built it
[Greg Brimble](https://gregbrimble.com/) and [James O'Donnell](https://www.james-odonnell.com/) are both full-stack engineers, who have worked together on a number of projects in the past. [Greg](https://gregbrimble.com/) primarily worked on the backend application and infrastructure setup, and [James O'Donnell](https://www.james-odonnell.com/), primarily on the frontend, but both lent a hand to the other when needed.

## Challenges we ran into
OAuth never _Just Works_.

## Accomplishments that we're proud of
We managed to create an aesthetic, polished proof-of-concept well within the timelimit, and had enough energy to begin investigating some extra features.

## What we learned
We originally wanted to investigate using a new package, [Responder](https://python-responder.org/en/latest/), but ran in to difficulties with its setup, so had to leave it for another time. We both further improved our web development skills, re-affirming learning in [Python](https://www.python.org/), [Flask](http://flask.pocoo.org/), [Angular JS](https://angularjs.org/), and [Bootstrap](https://getbootstrap.com/).

## What's next for contributeto.tech
More features:
* Better repository and issue suggestions for a user. GitHub have been expanding on their [security alerts for vulnerable dependencies](https://help.github.com/articles/about-security-alerts-for-vulnerable-dependencies/#githubs-security-alerts-for-vulnerable-dependencies), which actively scrapes a repository's dependencies, looking at the technologies and frameworks it uses. If [contributeto.tech](https://contributeto.tech/) could either connect to, or implement its own version of this, it would be possible to better refine suggestions by filtering on individual projects that a user has experience with.
* More user exposed controls in the application, allowing the user to refine and/or search the suggested issues (e.g. sorting by old to new, popular etc.)
* Expose repository licenses to the application and exclude any non-OSS-friendly projects
* Implement a lazy-load endless scroll in the application to continuely generate new suggestions of repositories and issues
* Integration with [https://www.bountysource.com/](Bountysource) or similar, showing the monetary reward for particularly challenging issues.
