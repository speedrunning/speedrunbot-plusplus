/*
 * This file contains all sorts of utility functions and variables that are
 * used throughout the programs in this directory.
 */

#include <stdlib.h>
#include <string.h>

#include <curl/curl.h>

#include "utils.h"

void init_string(string_t *str)
{
	str->len = 0;
	str->ptr = malloc(str->len + 1);
	if (str->ptr == NULL)
		exit(EXIT_FAILURE);

	str->ptr[0] = '\0';
	return;
}

char *get_uid(const char *const username)
{
	char uri[URIBUF];
	string_t user;
	init_string(&user);

	snprintf(uri, URIBUF, API "/users?lookup=%s", username);
	get_req(uri, &user);

	static char uid[UIDBUF];
	sscanf(user.ptr, "{\"data\":[{\"id\":\"%[^\"]", uid);

	if (uid[0] == '\0')
		return NULL;
	return uid;
}

size_t write_callback(const void *ptr, const size_t size, const size_t nmemb,
                      string_t *json)
{
	/* Update the length of the JSON, and allocate more memory if needed */
	const size_t new_len = json->len + size * nmemb;
	json->ptr = realloc(json->ptr, new_len + 1);
	if (json->ptr == NULL)
		exit(EXIT_FAILURE);

	/* Copy the incoming bytes to `json` */
	memcpy(json->ptr + json->len, ptr, size * nmemb);
	json->ptr[new_len] = '\0';
	json->len = new_len;

	return size * nmemb;
}

void get_req(const char *uri, string_t *json)
{
	CURL *curl = curl_easy_init();
	if (curl == NULL)
		exit(EXIT_FAILURE);

	/* Load the contents of the API request to `json` */
	curl_easy_setopt(curl, CURLOPT_URL, uri);
	curl_easy_setopt(curl, CURLOPT_WRITEFUNCTION, write_callback);
	curl_easy_setopt(curl, CURLOPT_WRITEDATA, json);

	CURLcode res;
	if ((res = curl_easy_perform(curl)) != 0) {
		curl_easy_cleanup(curl);
		exit(EXIT_FAILURE);
	}

	curl_easy_cleanup(curl);
}

unsigned int substr(const char *str, const char *const sub, const int subl)
{
	unsigned int c = 0;
	for (str = strstr(str, sub); str; str = strstr(str + subl, sub))
		c++;
	return c;
}
