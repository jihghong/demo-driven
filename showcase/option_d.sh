echo "> 'ddrun -d' to show target directory"
ddrun -d
echo "> 'ddrun -d -a' to show target directory and -a is ignored"
ddrun -d -a
echo "> 'ddrun -d example -a' to set target directory and -a is ignored"
ddrun -d example -a
echo "> 'ddrun -d target redundant unused superfluous' to test redundant arguments"
ddrun -d target redundant unused superfluous
echo "> 'ddrun -d' to show target directory after testing redundant arguments"
ddrun -d
echo "> 'cat .dddir' to show file content"
cat .dddir
echo  # for a newline
echo "> 'rm .dddir' to remove the .dddir file"
rm .dddir
echo "> 'ddrun -d' to show target directory. After .dddir is removed, this should show the default value"
ddrun -d
echo "> 'ddrun -d usage' to set target directory"
ddrun -d usage
echo "> 'ddrun -d' to show target directory after setting it"
ddrun -d
