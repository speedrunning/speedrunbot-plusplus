#ifndef __GAMES_H_
#define __GAMES_H_

/**
 * @brief Check if `gid` is in the `games` array, and if not, add it.
 * 
 * @param gid The game ID to check for.
 * @return true The game ID was in the array.
 * @return false The game ID was not in the array.
 */
bool in_games(char *gid);

#endif /* !__GAMES_H_ */