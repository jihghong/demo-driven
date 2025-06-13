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
echo "> 'ddnbo -d' to show target directory. Note that ddnbo also reads .dddir for target directory setting"
ddnbo -d
echo "> 'ddnbo -d -f -F' to show target directory and -f -F are ignored"
ddnbo -d -f -F
echo "> 'ddnbo -d example -f -F' to set target directory and -f -F are ignored"
ddnbo -d example -f -F
echo "> 'ddnbo -d target redundant unused superfluous' to test redundant arguments"
ddnbo -d target redundant unused superfluous
echo "> 'ddnbo -d' to show target directory after testing redundant arguments"
ddnbo -d
echo "> 'rm .dddir' to remove .dddir file"
rm .dddir
echo "> 'ddnbo -d' to show target directory. After .dddir is removed, this should show the default value"
ddnbo -d
echo "> 'ddnbo -d example' to set target directory"
ddnbo -d example
echo "> 'ddnbo -d' to show target directory after setting it"
ddnbo -d
echo "> 'ddrun -d' to show target dirctory, which was changed by a different program 'ddnbo'"
ddrun -d
