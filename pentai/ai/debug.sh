rm ab_game.so
rm ab_state.so
rm alpha_beta.so
rm openings_mover.so
rm utility_calculator.so
rm priority_filter.so
rm priority_filter_2.so
rm priority_filter_3.so
rm heuristic_filter.so
rm killer_filter.so

rm ab_game.py
rm ab_state.py
rm alpha_beta.py
rm length_lookup_table.py # TEMP
rm openings_mover.py
rm utility_calculator.py
rm priority_filter.py
rm priority_filter_2.py
rm priority_filter_3.py
rm heuristic_filter.py
rm killer_filter.py

ln -s ab_game.pyx            ab_game.py
ln -s ab_state.pyx           ab_state.py
ln -s alpha_beta.pyx         alpha_beta.py
ln -s openings_mover.pyx     openings_mover.py
ln -s utility_calculator.pyx utility_calculator.py
ln -s priority_filter.pyx    priority_filter.py
ln -s priority_filter_2.pyx  priority_filter_2.py
ln -s priority_filter_3.pyx  priority_filter_3.py
ln -s heuristic_filter.pyx   heuristic_filter.py
ln -s killer_filter.pyx      killer_filter.py

