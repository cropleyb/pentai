echo "Clearing databases"
rm db.fs.most.*

echo "Cleaning"
kivy ./setup.py clean

echo "Building"
kivy ./setup.py build_ext --inplace

echo "Creating players"
kivy ./pentai/db/create_default_players.py True

# TODO: Reset the guide
