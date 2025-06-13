echo "> 'ddrun -d' to show target directory"
ddrun -d
echo "> 'ddrun -d showcase' to set target directory"
ddrun -d showcase
echo "> 'ddrun option_d' to run showcase/option_d.sh"
ddrun option_d
echo "> 'ddrun -d' to verify that the target directory is restored, even if the called nested scripts modify the .dddir setting"
ddrun -d
