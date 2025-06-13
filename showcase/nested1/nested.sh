echo "> 'ddrun -d' to show target directory"
ddrun -d
echo "> 'ddrun -d showcase/nested2' to set target directory"
ddrun -d showcase/nested2
echo "> 'ddrun nested' to run showcase/nested2/nested.sh, which will call showcase/option_d.sh"
ddrun nested
echo "> 'ddrun -d' to verify that the target directory is restored, even if the called nested scripts modify the .dddir setting"
ddrun -d
