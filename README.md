# Black Box Game

## Description
This is a Python program that simulates the logic of a Black Box game, with an emphasis on object-oriented design for this implementation. Black Box is a game played on a 2D grid (8 by 8 squares). When a new game is initialized, locations are chosen for hidden "atoms" on the board. A player's goal is to guess the locations of all atoms before they run out of points. Please note, this implementation does not include a user interface, but can be "played" in a console window.

## Gameplay
See [Wikipedia Page](https://en.wikipedia.org/wiki/Black_Box_(game)) for full rules and detailed examples.
- A player starts with 25 points at the beginning of the game
- They have two actions they can take each turn:
  - **Shoot Ray:** Choose a location at the edge of the board to shoot a ray from (excluding corners). This will return the exit location of the ray. Each unique entry or exit space will subract 1 point from the player's score.
  - **Guess Atom Location:** Player guesses an atom location. The atom is marked as found if they guess correctly. If they guess incorrectly, they lose 5 points.
- Rays can interact with hidden atoms in a few different ways:
  - **Hit:** A ray hits an atom directly. In this case, there would be no exit location- it will return None.
  - **Deflection:** If a ray is about to enter a space right next to an atom, it will deflect instead. This means it will turn 90 degrees away from the atom.
  - **Reflection:** If there is an atom to the left or right of a ray as soon as it enters the board, it will reflect back to the same location it entered. A reflection can also occur in the case of a double-deflection (deflection to the left and right at the same time).
  - **Miss:** A ray never gets close enough to any atoms to interact. It travels in a straight line through the board. The exit location in this case is the space directly across from the entry space.
  - **Detour:** Detours can occur with a combination of the moves above. For example, you could have a deflection that leads to another deflection. Or a deflection, then a hit. The exit location would be highly variable in these cases, depending on the path the ray ends up taking.
- The game ends when a player runs out of points, or when they correctly guess all atom locations.

## Object-Oriented Design 
The figure below (created using the [PlantText UML Editor](https://www.planttext.com/)) shows the classes, data members, and methods I used to model this game, as well as the relationships between classes. For example, the diagram shows that each game only has one board (1 to 1), but each board can have many atoms or rays within it (1 to many).

![Class Diagram Image](https://www.planttext.com/api/plantuml/img/TLJDSeCW4Bxx58udqsaEVOCqbzxx0WoLjM62aBBB94udxruM8ser5rc-Rty_m0EIz1GwKnH5OoHYUJIoEH_TxKDsKFuMPVdbf5TnnSPvu9Ka1Op6Tm14O4jRJRKarmcZaNOHKHelHlOY1TUCuCav4bxsjNVNrx9n9dHsDwOH7BrYW1AEma1BzGYbHj8kN9GaoC0zpy1LS-yYDk82nMrAbc2lm0ly2T83Ye2WDgVWQlCKzQAhUd9PfKjSSuBcB7IxTAWl3ZLfPoUNrdbnYiKjt4XiqmfQ0mtZQwydqjuVQdpAdhK0IxxFSPmyU1_1EGGtlTZdinvzbVP35wDU6qSs16LrbdKdU5uge_zx6gxE5l4V61tNUN7TqqB2Z4uQZsUPA0f-yF43dsmriy6gf3xRMVNtU4LOzYWGwvSKcYlwJBq8JMea9czN3UUfuirVlDlghNhPAtUr-sWDpw58NsRA1rLMdRHznVVZESbZ5CKXZXX_4dy0)

## How to Test this Program
1. From this repository, click "Code" and "Download ZIP"
2. Unzip the BlackBoxGame.py file
3. Open this file in your chosen console/IDE
4. Try it out!

### Example Gameplay
```
# start a new game with atoms placed at the three locations in the atom list, in the form (row, column)
atom_list = [(2, 3), (4, 6), (5,8)]
new_game = BlackBoxGame(atom_list) 

# shoot a ray that will enter the board at row 1, column 2 (top border of the board)
new_game.shoot_ray(0, 2) # will return the exit location of the ray

# guess if an atom is located at row 3, column 3
new_game.guess_atom(3, 3) # will return True or False

# display the board (revealing atom locations)
new_game.display_board() # empty spaces are 'x's and atoms are 'o's

```
