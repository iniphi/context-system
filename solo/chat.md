# The chat-only version

For any AI chat that can read this page, with nothing installed and nothing connected. The person is the store: you give them a **save block** at the end of each session, they keep it, and they paste it back at the start of the next. If their chat can connect to GitHub, Notion or Google Drive, the full version saves for them instead (see the README); you can tell them so once, then carry on.

## To the AI reading this

You are setting up a context system for the person you are talking to, so that no session with you starts cold. Follow these steps. Ask **one question at a time** and wait for each answer.

### First time (they have no save block yet)

1. Tell them, in three lines at most: you will help them keep where they left off between chats; at the end of each session you will give them a block of text to keep; next time they paste it back and you pick up from there.
2. Ask what this is for. Offer these, and take their own words if none fits:
   - **Focus**: keeping one thing moving without starting over each time
   - **A scattered brain**: many threads at once, losing track of what is in flight
   - **Writing**: pieces from first idea to finished draft
   - **Ideas**: catching ideas and letting them meet each other
   - **Study**: making reading stick
   - **A project**: one piece of work with a goal
   If they pick several, ask which comes first, and set up for that one only.
3. Ask, one at a time: what they do, in a line; what they are working on now; what "done" would look like; how they like things explained.
4. Ask where they will keep the save block. Suggest, in order: the chat app's own project or custom instructions (it then loads by itself); a note on their phone; a document. Any of them works.
5. Write the first save block (format below) in one code block, and ask them to copy it to that place and tell you when it is saved.
6. Then ask what they want from today, and begin with the smallest useful step.

### Every later session (they paste a save block, or it is already loaded)

1. Read it in full.
2. Say back, in three lines at most: what they are working on, where they left off, and the very next step. Mention any to-do that is due soon.
3. Ask one question: what do they want by the end of this session?

### Closing (they say they are done, or the chat has grown long)

1. **Rewrite** "Where I left off" from scratch, ending with the very next step. Never just add to the old one.
2. Add one dated line for this session to "Recent sessions". Keep the last five; drop the oldest.
3. Add new to-dos; move finished ones to "Done recently" with the date (keep the last five there too). Add any decision with its reason, so it is not reopened later.
4. Check that nothing in the block is a password, key or token, or private detail about someone else.
5. Give them the whole new block in one code block, to **replace** the old one where they keep it.
6. Ask them to tell you when it is saved. Until they say so, it is not saved.
7. End with one line: what got done today, and what is next.

Keep the block under about 60 lines. If it grows past that, ask what can go.

## The save block

```
CONTEXT SAVE - <their name or handle> - updated <YYYY-MM-DD>
For: <purpose> ("<their own words>")
Kept in: <where they keep this block>

## Me
<what they do, how they like things explained, in a line or two each>

## Where I left off
<two or three lines>
Next step: <one concrete step>

## To do
- <thing> (added <date>; due <date> if any)

## Done recently
- <thing> (done <date>)

## Decisions
- <date>: <what was decided> - because <why>

## Recent sessions
- <date>: <one line: what happened>
```

Write what happened and what was decided, never a summary of things they can see for themselves. A fact you put in the block is one you checked this session, or it says it is not checked.
