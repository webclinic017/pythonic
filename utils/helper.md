

# remove history of a specific file from commit. especially after .gitignore edits. 
[](https://stackoverflow.com/questions/19573031/cant-push-to-github-because-of-large-file-which-i-already-deleted)

git filter-branch --index-filter 'git rm -r --cached --ignore-unmatch <file/dir>' HEAD