# Task 01: The Command Line Cup

## Approach

**Challenge 1:** First I had to find the "first perfect number" — a
number where its divisors add up to itself. That's 6 (1+2+3=6). Then
I took the derivative of x²-7x, which is 2x-7, and put in 6 to get 5.
So the folder was 06 and the file was Spell_05. It gave the spell
name "Impedimenta." I found that file in the spellbook and ran it to
get the first code.

**Challenge 2:** This one needed the atomic number of the first
element used to make semiconductors. That's germanium, atomic number
32. So the folder was 02 and the file was Spell_03, which gave the
spell name "Stupefy." I ran it and got the second code.

**Challenge 3:** I ran `git branch -a` to see all the branches and
found one called defenseAgainstTheDarkArts, which is what Lupin
taught. I switched to it. The riddle was about a creature that turns
into your worst fear — a Boggart — and the spell to beat it is
Riddikulus. That file was already there in the spellbook, so I ran it
and got the third code. Then I went back to main and used
`git checkout defenseAgainstTheDarkArts -- Riddikulus.py` to copy
just that one file over without switching branches, which I hadn't
done before.

**Challenge 4:** This one was hiding in the commit history instead of
a folder. I used `git log --all --oneline` and scrolled through until
I found a commit message with a riddle: the number of Horcruxes
Voldemort made (7), and a number whose name has the same number of
letters as itself (four has 4 letters, so that's 4). That gave folder
07, file Spell_04, on the thegraveyard branch. The spell there was
"Priori Incantatem," and running it gave the last code.

**Final step:** I put all four codes together into one file and
decoded it using base64, which gave me a GitHub link.

## What I learned
- How to list and switch git branches
- How to grab just one file from another branch without switching to
  it fully
- How to search through commit history using git log --all
- How base64 encoding and decoding works

## Review
It felt pretty satisfying to crack a few of the challenges, though
some parts were confusing at first. I learned a few new git commands
and already knew some others. Since I also just switched from Windows
to Linux, a lot of this felt new to me overall. But I liked the
puzzle format — it made things more interesting than just following
plain instructions.


