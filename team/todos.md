# Per-person to-dos

How a team of two to five keeps what each person owes, so nothing addressed to someone is lost. Read by `start.md` and written by `close.md`.

## Why

At a hackathon, ideas travel with the person who had them and cost nothing in the moment. Where they fail is the hand-off: a note written for a teammate in a shared folder was never picked up, because nobody checks a to-do board they were never introduced to. So anything addressed to another person is captured in that person's own list, and their next `start` reads it to them first. Nobody has to remember to look.

## Where it lives

In the team's GitHub repo, one file per person:

```
people/
  <name>/
    todo.md      what this person owes, and what was handed to them
    state.md     where this person left off (rewritten by their own close)
  _template/     copied for each new person
work/
  <name>/        each person's own working folder
state.md         where the shared work stands (the parts everyone uses)
```

`<name>` is the first name the team uses, lower case (`ana`, `fassaleh`). The same file can live in Notion or a Sheet instead (one page or tab per person); the rules below do not change.

## The file

```markdown
# To-dos: <Name>

## Open
- [ ] <what, in one line> · from <who> · <YYYY-MM-DD> · <link, if any>

## Done
- [x] <what> · from <who> · <YYYY-MM-DD> · done <YYYY-MM-DD>
```

- **One line per to-do.** Say what is wanted and what done looks like, short enough to read aloud.
- **From** is who asked. Your own to-dos say `from me`.
- **Add, never rewrite.** Anyone may add a line to anyone's `Open`. Only the person themselves moves a line to `Done` or changes its wording. That keeps two people from editing the same line, so git can merge.
- **Done moves, never deletes.** A finished line goes to `Done` with the date; a dropped one goes there too, as `dropped <date>` with a reason.

## Keep the bar high

A to-do is a promise someone else will have to read. Write one only when:

- it is addressed to a person (someone else, or yourself in a later session), and
- it cannot be done now, in this session.

If it can be done in the next five minutes, do it instead. An idea that belongs to nobody yet is a note in the shared `state.md`, not a to-do. A list that grows past about ten open lines has stopped being read; prune it with its owner.

## Before the event

The person setting up the repo:

1. Collects everyone's GitHub username, spelled exactly, before the day, and invites them all to the repo.
2. Makes `people/_template/` (a `todo.md` as in "The file" above, and a `state.md` holding one line, `Where I left off: not started.`), then `people/<name>/` for each person from it, and a `work/<name>/` folder.
3. Seeds each `todo.md` with that person's first one or two lines (their challenge, the dataset to look at, who to talk to), so the list already means something at their first `start`.
4. Introduces it in person: "run start, say who you are, and it reads you your list." People will not check a list they were never shown.
