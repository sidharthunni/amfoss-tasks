Found the genuine Devil Fruit by checking file permissions with `ls -la` 
across all 4 sectors. Only sector_C/devil_fruit_6.txt had execute 
permission (-rwxrwxr-x) while all other 39 files were plain read/write 
files (-rw-rw-r--). Ran ./eat.sh sector_C/devil_fruit_6.txt to get:
ONE_PIECE{GITO_GITO_NO_AWAKENING}

## Level 2
The visible feast_manifest.txt had nothing hidden. Checked git branches 
with `git branch -a` and found `whiskey_peak_investigation` - switching 
to it revealed a hidden folder `.baroque_works_cache` containing 
`unlock_vault.sh`. It required an environment variable AWAKENING_SIGNATURE 
set to the Level 1 flag:
export AWAKENING_SIGNATURE="ONE_PIECE{GITO_GITO_NO_AWAKENING}"
Running ./unlock_vault.sh then dropped two files, marine_intercept.log 
and bounty_hunter_feed.log. Running diff between them revealed the 
Executive Transmission Code:
BAROQUE_DIAL{SPLIT_TIMELINE_MISDIRECTION}
## Level 3
Searched the whole Wax_Jungle tree with grep -rli "baroque" and found 
GrandLine/Wax_Jungle/sector_beta/outpost/watchtower/storage/archive/agent_manifest.log 
buried deep in nested folders. It contained a SECURITY_TAG matching the 
base64 encoding of the Level 2 code, confirming this was the genuine 
report among hundreds of decoys. It also contained a bonus find:
PONEGLYPH_FRAGMENT_I = "KjY2MjF4bW0lKzYqNyBsIS0vbTAtJTcnL"
(saved for later - Level 5 needs two Poneglyph fragments combined)
## Level 4
The blueprint file had no name/extension. Used `file puffing_tom_blueprints` 
to identify its real nature - it was gzip data. Renamed it to add a 
.tar.gz extension, gunzipped it into a .tar file, extracted that with tar, 
which revealed a .zip file. Unzipping that gave two files: frame_specs.dat 
(a decoy, just plain text) and secret_link.txt containing the real second 
cipher fragment:
PONEGLYPH_FRAGMENT_II="SwnbzptDiM3JSpvFiMuJ28PJzAlJ28VIzA="
Now have both fragments needed for Level 5:
FRAGMENT_I  = "KjY2MjF4bW0lKzYqNyBsIS0vbTAtJTcnL"
FRAGMENT_II = "SwnbzptDiM3JSpvFiMuJ28PJzAlJ28VIzA="
## Level 5
Checked git log --all --oneline and found commit d4e7bf5 "Level 5 : 
Vault Sealed" - the last commit before evidence got erased in a later 
commit. Used `git checkout d4e7bf5 -- GrandLine/Enies_Lobby` to recover 
those files without switching branches. Found poneglyph.py which decodes 
a base64 string then XORs each byte with 0x42. Combined the two Poneglyph 
fragments found earlier (Level 3 + Level 4) into one string and ran it 
through the script:
KjY2MjF4bW0lKzYqNyBsIS0vbTAtJTcnLSwnbzptDiM3JSpvFiMuJ28PJzAlJ28VIzA=
Output revealed a new repo link:
https://github.com/rogueone-x/Laugh-Tale-Merge-War

## Level 6 - Laugh Tale
The decoded Level 5 message revealed a new repo: 
https://github.com/rogueone-x/Laugh-Tale-Merge-War
Cloned it and found two branches, ancient_history and pirate_king_path, 
both diverging from the same initial commit. Ran:
git merge origin/pirate_king_path
This conflicted in treasure/key_part_1.txt and key_part_2.txt. Each file 
had half the password on each branch:
key_part_1: "TheGrand" (pirate_king_path) + "Line" (ancient_history) = TheGrandLine
key_part_2: "Remem" (pirate_king_path) + "bers" (ancient_history) = Remembers
Combined password: TheGrandLineRemembers
Verified with sha256sum against the hash in victory.sh before committing.
Resolved both files, committed the merge, and ran ./victory.sh with the 
password to get the final flag:
FLAG{The_Grand_Line_Remembers_Your_Commit}

## Summary of all flags/codes found
- Level 1: ONE_PIECE{GITO_GITO_NO_AWAKENING}
- Level 2: BAROQUE_DIAL{SPLIT_TIMELINE_MISDIRECTION}
- Level 3: PONEGLYPH_FRAGMENT_I = KjY2MjF4bW0lKzYqNyBsIS0vbTAtJTcnL
- Level 4: PONEGLYPH_FRAGMENT_II = SwnbzptDiM3JSpvFiMuJ28PJzAlJ28VIzA=
- Level 5: https://github.com/rogueone-x/Laugh-Tale-Merge-War
- Level 6/Final: FLAG{The_Grand_Line_Remembers_Your_Commit}
