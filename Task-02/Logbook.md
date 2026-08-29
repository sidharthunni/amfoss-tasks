## Level 1
I started by checking file permissions in all 4 sectors using ls -la, 
since the story hinted the real fruit could "awaken itself." Turned out 
sector_C/devil_fruit_6.txt was the only file with execute permission 
(-rwxrwxr-x), while the other 39 files were just normal read/write 
files. Ran ./eat.sh sector_C/devil_fruit_6.txt and got:
ONE_PIECE{GITO_GITO_NO_AWAKENING}

## Level 2
The manifest file looked totally normal at first, nothing hidden in it. 
I checked git branch -a and found a branch called 
whiskey_peak_investigation. Switching to it showed a hidden folder 
called .baroque_works_cache with a script called unlock_vault.sh inside. 
It wouldn't run until I set an environment variable with my Level 1 flag:
export AWAKENING_SIGNATURE="ONE_PIECE{GITO_GITO_NO_AWAKENING}"
That unlocked two files, marine_intercept.log and bounty_hunter_feed.log. 
Running diff between them showed the actual transmission code:
BAROQUE_DIAL{SPLIT_TIMELINE_MISDIRECTION}

## Level 3
This one had hundreds of decoy report files spread across deeply nested 
folders. I used grep -rli "baroque" to search everything at once instead 
of checking files one by one, and it pointed me to 
GrandLine/Wax_Jungle/sector_beta/outpost/watchtower/storage/archive/agent_manifest.log. 
It had a SECURITY_TAG that matched the base64 version of my Level 2 
code, confirming it was the real one. It also had a bonus line I didn't 
need yet:
PONEGLYPH_FRAGMENT_I = "KjY2MjF4bW0lKzYqNyBsIS0vbTAtJTcnL"

## Level 4
The blueprint file had no name or extension at all, so I used the file 
command to figure out what it actually was - turned out to be gzip 
data. I renamed it with a .tar.gz extension, unzipped it, which gave a 
tar file, extracted that, and found a zip file inside. Unzipping that 
one gave two files - one was just a decoy, and the other, 
secret_link.txt, had the second fragment:
PONEGLYPH_FRAGMENT_II = "SwnbzptDiM3JSpvFiMuJ28PJzAlJ28VIzA="
Now I had both fragments needed for the next level.

## Level 5
This one was hidden in the git history instead of any folder. I ran 
git log --all --oneline and found a commit called "Level 5 : Vault 
Sealed" right before another commit that deleted everything. Used 
git checkout <commit> -- <path> to pull those old files back without 
switching my whole branch. Inside was a script called poneglyph.py that 
takes a base64 code, decodes it, and XORs each byte with 0x42. I joined 
both fragments together and ran them through the script, which gave me 
a new repo link:
https://github.com/rogueone-x/Laugh-Tale-Merge-War

## Level 6 - Laugh Tale
Cloned the new repo and found two branches that had grown apart from 
the same starting point. Running git merge caused a real conflict in 
two files, and each file had half the password split across both 
branches:
key_part_1: "TheGrand" + "Line" = TheGrandLine
key_part_2: "Remem" + "bers" = Remembers
So the full password was TheGrandLineRemembers. I checked this against 
the hash inside victory.sh using sha256sum before committing anything, 
just to be sure. Fixed both files, committed the merge, and ran 
./victory.sh with the password to get the final flag:
FLAG{The_Grand_Line_Remembers_Your_Commit}

## All the codes I found along the way
- Level 1: ONE_PIECE{GITO_GITO_NO_AWAKENING}
- Level 2: BAROQUE_DIAL{SPLIT_TIMELINE_MISDIRECTION}
- Level 3: PONEGLYPH_FRAGMENT_I = KjY2MjF4bW0lKzYqNyBsIS0vbTAtJTcnL
- Level 4: PONEGLYPH_FRAGMENT_II = SwnbzptDiM3JSpvFiMuJ28PJzAlJ28VIzA=
- Level 5: https://github.com/rogueone-x/Laugh-Tale-Merge-War
- Level 6/Final: FLAG{The_Grand_Line_Remembers_Your_Commit}
