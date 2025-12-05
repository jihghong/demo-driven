dir="showcase.jupyter/demo"
echo "> initialize $dir/current"
rm -f $dir/current/*
cp $dir/created/*.ipynb $dir/current
echo "> 'ddrun -d $dir/current' to set target directory"
ddrun -d $dir/current
echo "> 'ddrun' to run all demo scripts in $dir/current"
ddrun
echo "> 'ddrun' to run all demo scripts again. Notice that the output messages have changed"
ddrun
echo "> 'diff -r $dir/current $dir/created' should produce no output because all files match"
diff -r $dir/current $dir/created --exclude="*.html" --strip-trailing-cr
echo "> now modify demo scripts"
cp $dir/modified/*.ipynb $dir/current
echo "> 'ddrun' to run all demo scripts in $dir/current"
ddrun
echo "> 'ddrun' to run all demo scripts again. Notice that the output messages are the same"
ddrun
echo "> 'diff -r $dir/current $dir/modified' should produce no output because all files match"
diff -r $dir/current $dir/modified --exclude="*.html" --strip-trailing-cr
echo "> now revert demo scripts"
cp $dir/reverted/*.ipynb $dir/current
echo "> 'ddrun' to run all demo scripts in $dir/current"
ddrun
echo "> 'ddrun' to run all demo scripts again. Notice that the output messages are the same"
ddrun
echo "> 'diff -r $dir/current $dir/reverted' should produce no output because all files match"
diff -r $dir/current $dir/reverted --exclude="*.html" --strip-trailing-cr
echo "> now modify demo scripts again"
cp $dir/modified/*.ipynb $dir/current
echo "> 'ddrun' to run all demo scripts in $dir/current"
ddrun
echo "> 'ddrun' to run all demo scripts again. Notice that the output messages are the same"
ddrun
echo "> 'ddrun -a' to accept all results in $dir/current"
ddrun -a
echo "> 'ddrun -a' to accept all demo scripts again. Notice that the output messages have changed"
ddrun -a
echo "> 'diff -r $dir/current $dir/accepted' should produce no output because all files match"
diff -r $dir/current $dir/accepted --exclude="*.html" --strip-trailing-cr
echo "> 'ddnbo' to check all notebook outputs in $dir/current"
ddnbo
echo "> 'ddnbo -f' to fix all notebook outputs in $dir/current"
ddnbo -f
echo "> 'ddnbo -f' to fix all notebook outputs again. Notice that the output messages have changed"
ddnbo -f
echo "> 'diff -r $dir/current $dir/fixed' should produce no output because all files match"
diff -r $dir/current $dir/fixed --exclude="*.html" --strip-trailing-cr
echo "> restore $dir/current to its initial status"
rm -f $dir/current/*
cp $dir/created/*.ipynb $dir/current
