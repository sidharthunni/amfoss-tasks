# Task 02: One Piece Terminal Adventure

## Approach
Full level-by-level breakdown and all discovered codes/flags are 
documented in Logbook.md, with screenshots in the screenshots folder.

Quick summary:
- Level 1: found the real file among decoys by checking permissions 
  with ls -la (only one had execute permission)
- Level 2: explored git branches to find hidden content, then used 
  a flag from Level 1 as an environment variable to unlock a script
- Level 3: searched deeply nested folders across a different branch 
  using grep to find one genuine file among hundreds of decoys
- Level 4: used the file command to identify a renamed/hidden file's 
  real type, then unwrapped multiple layers of compression (gzip, tar, zip)
- Level 5: recovered deleted files from an old git commit using 
  git checkout <commit> -- <path>, then combined two cipher fragments 
  and ran them through a Python decoder
- Level 6: resolved a real git merge conflict between two branches, 
  where the password was split in half across both branches

## What I learned
- Checking file permissions and using file to identify real file types
- Digging through git branches and commit history for hidden/deleted content
- Using git checkout <commit> -- <path> to recover specific old files
- Environment variables as a way scripts can check for prerequisites
- Multi-layer archive extraction (gzip -> tar -> zip)
- Resolving real merge conflicts by combining content from both sides

## Review
Levels 5 and 6 were the most satisfying to crack, especially finally
getting the merge conflict resolved at the end. Honestly, most of the
other levels confused me too, but I kept at it and worked through them
one step at a time. There were moments it got frustrating, but it felt
really good once everything came together. What stood out to me the
most were the commands themselves — recovering old files from git
history and actually resolving a real merge conflict felt like proper
git skills, not just theory.
