/*
 *
 * Copyright (C) 2019, Broadband Forum
 * Copyright (C) 2016-2019  CommScope, Inc
 *
 * Redistribution and use in source and binary forms, with or without
 * modification, are permitted provided that the following conditions
 * are met:
 *
 * 1. Redistributions of source code must retain the above copyright
 *    notice, this list of conditions and the following disclaimer.
 *
 * 2. Redistributions in binary form must reproduce the above copyright
 *    notice, this list of conditions and the following disclaimer in the
 *    documentation and/or other materials provided with the distribution.
 *
 * 3. Neither the name of the copyright holder nor the names of its
 *    contributors may be used to endorse or promote products derived from
 *    this software without specific prior written permission.
 *
 * THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
 * AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
 * IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
 * ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE
 * LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
 * CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
 * SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
 * INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
 * CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
 * ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF
 * THE POSSIBILITY OF SUCH DAMAGE.
 *
 */

/**
 * \file vendor.c
 *
 * Implements the interface to all vendor implemented data model nodes
 *
 */

#include <stdio.h>
#include <stdlib.h>
#include <stdbool.h>

#include "usp_err_codes.h"
//#include "vendor_defs.h"
#include "vendor_api.h"
#include "usp_api.h"

#include <limits.h>       //For PATH_MAX
#include <string.h>
#include <dirent.h>
#include "dlfcn.h"

#define VENDORS_FOLDER "/usr/local/lib/amo"
#define VENDORS_MAX 128
static int NbreOfEntries;
typedef int (*called_func)(void*);
typedef int (*AMO_Start)(void*);
typedef int (*AMO_Stop)(void*);
struct Vendor
{
    char name[PATH_MAX + 1];
    char fullpath[PATH_MAX + 1];
    void *pointer;
    called_func init;
    called_func start;
    called_func stop;
    /* data */
};

struct Vendor vendors[VENDORS_MAX];



/*********************************************************************//**
**
** VENDOR_Init
**
** Initialises this component, and registers all parameters and vendor hooks, which it implements
**
** \param   None
**
** \return  USP_ERR_OK if successful
**
**************************************************************************/

int VENDOR_Init(void)
{
    int errRet = USP_ERR_OK;
    memset(&vendors,0,sizeof(vendors));

    DIR *d;
    struct dirent *dir;
    char path[] = VENDORS_FOLDER;
    d = opendir(path);
    if (d)
    {
        int NbreOfEntries=0;
        for(int i=0;(dir = readdir(d)) != NULL;i++){
            //Condition to check regular file.
            if(dir->d_type==DT_REG){
                char full_path[1000];
                full_path[0]='\0';
                strcat(full_path,path);
                strcat(full_path,"/");
                strcat(full_path,dir->d_name);
                printf("%s\n",full_path);
                snprintf(vendors[i].fullpath,strlen(vendors[i].fullpath),"%s",full_path);
                vendors[i].pointer = dlopen(full_path, RTLD_LAZY);
                if(vendors[i].pointer){
                    vendors[i].init = (called_func)dlsym(vendors[i].pointer,"AMO_Init");
                    char* error = dlerror();
                    if(error)
                    {
                        printf("could not dlsym: %s\n",error);
                        continue;
                    }
                    vendors[i].start = (called_func)dlsym(vendors[i].pointer,"AMO_Init");
                    error = dlerror();
                    if(error)
                    {
                        printf("could not dlsym: %s\n",error);
                        continue;
                    }
                    vendors[i].stop = (called_func)dlsym(vendors[i].pointer,"AMO_Init");
                    error = dlerror();
                    if(error)
                    {
                        printf("could not dlsym: %s\n",error);
                        continue;
                    }
                    void *ret =NULL;
                    printf("vendors[i].init(ret);\n");
                    errRet |= vendors[i].init(ret);
                }
                NbreOfEntries++;
            }
        }
        closedir(d);
    }
//    while (NbreOfEntries--) {
//        char buf[PATH_MAX + 1]; 
  //      realpath(namelist[n]->d_name, buf);

   // }
            //free(namelist[n]);
    //free(namelist);
    return errRet;
}


/*********************************************************************//**
**
** VENDOR_Start
**
** Called after data model has been registered and after instance numbers have been read from the USP database
** Typically this function is used to seed the data model with instance numbers or
** initialise internal data structures which require the data model to be running to access parameters
**
** \param   None
**
** \return  USP_ERR_OK if successful
**
**************************************************************************/
int VENDOR_Start(void)
{
    int errRet = USP_ERR_OK;
    for(int i=0;i<NbreOfEntries;i++){
        void *ret =NULL;
        if(vendors[i].start)
            errRet |= vendors[i].start(ret);
    }
    return errRet;
}

/*********************************************************************//**
**
** VENDOR_Stop
**
** Called when stopping USP agent gracefully, to free up memory and shutdown
** any vendor processes etc
**
** \param   None
**
** \return  USP_ERR_OK if successful
**
**************************************************************************/
int VENDOR_Stop(void)
{
    int errRet = USP_ERR_OK;
    for(int i=0;i<NbreOfEntries;i++){
        void *ret =NULL;
        if(vendors[i].stop)
            errRet |= vendors[i].stop(ret);
    }
    return errRet;
}

