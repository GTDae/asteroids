# Asteroids Clone

This is a clone of the classic arcade game, Asteroids. The objective is to survive as long as possible by navigating a spaceship through an asteroid field and shooting down incoming threats. The game features three sizes of asteroids: large, medium, and small. Destroying a large asteroid splits it into two medium ones, and a medium one splits into two small ones. Small asteroids are destroyed on impact.

___

## Controls:

W - Move forward

S - Move backward

A - Turn left

D - Turn right

Spacebar - Fire a bullet

___

## Scoring System & High Scores

To make the game more competitive, a scoring system has been implemented. Destroying asteroids now awards points based on their size:

- Large Asteroid: 3 points

- Medium Asteroid: 2 points

- Small Asteroid: 1 point

Your current score is displayed in the top-right corner of the screen.

The game also features a high-score system that persists between sessions. The top 10 scores are stored in a local file, and the top 3 are displayed in the top-left corner of the screen. This allows players to track their performance over time.

___

## Technologies Used

This project was developed using:

- Python 3: The core programming language.

- Pygame: A cross-platform set of Python modules designed for writing video games.

- Ubuntu 24.04: The operating system used for development.

- VSCode on Windows 10: The code editor and environment, with a remote SSH connection to the Ubuntu machine.

This setup showcases a modern development workflow using a powerful Linux backend accessed from a Windows frontend.

___

## Guided Project

This project was completed as a guided assignment from Boot.Dev, a platform focused on hands-on software development education. The project's structure and core logic were provided as part of a course curriculum, with additional features added to explore and extend the game's functionality.

___

## To Be Continued...

This project serves as a solid foundation for a more personalized version of the game. We will be building on this code to add custom features and make it more my own. The planned changes include:

- ~~Add a scoring system~~

- Mesure the length of the game in hh:mm:ss format.

- Implement multiple lives and respawning

- Add an explosion effect for the asteroids

- Add acceleration to the player movement

- Make the objects wrap around the screen instead of disappearing

- Add a background image

- Create different weapon types

- Make the asteroids lumpy instead of perfectly round

- Make the ship have a triangular hit box instead of a circular one

- Add a shield power-up

- Add a speed power-up

- Add bombs that can be dropped