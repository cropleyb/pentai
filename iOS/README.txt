but: 
git clone git://github.com/kivy/kivy-ios
cd kivy-ios
Replace / merge in these files (build-all.sh, build-pentai.sh,
template-Info.plist)
Run ./build-all

Follow the instructions at: 
http://kivy.org/docs/guide/packaging-ios.html

When it gets to building the app in XCode, add kivy-ios/build/lib/libPente.a
to the link under Build Phases. - without this none of the cythonized modules
will be linked in.
