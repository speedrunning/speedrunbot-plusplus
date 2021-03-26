#ifndef __COMPILE_H_
#define __COMPILE_H_

#ifdef clang
#	define CC "CCMP=clang"
#elif defined gcc
#	define CC "CCMP=gcc"
#else
#	define CC "CCMP=cc"
#endif

/**
 * @brief Check if a directory is in the list of excluded directories.
 * 
 * @param dname The directories name.
 * @return true The directory should be excluded.
 * @return false The directory should not be excluded.
 */
bool in_excludes(const char *fname);

/**
 * @brief Run the Makefile in the given directory.
 * 
 * @param dname The name of the directory.
 */
void make(const char *dname);

#endif /* !__COMPILE_H_ */
